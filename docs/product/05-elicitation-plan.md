# 05 · Requirements Elicitation Plan

**Prompt 5** · *RE concept: elicitation techniques*

A plan for gathering requirements from TSE's stakeholders, mapping each elicitation technique to the stakeholder it best targets and the kind of requirement it surfaces.

---

## 1. Objectives of elicitation

- Discover the **real** procurement workflow (not just the documented one).
- Surface **hidden / tacit** requirements (e.g. how vendors are *really* chosen, how tax-rate changes are handled).
- Capture **business rules** (approval gates, FBR tax rules) and **exceptions** (rejected PRs, disputed invoices).
- Confirm and correct the assumptions baked into the existing prototype.

## 2. Technique → stakeholder → outcome matrix

| # | Technique | Best for stakeholder(s) | What it surfaces here | Effort |
|---|-----------|--------------------------|------------------------|--------|
| 1 | **Interviews** (semi-structured) | Commercial (STK-02), PR (STK-03), Tax (STK-05), Accounts (STK-06) | Deep, role-specific needs and pain points; the "why" behind each step | Medium |
| 2 | **Questionnaires / surveys** | Accounts & Tax clerks, multiple vendors (STK-04) | Breadth — quantify frequencies, error rates, satisfaction; reach many vendors cheaply | Low |
| 3 | **Observation** (job shadowing) | Commercial & Accounts officers | The *actual* desk workflow, workarounds, where paper piles up — tacit knowledge people forget to mention | Medium–High |
| 4 | **Document analysis** | All — via existing forms & registers | Real data fields and business rules from current quotation sheets, POs, challans, invoices, tax circulars | Low |
| 5 | **Brainstorming / workshops** | Cross-department + Management (STK-08) | Resolve inter-department hand-off conflicts; agree the to-be workflow | Medium |
| 6 | **Prototyping** (the existing app) | Commercial, Tax, Accounts | Concrete reactions to real screens → fast correction of misunderstood requirements | Low (prototype exists) |

## 3. How each technique applies to TSE

### 3.1 Interviews
- **Who:** one officer per department (Bilal–Commercial, Sara–PR, Nadia–Tax, Hina–Accounts).
- **How:** 30–45 min semi-structured sessions using the scripts in [06-interview-questionnaire.md](06-interview-questionnaire.md). Start broad ("walk me through a typical order"), then probe exceptions.
- **Targets:** functional requirements + business rules + pain points.

### 3.2 Questionnaires
- **Who:** Accounts/Tax clerks and a sample of 8–10 vendors.
- **How:** short structured form (mostly closed questions + a few open ones) to quantify how often quotes are compared, how often tax is recalculated, typical delays.
- **Targets:** prioritisation data and non-functional expectations (speed, accuracy).

### 3.3 Observation
- **Who:** shadow the Commercial officer comparing quotations, and the Accounts clerk matching an invoice to a PO and challan.
- **How:** silent observation for half a day per role; note every manual step, tool switch and workaround.
- **Targets:** tacit requirements and usability needs the prototype must respect.

### 3.4 Document analysis
- **Who:** collect blank + filled samples of the current quotation comparison sheet, purchase order, delivery challan, invoice bill, and the latest FBR tax/withholding circular.
- **How:** extract every field and rule; reconcile against the prototype's models in [backend/models/](../../backend/models/).
- **Targets:** the **data dictionary** (doc 10) and tax business rules (BR-xx).

### 3.5 Brainstorming / workshop
- **Who:** all four department officers + a management representative, in one room.
- **How:** map the current procure-to-pay flow on a whiteboard; mark hand-off pain points; agree the to-be flow and the approval gates.
- **Targets:** conflict resolution input (doc 14) and the agreed end-to-end process.

### 3.6 Prototyping
- **Who:** the three personas.
- **How:** demo the existing department pages (order, quotation, tax, invoice); record every "that's not how we do it" reaction.
- **Targets:** validation/correction of already-captured requirements (doc 16).

## 4. Sequencing

```
Document analysis ─► Interviews ─► Observation ─► Questionnaire (breadth)
        │                                              │
        └──────────────► Workshop (reconcile) ◄────────┘
                              │
                              ▼
                    Prototype walkthrough (validate)
```

Document analysis first (cheap context) → interviews & observation (depth) → questionnaire (breadth/quantify) → workshop (reconcile conflicts) → prototype walkthrough (validate).

## 5. Anticipated elicitation challenges

| Challenge | Handling |
|-----------|----------|
| Stakeholders describe the *ideal*, not the *actual*, process | Cross-check interviews with observation and real documents. |
| "Everybody knows that" tacit rules go unsaid | Use observation + show-me-on-the-prototype prompts. |
| Inter-department disagreement on hand-offs | Resolve in the joint workshop, not 1:1. |
| Vendors hard to reach | Use the questionnaire (async) rather than interviews. |
| Conflicting tax-rate knowledge | Anchor on the official FBR circular (document analysis), not memory. |

## 6. Outputs of elicitation

Raw notes and forms feed directly into: functional requirements (doc 07), NFRs (doc 08), the data dictionary (doc 10), and the conflict log (doc 14).
