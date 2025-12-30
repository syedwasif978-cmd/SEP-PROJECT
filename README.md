
A comprehensive procurement and supply chain management application built with **Flask** (Python backend) and **HTML/CSS/JavaScript** (frontend).

---

## 📋 Project Overview

The SEP System is a **use-case-driven procure-to-pay platform** that streamlines the entire workflow from order placement through invoice generation and payment. It manages suppliers, quotations, purchase orders, and financial operations with built-in approval workflows and tax calculations.

### Key Objectives
- **Automated Procurement**: Streamline order-to-payment workflows
- **Vendor Management**: Track and negotiate with suppliers
- **Financial Control**: Tax calculations, invoice generation, and payment tracking
- **Multi-Department Coordination**: Order, Commercial, Procurement, Finance, and Warehouse teams
- **Real-Time Dashboard**: Monitor all ongoing processes and approvals

---

## 🏗️ Architecture

### Technology Stack
| Layer | Technology |
|-------|-----------|
| **Backend** | Flask 2.2.5, SQLAlchemy 3.0.3 |
| **Database** | SQLite (default) / Oracle (via cx_Oracle) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Migrations** | Flask-Migrate 4.0.4 |
| **Data Serialization** | Marshmallow 3.19.0 |

### Project Structure

```
SEP_PROJ/
├── backend/                      # Flask application & API
│   ├── app.py                   # Main Flask app entry point
│   ├── init_db.py              # Database initialization script
│   ├── apply_schema_fix.py      # Schema migration utilities
│   ├── requirements.txt         # Python dependencies
│   ├── config/                 # Configuration module
│   │   ├── db.py               # Database initialization
│   │   └── settings.py         # Flask configuration
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── order.py            # UC-01: Client orders
│   │   ├── quotation.py        # UC-02: Vendor quotations
│   │   ├── purchase_order.py   # UC-03: PO creation & tracking
│   │   ├── invoice.py          # UC-08: Invoice generation
│   │   ├── purchase_requisition.py
│   │   ├── vendor.py           # Vendor master data
│   │   ├── account.py          # Financial accounts
│   │   ├── tax_calculation.py  # Tax computations
│   │   ├── tax_record.py       # Tax records & compliance
│   │   ├── warehouse_item.py   # Inventory tracking
│   │   ├── client_confirmation.py
│   │   ├── commercial_approval.py
│   │   ├── pr_approval.py
│   │   ├── vendor_negotiation.py
│   │   ├── bank_charges.py
│   │   └── __pycache__/
│   ├── routes/                 # API endpoint blueprints
│   │   ├── order_routes.py     # /api/orders - Order management
│   │   ├── quotation_routes.py # /api/quotations - Quotation workflow
│   │   ├── invoice_routes.py   # /api/invoices - Invoice generation
│   │   ├── po_routes_new.py    # /api/po - New PO endpoints
│   │   ├── pr_routes.py        # /api/pr - Purchase requisitions
│   │   ├── vendor_routes.py    # /api/vendors - Vendor management
│   │   ├── commercial_routes.py # /api/commercial - Commercial dept
│   │   ├── tax_routes.py       # /api/tax - Tax operations
│   │   ├── account_routes.py   # /api/accounts - Account management
│   │   ├── client_routes.py    # /api/client - Client operations
│   │   ├── warehouse_routes.py # /api/warehouse - Inventory
│   │   ├── negotiation_routes.py # /api/negotiation - Vendor negotiation
│   │   ├── dashboard_routes.py # /api - Dashboard data
│   │   └── __pycache__/
│   ├── controllers/            # Business logic layer
│   │   ├── order_controller.py
│   │   ├── pr_controller.py
│   │   ├── purchase_order_controller.py
│   │   ├── vendor_controller.py
│   │   ├── commercial_controller.py
│   │   ├── account_controller.py
│   │   ├── tax_controller.py
│   │   ├── client_controller.py
│   │   └── warehouse_controller.py
│   ├── services/               # Service layer (business operations)
│   │   ├── pr_service.py       # PR workflows
│   │   ├── po_service.py       # PO workflows
│   │   ├── vendor_service.py   # Vendor operations
│   │   ├── tax_service.py      # Tax calculations
│   │   ├── approval_service.py # Approval workflows
│   │   ├── negotiation_service.py # Vendor negotiations
│   │   ├── account_service.py
│   │   └── warehouse_service.py
│   ├── utils/                  # Utility functions
│   │   ├── helpers.py          # Common helper functions
│   │   ├── validators.py       # Data validation
│   │   └── workflow.py         # Workflow orchestration
│   └── logs/                   # Application logs
│
├── Frontend/                    # Web UI & static assets
│   ├── dashboard_new.html      # Main dashboard (SPA entry point)
│   ├── order.html              # Order placement interface
│   ├── quotation.html          # Quotation review & approval
│   ├── invoice.html            # Invoice management
│   ├── po.html                 # Purchase order interface
│   ├── pr.html                 # Purchase requisition form
│   ├── vendors.html            # Vendor management UI
│   ├── commercial.html         # Commercial dept interface
│   ├── tax.html                # Tax calculation interface
│   ├── warehouse.html          # Inventory management
│   ├── accounts.html           # Account management
│   ├── client_confirmation.html
│   ├── components/             # Reusable HTML components
│   │   ├── header.html         # Navigation header
│   │   ├── sidebar.html        # Collapsible sidebar (hover-based)
│   │   ├── approval_box.html   # Approval workflow UI
│   │   ├── pr_list_item.html
│   │   └── vendor_card.html
│   ├── css/                    # Stylesheets
│   │   ├── dashboard.css
│   │   ├── po.css
│   │   ├── pr.css
│   │   ├── vendors.css
│   │   ├── commercial.css
│   │   ├── warehouse.css
│   │   ├── accounts.css
│   │   └── toast.css           # Toast notifications
│   └── js/                     # Frontend logic
│       ├── dashboard.js        # Main dashboard logic
│       ├── pr.js              # PR form handling
│       ├── vendor.js          # Vendor operations
│       ├── vendors.js         # Vendor list management
│       ├── commercial.js      # Commercial dept operations
│       ├── account.js         # Account operations
│       ├── tax.js             # Tax form handling
│       ├── warehouse.js       # Inventory operations
│       ├── negotiation.js     # Vendor negotiations
│       └── toast.js           # Toast notifications
│
├── init_db.py                  # Database initialization script
├── run.cmd                     # Windows batch script to run app
├── start_new.cmd               # Alternative startup script
└── README.md                   # This file
```

