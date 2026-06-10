# 10 · Domain Model & Data Dictionary

**Prompt 10** · *RE concept: domain modelling / data requirements*

A conceptual model of the product's entities and a field-level data dictionary, **validated against the actual SQLAlchemy models** in [backend/models/](../../backend/models/).

---

## 1. Conceptual class diagram (domain entities & relationships)

```
        ┌──────────┐ 1        N ┌─────────────┐ N        1 ┌──────────┐
        │  Order   │───────────►│  Quotation  │◄───────────│  Vendor  │
        └────┬─────┘  has       └──────┬──────┘  from      └────┬─────┘
             │ 1                        │ 1 (approved)            │ 1
             │                          ▼                         │
             │                   ┌──────────────┐ N               │
             │                   │ PurchaseOrder│◄────────────────┘  issued to
             │ 1                 └──────┬───────┘  for
             │                          │ 1
             ▼ N                        ▼ N
        ┌──────────┐ 1        N ┌─────────────┐ 1      N ┌─────────────┐
        │ Invoice  │───────────►│  TaxRecord  │          │ AccountEntry│
        └────┬─────┘  taxed by  └─────────────┘          └─────────────┘
             │ 1                                              ▲ N
             │ generates                                      │ pays (po)
             ▼ 1                                               │
        ┌────────────────┐                              ┌──────────────┐
        │ DeliveryChallan│                              │PurchaseRequis.│
        └────────────────┘                              └──────┬───────┘
                                                                │ 1
   Supporting:  WarehouseItem · ClientConfirmation ·            ▼ N
                VendorNegotiation · CommercialApproval /  ┌──────────────┐
                PRApproval · (proposed) User, Role,       │  Approval    │
                TaxRate                                   └──────────────┘
```

**Key relationships**
- An **Order** has many **Quotations**; each Quotation is *from* one **Vendor**.
- The *approved* Quotation yields one **PurchaseOrder** *issued to* the Vendor.
- An **Order/PO** produces one **Invoice**; an Invoice is *taxed by* one or more **TaxRecords** (cost + withholding) and *generates* a **DeliveryChallan**.
- A **PurchaseRequisition** is reviewed via **Approval** records (commercial/PR).
- **AccountEntry** tracks payment against a PO.

---

## 2. Data dictionary

Types reflect the SQLAlchemy column definitions. PK = primary key (UUID string), FK = foreign key, NN = NOT NULL.

### 2.1 `orders` — UC-01 ([order.py](../../backend/models/order.py))
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String(UUID) | PK | Order identifier |
| client_name | String | NN | Name of client placing order |
| client_email | String | — | Client contact email |
| description | Text | NN | What is being ordered |
| quantity | Integer | default 1 | Quantity requested |
| status | String | default `placed` | `placed → quotation_requested → po_created → completed` |
| total_budget | Float | default 0.0 | Client's budget (PKR) |
| created_at / updated_at | DateTime | auto | Audit timestamps |

### 2.2 `quotations` — UC-02/05 ([quotation.py](../../backend/models/quotation.py))
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String(UUID) | PK | Quotation id |
| order_id | String | FK→orders, NN | Order being quoted |
| vendor_id | String | FK→vendors, NN | Quoting vendor |
| unit_price | Float | NN | Per-unit price (PKR) |
| total_price | Float | NN | Total quoted price (PKR) |
| delivery_days | Integer | default 0 | Promised delivery lead time |
| notes | Text | — | Free-text terms |
| status | String | default `submitted` | `submitted → approved`/`rejected → po_issued` |
| created_at / updated_at | DateTime | auto | Timestamps |

### 2.3 `purchase_requisitions` — UC-04 ([purchase_requisition.py](../../backend/models/purchase_requisition.py))
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String(UUID) | PK | PR id |
| item | String | NN | Item requested |
| qty | Integer | default 1 | Quantity |
| requester | String | — | Who raised it |
| status | String | default `pending` | `pending → recommended → approved`/`rejected → po_created` |
| created_at | DateTime | auto | Timestamp |

### 2.4 `purchase_orders` — UC-03 ([purchase_order.py](../../backend/models/purchase_order.py))
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String(UUID) | PK | PO id |
| vendor_id | String | FK→vendors | Vendor fulfilling PO |
| items | Text (JSON) | — | Line items `[{sku,name,qty}]` |
| total | Float | default 0.0 | PO value (PKR) |
| status | String | default `created` | `created → sent → received` |
| inspection | String | nullable | `pass`/`fail`/`pending` |
| created_at | DateTime | auto | Timestamp |

> ⚠️ **Model exists but the UC-03 issue endpoint stores POs in memory** (`pos_store` in [po_routes_new.py](../../backend/routes/po_routes_new.py)). Product requirement FR-18 / NFR-14 = route the issue flow through this persisted model.

