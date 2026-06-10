# 18 · Requirements Change Management & Versioning

**Prompt 18** · *RE concept: requirements management / change control*

Defines how requirements change after the SRS is baselined, how the impact of a change is assessed against the RTM, who approves it, and how requirement **versions/baselines** are tracked across releases.

---

## 1. Why this matters
A *product* (unlike a one-off project) keeps evolving. Without control, scope creeps, the RTM rots, and the SRS stops reflecting reality. This lightweight process keeps requirements **traceable and current** through R1 → R2 → R3.

## 2. Baseline & versioning scheme

- **Baseline:** the SRS v1.0 ([12-srs.md](12-srs.md)), once signed off (SRS §5), is the **frozen reference**. Requirements are not edited in place after baselining — they change only via a Change Request.
- **Versioning:** semantic-style for the requirements set:
  - **Major (x.0):** new release scope (e.g. 2.0 adds full reporting).
  - **Minor (1.x):** approved additions/changes within a release.
  - **Patch (1.x.y):** clarifications/typo/defect fixes (e.g. the DEF-01…DEF-05 fixes from [15-requirements-validation.md](15-requirements-validation.md)).
- Each requirement carries an implicit version via the document's change log (§6).

## 3. Change-control workflow

```
  Requestor          Change Owner         CCB                Dev/Docs
     │ raise CR           │                 │                    │
     ▼                    │                 │                    │
 ┌────────┐  log   ┌─────────────┐  assess ┌──────────────┐      │
 │  CR    │───────►│ Impact      │────────►│ CCB decision │      │
 │ form   │        │ analysis    │         │ approve/defer│      │
 └────────┘        │ (vs RTM)    │         │ /reject      │      │
                   └─────────────┘         └──────┬───────┘      │
                                                  │ approved      ▼
                                                  └──────► update SRS + RTM + tests, bump version
```

**Steps**
1. **Raise** — any stakeholder submits a Change Request (CR) using the form in §4.
2. **Log** — CR recorded in the change log with a unique ID (CR-001…) and status `Open`.
3. **Impact analysis** — the Change Owner traces the affected items through the **RTM** ([17-traceability-matrix.md](17-traceability-matrix.md)): which FR/NFR, use cases, code modules, and tests are touched; estimates effort, cost, risk, and schedule impact.
4. **Decision (CCB)** — the Change Control Board (see §5) approves, defers (to a later release), or rejects, with rationale.
5. **Implement** — if approved: update the SRS and FR/NFR docs, update the RTM rows and the MoSCoW backlog, add/adjust test cases, and **bump the version**.
6. **Verify & close** — confirm the change is built and tested; set CR status `Closed`.

## 4. Change Request (CR) form template

```
CR-ID:              CR-007
Title:              Add NTN number to Vendor for tax compliance
Raised by:          Nadia Iqbal (Tax)            Date: 2026-07-xx
Type:               ☐ New  ☑ Change  ☐ Defect
Linked requirement: FR-20 (Vendor CRUD), NFR-23 (FBR compliance)
Description:        Vendors must store an NTN; tax records should reference it for FBR filing.
Business reason:    FBR withholding statements require payee NTN.
Impact (vs RTM):    Vendor model (+ntn), vendor_routes, tax_record link, TC-20/TC-27 updated.
Effort estimate:    Small (½ day)
Priority (MoSCoW):  Should (R2)
CCB decision:       ☐ Approve  ☐ Defer  ☐ Reject     Decided by: ____  Date: ____
Resulting version:  1.1
Status:             Open / Approved / In-progress / Closed
```

## 5. Change Control Board (CCB)

| Role | Member | Authority |
|------|--------|-----------|
| Chair / Product owner | Commercial lead | Final decision on scope |
| Tax/Accounts rep | Nadia / Hina | Compliance & financial impact |
| PR rep | Sara | Process/governance impact |
| Dev lead | (team) | Technical effort & feasibility |
| Supervisor (advisory) | Sir Usman Waheed | Academic alignment |

- **Quorum:** chair + dev lead + the rep of the affected area.
- **Fast-track:** *patch* clarifications/defects (e.g. wording fixes) may be approved by the chair alone and batched.

## 6. Change log (live)

| CR-ID | Date | Description | Decision | Version | Status |
|-------|------|-------------|----------|---------|--------|
| — | 2026-06-10 | Initial baseline of SRS v1.0 | Baseline | **1.0** | Closed |
| CR-001 | 2026-06-10 | Apply validation fixes DEF-01…DEF-05 (clarify FR-01/08/27/29/36) | Approve | 1.0.1 | Open |
| CR-002 | 2026-06-10 | Add BR-NEW-01 PKR approval threshold (from CONF-01) | Approve | 1.1 | Open |
| CR-003 | (future) | Add Vendor NTN (example) | Defer→R2 | — | Open |

## 7. Configuration management & tooling

- **Storage:** all requirement documents live in `docs/product/` under **Git** version control (this repository) — every change is diff-able and attributable.
- **Convention:** one CR = one commit/PR referencing the CR-ID in the message; the RTM and change log are updated in the same commit.
- **Branching:** requirement changes for a future release live on a release branch until that release is cut.
- **Traceability:** the RTM is the canonical link table; CRs must update it or they cannot be closed.

## 8. Metrics to watch

| Metric | Purpose |
|--------|---------|
| # open CRs per release | Scope-creep early warning |
| Avg. CR cycle time (raise→close) | Process responsiveness |
| % CRs deferred vs approved | Prioritisation health |
| RTM coverage of Must reqs | Release-readiness gate |

---

## 9. Summary

Requirements are **baselined** (SRS v1.0), **changed only via CRs**, **impact-analysed against the RTM**, **decided by a CCB**, **versioned**, and **kept in Git**. This closes the RE loop: the move from *project* (write it once) to *product* (manage it as it evolves) is now operational.

> End of the 18-document Requirements Engineering set. Start at [00-README-index.md](00-README-index.md).