---

## 🔄 Use Cases & Workflows

The system implements **8 core use cases (UC-01 through UC-08)**:

### UC-01: Order Placement
- **Actor**: Client/Customer
- **Process**: Client places an order with commercial department
- **Key Fields**: Client name, email, description, quantity, budget
- **Endpoint**: `POST /api/orders/`
- **Related Model**: `Order`

### UC-02: Quotation Submission
- **Actor**: Vendors
- **Process**: Vendors submit quotations in response to orders
- **Key Fields**: Unit price, total price, delivery days, notes
- **Endpoint**: `POST /api/quotations/`
- **Related Model**: `Quotation`
- **Status Flow**: submitted → under_review → approved/rejected

### UC-03: Purchase Order Creation
- **Actor**: Commercial/Procurement Department
- **Process**: Convert approved quotations into purchase orders
- **Key Fields**: Vendor ID, items list, total amount, inspection status
- **Endpoint**: `POST /api/po/`
- **Related Model**: `PurchaseOrder`
- **Status Flow**: created → sent → received

### UC-04: Purchase Requisition (PR)
- **Actor**: Procurement Department
- **Process**: Create purchase requisitions for internal processing
- **Key Fields**: PR number, items, quantity, approvals
- **Endpoint**: `POST /api/pr/`
- **Related Model**: `PurchaseRequisition`
- **Workflow**: Multi-level approval required

### UC-05: Vendor Negotiation
- **Actor**: Procurement Manager, Vendor
- **Process**: Negotiate terms, pricing, and delivery with vendors
- **Key Fields**: Negotiation terms, counter-offers, agreements
- **Endpoint**: `POST /api/negotiation/`
- **Related Model**: `VendorNegotiation`

### UC-06: Tax Calculation & Records
- **Actor**: Finance Department
- **Process**: Calculate applicable taxes (VAT, withholding tax, etc.)
- **Key Fields**: Tax percentage, base amount, tax amount, tax type
- **Endpoint**: `POST /api/tax/`
- **Related Models**: `TaxCalculation`, `TaxRecord`
- **Tax Types**: Standard VAT, Withholding Tax, Bank Charges

