# 07 · Functional Requirements

**Prompt 7** · *RE concept: functional requirements specification*

Each requirement states **actor → action → expected system response**, is uniquely identified (`FR-xx`), is traced to a use case, and is marked against the **current prototype** (✅ implemented, 🔶 partial, ⛔ not yet). Endpoints reference the real code in [backend/routes/](../../backend/routes/).

> Convention: "The system shall …" Every FR is verifiable; test references appear in the RTM ([17-traceability-matrix.md](17-traceability-matrix.md)).

---

## A. Order Management (UC-01)

| ID | Requirement | UC | Status / Endpoint |
|----|-------------|----|-------------------|
| FR-01 | The system **shall** let a Client place an order capturing client name, email, description, quantity and total budget, save it with status `placed`, and notify the Commercial Department. | UC-01 | ✅ `POST /api/orders/` |
| FR-02 | The system **shall** list all orders, most recent first. | UC-01 | ✅ `GET /api/orders/` |
| FR-03 | The system **shall** display the full details of a single order by its ID. | UC-01 | ✅ `GET /api/orders/<id>` |
| FR-04 | The system **shall** allow an authorised officer to update an order's status. | UC-01 | ✅ `PUT /api/orders/<id>` |

## B. Vendor Quotation — Submission & Comparison (UC-02, UC-05)

| ID | Requirement | UC | Status / Endpoint |
|----|-------------|----|-------------------|
| FR-05 | The system **shall** let a Vendor submit a quotation for an order (unit price, total price, delivery days, notes), store it with status `submitted`, and set the order status to `quotation_requested`. | UC-02 | ✅ `POST /api/quotations/` |
| FR-06 | The system **shall** list all submitted quotations. | UC-02 | ✅ `GET /api/quotations/` |
| FR-07 | The system **shall** retrieve all quotations for a given order so they can be compared side-by-side. | UC-05 | ✅ `GET /api/quotations/order/<order_id>` |
| FR-08 | The system **shall** identify and flag the lowest-cost quotation among those for an order (rank = 1). | UC-05 | 🔶 (comparison data returned; auto-flag to be added) |
| FR-09 | The system **shall** let the Commercial Department approve a quotation, setting its status to `approved` and marking it ready for PO issuance. | UC-05 | ✅ `POST /api/quotations/<id>/approve` |
| FR-10 | The system **shall** let the Commercial Department reject a quotation, setting its status to `rejected`. | UC-05 | ✅ `POST /api/quotations/<id>/reject` |

## C. Purchase Requisition & Approval (UC-04)

| ID | Requirement | UC | Status / Endpoint |
|----|-------------|----|-------------------|
| FR-11 | The system **shall** let an officer raise a Purchase Requisition (item, quantity, requester) with status `pending`. | UC-04 | ✅ `POST /api/pr/` |
| FR-12 | The system **shall** let the PR Department recommend a requisition, moving it to status `recommended`. | UC-04 | ✅ `POST /api/pr/<id>/recommend` |
| FR-13 | The system **shall** list requisitions pending commercial decision (status `recommended`). | UC-04 | ✅ `GET /api/commercial/pending` |
| FR-14 | The system **shall** record a commercial approve/reject decision on a requisition with the approver and comments; on approval it **shall** advance the requisition through the downstream workflow. | UC-04 | ✅ `POST /api/commercial/decision` (see [workflow.py](../../backend/utils/workflow.py)) |
| FR-15 | The system **shall** create a Purchase Order from an approved requisition's data. | UC-04 → UC-03 | ✅ `POST /api/pr/<id>/create_po` |

## D. Purchase Order Issuance (UC-03)

| ID | Requirement | UC | Status / Endpoint |
|----|-------------|----|-------------------|
| FR-16 | The system **shall** issue a Purchase Order from an **approved** quotation, generating a PO number and capturing vendor, order, total and delivery days. | UC-03 | ✅ `POST /api/po/` |
| FR-17 | The system **shall** reject any attempt to issue a PO from a quotation that is not in status `approved`. *(Business rule BR-01.)* | UC-03 | ✅ enforced in [po_routes_new.py](../../backend/routes/po_routes_new.py) |
| FR-18 | The system **shall** persist issued Purchase Orders durably so they survive a restart. | UC-03 | ⛔ **Gap** — currently held in memory (`pos_store`); must move to a DB model |
| FR-19 | The system **shall** list Purchase Orders and allow filtering by order, and display a single PO's details. | UC-03 | ✅ `GET /api/po/`, `GET /api/po/<id>` |

## E. Vendor Management & Negotiation

| ID | Requirement | UC | Status / Endpoint |
|----|-------------|----|-------------------|
| FR-20 | The system **shall** let authorised staff create, read, update and delete vendor master records (name required, contact, rating). | — | ✅ `/api/vendors/*` |
| FR-21 | The system **shall** let staff log a negotiation note against a vendor and mark a negotiation as accepted. | UC-05 (support) | ✅ `/api/negotiation/*` |

## F. Delivery Challan & Invoice Bills (UC-08)

