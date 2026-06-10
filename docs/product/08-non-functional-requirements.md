# 08 · Non-Functional Requirements (Quality Attributes)

**Prompt 8** · *RE concept: non-functional requirements / quality attributes*

Every NFR is **measurable** (has a target and a verification method), grouped by quality attribute. Several are written directly against gaps found in the current prototype.

> Format: *The system shall …* + **Metric/Target** + **Verification**.

---

## 1. Performance & Efficiency

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-01 | API responses for single-record reads/writes (order, quotation, invoice) shall be fast under normal load. | ≤ **500 ms** at the 95th percentile for ≤ 50 concurrent users | Load test (Locust/JMeter) |
| NFR-02 | Quotation comparison for an order shall return and flag the lowest cost quickly. | ≤ **2 s** for up to 50 quotations | Timed UI/API test |
| NFR-03 | Invoice + tax + withholding calculation shall complete promptly. | ≤ **1 s** per invoice | Unit/integration timing |
| NFR-04 | The dashboard shall load aggregate counts. | ≤ **3 s** initial render | Browser timing |

## 2. Security

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-05 | The system shall require authentication for all non-public endpoints. | 100% of `/api/**` write endpoints protected | Pen-test / auth test |
| NFR-06 | The system shall enforce role-based access control (Commercial, PR, Tax, Accounts, Admin). | 0 cross-role actions permitted | Access-control test matrix |
| NFR-07 | The system shall store passwords hashed (never plaintext). | bcrypt/argon2, cost ≥ default | Code & DB review |
| NFR-08 | The system shall prevent SQL injection via parameterised ORM queries. | 0 injectable endpoints | SQLMap / SAST |
| NFR-09 | All state-changing actions shall be recorded in an immutable audit log (actor, action, timestamp). | 100% coverage | Audit-log review |

> **Current gap:** the prototype has **no authentication or RBAC** — any client can POST to any endpoint. NFR-05…NFR-07 are mandatory for go-live (see [04-feasibility-study.md](04-feasibility-study.md)).

## 3. Usability

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-10 | A trained department officer shall complete their core task (e.g. compare & approve a quotation) without referring to a manual. | ≥ **90%** task success in usability test | Moderated usability test (5 users) |
| NFR-11 | The system shall give immediate feedback (toast/confirmation) on every action. | 100% of actions show success/error message | UI review (toast system already present) |
| NFR-12 | The UI shall be usable on standard desktop browsers and responsive down to tablet width. | Chrome/Edge/Firefox latest; ≥ 768px | Cross-browser test |
| NFR-13 | Monetary values shall display consistently in PKR with thousands separators. | 100% of money fields | UI review |

## 4. Reliability & Availability

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-14 | No committed business data shall be lost on application restart. | 0 data loss | Restart test |
| NFR-15 | The system shall be available during working hours. | ≥ **99%** uptime (business hours) | Uptime monitor |
| NFR-16 | Failed operations shall roll back cleanly without partial writes. | 100% transactional integrity | Fault-injection test |

> **Current gap:** Purchase Orders are stored **in memory** (`pos_store`) and are lost on restart — directly violates NFR-14. Closing FR-18 satisfies this.

## 5. Scalability

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-17 | The data store shall support concurrent multi-department writes without locking errors. | ≥ 50 concurrent users, 0 "database is locked" errors | Concurrency test |
| NFR-18 | The architecture shall scale from an SME (hundreds of transactions/month) to ~10× without redesign. | Linear capacity via DB swap | Capacity review |

> **Current gap:** **SQLite** is single-writer. Production should use **PostgreSQL** — the connection is already environment-driven in [settings.py](../../backend/config/settings.py), so this is a config swap, not a rewrite.

## 6. Maintainability

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-19 | Business logic shall live in the service layer, not in route handlers, to keep modules single-responsibility. | Services cover all multi-step operations | Code review |
| NFR-20 | The codebase shall have no duplicate/dead route modules. | 0 duplicate blueprints (`pr_routes_duplicate.py`, double PO blueprints removed) | Static review |
| NFR-21 | Automated tests shall cover the core procure-to-pay path. | ≥ **70%** line coverage on routes/services | pytest + coverage |
| NFR-22 | Public API endpoints shall be documented. | 100% endpoints in an OpenAPI/README table | Doc review |

> **Current gap:** empty [tax_service.py](../../backend/services/tax_service.py), duplicate routes, and no tests. NFR-19…NFR-21 capture the cleanup.

## 7. Compliance & Legal

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-23 | Sales-tax and withholding-tax calculations shall conform to current FBR rules. | 100% match to FBR-rule expected values | Compliance test vs circular |
| NFR-24 | Tax records shall be retained and exportable for FBR filing/audit. | ≥ 6 years retention; exportable | Records review |
| NFR-25 | All financial figures shall use a single currency (PKR) and a consistent rounding rule. | 2-decimal, round-half-up | Calculation test |

## 8. Portability & Deployment

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-26 | The system shall run on Windows and Linux servers with Python 3.8+. | Both OS verified | Deployment test |
| NFR-27 | The system shall switch between SQLite (dev) and PostgreSQL/Oracle (prod) via configuration only. | 0 code change to switch DB | Config test |

## 9. Data Integrity & Backup

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-28 | Referential integrity (orders→quotations→PO→invoice→tax) shall be enforced by foreign keys. | 0 orphan records | DB constraint check |
| NFR-29 | The database shall be backed up automatically. | Daily backup, ≤ 24 h RPO | Backup/restore drill |

---

## NFR ↔ gap summary (what the prototype must fix to become a product)

| Gap in prototype | NFR(s) that close it | Linked FR |
|------------------|----------------------|-----------|
| No authentication / RBAC | NFR-05, 06, 07 | FR-35, FR-36 |
| Purchase Orders in memory | NFR-14, 16 | FR-18 |
| SQLite single-writer | NFR-17, 18, 27 | — |
| Empty services, duplicate routes, no tests | NFR-19, 20, 21 | FR-38 |
| No actor on audit trail | NFR-09 | FR-37 |
| Tax-rate master not formalised | NFR-23, 25 | FR-29 |

These NFRs are prioritised in [13-moscow-prioritisation.md](13-moscow-prioritisation.md) and validated in [15-requirements-validation.md](15-requirements-validation.md).