### UC-07: Warehouse & Inventory
- **Actor**: Warehouse Manager
- **Process**: Track received goods and inventory levels
- **Key Fields**: Item description, quantity, location, SKU
- **Endpoint**: `POST /api/warehouse/`
- **Related Model**: `WarehouseItem`

### UC-08: Invoice Generation & Payment
- **Actor**: Finance Department
- **Process**: Generate invoices, track payments, manage accounts payable
- **Key Fields**: Invoice number, base amount, taxes, total, payment status
- **Endpoint**: `POST /api/invoices/`
- **Related Model**: `Invoice`
- **Status Flow**: generated → verified → approved → paid

---

## 📡 API Endpoints

### Orders API
```
POST   /api/orders/             Create new order
GET    /api/orders/             List all orders
GET    /api/orders/<order_id>   Get specific order
PUT    /api/orders/<order_id>   Update order
DELETE /api/orders/<order_id>   Delete order
```

### Quotations API
```
POST   /api/quotations/         Submit quotation
GET    /api/quotations/         List quotations
GET    /api/quotations/<id>     Get quotation details
PUT    /api/quotations/<id>     Update quotation status
DELETE /api/quotations/<id>     Delete quotation
```

### Purchase Orders API
```
POST   /api/po/                 Create PO
GET    /api/po/                 List POs
GET    /api/po/<po_id>          Get PO details
PUT    /api/po/<po_id>          Update PO
DELETE /api/po/<po_id>          Delete PO
```

### Invoices API
```
POST   /api/invoices/           Generate invoice
GET    /api/invoices/           List invoices
GET    /api/invoices/<id>       Get invoice
PUT    /api/invoices/<id>       Update invoice status
DELETE /api/invoices/<id>       Delete invoice
```

### Vendors API
```
POST   /api/vendors/            Add vendor
GET    /api/vendors/            List vendors
GET    /api/vendors/<id>        Get vendor details
PUT    /api/vendors/<id>        Update vendor
DELETE /api/vendors/<id>        Remove vendor
```

### Tax API
```
POST   /api/tax/                Calculate tax
GET    /api/tax/                Get tax records
PUT    /api/tax/<id>            Update tax record
```

### Warehouse API
```
POST   /api/warehouse/          Add inventory item
GET    /api/warehouse/          List inventory
PUT    /api/warehouse/<id>      Update stock
DELETE /api/warehouse/<id>      Remove item
```

### Purchase Requisitions API
```
POST   /api/pr/                 Create PR
GET    /api/pr/                 List PRs
PUT    /api/pr/<id>/approve     Approve PR
PUT    /api/pr/<id>/reject      Reject PR
```

### Dashboard API
```
GET    /api/dashboard           Dashboard summary data
GET    /api/reports            Reports & analytics
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Windows/Linux/macOS

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "d:\UNIVER\SEP PROJ"
   ```

