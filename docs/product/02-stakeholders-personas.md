# 02 · Stakeholder Analysis & Personas

**Prompt 2** · *RE concept: stakeholder analysis & personas*

---

## 1. Stakeholder register

Stakeholders are classified as **Primary** (use the system directly to do their job), **Secondary** (interact occasionally or supply/consume data), and **External** (outside TSE but materially affected).

| ID | Stakeholder | Class | Role in the procure-to-pay flow | Maps to system actor |
|----|-------------|-------|----------------------------------|----------------------|
| STK-01 | Client / Customer | Primary | Places the order that starts everything (UC-01) | `Order.client_*` |
| STK-02 | Commercial Department officer | Primary | Receives order, requests & compares quotations, issues PO (UC-02, UC-03, UC-05) | CommercialDept |
| STK-03 | PR (Procurement/Purchase Requisition) Department officer | Primary | Reviews and approves/rejects purchase requisitions (UC-04) | PRDepartment |
| STK-04 | Vendor / Supplier | Primary (external-facing) | Submits quotations, receives PO, delivers goods, sends invoice (UC-02, UC-08) | Vendor |
| STK-05 | Tax Department officer | Primary | Calculates sales/cost tax and withholding tax (UC-06, UC-07) | TaxDept |
| STK-06 | Accounts Department officer / clerk | Primary | Verifies invoices, generates delivery challan & invoice bills, records payment (UC-06, UC-07, UC-08) | Accounts |
| STK-07 | Warehouse / Store keeper | Secondary | Confirms goods receipt, updates inventory | WarehouseItem |
| STK-08 | TSE Management / Owner | Secondary | Consumes dashboard & reports; sets policy and budgets | Dashboard / reports |
| STK-09 | System Administrator | Secondary | Maintains masters (vendors, tax rates, users), backups | (admin role — to be added) |
| STK-10 | FBR (Federal Board of Revenue) | External | Recipient of tax/withholding filings; defines tax rules | Compliance constraint |
| STK-11 | Bank | External | Processes payments to vendors | Payment (future integration) |
| STK-12 | Development / Support team | Secondary | Builds, maintains and supports the product | — |

## 2. Stakeholder influence / interest grid

| | **Low interest** | **High interest** |
|---|---|---|
| **High influence** | FBR (STK-10), Bank (STK-11) — *keep satisfied (comply)* | Management (STK-08), Commercial (STK-02), Accounts (STK-06) — *manage closely* |
| **Low influence** | Warehouse (STK-07) — *monitor* | PR (STK-03), Tax (STK-05), Vendor (STK-04), Client (STK-01) — *keep informed* |

## 3. Stakeholder needs (one line each)

- **Client** — place an order easily and know its status.
- **Commercial** — request quotes from many vendors, compare fast, pick the cheapest/best, issue a PO without paperwork.
- **PR** — see what needs approval, approve/reject with reasons, and keep an audit trail.
- **Vendor** — receive clear POs and submit invoices; get paid on time.
- **Tax** — apply the correct FBR rate, calculate sales & withholding tax accurately, keep records.
- **Accounts** — verify amounts, generate challans/invoice bills, track and confirm payments.
- **Management** — one dashboard, real numbers, no surprises.

---

## 4. Personas

### Persona A — Bilal Raza · Commercial Department Officer (STK-02)

- **Snapshot:** 34, business-admin background, 8 years at TSE. Power user, comfortable with Excel, impatient with slow tools.
- **Goals:**
  - Turn a client order into competing vendor quotations quickly.
  - Compare quotations side-by-side and justify the choice to management.
  - Issue a purchase order the moment a quote is approved.
- **Pain points (today):**
  - Chases vendors by phone; quotes arrive on paper/WhatsApp and get lost.
  - Comparing prices means re-typing figures into a spreadsheet.
  - No record of *why* a vendor was chosen when management asks later.
- **Expectations of the product:**
  - One screen listing all quotations for an order with the lowest cost highlighted (UC-05).
  - One click from "approve quotation" to "PO issued" (UC-03).
  - Every action time-stamped against his name.
- **Success looks like:** "From client order to issued PO in under two days, with the comparison on record."

### Persona B — Nadia Iqbal · Tax Department Officer (STK-05)

- **Snapshot:** 41, accounting/tax specialist, knows FBR rules cold, risk-averse, audited annually.
- **Goals:**
  - Apply the correct sales-tax and withholding-tax rates to each invoice.
  - Produce defensible records for FBR filing.
  - Never under- or over-deduct withholding tax.
- **Pain points (today):**
  - Calculates tax on a calculator; transcription errors slip through.
  - Rate changes from FBR are tracked in her head / a printed circular.
  - Hard to reconcile what was deducted vs what was filed.
- **Expectations of the product:**
  - Enter a rate (or pick the current FBR rate) and have sales tax and withholding tax computed and **recorded** automatically (UC-06, UC-07).
  - A tax-records list she can filter by invoice and period.
  - Currency fixed to PKR; net payable computed for her.
- **Success looks like:** "Every withholding amount in the system matches the FBR rule, and I can prove it."

### Persona C — Hina Baig · Accounts Department Clerk (STK-06)

- **Snapshot:** 28, commerce graduate, 3 years' experience, methodical, handles the most data entry.
- **Goals:**
  - Verify the invoice against the PO and delivery, then generate the invoice bill.
  - Generate delivery challans and keep payment status current.
  - Close transactions cleanly so management's numbers are right.
- **Pain points (today):**
  - Matches invoices to POs and challans by hand across registers.
  - "Paid / not paid" lives in a spreadsheet that's often out of date.
  - Re-keys the same amounts the Tax department already calculated.
- **Expectations of the product:**
  - Invoice total auto-computed as *base + sales tax − withholding tax* (as in [invoice_routes.py](../../backend/routes/invoice_routes.py)).
  - "Mark as paid" updates status and date in one action (UC-08).
  - Delivery challan and invoice bill linked to the same vendor and order.
- **Success looks like:** "No double entry, and the payment dashboard is always live."

## 5. Anti-persona (who this is *not* for, yet)

- **The walk-in retail customer** wanting an e-commerce checkout — ProcureFlow is a B2B internal procurement tool, not a storefront.

> Links: persona goals become user stories in [09-user-stories-acceptance.md](09-user-stories-acceptance.md); their conflicting priorities are reconciled in [14-conflict-resolution.md](14-conflict-resolution.md).
