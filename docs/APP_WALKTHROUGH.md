# SEP Project — Full Application Walkthrough (context for an AI assistant)

> **Purpose of this file:** paste it into a fresh AI chat so the assistant understands the whole app without access to the repository. It is self-contained — code snippets and schemas are inline. It describes what the code **actually does today**, including its quirks and inconsistencies (which matter for giving correct help).

---

## 0. TL;DR (read this first)

This is a **procurement & accounts management web app** ("procure-to-pay") for a small automobile-machinery workshop called **Technical Solution Enterprise (TSE)**. It models the flow: **client order → vendor quotation → compare/approve → purchase order → goods receipt → invoice + tax → payment**, across five departments (Commercial, PR/Procurement, Tax, Accounts, Warehouse).

- **Backend:** Python **Flask** + **Flask-SQLAlchemy** ORM, **SQLite** database (`backend/app.db`).
- **Frontend:** plain **HTML/CSS/vanilla JavaScript** pages (one per department), served as static files by Flask.
- **No authentication, no user accounts, no roles** — any client can call any endpoint.
- **No automated tests.**
- It's a **student/academic prototype**: functional but with rough edges (in-memory data in one place, duplicate/overlapping routes, two "generations" of code, and documentation that contradicts the code in places).

---

## 1. Tech stack

| Layer | Technology |
|-------|-----------|
| Web framework | Flask 2.2.5 |
| ORM | Flask-SQLAlchemy 3.0.3 |
| DB (dev) | SQLite — file at `backend/app.db` |
| DB (intended prod) | PostgreSQL/Oracle via `DATABASE_URL` env var (not actually used) |
| Frontend | HTML5 + CSS3 + vanilla JS (no framework, no build step) |
| Serialization | a hand-written `to_dict()` helper (Marshmallow is listed but not really used) |
| Run | `python backend/app.py` → serves on `http://127.0.0.1:5000/` and auto-opens a browser |

Config (`backend/config/settings.py`):
```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + .../app.db)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

## 2. Folder structure (backend)

```
backend/
  app.py                # Flask entry point: registers blueprints, serves frontend
  config/
    db.py               # db = SQLAlchemy()
    settings.py         # Config (SQLite URI, secret key)
  models/               # SQLAlchemy ORM models (one table each)
    order.py quotation.py purchase_order.py purchase_requisition.py
    invoice.py tax_record.py tax_calculation.py vendor.py account.py
    warehouse_item.py client_confirmation.py commercial_approval.py
    pr_approval.py vendor_negotiation.py bank_charges.py
  routes/               # Flask blueprints (the actual API)
    order_routes.py quotation_routes.py invoice_routes.py po_routes_new.py   # "new" gen
    pr_routes.py vendor_routes.py negotiation_routes.py po_routes.py         # "legacy" gen
    commercial_routes.py account_routes.py tax_routes.py tax_routes_new.py
    client_routes.py warehouse_routes.py dashboard_routes.py
    pr_routes_duplicate.py                                                   # orphan dupe
  services/             # mostly EMPTY/thin stubs (tax_service.py is empty)
  controllers/          # thin/largely unused
  utils/
    helpers.py          # to_dict() serializer
    validators.py       # require_fields() (barely used)
    workflow.py         # process_pr_full(): the big automation chain
  apply_schema_fix.py   # one-off ALTER TABLE script for purchase_orders

Frontend/
  dashboard_new.html (SPA entry) order.html quotation.html po.html pr.html
  tax.html invoice.html accounts.html vendors.html warehouse.html client_confirmation.html
  css/  js/  components/
```

---

## 3. How it boots and serves (`backend/app.py`)

```python
app = Flask('sep_project', static_folder=FRONTEND_DIR, static_url_path='/')
app.config.from_object('config.settings.Config')
db.init_app(app)

# "New" use-case blueprints
app.register_blueprint(order_bp,     url_prefix='/api/orders')
app.register_blueprint(quotation_bp, url_prefix='/api/quotations')
app.register_blueprint(invoice_bp,   url_prefix='/api/invoices')
app.register_blueprint(po_bp_new,    url_prefix='/api/po')      # (1) in-memory PO

