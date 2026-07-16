# MDR Settlement Dashboard

## Overview

The MDR Settlement Dashboard is a Streamlit-based web application designed to automate the settlement preparation process for merchants.

The application processes uploaded Excel or CSV settlement files, automatically calculates Gross Amount, MDR, Net Settlement, and allows finance users to complete the settlement by entering Refund, Tax, Other deductions, and Payment Details.

The system reduces manual effort while maintaining a simple and user-friendly workflow.

---

# Features

## File Upload

Supports:

- Excel (.xlsx)
- Excel (.xls)
- CSV (.csv)

---

## Automatic Processing

After uploading a file, the backend automatically:

- Calculates Gross Amount
- Applies Merchant MDR
- Calculates MDR Amount
- Calculates Net Settlement

No manual calculation is required.

---

## Dashboard

Displays high-level settlement KPIs including:

- Total Merchants
- Total Volume
- Total Locked Payments
- Total Pending Payments

---

## Settlement Workflow

Users can:

- Select settlement date
- Select Merchant
- Enter Refund
- Enter Tax
- Enter Other Charges
- Select Payment Type
- Enter Payment Amount
- Enter Payment Date
- Enter Reference Number

The system automatically calculates:

Net2 = Net - (Refund + Tax + Other)

After submitting:

- Settlement is marked as Locked
- Payment information is stored
- Updated file becomes available for download

---

## Download

The application generates an updated settlement file containing:

- Gross
- MDR
- Net
- Refund
- Tax
- Other
- Net2
- Payment Details
- Reference
- Status

---

# Project Structure

```
Project/
│
├── app.py
├── backend.py
├── requirements.txt
├── README.md
├── QUICK_START.txt
└── SETUP_INSTRUCTIONS.md
```

---

# Requirements

Python 3.10 or higher

Required packages:

- streamlit
- pandas
- openpyxl
- xlrd

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run Application

Navigate to the project folder:

```bash
cd Project
```

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# Backend

The frontend does not perform any calculations.

All business logic including:

- Gross Calculation
- MDR Calculation
- Net Calculation
- Settlement Processing

is handled by backend.py.

---

# Frontend

The Streamlit frontend provides:

- Upload interface
- Dashboard
- Settlement workflow
- Merchant filtering
- Date filtering
- Payment locking
- Download updated settlement file

---

# Input File

The uploaded file must contain the required settlement columns used by the backend.

---

# Output File

The generated output contains the original uploaded data together with calculated settlement fields.

---

# Security

No database is required.

The application processes uploaded files in memory and returns the updated settlement file to the user.

---

# Developed By

Muhammad Sameed
AI Engineer / Data Science
