# Procurement Management System (Rewritten)

A complete rewrite of the procurement management system following formal use cases (UC-01 through UC-08) with a focus on user-friendly interface and automated workflow progression.

## 📋 System Overview

The system implements an 8-step procurement workflow:

### Use Cases (UC-01 to UC-08)

| UC | Title | Module | Description |
|---|---|---|---|
| **UC-01** | Place Order | Order Placement | Client places an order with Commercial Department |
| **UC-02** | Submission of Quotation | Quotation Management | Vendors submit quotations for approved orders |
| **UC-03** | Purchase Order Issued | PO Issuance | Commercial issues PO to selected vendor |
| **UC-04** | PR Approval | PR Department | PR approval (legacy - being refactored) |
| **UC-05** | Compare Vendor Quotation | Quotation Management | Commercial compares and selects best quotation |
| **UC-06** | Cost Calculation | Tax Department | Calculate base amount with applicable taxes |
| **UC-07** | Withholding Tax Calculation | Tax Department | Calculate FBR withholding tax per regulations |
| **UC-08** | Invoice Bills Generation | Accounts | Generate and manage invoice bills & payments |

## 🏗️ Architecture

### Backend (Flask + SQLAlchemy)
- **Framework**: Flask 2.2.x
- **ORM**: SQLAlchemy with SQLite
- **Python**: 3.14+

### Frontend (HTML/CSS/JavaScript)
- **Architecture**: Single Page Application (SPA)
- **Styling**: Modern CSS with gradient UI
- **Notifications**: Toast notification system (js/toast.js)

## 📂 Project Structure

### Backend (`backend/`)

#### Models (`models/`)
- **order.py** - Order model with client details, quantities, budgets, status
- **quotation.py** - Vendor quotations with unit/total prices, delivery days
- **invoice.py** - Invoice generation with tax and payment tracking
- **tax_record.py** - Tax calculations (cost and withholding tax)

#### Routes (`routes/`)
- **order_routes.py** - POST/GET/PUT endpoints for orders (UC-01)
- **quotation_routes.py** - Submit, list, approve, reject quotations (UC-02, UC-05)
- **invoice_routes.py** - Generate, list, mark paid invoices (UC-08)
- **tax_routes_new.py** - Calculate cost and withholding tax (UC-06, UC-07)

### Frontend (`Frontend/`)

#### Pages
- **dashboard_new.html** - Main dashboard with workflow overview and order tracking
- **order.html** - Order placement form (UC-01) with workflow indicator
- **quotation.html** - Vendor quotation submission and commercial comparison (UC-02, UC-05)
- **invoice.html** - Invoice generation with tax calculation and payment tracking (UC-06, UC-07, UC-08)

#### Components (`components/`)
- **header.html** - Navigation bar with toast container
- **sidebar.html** - Navigation menu with workflow steps

#### Styling (`css/`)
- **dashboard.css** - Main styling
- **toast.css** - Toast notification styles

#### Scripts (`js/`)
- **toast.js** - Toast notification system
- Other page-specific JavaScript

## 🚀 Getting Started

### Installation

1. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run Server**
   ```bash
   python app.py
   ```
   - Backend runs on `http://127.0.0.1:5000`
   - Frontend opens automatically in browser

### Database

- **SQLite** database in `backend/` (auto-created on first run)
- Models auto-create tables via SQLAlchemy
- New models: `orders`, `quotations`, `invoices`, `tax_records`

## 📊 API Endpoints

### Orders (UC-01)
```
POST   /api/orders/           - Create new order
GET    /api/orders/           - List all orders
GET    /api/orders/<order_id> - Get order details
PUT    /api/orders/<order_id> - Update order status
```

### Quotations (UC-02, UC-05)
```
POST   /api/quotations/                  - Submit quotation
GET    /api/quotations/order/<order_id>  - List quotations for order (comparison)
POST   /api/quotations/<quote_id>/approve - Approve quotation
POST   /api/quotations/<quote_id>/reject  - Reject quotation
```

### Invoices (UC-08)
```
POST   /api/invoices/               - Generate invoice
GET    /api/invoices/               - List all invoices
GET    /api/invoices/<invoice_id>   - Get invoice details
POST   /api/invoices/<id>/mark-paid - Mark invoice as paid
```

### Tax Calculations (UC-06, UC-07)
```
POST   /api/tax/calculate-cost             - Calculate cost with tax
POST   /api/tax/calculate-withholding-tax - Calculate withholding tax
GET    /api/tax/records                    - List all tax records
GET    /api/tax/records/<invoice_id>      - Get tax records for invoice
```

## 🎨 User Interface Features

### Dashboard
- 📊 Real-time statistics (total orders, invoices, pending quotations, awaiting payment)
- 🔄 Workflow overview with 8 steps
- 📋 Recent orders table
- 🎯 Quick links to each workflow step

### Order Placement (UC-01)
- 📝 Client information form
- 📦 Order details with quantity & budget
- 📊 Real-time order summary
- ✨ Workflow indicator showing progress

