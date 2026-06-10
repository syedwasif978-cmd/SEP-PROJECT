# 15 · Requirements Validation Review

**Prompt 15** · *RE concept: requirements validation against quality criteria*

A review that checks a sample of requirements against the seven quality criteria, records defects, and proposes fixes — so the SRS is sound before design proceeds.

> **Validation vs verification:** *Validation* = "are we building the right thing?" (requirements correct & complete). *Verification* = "are we building the thing right?" (the build matches the spec — done later via tests, see [17-traceability-matrix.md](17-traceability-matrix.md)).

---

## 1. Quality criteria used (per ISO/IEC/IEEE 29148)

| Criterion | A good requirement is… |
|-----------|------------------------|
| Correct | An accurate statement of a real need |
| Complete | Nothing essential missing (incl. exceptions) |
| Consistent | Doesn't contradict another requirement |
| Unambiguous | One interpretation only |
| Verifiable | Can be tested/measured |
| Traceable | Linked to a source and forward to design/test |
| Feasible | Achievable within constraints |

## 2. Sample review (12 requirements)

| Req | Correct | Complete | Consistent | Unambig. | Verifiable | Traceable | Feasible | Verdict |
|-----|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---------|
| FR-01 Place order | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | Minor fix |
| FR-08 Flag lowest quote | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | Minor fix |
| FR-16 Issue PO | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Pass |
| FR-18 Persist PO | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Pass |
| FR-22 Invoice total | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Pass |
| FR-27 Withholding tax | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | Minor fix |
| FR-29 PKR + FBR rates | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ | Fix |
| FR-36 RBAC | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | Minor fix |
| NFR-01 Performance | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | Check |
| NFR-14 No data loss | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | Note |
| NFR-23 FBR compliance | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Pass |
| BR-02 total=base+tax−WHT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Pass |

Legend: ✅ meets · ⚠️ partial/at-risk.

## 3. Defects found & fixes

| Defect ID | Requirement | Issue (criterion) | Fix |
|-----------|-------------|-------------------|-----|
| DEF-01 | FR-01 | *Completeness* — doesn't say what happens if budget is 0 or quantity invalid | Add validation rule: quantity ≥ 1, budget ≥ 0; reject otherwise (folds into FR-38). |
| DEF-02 | FR-08 | *Ambiguity* — "lowest cost": unit price or total? | Specify: flag the lowest **total_price** for the order; ties broken by fewest delivery_days. |
| DEF-03 | FR-27 | *Completeness* — base for WHT (gross vs net) unstated | Specify: WHT computed on **gross base_amount** (per UC-07 example: 4.5% × 60,000 = 2,700). |
| DEF-04 | FR-29 | *Ambiguity/Completeness* — "FBR-consistent rates" not pinned | Introduce **TaxRate master** with effective dates; reference the current FBR circular. |
| DEF-05 | FR-36 | *Completeness* — roles list not enumerated | Enumerate roles: Client, Commercial, PR, Tax, Accounts, Admin; define each role's allowed actions in an access matrix. |
| DEF-06 | NFR-01 | *Feasibility* — 500 ms target unproven on current stack | Confirm with a baseline load test; keep target but mark "to be validated in R1". |
| DEF-07 | NFR-14 | *Consistency* — conflicts with current in-memory PO design (FR-18 not yet done) | No spec change; flag as **must-fix-before-go-live** dependency (already MUST in doc 13). |

## 4. Coverage / completeness checks

- **Every use case has at least one FR?** ✅ UC-01→FR-01.., UC-02→FR-05.., UC-03→FR-16.., UC-04→FR-11.., UC-05→FR-07.., UC-06→FR-26, UC-07→FR-27, UC-08→FR-22.
- **Every persona goal has a story?** ✅ mapped in [09-user-stories-acceptance.md](09-user-stories-acceptance.md).
- **Every "Must" requirement traceable to code or a planned task?** ✅ see [17-traceability-matrix.md](17-traceability-matrix.md).
- **Exception flows captured?** ⚠️ partially — rejection paths (quotation reject, PR reject) covered; payment-failure and duplicate-invoice flows added as follow-ups (DEF list).

## 5. Validation techniques applied / planned

| Technique | Applied here |
|-----------|--------------|
| **Requirements review/inspection** | This document (checklist against 7 criteria) |
| **Prototyping** | The running app, evaluated in [16-prototype-validation.md](16-prototype-validation.md) |
| **Test-case derivation** | Acceptance criteria in doc 09 → test cases in the RTM |
| **Stakeholder walkthrough** | Planned: review this SRS with each department lead, capture sign-off (SRS §5) |

## 6. Outcome

- 12 requirements reviewed; **5 passed clean, 7 had minor/medium defects, all with fixes**; 0 fatal/contradictory requirements after CONF-resolutions (doc 14).
- **Action:** apply DEF-01…DEF-05 edits to the FR set; carry DEF-06/07 as R1 tasks.
- After fixes, the requirement set is judged **valid and ready to baseline** ([12-srs.md](12-srs.md) §5).
