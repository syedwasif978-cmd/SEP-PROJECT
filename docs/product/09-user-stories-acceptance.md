# 09 · User Stories & Acceptance Criteria

**Prompt 9** · *RE concept: user stories & acceptance criteria (Agile)*

Each use case is expressed as one or more user stories (*As a [role], I want [feature], so that [benefit]*) with **Given/When/Then** acceptance criteria. UC-04 (PR Approval) and UC-07 (Withholding Tax) are elaborated first and most fully, as required.

---

## ⭐ US-04 — PR Approval (UC-04)

> **As a** PR Department officer, **I want** to review a recommended purchase requisition and approve or reject it with a reason, **so that** only justified purchases proceed and every decision is on record.

**Acceptance criteria**

- **AC-04.1 — List pending**
  - *Given* requisitions exist with status `recommended`,
  - *When* I open the commercial/PR approval queue,
  - *Then* I see only those requisitions, each showing item, quantity, requester and date.
- **AC-04.2 — Approve advances the workflow**
  - *Given* a recommended requisition,
  - *When* I approve it with my name and a comment,
  - *Then* its status becomes `approved`, an approval record is stored, and the downstream workflow (PO → receive → inspect → invoice → pay) is triggered. *(BR-06)*
- **AC-04.3 — Reject returns to requester**
  - *Given* a recommended requisition,
  - *When* I reject it with a reason,
  - *Then* its status becomes `rejected` and it is returned to the requester for revision.
- **AC-04.4 — Audit**
  - *Given* any approve/reject action,
  - *Then* the system records the approver and a timestamp. *(FR-37)*
- **AC-04.5 — Guard**
  - *Given* a requisition that is not `recommended`,
  - *When* an approval is attempted,
  - *Then* the system rejects the action with a clear message.

*Traces:* FR-12, FR-13, FR-14 · `POST /api/commercial/decision`.

---

## ⭐ US-07 — Withholding Tax Calculation (UC-07)

> **As a** Tax Department officer, **I want** the system to calculate withholding tax on an invoice and record it, **so that** the correct FBR amount is deducted and I can prove compliance.

**Acceptance criteria**

- **AC-07.1 — Correct calculation**
  - *Given* an invoice with a base (gross) amount and a withholding rate (e.g. 4.5%),
  - *When* I run the withholding-tax calculation,
  - *Then* `withholding_amount = base_amount × rate/100`, and the invoice total updates to *base + sales tax − withholding*. *(BR-04, BR-02)*
  - *Example:* base = 60,000 PKR, rate = 4.5% → withholding = **2,700**, net payable = **57,300**. *(matches the UC-07 object diagram)*
- **AC-07.2 — Record written**
  - *Then* a tax record of type `withholding_tax` is stored with base amount, rate, amount and net amount.
- **AC-07.3 — Currency & rounding**
  - *Then* all values are in PKR, rounded to 2 decimals. *(NFR-25)*
- **AC-07.4 — Retrievable for filing**
  - *Given* stored withholding records,
  - *When* the officer filters by invoice or period,
  - *Then* the matching tax records are returned. *(FR-28)*
- **AC-07.5 — Validation**
  - *Given* a missing/negative rate or unknown invoice,
  - *When* calculation is attempted,
  - *Then* the system returns a clear error and writes nothing. *(FR-38)*

*Traces:* FR-27, FR-28, FR-29 · `POST /api/tax/calculate-withholding-tax`.

---

## US-01 — Place Order (UC-01)

> **As a** Client, **I want** to place an order with description, quantity and budget, **so that** the Commercial Department can start procurement.

- **AC-01.1** *Given* valid order details, *When* I submit, *Then* an order is created with status `placed` and I get a confirmation that it was sent to Commercial.
- **AC-01.2** *Given* a missing description, *When* I submit, *Then* the system rejects it with a field error.
- **AC-01.3** *Then* the order appears in the orders list, newest first.

*Traces:* FR-01, FR-02, FR-03 · `POST /api/orders/`.

## US-02 — Submit Quotation (UC-02)

> **As a** Vendor, **I want** to submit a quotation against an order, **so that** I can compete for the business.

