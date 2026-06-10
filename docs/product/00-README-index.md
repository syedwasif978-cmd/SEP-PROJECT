# ProcureFlow (PAMS) — Product Requirements Documentation

**Product:** ProcureFlow — Procurement & Accounts Management System (PAMS)
**Client / Domain:** Technical Solution Enterprise (TSE) — Automobile Machinery Workshop
**Course:** Software Requirements Engineering (SRE)
**Authors:** Syed M Wasif (24FA-023-SE), Abdul Basit (24FA-017-SE), Syed M Haziq (24FA-036-SE), Muhammad Saqib (24FA-006-SE), Shumail Ahmed Zia (24SP-013-SE)
**Instructor:** Sir Usman Waheed
**Version:** 1.0 · **Date:** 2026-06-10

---

## Purpose of this folder

This folder converts the academic **project** (a documented procurement system with a Flask + SQLite prototype) into a **product** by running it through the full Software Requirements Engineering (RE) process. Each document below is the output of one engineered RE activity, grounded in the **actual** running system in [`backend/`](../../backend/) and [`Frontend/`](../../Frontend/).

> **Project vs Product.** A *project* ends when it is graded. A *product* is driven by a vision, real stakeholders, and a value proposition, and is engineered to evolve through versions. These documents make that shift explicit.

## How to read it (recommended order)

| # | Document | RE concept demonstrated |
|---|----------|--------------------------|
| — | [00-prompt-log.md](00-prompt-log.md) | The 18 engineered prompts (process evidence) |
| 1 | [01-product-vision.md](01-product-vision.md) | Product vision & scope |
| 2 | [02-stakeholders-personas.md](02-stakeholders-personas.md) | Stakeholder analysis & personas |
| 3 | [03-problem-value-mvp.md](03-problem-value-mvp.md) | Problem statement, value proposition, MVP |
| 4 | [04-feasibility-study.md](04-feasibility-study.md) | Feasibility analysis |
| 5 | [05-elicitation-plan.md](05-elicitation-plan.md) | Elicitation techniques |
| 6 | [06-interview-questionnaire.md](06-interview-questionnaire.md) | Elicitation instruments |
| 7 | [07-functional-requirements.md](07-functional-requirements.md) | Functional requirements |
| 8 | [08-non-functional-requirements.md](08-non-functional-requirements.md) | Non-functional requirements / quality attributes |
| 9 | [09-user-stories-acceptance.md](09-user-stories-acceptance.md) | User stories & acceptance criteria |
| 10 | [10-domain-data-model.md](10-domain-data-model.md) | Domain model & data dictionary |
| 11 | [11-context-dfd.md](11-context-dfd.md) | Context diagram & DFD |
| 12 | [12-srs.md](12-srs.md) | Software Requirements Specification (ISO/IEC/IEEE 29148) |
| 13 | [13-moscow-prioritisation.md](13-moscow-prioritisation.md) | Requirements prioritisation (MoSCoW) |
| 14 | [14-conflict-resolution.md](14-conflict-resolution.md) | Requirements negotiation |
| 15 | [15-requirements-validation.md](15-requirements-validation.md) | Requirements validation |
| 16 | [16-prototype-validation.md](16-prototype-validation.md) | Prototyping as validation |
| 17 | [17-traceability-matrix.md](17-traceability-matrix.md) | Requirements traceability matrix |
| 18 | [18-change-management.md](18-change-management.md) | Requirements management & change control |

## Identifier scheme (used across all documents)

| Prefix | Meaning | Example |
|--------|---------|---------|
| `UC-xx` | Use case | UC-05 Compare Vendor Quotation |
| `FR-xx` | Functional requirement | FR-12 |
| `NFR-xx` | Non-functional requirement | NFR-03 |
| `US-xx` | User story | US-07 |
| `STK-xx` | Stakeholder | STK-02 |
| `BR-xx` | Business rule | BR-04 |

These IDs are the threads that the **Traceability Matrix** (doc 17) weaves together: stakeholder → use case → requirement → design/code → test.

## Snapshot of the system these documents describe

- **Backend:** Python / Flask 2.2.5, Flask-SQLAlchemy 3.0.3, SQLite (`backend/app.db`).
- **Frontend:** static HTML/CSS/vanilla-JS pages, one per department, served by Flask.
- **Scope:** order placement → vendor quotation → comparison → PR approval → purchase order → delivery challan & invoice bills → sales-tax & withholding-tax calculation → payment.
- **Tax regime:** Pakistan / FBR — currency PKR, sales tax (~17%) and withholding tax (~4.5%).
- **Known gaps (intentionally captured as requirements):** no authentication/role-based access, purchase orders held in memory (not persisted), no automated tests, thin input validation.