| ID | Requirement | UC | Status / Endpoint |
|----|-------------|----|-------------------|
| FR-22 | The system **shall** let Accounts generate an invoice for an order/PO/vendor, auto-assign a unique invoice number, and compute the total as *base + sales tax − withholding tax*. *(BR-02.)* | UC-08 | ✅ `POST /api/invoices/` |
| FR-23 | The system **shall** list all invoices and display a single invoice's details. | UC-08 | ✅ `GET /api/invoices/`, `GET /api/invoices/<id>` |
| FR-24 | The system **shall** let Accounts mark an invoice as paid, setting status `paid`, payment status `completed`, and recording the payment date. | UC-08 | ✅ `POST /api/invoices/<id>/mark-paid` |
| FR-25 | The system **shall** generate a Delivery Challan linked to the order/vendor and reference it on the invoice. | UC-08 | 🔶 challan held as a reference string; to be formalised as an entity |

## G. Tax & Withholding Tax (UC-06, UC-07)

| ID | Requirement | UC | Status / Endpoint |
|----|-------------|----|-------------------|
| FR-26 | The system **shall** calculate cost/sales tax on an invoice from a given tax rate (%), update the invoice's tax amount and total, and write a tax record of type `cost_calc`. *(BR-03.)* | UC-06 | ✅ `POST /api/tax/calculate-cost` and `POST /api/invoices/<id>/calculate-tax` |
| FR-27 | The system **shall** calculate withholding tax on an invoice from a given withholding rate (%), update the invoice's withholding amount and total, and write a tax record of type `withholding_tax`. *(BR-04.)* | UC-07 | ✅ `POST /api/tax/calculate-withholding-tax` |
| FR-28 | The system **shall** retrieve tax records, all or filtered by invoice. | UC-06/07 | ✅ `GET /api/tax/records`, `GET /api/tax/records/<invoice_id>` |
| FR-29 | The system **shall** treat all monetary amounts as PKR and apply rates consistent with current FBR rules. *(BR-05, BR-07.)* | UC-06/07 | 🔶 PKR assumed; rate master to be added |

## H. Accounts, Goods Receipt & Client Confirmation (supporting)

| ID | Requirement | UC | Status / Endpoint |
|----|-------------|----|-------------------|
| FR-30 | The system **shall** create an account/payment entry against a PO, list pending payments, and mark an entry as paid. | UC-08 (support) | ✅ `/api/accounts/*` |
| FR-31 | The system **shall** record goods receipt by maintaining warehouse items (SKU, name, qty) and incrementing stock when a PO is received. | UC support | ✅ `/api/warehouse/*`, [workflow.py](../../backend/utils/workflow.py) |
| FR-32 | The system **shall** record client confirmation of delivery against a PO. | UC support | ✅ `/api/client/*` |

## I. Dashboard & Reporting

| ID | Requirement | UC | Status / Endpoint |
|----|-------------|----|-------------------|
| FR-33 | The system **shall** present a dashboard summarising orders, pending approvals and unpaid invoices across departments. | — | 🔶 dashboard UI exists; live aggregates to be completed (`/api/health`, `/api/info` present) |
| FR-34 | The system **shall** produce the detailed, summary and exception reports listed in the Report List (order, quotation, challan, invoice, tax). | — | ⛔ planned |

## J. Cross-cutting product requirements (derived from gaps)

| ID | Requirement | Rationale | Status |
|----|-------------|-----------|--------|
| FR-35 | The system **shall** authenticate users before any state-changing action. | No auth today → any caller can post | ⛔ |
| FR-36 | The system **shall** enforce role-based access so each department performs only its own actions (Commercial issues POs, Tax calculates tax, Accounts pays, etc.). | Separation of duties / approval integrity | ⛔ |
| FR-37 | The system **shall** record the acting user and a timestamp for every create/approve/reject/pay action (audit trail). | Goal G-4 traceability | 🔶 timestamps exist; actor identity missing |
| FR-38 | The system **shall** validate all incoming data (required fields, types, non-negative amounts) and return a clear error on violation. | Thin validation today | 🔶 partial ([validators.py](../../backend/utils/validators.py)) |

---

## Business rules referenced above

| BR | Rule |
|----|------|
| BR-01 | A Purchase Order may be issued **only** from a quotation whose status is `approved`. |
| BR-02 | `invoice.total = base_amount + tax_amount − withholding_tax`. |
| BR-03 | `tax_amount = base_amount × (tax_rate / 100)`. |
| BR-04 | `withholding_amount = base_amount × (withholding_rate / 100)`; `net_payable = gross − withholding_amount`. |
| BR-05 | All monetary values are in **PKR**. |
| BR-06 | Approving a recommended requisition triggers the automated PO → receive → inspect → invoice → pay workflow. |
| BR-07 | Tax and withholding rates follow current **FBR** rules (reference case: ~17% sales tax, ~4.5% withholding). |
| BR-08 | Order status progresses `placed → quotation_requested → po_created → completed`. |
| BR-09 | Quotation status progresses `submitted → approved`/`rejected → po_issued`. |

**Coverage:** 38 functional requirements across all 8 use cases plus cross-cutting product needs. Non-functional requirements are specified separately in [08-non-functional-requirements.md](08-non-functional-requirements.md).
