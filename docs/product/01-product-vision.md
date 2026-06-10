# 01 · Product Vision & Scope

**Prompt 1** · *RE concept: product vision / scoping*
**Product:** ProcureFlow — Procurement & Accounts Management System (PAMS)

---

## 1. Vision statement (Geoffrey Moore template)

> **For** the Commercial, Procurement (PR), Tax and Accounts departments of Technical Solution Enterprise (TSE) — an automobile machinery workshop —
> **who** today run procurement and payments on paper registers, verbal approvals and scattered spreadsheets,
> **the** ProcureFlow (PAMS)
> **is a** web-based procure-to-pay platform
> **that** digitises the full workflow from a client order through vendor quotation, requisition approval, purchase order, delivery challan, invoice bills and FBR-compliant tax/withholding-tax calculation to payment — in one auditable system,
> **unlike** the current mix of manual paperwork, standalone spreadsheets and generic accounting tools,
> **our product** models TSE's real departmental hierarchy and inter-department hand-offs, enforces approval gates, and keeps a single traceable record of every transaction.

## 2. Elevator pitch (one line)

*ProcureFlow turns TSE's paper-and-spreadsheet procurement into one connected, approval-driven, tax-compliant digital workflow.*

## 3. Why this is a *product*, not just a project

| Project framing (before) | Product framing (this vision) |
|---|---|
| "Document the procurement workflow with UML." | "Continuously run TSE's procurement on a system that evolves with the business." |
| Success = diagrams + a demo. | Success = measurable reduction in cycle time, errors and lost documents. |
| One delivery, then done. | Versioned releases (MVP → R2 → R3) with a backlog. |
| Actors on a diagram. | Named stakeholders and personas with goals and pain points. |

## 4. Measurable product goals

| Goal ID | Product goal | Baseline (manual today) | Target (12 months) |
|---------|--------------|--------------------------|--------------------|
| G-1 | Reduce procurement cycle time (order → PO issued) | ~5–7 working days | ≤ 2 working days |
| G-2 | Eliminate lost/misplaced documents | Frequent | 0 — every document persisted & retrievable |
| G-3 | Reduce tax/withholding calculation errors | Manual, error-prone | ≥ 99% calculations match FBR-rule expected value |
| G-4 | Make every approval traceable | No audit trail | 100% of PR/quotation/payment actions logged with actor + timestamp |
| G-5 | Single source of truth for spend | Fragmented | 1 consolidated dashboard across all 5 departments |
| G-6 | Speed of vendor comparison | Manual side-by-side | Lowest-cost quote auto-flagged in < 2 s |

## 5. Product scope

### In scope (the product boundary)
- Client **order placement** (UC-01).
- **Vendor quotation** submission and **comparison/selection** (UC-02, UC-05).
- **Purchase Requisition approval** by the PR department (UC-04).
- **Purchase Order** issuance to the selected vendor (UC-03).
- **Delivery challan** and **invoice bill** generation (UC-08).
- **Sales/cost tax** and **withholding tax** calculation, FBR-compliant, in PKR (UC-06, UC-07).
- **Payment tracking** and an overview **dashboard**.
- Supporting masters: vendors, warehouse/inventory receipt, client delivery confirmation.

### Out of scope (deliberately, for now)
- Integration with the FBR e-filing portal or bank payment gateways (future work).
- Payroll, HR, or general ledger / full ERP accounting.
- The mechanical workshop's job-card / repair scheduling system.
- Mobile native apps (responsive web only).

## 6. Target market & positioning

- **Primary market:** small-to-medium enterprises (SMEs) in Pakistan that procure parts/materials and must comply with FBR sales-tax and withholding-tax rules — starting with TSE as the reference customer.
- **Positioning:** lighter and cheaper than a full ERP (SAP/Oracle), but structured and auditable — unlike spreadsheets — and tailored to Pakistani tax compliance.

## 7. Product constraints & assumptions

- **C-1:** Must operate in PKR and follow FBR sales-tax and withholding-tax rules.
- **C-2:** Initial deployment is on-premise / single-server (Flask + SQLite today; PostgreSQL for production).
- **C-3:** Departmental staff have basic computer literacy and a shared LAN/browser.
- **A-1:** Departments will follow the modelled approval sequence rather than bypassing it.
- **A-2:** Vendor and tax-rate master data are maintained by authorised staff.

## 8. Success metrics (how we'll know the vision is met)

Cycle time (G-1), document-loss rate (G-2), calculation accuracy (G-3), audit completeness (G-4) and user adoption (≥ 80% of procurement transactions entered in the system within 3 months of go-live).

> Links: realised by use cases in [12-srs.md](12-srs.md), prioritised in [13-moscow-prioritisation.md](13-moscow-prioritisation.md); stakeholders detailed in [02-stakeholders-personas.md](02-stakeholders-personas.md).
