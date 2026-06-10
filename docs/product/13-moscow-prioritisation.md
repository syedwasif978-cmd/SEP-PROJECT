# 13 · Requirements Prioritisation (MoSCoW) & Release-1 Backlog

**Prompt 13** · *RE concept: requirements prioritisation*

Every functional and key non-functional requirement is prioritised with **MoSCoW** — **M**ust have, **S**hould have, **C**ould have, **W**on't have (this release). This table doubles as the **Release-1 product backlog**.

> Rule of thumb applied: *Must* items are non-negotiable for a usable, compliant, end-to-end procure-to-pay loop; they should be ≤ ~60% of effort, leaving contingency.

---

## 1. Functional requirements

| Priority | ID | Requirement (short) | Justification |
|----------|----|--------------------|---------------|
| **MUST** | FR-01 | Place order | Trigger of the whole flow |
| **MUST** | FR-05 | Submit quotation | No quotations → nothing to buy |
| **MUST** | FR-07 | Retrieve quotations for an order | Required for comparison |
| **MUST** | FR-09 | Approve quotation | Gate before PO (BR-01) |
| **MUST** | FR-16 | Issue PO from approved quotation | Core commitment to vendor |
| **MUST** | FR-17 | Block PO from non-approved quotation | Integrity rule BR-01 |
| **MUST** | FR-18 | **Persist purchase orders** | Closes the in-memory data-loss gap |
| **MUST** | FR-22 | Generate invoice with total = base+tax−WHT | Closes the loop; BR-02 |
| **MUST** | FR-24 | Mark invoice paid | Completes procure-to-pay |
| **MUST** | FR-26 | Calculate sales/cost tax | Legally required (UC-06) |
| **MUST** | FR-27 | Calculate withholding tax | FBR mandatory (UC-07) |
| **MUST** | FR-29 | PKR currency + FBR-consistent rates | Compliance |
| **MUST** | FR-35 | Authentication | No unauthenticated writes |
| **MUST** | FR-36 | Role-based access | Separation of duties |
| **SHOULD** | FR-02/03/04 | List/view/update order | Operational completeness |
| **SHOULD** | FR-08 | Auto-flag lowest-cost quotation | Big usability win, not strictly required |
| **SHOULD** | FR-10 | Reject quotation | Cleaner workflow |
| **SHOULD** | FR-11–FR-14 | PR raise/recommend/approve | Governance (MVP-lite acceptable) |
| **SHOULD** | FR-28 | Retrieve tax records | Needed for filing/audit |
| **SHOULD** | FR-30 | Account/payment entries | Payment tracking |
| **SHOULD** | FR-37 | Actor on audit trail | Goal G-4 |
| **SHOULD** | FR-38 | Input validation | Quality/robustness |
| **COULD** | FR-15 | Auto-create PO from PR | Convenience automation |
| **COULD** | FR-19 | Filter/list POs | Nice-to-have view |
| **COULD** | FR-20 | Vendor CRUD UI | Can seed masters manually first |
| **COULD** | FR-21 | Vendor negotiation log | Enhancement |
| **COULD** | FR-25 | Delivery-challan **entity** | String ref acceptable short-term |
| **COULD** | FR-31 | Warehouse goods-receipt | Supporting |
| **COULD** | FR-32 | Client delivery confirmation | Supporting |
| **COULD** | FR-33 | Live dashboard aggregates | Valued by management |
| **WON'T (R1)** | FR-34 | Full detailed/summary/exception reports | Defer to R2 |

## 2. Non-functional requirements

| Priority | ID | NFR (short) | Justification |
|----------|----|-------------|---------------|
| **MUST** | NFR-05/06/07 | Auth, RBAC, password hashing | Security baseline |
| **MUST** | NFR-14/16 | No data loss / transactional integrity | Trust in the system |
| **MUST** | NFR-23/25 | FBR compliance + PKR rounding | Legal correctness |
| **SHOULD** | NFR-01/02/03 | Performance targets | Adoption depends on speed |
| **SHOULD** | NFR-09 | Audit log | Traceability goal |
| **SHOULD** | NFR-17/27 | Concurrency / DB switch to PostgreSQL | Multi-department use |
| **SHOULD** | NFR-21 | ≥70% test coverage on core path | Maintainability |
| **COULD** | NFR-10/12 | Usability test, responsive ≤768px | Quality polish |
| **COULD** | NFR-19/20/22 | Service layer, no dup routes, API docs | Code health |
| **WON'T (R1)** | NFR-24/29 | 6-yr retention, automated daily backup | Ops maturity, R2 |

## 3. Release plan derived from MoSCoW

| Release | Theme | Contents |
|---------|-------|----------|
| **R1 (MVP)** | "Compliant end-to-end loop" | All **MUST** FRs/NFRs + the highest-value **SHOULD**s (FR-08, FR-28, FR-37, FR-38) |
| **R2** | "Governance & visibility" | Remaining SHOULDs + dashboard aggregates (FR-33), full PR approval, audit log, reports (FR-34) |
| **R3** | "Integrations & polish" | Negotiation, challan entity, FBR e-filing, bank gateway, notifications, mobile |

## 4. Effort/value sanity check

- **Must** items map mostly to **already-implemented** endpoints plus three real gaps (PO persistence FR-18, auth/RBAC FR-35/36, tax hardening FR-29). This keeps Must-effort bounded and leaves room for Shoulds — a healthy MoSCoW balance.
- The two riskiest Musts (FR-18 persistence, FR-35/36 security) are scheduled **first** in R1 (see [04-feasibility-study.md](04-feasibility-study.md) milestones).

> Conflicts that arise when stakeholders disagree on these priorities are resolved in [14-conflict-resolution.md](14-conflict-resolution.md).
