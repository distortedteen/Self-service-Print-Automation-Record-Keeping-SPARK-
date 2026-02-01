---

# SPARK

Self-service Print Automation & Record-Keeping

**SPARK** is a QR-based, local-network print automation system designed for college campuses. It replaces manual, email-based printing and handwritten logbooks with a transparent, efficient, and auditable digital workflow.

Built for reliability and real-world deployment, SPARK automates print submission, cost calculation, record keeping, and payment tracking—without internet dependency.

---

## Project Details

* **Team:** The Trio
* **Team Leader:** Saniya Khatri
* **Team Members:** Pratyay Mukherjee, Mohit Kumar Yadav
* **Institution:** National Forensic Sciences University – Tripura Campus (NFSU-TC)
* **Hackathon:** NFSU SMART Hackathon 2026

---

## Problem

The existing campus printing system relies on:

* Email-based file submission
* Manual printing by staff
* Handwritten logbooks
* Manual payment verification

This leads to delays, errors, lack of transparency, and increased workload for staff.

---

## Solution

SPARK introduces a **self-service, QR-based print system** that:

* Allows students to submit print jobs via smartphone
* Automatically calculates page count and cost
* Maintains a digital print logbook
* Tracks payment status
* Provides an admin dashboard with summaries and export features
* Operates entirely on a local network (offline-first)

---

## Key Features

### Student Interface

* QR-code access (no login)
* PDF upload
* Automatic page detection
* Page range and copy selection
* Live cost calculation (₹1 per page)
* Clear payment instructions

### Admin Interface

* PIN-protected access
* Digital print logbook
* Payment status tracking (Pending / Paid)
* Daily summary dashboard
* Filter logs by payment status
* CSV export for auditing

---

## Tech Stack

* **OS:** Fedora Linux 41
* **Python:** 3.12.10
* **Backend:** Flask
* **Database:** SQLite
* **Printing:** CUPS (`lp` command)
* **Frontend:** HTML, CSS, JavaScript (PDF.js)
* **Printer:** USB-connected

---

## Architecture Overview

```
Student Phone → QR Scan → Flask Web App → SQLite DB → USB Printer
```

---

## Project Structure

```
SPARK/
├── app.py
├── logs.db
├── uploads/
├── templates/
│   ├── index.html
│   ├── admin.html
│   └── admin_login.html
├── static/
│   ├── style.css
│   └── college_logo.png
├── requirements.txt
└── README.md
```

---

## Installation (Fedora Linux 41)

### 1. Install system dependencies

```bash
sudo dnf install python3 python3-pip cups qrencode
```

Enable CUPS:

```bash
sudo systemctl start cups
sudo systemctl enable cups
```

Add the printer via **Settings → Printers**.

---

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the application

```bash
python3 app.py
```

Server runs at:

```
http://0.0.0.0:5000
```

---

## Usage

### Student

1. Connect to the same Wi-Fi network
2. Scan QR code near printer
3. Upload PDF and select options
4. View cost and submit print request

### Admin

1. Visit `/admin`
2. Login using admin PIN
3. View logs, mark payments, export CSV

---

## Design Decisions

* **Offline-first:** No internet or cloud dependency
* **Payment decoupling:** Payment verification is tracked, not processed
* **Admin control:** Manual verification prevents disputes
* **Simplicity:** Focused on one real campus workflow

---

## Limitations

* Manual payment verification
* Single printer support
* Hardcoded admin PIN (demo purpose)

---

## Future Scope

* Multi-printer support
* Configurable pricing
* Receipt generation
* Backend PDF verification
* Campus ERP integration

---

## License

Developed for academic and demonstration purposes as part of **NFSU SMART Hackathon 2026**.

---