- **AC-02.1** *Given* an existing order, *When* I submit unit price, total, delivery days and notes, *Then* a quotation is stored with status `submitted` and the order moves to `quotation_requested`.
- **AC-02.2** *Then* the quotation is visible in that order's comparison view.

*Traces:* FR-05, FR-06 · `POST /api/quotations/`.

## US-05 — Compare & Select Quotation (UC-05)

> **As a** Commercial officer, **I want** to compare all quotations for an order and select the best, **so that** I choose the most cost-effective vendor defensibly.

- **AC-05.1** *Given* multiple quotations for one order, *When* I open the comparison, *Then* I see them side-by-side and the lowest cost is flagged (rank = 1).
- **AC-05.2** *When* I approve one quotation, *Then* its status becomes `approved` and it is marked ready for PO; *and* I may reject the others.
- **AC-05.3** *Then* the selection (with saving vs the next-best) is recorded.

*Traces:* FR-07, FR-08, FR-09, FR-10 · `GET /api/quotations/order/<id>`, `POST .../approve|reject`.

## US-03 — Issue Purchase Order (UC-03)

> **As a** Commercial officer, **I want** to issue a PO from an approved quotation, **so that** the vendor is formally committed.

- **AC-03.1** *Given* a quotation with status `approved`, *When* I issue a PO, *Then* a PO with a generated number, vendor, total and delivery days is created and the quotation moves to `po_issued`.
- **AC-03.2** *Given* a quotation that is **not** approved, *When* I attempt to issue a PO, *Then* the system refuses with "Only approved quotations can be issued as PO". *(BR-01)*
- **AC-03.3** *Then* the issued PO is **persisted** and survives a restart. *(FR-18, NFR-14)*

*Traces:* FR-16, FR-17, FR-18, FR-19 · `POST /api/po/`.

## US-06 — Cost / Sales Tax Calculation (UC-06)

> **As a** Tax officer, **I want** sales/cost tax computed on an invoice, **so that** the invoice total is legally correct before payment.

- **AC-06.1** *Given* an invoice and a tax rate, *When* I calculate cost tax, *Then* `tax_amount = base × rate/100`, the invoice total updates, and a `cost_calc` tax record is stored.
- **AC-06.2** *Example:* base = 60,000, rate = 17% → tax = **10,200**, total = **70,200** (before withholding). *(matches UC-06 object diagram)*

*Traces:* FR-26, FR-28 · `POST /api/tax/calculate-cost`.

## US-08 — Invoice Bills & Delivery Challan (UC-08)

> **As an** Accounts clerk, **I want** to generate an invoice (and delivery challan) and track payment, **so that** the transaction closes cleanly.

- **AC-08.1** *Given* an order/PO/vendor, *When* I generate an invoice, *Then* a unique invoice number is assigned and total = *base + sales tax − withholding*.
- **AC-08.2** *When* I mark the invoice paid, *Then* status = `paid`, payment status = `completed`, and the payment date is recorded.
- **AC-08.3** *Then* the delivery challan and invoice bill reference the same order and vendor.

*Traces:* FR-22, FR-23, FR-24, FR-25 · `POST /api/invoices/`, `.../mark-paid`.

---

## Cross-cutting stories (product hardening)

## US-09 — Authentication & Roles

> **As a** department officer, **I want** to log in and only see/do my department's actions, **so that** approvals and payments can't be made by the wrong person.

- **AC-09.1** *Given* no/invalid credentials, *When* I call a write endpoint, *Then* I am denied (401/403).
- **AC-09.2** *Given* I am a Tax officer, *When* I attempt to mark an invoice paid (an Accounts action), *Then* I am denied. *(NFR-06)*

*Traces:* FR-35, FR-36, FR-37.

## US-10 — Management Dashboard

> **As** TSE Management, **I want** one dashboard of orders, pending approvals and unpaid invoices, **so that** I have real-time control of procurement.

- **AC-10.1** *Then* the dashboard shows live counts that match the database.
- **AC-10.2** *Then* I can drill from a count into the underlying records.

*Traces:* FR-33, FR-34.

---

> **INVEST check:** every story above is Independent, Negotiable, Valuable, Estimable, Small and Testable. Acceptance criteria double as the basis for the test cases in the RTM ([17-traceability-matrix.md](17-traceability-matrix.md)).