2. **Create Python virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```
   This creates the SQLite database (`app.db`) with all required tables.

5. **Run the application**
   
   **Option A - Windows batch script:**
   ```bash
   cd ..
   run.cmd
   ```
   
   **Option B - Direct Python:**
   ```bash
   cd backend
   python app.py
   ```

6. **Access the application**
   - Open browser: http://127.0.0.1:5000/
   - The dashboard will automatically open in your default browser

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.2.5 | Web framework |
| Flask-SQLAlchemy | 3.0.3 | ORM & database handling |
| Flask-Migrate | 4.0.4 | Database migrations |
| Marshmallow | 3.19.0 | Data serialization & validation |
| python-dotenv | 1.0.0 | Environment variable management |
| cx_Oracle | Latest | Oracle database support (optional) |

---

## 🛢️ Database Configuration

### Default (SQLite)
```python
# backend/config/settings.py
DATABASE_URL = 'sqlite:///app.db'
```

### Oracle (Optional)
Update the `DATABASE_URL` in environment or `config/settings.py`:
```python
DATABASE_URL = 'oracle://user:password@host:1521/sid'
```

### Database Models
All models inherit from `db.Model` (SQLAlchemy):
- Automatic UUID primary keys
- Timestamp tracking (created_at, updated_at)
- Foreign key relationships
- JSON field support for complex data

---

## 🎨 Frontend Architecture

### Responsive Design
- **Sidebar**: Hover-based expansion (60px collapsed, full width expanded)
- **Dashboard**: 8 workflow button grid (responsive grid layout)
- **Mobile**: Touch-friendly interface with visual feedback
- **Animations**: Smooth 0.35s transitions

### Components
- **header.html**: Navigation and branding
- **sidebar.html**: Module navigation with hover expansion
- **approval_box.html**: Workflow approval UI
- **Toast notifications**: Real-time user feedback

### Static Files
All frontend files served from `/Frontend` directory via Flask static route.

---

## 🔐 Security Features

- **CSRF Protection**: Flask default CSRF handling
- **SQL Injection Prevention**: SQLAlchemy parameterized queries
- **Input Validation**: Server-side validation in controllers
- **Database Constraints**: Unique constraints, foreign keys

---

## 📊 Dashboard Modules

The dashboard provides access to 8 core workflow modules:

1. **Orders** - Create and track customer orders
2. **Quotations** - Manage vendor quotations
3. **Purchase Orders** - Create and monitor POs
4. **Invoices** - Generate and track invoices
5. **Vendors** - Manage supplier database
6. **Tax** - Calculate and record taxes
7. **Warehouse** - Manage inventory
8. **Commercial** - Commercial dept operations

---

## 🔄 Data Flow Example: Order-to-Payment

```
1. Customer places Order (UC-01)
   ↓
2. Vendors submit Quotations (UC-02)
   ↓
3. Commercial approves best Quotation
   ↓
4. System creates Purchase Order (UC-03)
   ↓
5. Goods received in Warehouse (UC-07)
   ↓
6. Vendor submits Invoice with Taxes (UC-06 + UC-08)
   ↓
7. Finance approves and records Payment
   ↓
8. Order marked as Complete
```

---

## 🧪 Testing & Validation

### Testing Files (Removed)
The following test/check files have been removed as part of cleanup:
- `e2e_test.py` - End-to-end tests
- `test_api.py` - API endpoint tests
- `test_endpoints_direct.py` - Direct endpoint tests
- `test_uc_workflow.py` - Use-case workflow tests
- `check_endpoints.py` - Endpoint validation
- `db_inspect.py` - Database schema inspection

For testing, use Python's built-in `unittest` or `pytest`:
```bash
pip install pytest
pytest backend/
```

---

## 🐛 Troubleshooting

### Issue: Port 5000 already in use
```bash
# Windows: Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :5000
kill -9 <PID>
```

### Issue: Database locked
- Delete `app.db` and reinitialize:
```bash
python init_db.py
```

### Issue: Module import errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Issue: Frontend files not loading
- Verify `/Frontend` folder exists in project root
- Check Flask logs for static file path errors

---

## 📝 Environment Variables

Create `.env` file in project root:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
```

---

## 📚 Documentation References

- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Marshmallow**: https://marshmallow.readthedocs.io/

---

## 🤝 Contributing

### Code Structure Guidelines
1. Keep business logic in `services/`
2. Keep API logic in `routes/` and `controllers/`
3. Keep data models in `models/`
4. Use utilities from `utils/` for common operations

### Adding New Features
1. Create model in `models/`
2. Create routes in `routes/`
3. Add service logic in `services/`
4. Create frontend UI in `Frontend/`
5. Create controller if needed in `controllers/`

---

## 📄 License

This project is developed for educational purposes.

---

## 📞 Support

For issues or questions:
1. Check the API endpoint documentation above
2. Review model definitions in `backend/models/`
3. Check application logs in `backend/logs/`
4. Review Flask error messages in console

---

## ✅ Last Updated

**Date**: December 30, 2025  
**Version**: 1.0 - Production Ready

---

## 🗑️ Cleanup Summary

The following files were removed during repository cleanup (December 30, 2025):
- Test files: `e2e_test.py`, `test_api.py`, `test_endpoints_direct.py`, `test_uc_workflow.py`
- Check files: `check_endpoints.py`, `db_inspect.py`
- Documentation: `DASHBOARD_FIXES_FINAL.md`

This README serves as the single source of truth for all system documentation.
