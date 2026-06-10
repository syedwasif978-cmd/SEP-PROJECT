# 17 · Requirements Traceability Matrix (RTM)

**Prompt 17** · *RE concept: traceability*

The RTM threads each requirement from its **source** (stakeholder/use case) forward through **design** to the **code** that implements it and the **test** that verifies it. This is what proves coverage — nothing requested is unbuilt, nothing built is unrequested.

> Trace chain: **Stakeholder → Use Case → FR/NFR → User Story → Design/Data → Code (route/model) → Test Case → Status**

---

## 1. Forward traceability (requirement → implementation → test)

| FR | UC | Story | Backend code (route / model) | Test case | Status |
|----|----|-------|------------------------------|-----------|--------|
| FR-01 | UC-01 | US-01 | [order_routes.py](../../backend/routes/order_routes.py) `POST /` · [order.py](../../backend/models/order.py) | TC-01 place order returns 201, status `placed` | ✅ Implemented |
| FR-05 | UC-02 | US-02 | [quotation_routes.py](../../backend/routes/quotation_routes.py) `POST /` · [quotation.py](../../backend/models/quotation.py) | TC-05 submit quote sets order `quotation_requested` | ✅ |
| FR-07 | UC-05 | US-05 | quotation_routes `GET /order/<id>` | TC-07 returns all quotes for order | ✅ |
| FR-08 | UC-05 | US-05 | (to add) compare/flag lowest total | TC-08 lowest total flagged rank=1 | 🔶 Partial |
| FR-09 | UC-05 | US-05 | quotation_routes `POST /<id>/approve` | TC-09 status→`approved` | ✅ |
| FR-10 | UC-05 | US-05 | quotation_routes `POST /<id>/reject` | TC-10 status→`rejected` | ✅ |
| FR-11 | UC-04 | US-04 | [pr_routes.py](../../backend/routes/pr_routes.py) `POST /` · [purchase_requisition.py](../../backend/models/purchase_requisition.py) | TC-11 PR created `pending` | ✅ |
| FR-12 | UC-04 | US-04 | pr_routes `POST /<id>/recommend` | TC-12 status→`recommended` | ✅ |
| FR-13 | UC-04 | US-04 | [commercial_routes.py](../../backend/routes/commercial_routes.py) `GET /pending` | TC-13 lists recommended PRs | ✅ |
| FR-14 | UC-04 | US-04 | commercial_routes `POST /decision` · [workflow.py](../../backend/utils/workflow.py) | TC-14 approve advances workflow + audit | ✅ |
| FR-16 | UC-03 | US-03 | [po_routes_new.py](../../backend/routes/po_routes_new.py) `POST /` | TC-16 PO issued from approved quote | ✅ |
| FR-17 | UC-03 | US-03 | po_routes_new (status guard) | TC-17 reject PO from non-approved quote (BR-01) | ✅ |
| FR-18 | UC-03 | US-03 | (to add) persist PO via [purchase_order.py](../../backend/models/purchase_order.py) | TC-18 PO survives restart | ⛔ Gap |
| FR-22 | UC-08 | US-08 | [invoice_routes.py](../../backend/routes/invoice_routes.py) `POST /` · [invoice.py](../../backend/models/invoice.py) | TC-22 total=base+tax−WHT, unique no. | ✅ |
| FR-24 | UC-08 | US-08 | invoice_routes `POST /<id>/mark-paid` | TC-24 status→`paid`, date set | ✅ |
| FR-25 | UC-08 | US-08 | (to add) DeliveryChallan entity | TC-25 challan linked to order/vendor | 🔶 |
| FR-26 | UC-06 | US-06 | [tax_routes_new.py](../../backend/routes/tax_routes_new.py) `POST /calculate-cost` · [tax_record.py](../../backend/models/tax_record.py) | TC-26 tax=base×rate, record written | ✅ |
| FR-27 | UC-07 | US-07 | tax_routes_new `POST /calculate-withholding-tax` | TC-27 WHT=base×rate (2,700 on 60k @4.5%) | ✅ |
| FR-28 | UC-06/07 | US-07 | tax_routes_new `GET /records[/<invoice_id>]` | TC-28 records retrievable by invoice | ✅ |
| FR-29 | UC-06/07 | US-06/07 | (to add) TaxRate master; PKR rounding | TC-29 rate from master, PKR 2-dp | 🔶 |
| FR-30 | UC-08 | — | [account_routes.py](../../backend/routes/account_routes.py) | TC-30 pay entry lifecycle | ✅ |
| FR-31 | support | — | [warehouse_routes.py](../../backend/routes/warehouse_routes.py) · workflow.py | TC-31 stock increment on receipt | ✅ |
| FR-32 | support | — | [client_routes.py](../../backend/routes/client_routes.py) | TC-32 confirm delivery | ✅ |
| FR-33 | — | US-10 | [dashboard_routes.py](../../backend/routes/dashboard_routes.py) (+ aggregates to add) | TC-33 live counts match DB | 🔶 |
| FR-35 | x-cut | US-09 | (to add) auth/User model | TC-35 unauthenticated write → 401 | ⛔ Gap |
| FR-36 | x-cut | US-09 | (to add) RBAC/Role | TC-36 cross-role action → 403 | ⛔ Gap |
| FR-37 | x-cut | US-09 | (to add) AuditLog; timestamps exist on models | TC-37 actor+timestamp on each action | 🔶 |
| FR-38 | x-cut | — | [validators.py](../../backend/utils/validators.py) (extend) | TC-38 invalid input → 400, no write | 🔶 |

