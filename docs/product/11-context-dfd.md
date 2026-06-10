# 11 · Context Diagram & Data-Flow Diagram

**Prompt 11** · *RE concept: context & data-flow modelling*

Shows the product boundary (who/what is outside) and how data moves through the procure-to-pay process.

---

## 1. Context diagram (Level-0 DFD)

The whole product is one process; external entities exchange data flows with it.

```
                         ┌───────────────────────────────────────────┐
        order request    │                                           │   quotation request
   ┌────────┐──────────► │                                           │ ──────────────► ┌────────┐
   │ CLIENT │            │                                           │                 │ VENDOR │
   │(STK-01)│ ◄──────────│        ProcureFlow / PAMS                 │ ◄────────────── │(STK-04)│
   └────────┘  order &   │   Procurement & Accounts Management        │  quotation /    └────────┘
              delivery   │            System                          │  PO / invoice
              status     │                                           │
                         │                                           │
   ┌──────────────┐      │                                           │   tax/withholding rules
   │  COMMERCIAL  │◄────►│                                           │◄──────────────► ┌────────┐
   │   (STK-02)   │ quote│                                           │  filing data    │  FBR   │
   └──────────────┘ compare,                                         │                 │(STK-10)│
                    PO    │                                           │                 └────────┘
   ┌──────────────┐      │                                           │
   │ PR DEPARTMENT│◄────►│                                           │   payment instruction
   │   (STK-03)   │ approve                                          │◄──────────────► ┌────────┐
   └──────────────┘ /reject                                         │  confirmation   │  BANK  │
                          │                                           │                 │(STK-11)│
   ┌──────────────┐       │                                           │                 └────────┘
   │  TAX / ACCTS │◄─────►│                                           │
   │ (STK-05/06)  │ tax calc,                                         │   dashboards/reports
   └──────────────┘ invoice,                                         │ ──────────────► ┌────────────┐
                    payment │                                         │                 │ MANAGEMENT │
                          └───────────────────────────────────────────┘                 │  (STK-08)  │
                                                                                          └────────────┘
```

**External entities & primary data flows**

| External entity | Sends to system | Receives from system |
|-----------------|-----------------|----------------------|
| Client (STK-01) | Order request (description, qty, budget) | Order confirmation, delivery status |
| Vendor (STK-04) | Quotation, invoice | Quotation request, Purchase Order |
| Commercial (STK-02) | Quote comparison decision, PO issue | Pending orders, quotation list |
| PR Dept (STK-03) | Approve/reject decision | Pending requisitions |
| Tax/Accounts (STK-05/06) | Tax rates, payment action | Invoice, tax records, payment status |
| FBR (STK-10) | Tax/withholding rules | Filing data (future) |
| Bank (STK-11) | Payment confirmation (future) | Payment instruction (future) |
| Management (STK-08) | Report queries | Dashboards & reports |

---

## 2. Level-1 DFD — Procure-to-Pay

Decomposes the single process into the main sub-processes (P1…P8) and data stores (D1…D6).

```
 CLIENT
   │ order
   ▼
┌────────────────┐   order rec.   ╔═══════════════╗
│ P1 Place Order │──────────────►║ D1 orders     ║
└──────┬─────────┘                ╚═══════════════╝
       │ order ready for sourcing
       ▼
┌────────────────────┐  quote req.   VENDOR
│ P2 Request/Receive │◄────────────────┐
│    Quotation       │── quotation ───►║ D2 quotations ║
└──────┬─────────────┘                ╚═══════════════╝
       │ quotations for order
       ▼
┌────────────────────┐  selection    ╔═══════════════╗
│ P3 Compare &       │──────────────►║ D2 quotations ║ (status=approved)
│    Select (UC-05)  │               ╚═══════════════╝
└──────┬─────────────┘
       │ approved quotation
       ▼
┌────────────────────┐  requisition  ╔═══════════════════════╗
│ P4 PR Approval     │◄─────────────►║ D3 purchase_requisitions║
│    (UC-04)         │  decision     ╚═══════════════════════╝
└──────┬─────────────┘
       │ approved
       ▼
┌────────────────────┐   PO          ╔═══════════════════╗   PO
│ P5 Issue PO (UC-03)│──────────────►║ D4 purchase_orders ║ ─────► VENDOR
└──────┬─────────────┘               ╚═══════════════════╝
       │ goods received / challan
       ▼
┌────────────────────┐   invoice     ╔═══════════════╗
│ P6 Generate        │──────────────►║ D5 invoices   ║
│    Challan+Invoice │               ╚═══════════════╝
│    (UC-08)         │
└──────┬─────────────┘
       │ base amount
       ▼
┌────────────────────┐   tax records ╔═══════════════╗   filing data
│ P7 Calculate Tax & │──────────────►║ D6 tax_records ║ ─────────────► FBR
│    Withholding     │               ╚═══════════════╝
│    (UC-06, UC-07)  │
└──────┬─────────────┘
       │ net payable
       ▼
┌────────────────────┐  payment      ╔═══════════════╗  payment
│ P8 Record Payment  │──────────────►║ D5 invoices   ║ ─────► BANK / VENDOR
└────────────────────┘  status       ╚═══════════════╝
```

**Processes ↔ implementation**

| Process | Use case | Implemented by (route) | Data store |
|---------|----------|------------------------|------------|
| P1 Place Order | UC-01 | [order_routes.py](../../backend/routes/order_routes.py) | D1 orders |
| P2 Request/Receive Quotation | UC-02 | [quotation_routes.py](../../backend/routes/quotation_routes.py) | D2 quotations |
| P3 Compare & Select | UC-05 | quotation_routes (`/order/<id>`, approve/reject) | D2 |
| P4 PR Approval | UC-04 | [pr_routes.py](../../backend/routes/pr_routes.py), [commercial_routes.py](../../backend/routes/commercial_routes.py) | D3 |
| P5 Issue PO | UC-03 | [po_routes_new.py](../../backend/routes/po_routes_new.py) | D4 (to persist) |
| P6 Challan + Invoice | UC-08 | [invoice_routes.py](../../backend/routes/invoice_routes.py) | D5 invoices |
| P7 Tax & Withholding | UC-06/07 | [tax_routes_new.py](../../backend/routes/tax_routes_new.py) | D6 tax_records |
| P8 Record Payment | UC-08 | invoice_routes (`/mark-paid`), [account_routes.py](../../backend/routes/account_routes.py) | D5 / accounts |

---

## 3. Notes on the flow

- The diagram makes the **approval gates** explicit (P3 → P4 → P5): a quotation must be *approved* before a PO can issue (BR-01), and a requisition must be *approved* before procurement proceeds (BR-06).
- **Data stores D1–D6** correspond one-to-one with the SQLite tables in [10-domain-data-model.md](10-domain-data-model.md).
- FBR and Bank flows are **planned external integrations** (out of MVP scope per [03-problem-value-mvp.md](03-problem-value-mvp.md)).