# "Legacy" blueprints
app.register_blueprint(pr_bp,          url_prefix='/api/pr')
app.register_blueprint(vendor_bp,      url_prefix='/api/vendors')
app.register_blueprint(negotiation_bp, url_prefix='/api/negotiation')
app.register_blueprint(po_bp,          url_prefix='/api/po')    # (2) DB PO — SAME prefix!
app.register_blueprint(commercial_bp,  url_prefix='/api/commercial')
app.register_blueprint(account_bp,     url_prefix='/api/accounts')
app.register_blueprint(tax_bp,         url_prefix='/api/tax')   # legacy tax (flat 10%)
app.register_blueprint(client_bp,      url_prefix='/api/client')
app.register_blueprint(warehouse_bp,   url_prefix='/api/warehouse')
app.register_blueprint(dashboard_routes.bp, url_prefix='/api')
```

- `/` serves `Frontend/dashboard_new.html`. Unknown non-API paths fall back to the dashboard (SPA-style). Unknown `/api/...` paths return JSON 404.
- **Important:** `tax_routes_new.py` is **NOT imported/registered** here. Its fancy `calculate-cost` / `calculate-withholding-tax` endpoints are effectively **dead code**. The live `/api/tax` is the legacy one.
- **Important:** `po_bp_new` and legacy `po_bp` are **both registered at `/api/po`** → overlapping routes (see §7).

**Architecture pattern (intended):** `Frontend (JS fetch) → Flask route (blueprint) → [service] → SQLAlchemy model → SQLite`. In practice most business logic lives directly in the route functions; the `services/` and `controllers/` layers are mostly empty.

`to_dict()` (`utils/helpers.py`) is the universal serializer — it just loops over a model's columns and returns a dict, which routes `jsonify`.

---

## 4. Database model (all tables)

All primary keys are UUID strings (`default=lambda: str(uuid.uuid4())`). Money is `Float`. There are no enforced enums — "status" fields are free strings with conventional values.

| Table (model) | Key columns | Status values | Notes |
|---------------|------------|---------------|-------|
| `orders` (Order) | client_name, client_email, description, quantity, total_budget, status | `placed → quotation_requested → po_created → completed` | UC-01 |
| `quotations` (Quotation) | order_id→orders, vendor_id→vendors, unit_price, total_price, delivery_days, notes, status | `submitted → approved/rejected → po_issued` | UC-02/05 |
| `purchase_requisitions` (PurchaseRequisition) | item, qty, requester, status | `pending → recommended → approved/rejected → po_created` | UC-04 |
| `purchase_orders` (PurchaseOrder) | vendor_id→vendors, items(JSON text), total, status, inspection | `created → sent → received`; inspection `pass/fail/pending` | UC-03 (DB) |
| `invoices` (Invoice) | order_id, po_id, vendor_id, delivery_challan(str), invoice_number(unique), base_amount, tax_amount, withholding_tax, total_amount, status, payment_status, payment_date | status `generated→verified→approved→paid`; payment `pending→partial→completed` | UC-08 |
| `tax_records` (TaxRecord) | order_id, invoice_id, base_amount, tax_rate, tax_amount, withholding_tax_rate, withholding_tax_amount, net_amount, calculation_type | `calculated→verified→recorded`; type `cost_calc`/`withholding_tax` | UC-06/07 |
| `tax_calculations` (TaxCalculation) | amount, tax_amount | — | ⚠️ legacy duplicate of tax_records; used by the live `/api/tax` |
| `vendors` (Vendor) | name, contact, rating | — | master data |
| `accounts` (AccountEntry) | po_id→purchase_orders, amount, status | `pending → paid` | payment ledger |
| `warehouse_items` (WarehouseItem) | sku(unique), name, qty | — | inventory |
| `client_confirmations` (ClientConfirmation) | po_id, status | `delivered → confirmed` | delivery confirm |
| `commercial_approvals` (CommercialApproval) | pr_id, approver, decision, comments | — | audit of commercial decision |
| `pr_approvals` (PRApproval) | pr_id, approver, status, comments | — | audit of PR decision |
| `vendor_negotiations` (VendorNegotiation) | vendor_id, note | — | negotiation log |
| `bank_charges` (BankCharge) | name, amount | — | reference only |

**Relationships:** Order 1—N Quotation N—1 Vendor; approved Quotation → PurchaseOrder → Invoice → TaxRecord(s); PurchaseRequisition → Approval records; AccountEntry tracks payment per PO. (FKs are declared but SQLite doesn't enforce them by default.)

---

## 5. The 8 use cases → endpoints → what happens

> Note: there are **two numbering schemes** floating around the project. The **object/use-case diagrams** (the submitted report) use the list below. A separate `README.md` and `VIVA_PREPARATION.md` use a slightly different UC numbering and even a different tax model — treat those two docs with caution (see §9).

| UC | Name | Primary actor | Live endpoint(s) | Effect |
|----|------|---------------|------------------|--------|
| UC-01 | Place Order | Client | `POST /api/orders/` | create Order, status `placed` |
| UC-02 | Submit Quotation | Vendor | `POST /api/quotations/` | create Quotation `submitted`; sets order `quotation_requested` |
| UC-05 | Compare Quotations | Commercial | `GET /api/quotations/order/<order_id>` then `POST /api/quotations/<id>/approve|reject` | list quotes for an order; approve sets `approved` |
| UC-03 | Issue Purchase Order | Commercial | `POST /api/po/` (with `quotation_id`) | issue PO from an **approved** quote (in-memory — see §7) |
| UC-04 | PR Approval | PR Dept | `POST /api/pr/`, `POST /api/pr/<id>/recommend`, `POST /api/commercial/decision` | requisition lifecycle; approval triggers automation |
| UC-06 | Cost/Sales Tax | Tax Dept | `POST /api/invoices/<id>/calculate-tax` (live) | compute sales tax on invoice + write TaxRecord |
| UC-07 | Withholding Tax | Tax Dept | (same calculate-tax endpoint, withholding_rate) | compute WHT, adjust invoice total |
| UC-08 | Invoice Bills + Payment | Accounts | `POST /api/invoices/`, `POST /api/invoices/<id>/mark-paid` | generate invoice; mark paid |

---

## 6. The end-to-end "procure-to-pay" story

There are actually **two procurement paths** in the code that both reach a payment, because of the new-vs-legacy split:

### Path A — the "new" use-case path (order/quotation driven)
1. **Client places order** → `POST /api/orders/` → Order `placed`.
2. **Vendor submits quotation(s)** → `POST /api/quotations/` → order becomes `quotation_requested`.
3. **Commercial compares** quotes for the order (`GET /api/quotations/order/<id>`) and **approves** one (`POST /api/quotations/<id>/approve` → `approved`).
4. **Commercial issues a PO** → `POST /api/po/` with `quotation_id`. The handler checks the quote is `approved`, then stores the PO **in a Python dict in memory** (`pos_store`) and sets the quote to `po_issued`. *(This PO is not in the database and is lost on restart.)*
5. **Accounts generates an invoice** → `POST /api/invoices/` (base_amount, tax_amount, withholding_tax). Total is computed: `total = base + tax − withholding`.
6. **Tax is calculated** on the invoice → `POST /api/invoices/<id>/calculate-tax` (pass `tax_rate` and/or `withholding_rate` as %), which updates the invoice and writes a `TaxRecord`.
7. **Payment** → `POST /api/invoices/<id>/mark-paid` → status `paid`, payment_status `completed`, payment_date set.

### Path B — the "legacy" requisition path (PR driven, DB-backed, automated)
1. A **purchase requisition** is raised → `POST /api/pr/` (item, qty, requester), status `pending`.
2. PR is **recommended** → `POST /api/pr/<id>/recommend` → `recommended`.
3. **Commercial decision** → `POST /api/commercial/decision` (`pr_id`, `approve`). If approved, it calls **`process_pr_full(pr_id)`** which runs the entire chain automatically (see §8). If rejected, PR → `rejected`.
4. Alternatively a PO can be made directly from a PR → `POST /api/pr/<id>/create_po` (optionally `auto_full=true` to run the automation).
5. Legacy PO endpoints then handle goods receipt and inspection against the **database** PurchaseOrder:
   - `POST /api/po/<id>/receive` → status `received`, pushes items into `warehouse_items`.
   - `POST /api/po/<id>/inspect` (`result: pass|fail`) → on `pass`, creates an `AccountEntry` (the "invoice") with status `pending`.
   - `POST /api/po/<id>/invoice` → create an AccountEntry explicitly.
6. **Payment** → `POST /api/accounts/<id>/pay` → AccountEntry `paid`.

> So "invoice" means two different things depending on path: a rich `Invoice` row (Path A) vs a simple `AccountEntry` (Path B). This is one of the app's main inconsistencies.

---

## 7. The `/api/po` overlap (important quirk)

Both blueprints are registered at `/api/po`:
- **`po_bp_new`** (`po_routes_new.py`) defines `POST /`, `GET /`, `GET /<id>` — issues a PO **from an approved quotation** and keeps it **in memory** (`pos_store = {}`):
  ```python
  if quotation.status != 'approved':
      return jsonify({'error': 'Only approved quotations can be issued as PO'}), 400
  pos_store[po_id] = po_data         # <-- in-memory, not the database
  quotation.status = 'po_issued'
  ```
- **`po_bp`** (`po_routes.py`) defines `POST /` (create from `vendor_id`, **DB-backed**), `GET /`, plus the unique `POST /<id>/receive`, `/inspect`, `/invoice`, `PUT`, `DELETE`.

Because `po_bp_new` is registered first, for the colliding routes (`POST /`, `GET /`, `GET /<id>`) **the new in-memory handlers win** and the legacy DB create/list are shadowed. The legacy `/receive`, `/inspect`, `/invoice` routes are unique, so they still work — **but they operate on database POs**, which are created by the PR path (`process_pr_full` / `create_po_from_pr`), *not* by the (shadowed) legacy `POST /api/po/`. Net effect: the in-memory POs (Path A) and the DB POs (Path B) are two separate worlds that don't meet.

---

## 8. The automation chain: `utils/workflow.py → process_pr_full(pr_id)`

This single function powers the "approve a PR and everything happens" behavior. It:
1. Loads the PR, builds an items list from it, and **creates a DB PurchaseOrder** (`vendor_id=None`, total `0.0`); sets PR status `po_created`.
2. Marks the PO `received` and **adds/increments `warehouse_items`** from the PO's items JSON.
3. Sets PO `inspection = 'pass'` and **creates an `AccountEntry`** for the PO total, status **`paid`**.
4. Returns a summary dict of the steps (`po_created`, `po_received`, `inspection`, `invoice_id`, `payment completed`).

So approving a recommended PR via `/api/commercial/decision` (with `approve=true`) cascades all the way to a paid account entry in one call. (Totals are 0.0 because PRs don't carry pricing — a known simplification.)

---

## 9. Tax & money logic (and the documentation contradiction)

**What the code actually does:**
- **Live invoice tax calc** (`POST /api/invoices/<id>/calculate-tax`): takes `tax_rate` and `withholding_rate` as **percentages passed in by the caller**, then:
  ```python
  tax_amount        = base_amount * (tax_rate/100)
  withholding_amount = base_amount * (withholding_rate/100)
  invoice.total_amount = base_amount + tax_amount - withholding_amount
  # writes a TaxRecord(calculation_type='cost_calc')
  ```
- **Live legacy `/api/tax`** (`tax_routes.py`): `POST /api/tax/` computes a **flat 10%** of an `amount` and stores a `TaxCalculation`. `POST /api/tax/calc` returns amount+10% without saving.
- **`tax_routes_new.py`** (the nice `calculate-cost` / `calculate-withholding-tax` endpoints) exists but is **not registered**, so it doesn't run.

**The contradiction to be aware of (3 different tax stories in the repo):**
1. The **object/use-case diagrams** (submitted report) use a **Pakistan/FBR** model: currency **PKR**, sales tax **17%**, withholding **4.5%** (e.g. base 60,000 → tax 10,200 → withholding 2,700 → net 57,300).
2. The **code** doesn't hard-code any of these — it uses whatever rate the caller passes (or a flat 10% in the legacy route).
3. The **`README.md`/`VIVA_PREPARATION.md`** describe an **Indian GST** model (5/12/18/28%) — this does **not** match either the diagrams or the code.

**Treat the FBR/PKR version (the diagrams) as the intended domain**, the code as "rate is an input," and the README's GST text as stale/incorrect.

Invoice total rule (consistent everywhere it's implemented): **`total = base_amount + tax_amount − withholding_tax`**.

---

## 10. Condensed API reference (live endpoints)

```
Orders        POST /api/orders/        GET /api/orders/   GET /api/orders/<id>   PUT /api/orders/<id>
Quotations    POST /api/quotations/    GET /api/quotations/   GET /api/quotations/order/<order_id>
              POST /api/quotations/<id>/approve     POST /api/quotations/<id>/reject