### Quotation Management (UC-02, UC-05)
- 💬 **Submit Quotation Tab**: Vendors submit bids with unit/total prices, delivery days
- ⚖️ **Compare Quotations Tab**: Commercial compares multiple vendor bids
- 📊 **History Tab**: View all quotations and their status
- Color-coded status badges (submitted, approved, rejected)

### Invoice Management (UC-06, UC-07, UC-08)
- 💵 **Generate Invoice Tab**: Create invoices with tax calculation
- 🧮 **Tax Calculator**: Integrated cost calculation and withholding tax
- 💳 **Payment Tracking Tab**: Mark invoices as paid
- 📋 **Invoice List Tab**: View all generated invoices

### Notifications
- 🎯 Toast notifications (success, error, warning, info)
- ✨ Non-intrusive user feedback
- Automatic dismissal after 4 seconds

## 🔄 Workflow Logic

### Order Progression
1. **Client** places order → Status: `placed`, then → `submitted_to_commercial`
2. **Commercial** receives order → Requests quotations from vendors
3. **Vendors** submit quotations → Status: `submitted`
4. **Commercial** compares quotations (UC-05) → Selects best vendor → Status: `approved`
5. **Commercial** issues PO → Transfer to warehouse
6. **Warehouse** receives goods
7. **Tax Dept** calculates cost (UC-06) and withholding tax (UC-07)
8. **Accounts** generates invoice (UC-08) → Status: `generated`
9. **Accounts** marks as paid → Status: `paid`

### Status Fields
- **Orders**: `placed`, `submitted_to_commercial`, `quotation_requested`
- **Quotations**: `submitted`, `under_review`, `approved`, `rejected`
- **Invoices**: `generated`, `verified`, `approved`, `paid`
- **Tax Records**: `calculated`, `verified`, `recorded`

## 📝 Data Models

### Order
```python
{
    "id": "uuid",
    "client_name": "string",
    "client_email": "string",
    "description": "string",
    "quantity": "integer",
    "total_budget": "float",
    "status": "string",
    "created_at": "datetime"
}
```

### Quotation
```python
{
    "id": "uuid",
    "order_id": "uuid",
    "vendor_id": "string",
    "unit_price": "float",
    "total_price": "float",
    "delivery_days": "integer",
    "notes": "string",
    "status": "string",
    "created_at": "datetime"
}
```

### Invoice
```python
{
    "id": "uuid",
    "order_id": "uuid",
    "po_id": "uuid",
    "vendor_id": "string",
    "delivery_challan": "string",
    "invoice_number": "string",
    "base_amount": "float",
    "tax_amount": "float",
    "withholding_tax": "float",
    "total_amount": "float",
    "status": "string",
    "payment_status": "string",
    "payment_date": "datetime"
}
```

### TaxRecord
```python
{
    "id": "uuid",
    "order_id": "uuid",
    "invoice_id": "uuid",
    "base_amount": "float",
    "tax_rate": "float",
    "tax_amount": "float",
    "withholding_tax_rate": "float",
    "withholding_tax_amount": "float",
    "net_amount": "float",
    "calculation_type": "cost_calc|withholding_tax",
    "status": "calculated|verified|recorded"
}
```

## 🧪 Testing

Run the end-to-end test:
```bash
cd backend
python e2e_test.py
```

## 🔐 Security & Compliance

- **FBR Withholding Tax**: Implemented as per Pakistan tax regulations (UC-07)
- **Input Validation**: All API endpoints validate input data
- **Error Handling**: Comprehensive error messages for user guidance

## 📈 Future Enhancements

- [ ] Role-based access control (Client, Commercial, Vendor, Tax Dept, Accounts)
- [ ] PO issuance form (UC-03) - In progress
- [ ] Warehouse/Delivery management
- [ ] Inspection reports
- [ ] Email notifications to stakeholders
- [ ] Document uploads (invoices, delivery challans)
- [ ] Multi-currency support
- [ ] Advanced reporting and analytics
- [ ] Mobile app version

## 🤝 Integration Notes

### Legacy Modules
The following modules are from the previous version and are being refactored:
- `pr.html`, `commercial.html`, `po.html` (being replaced by new workflow)
- `vendor_routes.py`, `negotiation_routes.py` (legacy - will be consolidated)
- `account_routes.py`, `client_routes.py` (legacy - will be consolidated)

### Migration Path
- Old tables remain in database for backward compatibility
- New models use separate tables (`orders`, `quotations`, `invoices`, `tax_records`)
- Both old and new routes are active simultaneously during transition

## 📞 Support

For issues or questions:
1. Check the `logs/` directory for error messages
2. Review API responses for detailed error information
3. Check browser console for frontend errors
4. Review Flask terminal output for backend errors

## 📄 License

Internal project - Technical Solution Enterprise

---

**Last Updated**: 2024
**Version**: 2.0 (Complete Rewrite - Use Cases)
**Status**: Active Development
