# SEP-PROJECT: Procurement System

A complete, beginner-friendly procurement management system with backend REST APIs and interactive frontend GUI.


## 📋 System Features

### Purchase Requisition (PR) Management
- **Create** new purchase requisitions
- **Recommend** PRs to commercial team
- **Track** PR status (pending → recommended → approved/rejected)

### Vendor Management
- **List** all vendors with ratings
- **Create** vendor records
- **Negotiate** with vendors

### Commercial Approval
- **View** pending PRs
- **Approve** or **Reject** PRs
- Track approval decisions

### Purchase Order (PO) Management
- **Create** purchase orders from approved PRs
- **Link** vendors to orders
- **Track** items and totals

### Accounts & Payments
- **Monitor** pending payments
- **Mark** payments as paid
- Track payment status

### Tax Calculation
- **Calculate** tax (10% simple rate)
- View total with tax
- Validate inputs

### Warehouse Management
- **View** inventory items
- **Create** new warehouse items with SKU
- Track quantities

### Client Confirmation
- **Track** deliveries
- **Confirm** delivery completion
- Manage delivery status

---

## 🛠️ Technology Stack

- **Backend**: Python Flask 2.2.5
- **Database**: SQLite (file-based)
- **Frontend**: HTML5 + Vanilla JavaScript (no frameworks)
- **API**: RESTful JSON endpoints
- **ORM**: SQLAlchemy 2.0

---

## 📁 Project Structure

```
SEP PROJ/
├── backend/
│   ├── app.py                 # Flask application entry
│   ├── requirements.txt        # Python dependencies
│   ├── app.db                 # SQLite database (auto-created)
│   ├── config/
│   │   ├── db.py             # Database config
│   │   └── settings.py        # App settings
│   ├── models/                # SQLAlchemy models (11 entities)
│   ├── routes/                # API endpoints (9 blueprints)
│   └── utils/
│       ├── helpers.py         # to_dict() serializer
│       └── validators.py      # Field validation
├── Frontend/
│   ├── dashboard.html         # Main dashboard
│   ├── pr.html               # Purchase Requisitions
│   ├── vendors.html          # Vendor Management
│   ├── po.html               # Purchase Orders
│   ├── accounts.html         # Payments & Accounts
│   ├── tax.html              # Tax Calculator
│   ├── commercial.html       # Commercial Approvals
│   ├── warehouse.html        # Warehouse Inventory
│   ├── client_confirmation.html  # Delivery Confirmations
│   ├── js/                    # JavaScript files (error handlers)
│   ├── css/                   # Stylesheets
│   └── components/            # Reusable HTML components
├── init_db.py                 # Database initialization script
├── start.cmd                  # Quick start batch file
├── PROJECT_STATUS.md          # Detailed status report
└── README.md                  # This file
```

---

## ✅ Testing Results

All 9 API modules tested and verified:
- ✓ PR CRUD + Recommend + Commercial Decision
- ✓ Vendor CRUD + Negotiations
- ✓ PO CRUD
- ✓ Account CRUD + Payment marking
- ✓ Tax calculation
- ✓ Client confirmations
- ✓ Warehouse items
- ✓ Error handling (400, 404, 500)
- ✓ All 9 frontend pages load and display data

---

## 💾 Key Files for Viva Explanation

**Backend API Examples**:
- `backend/routes/pr_routes.py` - CRUD pattern
- `backend/routes/commercial_routes.py` - Business logic (filter + update)
- `backend/routes/tax_routes.py` - Simple calculation

**Frontend Examples**:
- `Frontend/pr.html` - Fetch + error handling
- `Frontend/tax.html` - Form validation + calculation
- `Frontend/js/dashboard.js` - Error handler pattern

All code is simple, commented, and easy to explain in interviews.

---

**Status**: ✅ Complete & Tested
**Last Updated**: December 5, 2025
**Servers Running**: http://127.0.0.1:5000 (API) + http://localhost:5500 (GUI)