Purchase Order (in-mem)  POST /api/po/ {quotation_id}   GET /api/po/   GET /api/po/<id>
Purchase Order (DB, legacy, unique routes)  POST /api/po/<id>/receive   POST /api/po/<id>/inspect
              POST /api/po/<id>/invoice   PUT /api/po/<id>   DELETE /api/po/<id>
Requisitions  POST /api/pr/   GET /api/pr/   GET/PUT/DELETE /api/pr/<id>
              POST /api/pr/<id>/recommend     POST /api/pr/<id>/create_po
Commercial    GET /api/commercial/   GET /api/commercial/pending   POST /api/commercial/
              POST /api/commercial/decision {pr_id, approve}
Invoices      POST /api/invoices/   GET /api/invoices/   GET /api/invoices/<id>
              POST /api/invoices/<id>/mark-paid     POST /api/invoices/<id>/calculate-tax
Tax (legacy)  GET /api/tax/   POST /api/tax/ {amount}   POST /api/tax/calc   GET/DELETE /api/tax/<id>
Vendors       GET/POST /api/vendors/   GET/PUT/DELETE /api/vendors/<id>
Negotiation   GET/POST /api/negotiation/   POST /api/negotiation/<id>/accept   ...
Accounts      GET /api/accounts/   GET /api/accounts/pending   POST /api/accounts/
              POST /api/accounts/<id>/pay   GET/PUT/DELETE /api/accounts/<id>
