from flask import Flask, request, render_template
import os, sqlite3, datetime
from flask import session, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.secret_key = "qprint-secret-key"

ADMIN_PIN = "nfsu@123"

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/print", methods=["POST"])
def print_file():
    # Get form data
    student_name = request.form["student_name"]
    course = request.form["course"]
    copies = int(request.form["copies"])
    pages_input = request.form["pages"]

    # Handle file upload
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    pages_printed = 0
    if pages_input:
        if "-" in pages_input:
            start, end = pages_input.split("-")
            pages_printed = int(end) - int(start) + 1
        else:
            pages_printed = int(pages_input)

    if pages_printed <= 0:
        pages_printed = 1

    cost = pages_printed * copies * 1


    if "pages_printed" in request.form and "total_cost" in request.form:
        try:
            pages_printed = int(request.form["pages_printed"])
            cost = int(request.form["total_cost"])
        except ValueError:
            pass  

    # Printing disabled for now
    # subprocess.run(["lp", "-n", str(copies), filepath])

    # Save to db
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO logs
        (student_name, course, filename, pages, copies, cost, timestamp, payment_status)
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        student_name,
        course,
        file.filename,
        pages_printed,
        copies,
        cost,
        str(datetime.datetime.now()),
        "Pending"
    ))
    conn.commit()
    conn.close()

    return "Print request submitted successfully"

@app.route("/mark_paid/<int:log_id>")
def mark_paid(log_id):
    if not session.get("admin_logged_in"):
        return redirect("/admin_login")

    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute(
        "UPDATE logs SET payment_status = 'Paid' WHERE id = ?",
        (log_id,)
    )
    conn.commit()
    conn.close()
    return "Payment marked as Paid"

@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect("/admin_login")

    status_filter = request.args.get("status")  # Paid / Pending / None

    conn = sqlite3.connect("logs.db")
    c = conn.cursor()

    # Apply filter if selected
    if status_filter in ["Paid", "Pending"]:
        c.execute(
            "SELECT * FROM logs WHERE payment_status = ? ORDER BY id DESC",
            (status_filter,)
        )
    else:
        c.execute("SELECT * FROM logs ORDER BY id DESC")

    rows = c.fetchall()

    # Daily summary (Paid only)
    c.execute("""
        SELECT 
            COUNT(*),
            SUM(pages * copies),
            SUM(cost)
        FROM logs
        WHERE DATE(timestamp) = DATE('now')
        AND payment_status = 'Paid'
    """)
    summary = c.fetchone()

    conn.close()

    total_jobs = summary[0] or 0
    total_pages = summary[1] or 0
    total_amount = summary[2] or 0

    return render_template(
        "admin.html",
        rows=rows,
        total_jobs=total_jobs,
        total_pages=total_pages,
        total_amount=total_amount,
        current_filter=status_filter
    )

import csv
from flask import Response

@app.route("/export_csv")
def export_csv():
    if not session.get("admin_logged_in"):
        return redirect("/admin_login")

    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("""
        SELECT
            student_name,
            course,
            filename,
            pages,
            copies,
            cost,
            payment_status,
            timestamp
        FROM logs
        ORDER BY id DESC
    """)
    rows = c.fetchall()
    conn.close()

    def generate():
        # CSV header
        yield "Student Name,Course,File Name,Pages,Copies,Amount,Payment Status,Date & Time\n"

        # CSV rows
        for r in rows:
            yield f"{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=print_logs.csv"}
    )

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        entered_pin = request.form.get("pin")

        if entered_pin == ADMIN_PIN:
            session["admin_logged_in"] = True
            return redirect("/admin")
        else:
            return render_template("admin_login.html", error="Invalid PIN")

    return render_template("admin_login.html")

@app.route("/admin_logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect("/admin_login")

app.run(host="0.0.0.0", port=5000)