## 2. Backward traceability (code → requirement)

Spot-check that existing modules map to a requirement (no orphan code):

| Existing module | Traces back to |
|-----------------|----------------|
| order_routes.py | FR-01…FR-04 (UC-01) |
| quotation_routes.py | FR-05…FR-10 (UC-02/05) |
| po_routes_new.py | FR-16…FR-19 (UC-03) |
| pr_routes.py / commercial_routes.py | FR-11…FR-15 (UC-04) |
| invoice_routes.py | FR-22…FR-26 (UC-08, UC-06) |
| tax_routes_new.py | FR-26…FR-29 (UC-06/07) |
| vendor_routes.py / negotiation_routes.py | FR-20…FR-21 |
| account_routes.py / warehouse_routes.py / client_routes.py | FR-30…FR-32 |
| workflow.py | FR-14, BR-06 |
| tax_calculation.py (model) | ⚠️ no active requirement — legacy duplicate of tax_records → remove (NFR-20) |
| pr_routes_duplicate.py | ⚠️ orphan duplicate → remove (NFR-20) |

> Backward tracing flagged **2 orphan modules** with no requirement → scheduled for removal under maintainability (NFR-20).

## 3. NFR traceability

| NFR | Verified by | Status |
|-----|-------------|--------|
| NFR-05/06/07 (auth/RBAC/hash) | TC-35, TC-36 + security review | ⛔ to build |
| NFR-14/16 (no data loss / atomic) | TC-18 restart + rollback test | ⛔ tied to FR-18 |
| NFR-17/27 (concurrency / DB switch) | concurrency load test on PostgreSQL | 🔶 |
| NFR-23/25 (FBR compliance / PKR) | TC-26/27/29 vs FBR circular | 🔶 |
| NFR-21 (test coverage ≥70%) | pytest coverage report | ⛔ |

## 4. Coverage summary

| Metric | Count |
|--------|-------|
| Functional requirements traced | 38 |
| Implemented (✅) | ~22 |
| Partial (🔶) | ~9 |
| Gap to build (⛔) | ~7 (FR-18, FR-34, FR-35, FR-36 + NFR-driven) |
| Use cases with ≥1 implemented FR | 8 / 8 |
| Orphan code modules found | 2 (to remove) |

## 5. How to keep the RTM alive
- Add a row whenever a requirement is added (under change control, [18-change-management.md](18-change-management.md)).
- Update the **Status** and **Test** columns as code and pytest cases land.
- Before each release, confirm every **Must** requirement (doc 13) shows ✅ with a passing test.

> The RTM is the single artefact a reviewer (or your instructor) can use to confirm the product does everything the requirements promised — and only that.
