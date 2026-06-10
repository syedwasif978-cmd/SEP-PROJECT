# 12 · Software Requirements Specification (SRS)

**Prompt 12** · *RE concept: SRS standard — ISO/IEC/IEEE 29148:2018 (supersedes IEEE 830)*
**Product:** ProcureFlow — Procurement & Accounts Management System (PAMS)
**Version:** 1.0 · **Status:** Baseline for Release 1 · **Date:** 2026-06-10

---

## 1. Introduction

### 1.1 Purpose
This document specifies the software requirements for **ProcureFlow (PAMS)**, a procure-to-pay platform for Technical Solution Enterprise (TSE), an automobile machinery workshop. It is the agreed, verifiable basis for design, implementation, testing and acceptance, and the baseline against which changes are controlled ([18-change-management.md](18-change-management.md)). The intended readers are the development team, the project supervisor, and TSE departmental stakeholders.

### 1.2 Scope
ProcureFlow digitises the workflow from a **client order** through **vendor quotation**, **comparison/selection**, **purchase-requisition approval**, **purchase-order issuance**, **delivery challan & invoice bills**, and **FBR-compliant sales-tax and withholding-tax calculation**, to **payment** — across the Commercial, PR, Tax and Accounts departments, with a management dashboard. It explicitly excludes full ERP/GL accounting, payroll, the workshop's job scheduling, and (for Release 1) direct FBR e-filing and bank-gateway integration. See [01-product-vision.md](01-product-vision.md) and [03-problem-value-mvp.md](03-problem-value-mvp.md).

### 1.3 Definitions, acronyms, abbreviations
| Term | Meaning |
|------|---------|
| PR | Purchase Requisition (and the department that approves it) |
| PO | Purchase Order |
| WHT | Withholding Tax |
| FBR | Federal Board of Revenue (Pakistan tax authority) |
| PKR | Pakistani Rupee |
| RBAC | Role-Based Access Control |
| Challan | Delivery document accompanying goods |
| FR / NFR | Functional / Non-Functional Requirement |
| UC | Use Case |

### 1.4 References
- Functional requirements: [07-functional-requirements.md](07-functional-requirements.md)
- Non-functional requirements: [08-non-functional-requirements.md](08-non-functional-requirements.md)
- Domain model & data dictionary: [10-domain-data-model.md](10-domain-data-model.md)
- Context & DFD: [11-context-dfd.md](11-context-dfd.md)
- Original project report, use-case and object diagrams (UC-01…UC-08).
- ISO/IEC/IEEE 29148:2018 — Requirements engineering.

### 1.5 Overview
Section 2 gives the overall description (perspective, functions, users, constraints, assumptions). Section 3 gives specific requirements (external interfaces, functional, data, and non-functional). Section 4 covers prioritisation and verification cross-references.

---

## 2. Overall Description

### 2.1 Product perspective
ProcureFlow is a **new, self-contained web application** built on a 3-tier architecture (see [VIVA_PREPARATION.md](../../VIVA_PREPARATION.md) and the real code):

```
Frontend (HTML/CSS/JS)  →  Flask routes/blueprints  →  Services  →  SQLAlchemy models  →  SQLite/PostgreSQL
```

It replaces a manual, paper-and-spreadsheet process. It interfaces (now or in future) with external actors: Clients, Vendors, FBR (tax rules/filing) and Banks (payment). The current implementation is a working prototype; this SRS specifies the requirements to harden it into a product.

### 2.2 Product functions (summary)
1. Order placement (UC-01).
2. Vendor quotation submission (UC-02).
3. Quotation comparison & selection (UC-05).
4. Purchase-requisition approval (UC-04).
5. Purchase-order issuance (UC-03).
6. Delivery challan & invoice-bill generation (UC-08).
7. Sales/cost-tax and withholding-tax calculation (UC-06, UC-07).
8. Payment tracking and management dashboard/reporting.
9. (Product) Authentication, RBAC and audit trail.

Detailed behaviour is in §3.2.

### 2.3 User characteristics
| User class | Technical skill | Frequency | Key functions |
|------------|-----------------|-----------|---------------|
| Client | Low | Occasional | Place order, view status |
| Commercial officer | Medium | Daily | Quotations, comparison, PO |
| PR officer | Medium | Daily | Approve/reject requisitions |
| Tax officer | Medium–High | Daily | Tax & withholding calculation |
| Accounts clerk | Medium | Daily (high volume) | Invoices, challans, payments |
| Vendor | Low–Medium | Occasional | Submit quotation/invoice |
| Management | Low | Weekly | Dashboard & reports |
| Administrator | High | As needed | Masters, users, backups |

(Personas in [02-stakeholders-personas.md](02-stakeholders-personas.md).)

### 2.4 Constraints
- **C-1** Tax logic must conform to FBR rules; currency is PKR.
- **C-2** Implementation stack: Python/Flask, SQLAlchemy; SQLite for dev, PostgreSQL/Oracle for production (config-switchable).
- **C-3** On-premise/single-server deployment initially; standard desktop browsers.
- **C-4** Separation of duties: a user may not perform another department's approval/payment actions (RBAC).
- **C-5** Academic timeframe for Release 1.

