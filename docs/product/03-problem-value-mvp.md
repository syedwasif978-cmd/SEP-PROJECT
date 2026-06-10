# 03 · Problem Statement, Value Proposition & MVP

**Prompt 3** · *RE concept: scope definition / MVP*

---

## 1. Problem statement

Technical Solution Enterprise (TSE) runs its procurement and accounts on **manual paperwork, verbal approvals and disconnected spreadsheets**. Because no single system links the Commercial, PR, Tax and Accounts departments:

- Orders, quotations, POs, challans and invoices live on **separate paper registers** and are frequently **lost or mismatched**.
- Approvals happen **verbally**, leaving **no audit trail** of who approved what and when.
- Vendor quotations are compared **by hand**, so the **cheapest/best offer is not reliably chosen** and the choice cannot be justified later.
- Sales tax and **withholding tax are calculated manually**, producing **errors and FBR-compliance risk**.
- Management has **no consolidated, real-time view** of procurement spend or pending work.

The result is **slow cycle times, financial errors, weak traceability and compliance exposure**.

> **Problem in one sentence:** *TSE cannot run, approve, trace or tax-comply its procurement reliably because the workflow is manual and fragmented across departments.*

## 2. Value proposition

| For the user… | The pain… | ProcureFlow delivers… | The gain |
|---------------|-----------|------------------------|----------|
| Commercial | Lost quotes, slow manual comparison | One order → many quotations → auto-flagged lowest cost → one-click PO | Faster, defensible vendor selection |
| PR | Verbal, untraceable approvals | Approve/reject with reason + timestamp; status-gated flow | A full audit trail |
| Tax | Manual, error-prone tax math | Automatic sales-tax & withholding-tax calculation, recorded | FBR-compliant accuracy |
| Accounts | Double entry, stale payment status | Auto-computed invoice totals, linked challan/bill, one-click "paid" | No re-keying, live status |
| Management | No visibility | One dashboard across all departments | Real-time control |

**Value proposition statement:**
> *ProcureFlow replaces TSE's paper-and-spreadsheet procurement with one connected, approval-driven, FBR-tax-compliant digital workflow — cutting cycle time, eliminating lost documents, and making every transaction traceable.*

## 3. MVP definition

The MVP is the **smallest end-to-end slice that delivers a working procure-to-pay loop** — a client order can travel all the way to a paid, tax-correct invoice. We prioritise the **"happy path"** of the eight use cases and defer enrichments.

### MVP scope decision (per use case)

| UC | Use case | In MVP? | Justification |
|----|----------|---------|---------------|
| UC-01 | Place Order | ✅ Must | The trigger of the whole flow; nothing works without it. Already implemented ([order_routes.py](../../backend/routes/order_routes.py)). |
| UC-02 | Submission of Quotation | ✅ Must | Without quotations there is nothing to compare or buy. Implemented ([quotation_routes.py](../../backend/routes/quotation_routes.py)). |
| UC-05 | Compare Vendor Quotation | ✅ Must | The core value-add (defensible, cheapest selection). Implemented via `/quotations/order/<id>` + approve. |
| UC-03 | Purchase Order Issued | ✅ Must | Converts a decision into a commitment to the vendor. Implemented ([po_routes_new.py](../../backend/routes/po_routes_new.py)). **Caveat: must move PO from in-memory to DB before go-live.** |
| UC-08 | Invoice Bills Generation | ✅ Must | Closes the loop financially; computes total. Implemented ([invoice_routes.py](../../backend/routes/invoice_routes.py)). |
| UC-06 | Cost / Sales Tax Calculation | ✅ Must | Legally required before payment; FBR compliance. Implemented ([tax_routes_new.py](../../backend/routes/tax_routes_new.py)). |
| UC-07 | Withholding Tax Calculation | ✅ Must | FBR withholding is mandatory; high audit risk if wrong. Implemented (tax routes). |
| UC-04 | PR Approval | 🔶 Should (MVP-lite) | Important for governance, but the happy path can run with a single commercial approval gate first; full multi-level PR approval can follow in R2. Implemented ([pr_routes.py](../../backend/routes/pr_routes.py), [commercial_routes.py](../../backend/routes/commercial_routes.py)). |

> All eight use cases already exist in prototype form, so the MVP is **"harden the happy path + close the critical gaps,"** not "build from zero."

### MVP exit criteria (definition of done for Release 1)

1. A client order can be carried end-to-end to a **paid invoice** without leaving the system.
2. **Purchase Orders are persisted** in the database (close the in-memory gap in [po_routes_new.py](../../backend/routes/po_routes_new.py)).
3. Sales tax and withholding tax are **calculated and recorded** for every invoice, in PKR, matching the FBR rule.
4. Every approval/payment action stores **actor + timestamp**.
5. **Basic authentication + role separation** so each department only does its own steps (currently missing — see [08-non-functional-requirements.md](08-non-functional-requirements.md)).
6. The **dashboard** shows live counts of orders, pending approvals, and unpaid invoices.

### Explicitly deferred beyond MVP (R2/R3)

- FBR e-filing and bank-payment-gateway integration.
- Multi-round vendor negotiation workflow (model exists: [vendor_negotiation.py](../../backend/models/vendor_negotiation.py)).
- Advanced analytics / exportable management reports.
- Email/SMS notifications on status changes.
- Mobile-optimised UI and offline mode.

## 4. MVP value hypothesis

> *If TSE's five departments enter procurement transactions in ProcureFlow instead of on paper, then cycle time and document loss will fall measurably within one quarter — validating the move from project to product.*

Measured against goals **G-1…G-6** in [01-product-vision.md](01-product-vision.md).
