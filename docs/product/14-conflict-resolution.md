# 14 · Requirements Negotiation & Conflict Resolution

**Prompt 14** · *RE concept: requirements negotiation*

Requirements from different stakeholders pull in different directions. This document logs the **conflicts**, the **stakeholders** on each side, the **trade-off**, and the **negotiated resolution** carried into the SRS and backlog.

> Method: each conflict is framed as *Position A vs Position B → underlying interest → win-win resolution* (interest-based negotiation), then recorded with an owner and status.

---

## Conflict log

### CONF-01 — Speed vs control (Commercial ↔ PR/Accounts)
- **Position A (Commercial, STK-02):** "Let me issue a PO the moment I pick a quote — approval steps slow me down."
- **Position B (PR + Accounts, STK-03/06):** "Every purchase must pass an approval gate, or we lose financial control."
- **Underlying interest:** both want *correct, fast* purchasing — A fears delay, B fears uncontrolled spend.
- **Resolution:** keep the approval gate (BR-01, BR-06) but make it **fast and digital** — pending items surface instantly (FR-13) and approval is one click with auto-advance (FR-14). Add a **threshold rule (BR-NEW-01):** orders below a configurable PKR amount need only a single commercial approval; above it, full PR approval. → Satisfies speed *and* control.
- **Owner:** Product owner · **Status:** Agreed · **Affects:** FR-14, FR-16, new business rule.

### CONF-02 — Cheapest vs best vendor (Commercial ↔ Management)
- **Position A (Commercial):** "Auto-select the lowest-cost quotation to save time."
- **Position B (Management, STK-08):** "Cheapest isn't always best — delivery time and vendor rating matter."
- **Underlying interest:** value for money, not just lowest price.
- **Resolution:** the system **flags** the lowest cost (FR-08, rank=1) but does **not auto-approve**; the officer still chooses and the decision (including delivery days, rating, and saving vs next-best) is **recorded** for justification (UC-05). → Decision support, not decision replacement.
- **Owner:** Commercial lead · **Status:** Agreed · **Affects:** FR-08, FR-09.

### CONF-03 — Calculation convenience vs compliance accuracy (Accounts ↔ Tax)
- **Position A (Accounts, STK-06):** "Let me type a quick tax figure on the invoice and move on."
- **Position B (Tax, STK-05):** "Tax and withholding must be computed from the official FBR rate and recorded, or we risk penalties."
- **Underlying interest:** fast invoicing vs defensible compliance.
- **Resolution:** Accounts generates the invoice, but **tax and withholding are computed by the system** from the configured FBR rate and **written as tax records** (FR-26, FR-27, FR-28); Accounts cannot hand-edit the tax once calculated. A **TaxRate master** (proposed entity, doc 10) keeps rates current. → Convenience for Accounts, control for Tax.
- **Owner:** Tax lead · **Status:** Agreed · **Affects:** FR-26–29, NFR-23, new TaxRate entity.

### CONF-04 — Open access vs separation of duties (Commercial ↔ all / Admin)
- **Position A (some users):** "It's easier if anyone can do any step when colleagues are away."
- **Position B (Accounts/Audit/Admin):** "The person who approves a PR must not also pay the invoice — separation of duties."
- **Underlying interest:** operational flexibility vs fraud prevention.
- **Resolution:** enforce **RBAC** (FR-36, NFR-06) with an **Admin override** that is itself **audited** (NFR-09). Cover absences with role *delegation* rather than open access. → Flexibility without losing the control.
- **Owner:** Admin · **Status:** Agreed · **Affects:** FR-36, FR-37, NFR-06/09.

### CONF-05 — Rich features now vs ship a reliable core (Management ↔ Dev team)
- **Position A (Management):** "We want dashboards, reports, negotiation, notifications in v1."
- **Position B (Dev team, STK-12):** "Trying to ship everything risks a buggy, late release; the core loop and data safety come first."
- **Underlying interest:** business value vs delivery risk.
- **Resolution:** apply **MoSCoW** (doc 13) — R1 delivers the compliant end-to-end loop + security + persistence; dashboards/reports/negotiation move to **R2/R3**. Management gets a **roadmap** so deferral is transparent. → Value delivered incrementally, low risk.
- **Owner:** Product owner · **Status:** Agreed · **Affects:** release plan, FR-33/34, FR-21.

### CONF-06 — SQLite simplicity vs concurrent multi-department use (Dev ↔ Operations)
- **Position A (Dev):** "SQLite is simple and already working."
- **Position B (Operations/Users):** "Five departments writing at once hit 'database is locked'."
- **Underlying interest:** simplicity vs reliability under load.
- **Resolution:** keep **SQLite for development/demo**, switch to **PostgreSQL for production** via configuration only (NFR-17, NFR-27) — already env-driven in [settings.py](../../backend/config/settings.py). → No rewrite, production-safe.
- **Owner:** Dev lead · **Status:** Agreed · **Affects:** NFR-17/27.

---

## Summary of new/changed rules from negotiation

| New rule | From | Carried into |
|----------|------|--------------|
| BR-NEW-01: PKR threshold decides single vs full approval | CONF-01 | FR-14, SRS §3.2 |
| Lowest-cost is flagged, never auto-approved | CONF-02 | FR-08 |
| Tax once calculated is system-owned (not hand-edited) | CONF-03 | FR-26–29 |
| Admin override is always audited | CONF-04 | NFR-09 |
| Feature richness deferred per MoSCoW roadmap | CONF-05 | doc 13 |
| PostgreSQL in production via config | CONF-06 | NFR-17/27 |

## Open conflicts (to revisit)
- **OPEN-01:** Whether vendors get a **self-service portal** (Vendor wants it; security wary). Parked for R3 pending a security review.

> Resolutions here are reflected in the validated requirement set ([15-requirements-validation.md](15-requirements-validation.md)) and tracked under change control ([18-change-management.md](18-change-management.md)).