### 2.5 Assumptions and dependencies
- **A-1** Departments follow the modelled approval sequence.
- **A-2** Vendor and tax-rate master data are maintained by authorised staff.
- **A-3** A shared network and modern browser are available to all users.
- **D-1** Availability of the FBR current rate circular for tax configuration.
- **D-2** Future FBR/bank integrations depend on those parties' APIs.

---

## 3. Specific Requirements

### 3.1 External interface requirements

#### 3.1.1 User interfaces
- Web UI, one page per department (order, quotation, PO, PR, tax, invoice, accounts, vendors, warehouse, dashboard) served by Flask from [Frontend/](../../Frontend/).
- Every action returns an on-screen toast/confirmation (NFR-11).
- Money shown in PKR with separators (NFR-13).

#### 3.1.2 Software/API interfaces
- RESTful JSON API under `/api/**`. Representative endpoints:
  - `POST /api/orders/`, `GET /api/orders/`
  - `POST /api/quotations/`, `GET /api/quotations/order/<id>`, `POST /api/quotations/<id>/approve|reject`
  - `POST /api/po/` (issue from approved quotation)
  - `POST /api/pr/`, `POST /api/pr/<id>/recommend`, `POST /api/commercial/decision`
  - `POST /api/invoices/`, `POST /api/invoices/<id>/mark-paid`
  - `POST /api/tax/calculate-cost`, `POST /api/tax/calculate-withholding-tax`, `GET /api/tax/records`
- Full list in [07-functional-requirements.md](07-functional-requirements.md) and the project [README.md](../../README.md).

#### 3.1.3 Hardware interfaces
- No special hardware. Standard server + client workstations. (Future: receipt printer for challans/POs — out of scope R1.)

#### 3.1.4 Communications interfaces
- HTTP/HTTPS over LAN/intranet. HTTPS required in production (NFR-05 supporting).

### 3.2 Functional requirements
The complete, identified functional requirements (FR-01 … FR-38) and business rules (BR-01 … BR-09) are specified in **[07-functional-requirements.md](07-functional-requirements.md)** and incorporated here by reference. They are organised by module:

| Module | FRs | Use case |
|--------|-----|----------|
| Order Management | FR-01…FR-04 | UC-01 |
| Quotation & Comparison | FR-05…FR-10 | UC-02, UC-05 |
| PR & Approval | FR-11…FR-15 | UC-04 |
| Purchase Order | FR-16…FR-19 | UC-03 |
| Vendor & Negotiation | FR-20…FR-21 | support |
| Challan & Invoice | FR-22…FR-25 | UC-08 |
| Tax & Withholding | FR-26…FR-29 | UC-06, UC-07 |
| Accounts/Warehouse/Client | FR-30…FR-32 | support |
| Dashboard & Reports | FR-33…FR-34 | — |
| Security/Audit/Validation | FR-35…FR-38 | cross-cutting |

> Each FR states actor → action → response and is individually verifiable; acceptance criteria are in [09-user-stories-acceptance.md](09-user-stories-acceptance.md).

### 3.3 Data requirements
Entities, attributes, types and constraints are specified in **[10-domain-data-model.md](10-domain-data-model.md)** (data dictionary) and depicted in the context/DFD ([11-context-dfd.md](11-context-dfd.md)). Key integrity rules:
- Referential integrity across orders → quotations → PO → invoice → tax records (NFR-28).
- Monetary fields are PKR, 2-decimal, round-half-up (NFR-25).
- Unique invoice numbers (FR-22).

### 3.4 Non-functional requirements
The complete, measurable NFRs (NFR-01 … NFR-29) are specified in **[08-non-functional-requirements.md](08-non-functional-requirements.md)** and incorporated by reference, grouped as: Performance, Security, Usability, Reliability/Availability, Scalability, Maintainability, Compliance, Portability, Data Integrity/Backup.

The **mandatory go-live NFRs** (close prototype gaps) are: NFR-05/06/07 (auth + RBAC + hashing), NFR-14/16 (no data loss / transactional integrity — persist POs), NFR-17 (concurrency), NFR-23/25 (FBR compliance + currency).

### 3.5 Other requirements
- **Localisation:** PKR currency; English UI (Urdu optional, future).
- **Retention:** tax/financial records retained ≥ 6 years (NFR-24).
- **Backup:** daily DB backups (NFR-29).

---

## 4. Verification & prioritisation cross-reference

- **Prioritisation (MoSCoW):** [13-moscow-prioritisation.md](13-moscow-prioritisation.md) — defines Release-1 scope.
- **Conflicts & negotiation:** [14-conflict-resolution.md](14-conflict-resolution.md).
- **Validation of these requirements:** [15-requirements-validation.md](15-requirements-validation.md).
- **Traceability (requirement → design → code → test):** [17-traceability-matrix.md](17-traceability-matrix.md).

---

## 5. Approval (sign-off)

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product owner (Commercial rep) | _________ | | |
| PR Department rep | _________ | | |
| Tax/Accounts rep | _________ | | |
| Project supervisor | Sir Usman Waheed | | |
| Lead author | Syed M Wasif | | |

> Once signed, this SRS v1.0 is the **baseline**; all subsequent changes follow the change-control process in [18-change-management.md](18-change-management.md).
