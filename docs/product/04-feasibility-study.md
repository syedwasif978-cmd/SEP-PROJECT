# 04 · Feasibility Study

**Prompt 4** · *RE concept: feasibility analysis*

Assesses whether building ProcureFlow (PAMS) into a real product for TSE is worthwhile across four dimensions: **Technical, Economic, Operational, Schedule** (the "TEOS" feasibility model). A working prototype already exists, which de-risks several dimensions.

---

## 1. Technical feasibility — ✅ Feasible

**Question:** Can the product be built and run with available technology and skills?

| Factor | Assessment |
|--------|------------|
| Existing stack | Python / Flask 2.2.5, Flask-SQLAlchemy 3.0.3, SQLite — mature, well-documented, free. A functioning prototype already implements all 8 use cases. |
| Team skills | The team has already built the prototype (models, blueprint routes, ORM) → required competency is demonstrated, not hypothetical. |
| Architecture | Layered: routes → models → DB, with a `services/` and `controllers/` structure ready to absorb business logic. Supports growth. |
| Data volume | An SME workshop generates hundreds–low-thousands of transactions/month — trivial for the stack. |

**Technical risks & mitigations:**

| Risk | Severity | Mitigation |
|------|----------|------------|
| Purchase Orders held **in memory** (`pos_store` in [po_routes_new.py](../../backend/routes/po_routes_new.py)) → lost on restart | High | Migrate PO to a persisted SQLAlchemy model (planned for MVP). |
| **SQLite** is single-writer → concurrency limits under multi-department load | Medium | Swap to PostgreSQL for production (config already env-driven in [settings.py](../../backend/config/settings.py)). |
| **No automated tests** | Medium | Add pytest suite (see [15-requirements-validation.md](15-requirements-validation.md)). |
| **Duplicate/legacy routes** (e.g. `pr_routes_duplicate.py`, two PO blueprints) | Low | Consolidate during hardening. |

**Verdict:** technically feasible; the work is *hardening and gap-closing*, not greenfield build.

## 2. Economic feasibility — ✅ Feasible (strongly positive)

**Question:** Do the benefits outweigh the costs?

**Costs (indicative, for a production-grade R1):**

| Cost item | Notes |
|-----------|-------|
| Software licences | ≈ **PKR 0** — Flask, SQLAlchemy, PostgreSQL are open-source. |
| Development effort | Team labour (academic) for hardening + MVP gaps. |
| Hosting | Low — single VM / on-prem server; optionally a small cloud instance. |
| Training | Minimal — 1 short session per department. |
| Support | 6-month support window per the project's support contract. |

**Benefits (tangible + intangible):**

- **Tangible:** fewer tax-calculation errors (avoided FBR penalties), less rework, faster cycle time (G-1), no cost of lost documents/re-procurement.
- **Intangible:** audit-readiness, management visibility, professional vendor-facing image, scalable foundation.

**Cost–benefit conclusion:** near-zero licence cost against recurring savings in time and error-avoidance → **payback is rapid**; the dominant cost is people-time, already partly sunk in the prototype.

## 3. Operational feasibility — ✅ Feasible (with change management)

**Question:** Will the organisation actually adopt and use it?

| Factor | Assessment |
|--------|------------|
| Fit to real workflow | The product mirrors TSE's **actual** departmental hand-offs (Commercial → PR → Vendor → Tax → Accounts), so it fits existing roles rather than forcing reorganisation. |
| User capability | Web UI with one page per department; basic computer literacy is sufficient. |
| Process discipline | Requires departments to follow approval gates instead of verbal shortcuts (assumption A-1). |
| Resistance | Possible reluctance to drop familiar paper/Excel habits. |

**Operational risks & mitigations:**

| Risk | Mitigation |
|------|------------|
| Staff bypass the system (parallel paper) | Management mandate + make the system faster than paper; dashboard makes bypassing visible. |
| Role confusion | Add authentication + role-based access so each page is scoped to a department (NFR-Security). |
| Data-entry burden | Auto-computation (totals, taxes) reduces typing vs the manual baseline. |

**Verdict:** operationally feasible provided it is paired with a light change-management push and role-based access.

## 4. Schedule feasibility — ✅ Feasible

**Question:** Can it be delivered in the available time?

Because the prototype already covers all eight use cases, the remaining MVP work is bounded:

| Milestone | Work | Indicative effort |
|-----------|------|-------------------|
| M1 | Persist Purchase Orders; consolidate duplicate routes | Small |
| M2 | Add authentication + role-based access | Small–Medium |
| M3 | Harden tax/withholding calculation + records; lock currency to PKR | Small |
| M4 | Dashboard live counts + audit fields (actor/timestamp) | Small |
| M5 | pytest suite + UAT with departments | Medium |

These fit within a single academic term / a short product sprint sequence → schedule-feasible.

## 5. Additional lenses

- **Legal/compliance feasibility:** must comply with **FBR** sales-tax and withholding-tax rules and operate in PKR (constraint C-1). No personal-data/privacy blockers beyond standard business records.
- **Schedule vs scope trade-off:** if time is short, defer UC-04 full multi-level PR approval (MVP-lite, per [03-problem-value-mvp.md](03-problem-value-mvp.md)) rather than cutting tax compliance.

## 6. Overall recommendation

| Dimension | Verdict |
|-----------|---------|
| Technical | ✅ Feasible (hardening, not rebuild) |
| Economic | ✅ Strongly positive (open-source, fast payback) |
| Operational | ✅ Feasible with change management + RBAC |
| Schedule | ✅ Feasible (prototype already covers UC-01…UC-08) |

> **Go decision:** proceed to productise. Prioritise the three highest-severity technical risks — PO persistence, authentication/RBAC, and tax-record hardening — within the MVP.