Warehouse     GET/POST /api/warehouse/items   GET/PUT/DELETE /api/warehouse/items/<id>
Client        GET /api/client/   POST /api/client/   POST /api/client/<id>/confirm
Dashboard     GET /api/health     GET /api/info
```
Most write endpoints return `{ "<entity>": {...}, "message": "..." }` with a 201/200, or `{ "error": "..." }` with 4xx/5xx. There's a consistent try/except + `db.session.rollback()` pattern.

---

## 11. Frontend (brief)

- Static pages served from `Frontend/` at `/` (e.g. visiting `/order` serves `order.html`). `dashboard_new.html` is the SPA-ish entry with an 8-module workflow grid and a hover sidebar.
- Each page has matching JS in `Frontend/js/` that calls the `/api/...` endpoints with `fetch` and renders results; a toast system gives feedback. No client-side framework, no bundler.

---

## 12. Known gaps / things to keep in mind when helping

1. **No authentication or roles** — every endpoint is open; "which department does this" is only a UI convention.
2. **In-memory POs** — the quotation→PO issue path stores POs in a dict; they vanish on restart and aren't queryable with the DB POs.
3. **Two code generations** — "new" UC routes (orders/quotations/invoices/po_new) vs "legacy" department routes (pr/po/commercial/accounts/tax/...). They overlap and sometimes duplicate concepts (Invoice vs AccountEntry; tax_records vs tax_calculations).
4. **Dead/orphan code** — `tax_routes_new.py` (unregistered), `pr_routes_duplicate.py`, mostly empty `services/` and `controllers/`.
5. **Docs vs code mismatch** — `README.md`/`VIVA_PREPARATION.md` describe Indian GST and some endpoints (e.g. `/create`, `/by-order`, `/generate`) that don't match the real route names; the FBR/PKR diagrams are the intended domain.
6. **SQLite single-writer**, FKs not enforced, no migrations beyond a one-off `apply_schema_fix.py`.
7. **No tests.**

There is also a full set of requirements-engineering documents under `docs/product/` (an SRS, FR/NFR lists, traceability matrix, etc.) that reframe this prototype as a planned product called **"ProcureFlow (PAMS)"** — useful if the assistant is asked about requirements rather than current behavior.

---

## 13. How to run

```bash
cd backend
pip install -r requirements.txt
python init_db.py        # creates app.db with tables (if present)
python app.py            # serves http://127.0.0.1:5000/ and opens a browser
```
(`debug=True`, `use_reloader=False`. On Windows, `run.cmd` / `start_new.cmd` exist as shortcuts.)

---

## 14. One-line glossary

- **PR** = Purchase Requisition (internal request to buy) and the department that approves it.
- **PO** = Purchase Order (formal order to a vendor).
- **Quotation** = a vendor's price offer for an order.
- **Challan** = delivery note accompanying goods (stored only as a string reference here).
- **WHT** = Withholding Tax (deducted at source for FBR, Pakistan's tax authority).
- **AccountEntry** = the legacy path's lightweight "invoice/payable" record.
- **process_pr_full** = the function that auto-runs PO→receive→inspect→invoice→paid.
```