### 2.5 `invoices` — UC-08 ([invoice.py](../../backend/models/invoice.py))
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String(UUID) | PK | Invoice id |
| order_id | String | FK→orders, NN | Related order |
| po_id | String | FK→purchase_orders | Related PO |
| vendor_id | String | FK→vendors, NN | Vendor billed |
| delivery_challan | String | — | Challan reference (to be entity-ised) |
| invoice_number | String | unique | Human-readable invoice no. |
| base_amount | Float | NN | Pre-tax amount (PKR) |
| tax_amount | Float | default 0.0 | Sales/cost tax (BR-03) |
| withholding_tax | Float | default 0.0 | Withholding deduction (BR-04) |
| total_amount | Float | NN | `base + tax − withholding` (BR-02) |
| status | String | default `generated` | `generated → verified → approved → paid` |
| payment_status | String | default `pending` | `pending → partial → completed` |
| payment_date | DateTime | — | When paid |
| created_at / updated_at | DateTime | auto | Timestamps |

### 2.6 `tax_records` — UC-06/07 ([tax_record.py](../../backend/models/tax_record.py))
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String(UUID) | PK | Tax record id |
| order_id | String | FK→orders | Related order |
| invoice_id | String | FK→invoices | Related invoice |
| base_amount | Float | NN | Amount taxed |
| tax_rate | Float | default 0 | Sales/cost tax % |
| tax_amount | Float | default 0 | Computed sales tax |
| withholding_tax_rate | Float | default 0 | WHT % (FBR) |
| withholding_tax_amount | Float | default 0 | Computed WHT |
| net_amount | Float | default 0 | Net payable |
| calculation_type | String | — | `cost_calc` / `withholding_tax` |
| status | String | default `calculated` | `calculated → verified → recorded` |
| created_at | DateTime | auto | Timestamp |

### 2.7 `vendors` ([vendor.py](../../backend/models/vendor.py))
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String(UUID) | PK | Vendor id |
| name | String | NN | Vendor name |
| contact | String | — | Contact person/number |
| rating | Integer | default 0 | Internal rating |

### 2.8 Supporting tables
| Table | Key fields | Purpose |
|-------|-----------|---------|
| `accounts` ([account.py](../../backend/models/account.py)) | id, po_id→FK, amount, status(`pending`/`paid`), created_at | Payment entry per PO |
| `warehouse_items` ([warehouse_item.py](../../backend/models/warehouse_item.py)) | id, sku(unique), name, qty | Inventory / goods receipt |
| `client_confirmations` ([client_confirmation.py](../../backend/models/client_confirmation.py)) | id, po_id→FK, status(`delivered`/`confirmed`), created_at | Delivery confirmation |
| `commercial_approvals` ([commercial_approval.py](../../backend/models/commercial_approval.py)) | id, pr_id→FK, approver, decision, comments | Commercial decision audit |
| `pr_approvals` ([pr_approval.py](../../backend/models/pr_approval.py)) | id, pr_id→FK, approver, status, comments | PR decision audit |
| `vendor_negotiations` ([vendor_negotiation.py](../../backend/models/vendor_negotiation.py)) | id, vendor_id→FK, note | Negotiation log |
| `tax_calculations` ([tax_calculation.py](../../backend/models/tax_calculation.py)) | id, amount, tax_amount | ⚠️ legacy/duplicate of `tax_records` |
| `bank_charges` ([bank_charges.py](../../backend/models/bank_charges.py)) | id, name, amount | Bank fee reference |

---

## 3. Proposed entities to add (to make it a product)

| Entity | Why needed | Linked requirement |
|--------|-----------|--------------------|
| **User** (id, name, email, password_hash, role_id) | Authentication | FR-35, NFR-07 |
| **Role** (id, name) — Commercial/PR/Tax/Accounts/Admin | RBAC | FR-36, NFR-06 |
| **DeliveryChallan** (id, order_id, vendor_id, items, date, status) | Currently a string on Invoice | FR-25 |
| **TaxRate** (id, type, rate, effective_from) | FBR rates as data, not hard-coded | FR-29, NFR-23 |
| **AuditLog** (id, user_id, action, entity, entity_id, timestamp) | Full audit trail | FR-37, NFR-09 |

## 4. Data-modelling observations (normalisation & integrity)

- **Redundant tables:** `tax_calculations` duplicates `tax_records` → consolidate (NFR-20).
- **PO line items as JSON** (`purchase_orders.items`) is acceptable for immutability but blocks per-item querying; acceptable for MVP, revisit for analytics.
- **Foreign keys** are declared but **FK enforcement is off by default in SQLite** → enable `PRAGMA foreign_keys=ON` or move to PostgreSQL (NFR-28).
- **Challan as a string** breaks referential integrity → entity-ise (above).

> This model underpins the SRS data requirements ([12-srs.md](12-srs.md)) and the original object/class diagrams in the project report.
