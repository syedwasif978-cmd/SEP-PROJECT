# SEP Project - Complete Viva Voce Preparation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture & Design](#architecture--design)
3. [Technology Stack](#technology-stack)
4. [Database Schema](#database-schema)
5. [Use Cases (UC-01 to UC-08)](#use-cases)
6. [Complete Workflow](#complete-workflow)
7. [Key Features](#key-features)
8. [API Endpoints](#api-endpoints)
9. [Important Q&A](#important-qa)

---

## Project Overview

### What is SEP?
**SEP (Supply & Expense Procurement)** is a Flask-based procurement and supply chain management system that automates the entire procure-to-pay workflow from client orders to invoice generation and payment.

### Core Purpose
- **Automate procurement workflows** from order placement to payment
- **Manage vendor relationships** with negotiation capabilities
- **Calculate taxes** automatically on transactions
- **Track inventory** in warehouses
- **Generate invoices** and manage financial accounts
- **Implement approval workflows** for multi-department coordination

### Target Users
- **Clients/Purchasers**: Place orders
- **Commercial Department**: Reviews client orders, requests quotations
- **Procurement Team**: Manages vendors and purchase requisitions
- **Finance Department**: Handles invoices, tax calculations, payments
- **Warehouse**: Receives goods, tracks inventory

---

## Architecture & Design

### 3-Tier Architecture
```
┌─────────────────────────────────────┐
│      Frontend Layer (HTML/CSS/JS)   │ ← User Interface
├─────────────────────────────────────┤
│  Controllers & Routes (API Layer)   │ ← HTTP Endpoints
├─────────────────────────────────────┤
│  Services & Business Logic          │ ← Core Logic
├─────────────────────────────────────┤
│  Models (ORM)                       │ ← Database Mapping
├─────────────────────────────────────┤
│  Database (SQLite/Oracle)           │ ← Data Persistence
└─────────────────────────────────────┘
```

### Design Principles
1. **MVC Pattern**: Models, Views, Controllers separation
2. **Service-Oriented**: Business logic in services
3. **RESTful API**: Standard HTTP methods for operations
4. **Modular Routes**: Separate blueprint files for different features
5. **ORM-Based**: SQLAlchemy for database abstraction

### Why This Architecture?
- **Maintainability**: Each layer has distinct responsibilities
- **Scalability**: Easy to add new features without affecting existing code
- **Testability**: Layers can be tested independently
- **Reusability**: Services can be used by multiple controllers
- **Flexibility**: Can switch databases without changing business logic

---

## Technology Stack

### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | Flask | 2.2.5 | Lightweight web framework |
| ORM | SQLAlchemy | 3.0.3 | Database abstraction layer |
| Migrations | Flask-Migrate | 4.0.4 | Schema version control |
| Serialization | Marshmallow | 3.19.0 | JSON schema validation |
| Environment | python-dotenv | 1.0.0 | Configuration management |
| Database Adapter | cx_Oracle | - | Oracle database connectivity |

### Frontend
- **HTML5**: Semantic markup, form handling
- **CSS3**: Styling with responsive design
- **Vanilla JavaScript**: DOM manipulation, API calls, event handling
- **No Framework**: Lightweight, fast loading

### Database
- **SQLite**: Default (development) - located at `backend/app.db`
- **Oracle**: Production (via cx_Oracle)

### Why Flask?
- Lightweight and flexible
- Easy to understand and modify
- Excellent ORM support (SQLAlchemy)
- Good for rapid development
- Sufficient for enterprise applications

---

## Database Schema

### Entity Relationship Diagram
```
                    ┌─────────────────┐
                    │    orders       │
                    └────────┬────────┘
                             │ 1:N
                    ┌────────┴────────┐
                    │                 │
        ┌───────────▼─────────┐      │
        │  quotations         │      │
        │                     │      │
        └───────────┬─────────┘      │
                    │ Selected       │
                    │                │
        ┌───────────▼──────────────┐ │
        │ purchase_orders          │◄┘
        │ (vendor_id, items JSON)  │
        └───────────┬──────────────┘
                    │
        ┌───────────┼──────────────┐
        │           │              │
    ┌───▼────┐  ┌───▼────┐  ┌────▼─────┐
    │invoices│  │accounts│  │warehouse │
    │        │  │        │  │items     │
    └────────┘  └────────┘  └──────────┘
    
    ┌──────────────┐
    │   vendors    │ ← Referenced by quotations & POs
    └──────────────┘
    
    ┌────────────────────┐
    │ tax_calculations   │
    └────────────────────┘
```

### Core Tables

#### 1. **orders** (UC-01)
- **id**: UUID (Primary Key)
- **client_name**: String
- **description**: Text
- **quantity**: Integer
- **status**: placed → submitted_to_commercial → quotation_requested → po_created → completed
- **total_budget**: Float
- **created_at, updated_at**: DateTime

**Purpose**: Capture initial client orders

---

#### 2. **quotations** (UC-02)
- **id**: Primary Key
- **order_id**: FK → orders
- **vendor_id**: FK → vendors
- **quote_value**: Float (price offered)
- **status**: requested → quoted → selected
- **created_at**: DateTime

**Purpose**: Manage vendor quotations for client orders

---

#### 3. **purchase_orders** (UC-03)
- **id**: UUID (Primary Key)
- **vendor_id**: FK → vendors
- **items**: JSON (list of items with sku, name, qty, unit_price)
- **total**: Float
- **status**: created → sent → received → inspected
- **inspection**: pass/fail/pending
- **created_at**: DateTime

**Purpose**: Purchase orders sent to vendors

**Why JSON for items?**
- Flexibility - store any item structure
- Simplicity - no need for separate items table
- Performance - faster queries
- Immutability - PO items don't change

---

#### 4. **invoices** (UC-08)
- **id**: Primary Key
- **po_id**: FK → purchase_orders
- **invoice_number**: String (Unique)
- **amount**: Float (base)
- **tax_amount**: Float
- **total**: Computed (amount + tax)
- **status**: generated → reviewed → paid → archived
- **created_at**: DateTime

**Purpose**: Invoice generation and tracking for payment

---

#### 5. **vendors**
- **id**: UUID (Primary Key)
- **name**: String
- **contact**: String
- **rating**: Integer (1-5)
- **payment_terms**: String
- **discount_percentage**: Float

**Purpose**: Vendor master data

---

#### 6. **warehouse_items** (UC-06)
- **id**: UUID (Primary Key)
- **sku**: String (Unique - Stock Keeping Unit)
- **name**: String
- **qty**: Integer (current stock)
- **updated_at**: DateTime

**Purpose**: Inventory tracking

---

#### 7. **accounts** (UC-07)
- **id**: Primary Key
- **po_id**: FK → purchase_orders
- **amount**: Float
- **status**: pending → paid
- **created_at**: DateTime

**Purpose**: Financial transactions tracking

---

#### 8. **tax_calculations** & **tax_records** (UC-08)
- **tax_rate**: 5%, 12%, 18%, or 28% (India GST model)
- **tax_amount**: Calculated amount
- **calculation_date**: DateTime

**Tax Rates**:
- **5%**: Essential goods (food, medicine)
- **12%**: Intermediate goods (raw materials)
- **18%**: General items (office supplies, furniture)
- **28%**: Luxury items (electronics, premium goods)

---

## Use Cases

### UC-01: Client Places Order
1. Client fills in order form with description, quantity, budget
2. Order saved with status='placed'
3. Commercial department receives notification
4. **Endpoint**: `POST /api/orders/create`

---

### UC-02: Request Quotations from Vendors
1. Commercial dept reviews placed order
2. System identifies suitable vendors
3. Quotation requests sent
4. Vendors respond with quotes
5. **Endpoints**: 
   - `GET /api/quotations/by-order/<order_id>`
   - `POST /api/quotations/request`

---

### UC-03: Create & Send Purchase Orders
1. Quotation comparison and vendor selection
2. Purchase order generated from selected quotation
3. PO sent to vendor (status='sent')
4. **Endpoints**:
   - `POST /api/po/create`
   - `PUT /api/po/<po_id>/send`

---

### UC-04: Vendor Negotiation
1. Negotiation initiated for discounts/terms
2. Back-and-forth communication logged
3. Final terms agreed upon
4. PO updated with negotiated terms
5. **Endpoints**: 
   - `POST /api/negotiation/start`
   - `POST /api/negotiation/<neg_id>/update-terms`

---

### UC-05: Goods Receipt & Inspection
1. PO marked as 'received'
2. Goods physically inspected
3. Inspection result recorded (pass/fail)
4. Items added to warehouse if passed
5. **Endpoints**:
   - `PUT /api/po/<po_id>/receive`
   - `PUT /api/po/<po_id>/inspect`

---

### UC-06: Warehouse Management
1. Received items tracked in warehouse
2. Inventory levels updated
3. Stock alerts generated if low
4. **Endpoints**:
   - `GET /api/warehouse/inventory`
   - `POST /api/warehouse/items`
   - `PUT /api/warehouse/items/<sku>`

---

### UC-07: Financial Accounting
1. Invoice generated from completed PO
2. Account entry created for transaction
3. Payment status tracked (pending/paid)
4. **Endpoints**:
   - `GET /api/accounts/all`
   - `POST /api/accounts/record`
   - `PUT /api/accounts/<account_id>/pay`

---

### UC-08: Invoice Generation & Tax Calculation
1. PO completion triggers invoice generation
2. Tax rate determined based on item type
3. Tax amount calculated (5%, 12%, 18%, or 28%)
4. Invoice total = PO amount + tax
5. Invoice stored and marked for payment
6. **Endpoints**:
   - `POST /api/tax/calculate`
   - `POST /api/invoices/generate`
   - `GET /api/invoices/<invoice_id>`

---

## Complete Workflow

### Procure-to-Pay Flow
```
┌─────────────────┐
│ Client Places   │
│ Order (UC-01)   │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│ Commercial Requests      │
│ Quotations (UC-02)       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Vendor Provides Quotes & │
│ Negotiates (UC-04)       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Procurement Creates PO & │
│ Sends to Vendor (UC-03)  │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Warehouse Receives Goods │
│ & Inspects (UC-05, UC-06)│
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Finance Generates Invoice│
│ & Calculates Tax (UC-08) │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Finance Records Payment  │
│ (UC-07)                  │
└──────────────────────────┘
```

### Status Transitions
**Order**: placed → submitted_to_commercial → quotation_requested → po_created → completed

**PO**: created → sent → received → inspected (pass/fail/pending)

**Invoice**: generated → reviewed → paid → archived

---

## Key Features

### 1. Vendor Negotiation
- Negotiation rounds logged
- Discount tracking
- Terms auditing
- History maintained

### 2. Multi-Level Approvals
- Commercial Manager reviews orders
- Procurement Manager approves quotations
- Finance Manager approves invoices

### 3. Automatic Tax Calculation
- Rates: 5%, 12%, 18%, 28%
- Based on item type and category
- Tax records for compliance

### 4. Inventory Management
- SKU-based tracking
- Real-time quantity updates
- Stock alerts

### 5. Workflow Automation
- `utils/workflow.py` contains `process_pr_full()` function
- Automates entire PR-to-payment workflow in one call

---

## API Endpoints

### Order APIs
```
POST   /api/orders/create              → Create new order
GET    /api/orders/<order_id>          → Get order details
GET    /api/orders/all                 → List all orders
PUT    /api/orders/<order_id>          → Update order
DELETE /api/orders/<order_id>          → Delete order
```

### Purchase Order APIs
```
POST   /api/po/create                  → Create PO
GET    /api/po/<po_id>                 → Get PO details
GET    /api/po/all                     → List all POs
PUT    /api/po/<po_id>/send            → Send PO to vendor
PUT    /api/po/<po_id>/receive         → Mark as received
PUT    /api/po/<po_id>/inspect         → Record inspection
```

### Quotation APIs
```
POST   /api/quotations/request         → Request quotation
GET    /api/quotations/by-order/<id>   → Get quotes for order
PUT    /api/quotations/<quote_id>/select → Select quotation
```

### Vendor APIs
```
GET    /api/vendors/all                → List all vendors
POST   /api/vendors/create             → Add new vendor
PUT    /api/vendors/<vendor_id>        → Update vendor
GET    /api/vendors/<vendor_id>        → Get vendor details
```

### Invoice APIs
```
POST   /api/invoices/generate          → Create invoice from PO
GET    /api/invoices/<invoice_id>      → Get invoice
GET    /api/invoices/all               → List all invoices
PUT    /api/invoices/<invoice_id>/pay  → Mark invoice paid
```

### Tax APIs
```
POST   /api/tax/calculate              → Calculate tax for order
GET    /api/tax/records                → Get tax records
```

### Account APIs
```
POST   /api/accounts/record            → Record financial transaction
GET    /api/accounts/all               → List all accounts
PUT    /api/accounts/<account_id>/pay  → Record payment
```

### Warehouse APIs
```
GET    /api/warehouse/inventory        → Get warehouse stock
POST   /api/warehouse/items            → Add item to warehouse
PUT    /api/warehouse/items/<sku>      → Update item quantity
```

### Dashboard APIs
```
GET    /api/dashboard/stats            → Get dashboard statistics
GET    /api/dashboard/pending-approvals → Get pending tasks
```

---

## Important Q&A

### Why Flask instead of Django?
✅ **Advantages**:
- Lightweight and flexible
- Not opinionated - allows custom architecture
- Easy to understand and modify
- Great learning experience
- Excellent ORM support (SQLAlchemy)
- Sufficient for this project's scope

### Why SQLAlchemy ORM instead of raw SQL?
✅ **Advantages**:
- **Abstraction**: Switch databases without code changes (SQLite → Oracle)
- **Type safety**: Python objects instead of raw queries
- **Relationships**: Easy to define foreign keys
- **Validation**: Built-in data type checking
- **Security**: Prevents SQL injection automatically
- **Flexibility**: Can use raw SQL when needed

### Why vanilla JavaScript instead of React/Vue/Angular?
✅ **Advantages**:
- No build process - files served directly
- Minimal dependencies - no npm
- Fast loading - small bundle size
- Deep DOM understanding
- Sufficient for current needs

❌ **Trade-offs**:
- More boilerplate code
- Steeper learning curve for component reuse
- If project grows significantly, would consider Vue.js

### Why store items as JSON in purchase_orders?
✅ **Advantages**:
- **Flexibility** - store any item structure
- **Simplicity** - no need for separate items table
- **Performance** - faster queries
- **Immutability** - PO items are immutable
- **Denormalization** - faster read operations

### How does tax calculation work?
Tax is based on 4 GST brackets:
- **5%**: Essential goods
- **12%**: Intermediate goods
- **18%**: General items (Office supplies, furniture)
- **28%**: Luxury items (Electronics, premium goods)

Calculation: `tax_amount = order_amount × tax_rate / 100`

### How does vendor negotiation work?
1. Negotiation initiated after quotation received
2. Rounds of negotiation logged
3. Initial quote → Negotiated price → Final agreed price
4. Discount percentage tracked
5. PO updated with final price

### What databases are supported?
- **Development**: SQLite (file-based at `backend/app.db`)
- **Production**: Oracle (via cx_Oracle)
- **Configuration**: `DATABASE_URL` environment variable switches between them
- **Zero code changes** required for database switch

### Key Files to Know
- `app.py` - Flask application setup
- `config/settings.py` - Configuration
- `config/db.py` - Database initialization
- `utils/workflow.py` - Workflow automation
- `models/*.py` - Data structures
- `services/*.py` - Business logic
- `routes/*.py` - API endpoints
- `controllers/*.py` - Request handling

### What is the Request-Response Cycle?
1. **User**: Clicks action in frontend
2. **Frontend**: JavaScript validates input and sends HTTP request
3. **Route**: Flask route handler receives request
4. **Controller**: Processes request and calls service
5. **Service**: Executes business logic
6. **Model**: Interacts with database via ORM
7. **Database**: Stores/retrieves data
8. **Response**: JSON response sent back
9. **Frontend**: JavaScript updates DOM with response

### Challenges Faced & Solutions
1. **Database abstraction** - Used SQLAlchemy ORM
2. **Workflow complexity** - Created workflow.py with automation
3. **Tax calculation** - Implemented tax_service.py with 4 brackets
4. **Vendor negotiation** - Created vendor_negotiation model and routes
5. **Multi-level approvals** - Implemented approval workflows in services
6. **Real-time inventory** - SKU-based warehouse item tracking

### What Would You Improve?
1. **Frontend Framework**: Migrate to Vue.js or React for better component reuse
2. **Testing**: Add comprehensive unit and integration tests
3. **API Documentation**: Use Swagger/OpenAPI for auto-generated docs
4. **Logging**: Implement structured logging with ELK stack
5. **Authentication**: Add role-based access control (RBAC)
6. **Caching**: Implement Redis for performance
7. **Async Jobs**: Use Celery for long-running tasks
8. **Notifications**: Add email/SMS for status updates

---

**Good luck with your viva! You've built a comprehensive procurement system. Be confident and explain your design decisions clearly.**
