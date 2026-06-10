# Prompt Log — Engineering the Project into a Product

This is the **process evidence** requested by the course: the ordered set of 18 prompts used to drive the Requirements Engineering of ProcureFlow (PAMS). Each prompt maps to one RE concept and produced the correspondingly numbered document in this folder.

> How to use: run each prompt in order against an AI assistant (or work it by hand). Each output becomes one artefact. The concept tag next to each prompt is what the prompt demonstrates.

---

### Phase 0 — Product framing (project → product)

**Prompt 1 — Product Vision** · *Concept: product vision / scoping* → [01-product-vision.md](01-product-vision.md)
> "Act as a product owner. Based on my Procurement and Accounts Management System (order placement, vendor quotations, PR approval, delivery challan, invoice bills, cost tax and withholding tax for Technical Solution Enterprise's automobile machinery workshop), write a one-paragraph product vision statement using the Geoffrey Moore template — *For [customer], who [need], the [product] is a [category] that [benefit], unlike [alternative]* — and a set of measurable product goals."

**Prompt 2 — Stakeholders & Personas** · *Concept: stakeholder analysis* → [02-stakeholders-personas.md](02-stakeholders-personas.md)
> "Identify every stakeholder of this product, classify them as primary / secondary / external, and build three detailed personas (Commercial Officer, Tax Officer, Accounts Clerk) with goals, pain points in the current manual process, and expectations of the product."

**Prompt 3 — Problem, Value Proposition & MVP** · *Concept: scope definition / MVP* → [03-problem-value-mvp.md](03-problem-value-mvp.md)
> "Write a sharp problem statement and a value proposition, then define the MVP: which of the 8 use cases (UC-01 … UC-08) must ship first versus later, with justification."

### Phase 1 — Feasibility & business case

**Prompt 4 — Feasibility Study** · *Concept: feasibility analysis* → [04-feasibility-study.md](04-feasibility-study.md)
> "Produce a feasibility study covering technical (Flask + SQLite stack), economic (cost vs benefit), operational (departmental adoption) and schedule feasibility for turning this documented system into a real product."

### Phase 2 — Requirements elicitation

**Prompt 5 — Elicitation Plan** · *Concept: elicitation techniques* → [05-elicitation-plan.md](05-elicitation-plan.md)
> "Design a requirements elicitation plan. For each technique — interviews, questionnaires, observation, document analysis, brainstorming, prototyping — explain how I would apply it to TSE's procurement workflow and which stakeholder it targets."

**Prompt 6 — Interview & Questionnaire** · *Concept: elicitation instruments* → [06-interview-questionnaire.md](06-interview-questionnaire.md)
> "Write a realistic 10-question interview script for the Commercial Department officer and a 10-item questionnaire for the Accounts/Tax departments, designed to surface hidden requirements in quotation comparison and withholding-tax handling."

### Phase 3 — Analysis & modelling

**Prompt 7 — Functional Requirements** · *Concept: functional requirements* → [07-functional-requirements.md](07-functional-requirements.md)
> "From the 8 use cases and the existing API, derive numbered functional requirements (FR-01, FR-02, …). Each must state actor, action and expected system response."

**Prompt 8 — Non-Functional Requirements** · *Concept: quality attributes* → [08-non-functional-requirements.md](08-non-functional-requirements.md)
> "Write measurable non-functional requirements grouped by quality attribute — performance, security, usability, reliability, scalability, maintainability, compliance (FBR tax rules) — each with a verifiable target."

**Prompt 9 — User Stories & Acceptance Criteria** · *Concept: user stories & acceptance criteria* → [09-user-stories-acceptance.md](09-user-stories-acceptance.md)
> "Convert each use case into Agile user stories (*As a [role], I want [feature], so that [benefit]*) with Given/When/Then acceptance criteria, starting with UC-04 PR Approval and UC-07 Withholding Tax."

**Prompt 10 — Domain & Data Model** · *Concept: domain modelling / data requirements* → [10-domain-data-model.md](10-domain-data-model.md)
> "Produce a conceptual class diagram and a data dictionary for the core entities (Order, Quotation, PurchaseRequest, PurchaseOrder, Invoice, TaxRecord, Vendor, Account…), with each attribute's type and constraints, validated against the SQLite models in backend/models/."

**Prompt 11 — Context & Data Flow** · *Concept: context & DFD modelling* → [11-context-dfd.md](11-context-dfd.md)
> "Describe the system context diagram (product as one process with all external actors and data flows) and a level-1 DFD for the procure-to-pay flow."

### Phase 4 — Requirements specification

**Prompt 12 — Software Requirements Specification** · *Concept: SRS standard (ISO/IEC/IEEE 29148)* → [12-srs.md](12-srs.md)
> "Assemble a complete SRS following the ISO/IEC/IEEE 29148 (IEEE 830) structure — Introduction, Overall Description, Specific Requirements, External Interfaces — reusing the FRs and NFRs already produced."

### Phase 5 — Prioritisation & negotiation

**Prompt 13 — MoSCoW Prioritisation** · *Concept: requirements prioritisation* → [13-moscow-prioritisation.md](13-moscow-prioritisation.md)
> "Prioritise every functional requirement using MoSCoW (Must/Should/Could/Won't-for-now) as a table with a one-line justification, doubling as the release-1 product backlog."

**Prompt 14 — Conflict Resolution** · *Concept: requirements negotiation* → [14-conflict-resolution.md](14-conflict-resolution.md)
> "Identify likely requirement conflicts between stakeholders (Commercial wants speed, Accounts wants approval gates, Tax wants compliance checkpoints) and propose a negotiated resolution for each."

### Phase 6 — Validation & verification

**Prompt 15 — Requirements Validation** · *Concept: validation against quality criteria* → [15-requirements-validation.md](15-requirements-validation.md)
> "Run a validation review: for a sample of requirements, check each against correct, complete, consistent, unambiguous, verifiable, traceable, feasible — flag failures with fixes."

**Prompt 16 — Prototype Validation** · *Concept: prototyping as validation* → [16-prototype-validation.md](16-prototype-validation.md)
> "Treat the existing Flask + HTML prototype as an evolutionary prototype. Write a prototype evaluation describing how each department page validates or corrects the requirements."

### Phase 7 — Requirements management

**Prompt 17 — Traceability Matrix** · *Concept: traceability* → [17-traceability-matrix.md](17-traceability-matrix.md)
> "Build a Requirements Traceability Matrix linking each requirement → use case → design element → backend route/model that implements it → test case."

**Prompt 18 — Change & Version Management** · *Concept: requirements management / change control* → [18-change-management.md](18-change-management.md)
> "Define a lightweight requirements change-management process: how a change request is raised, impact-analysed against the RTM, approved, and how requirement versions/baselines are tracked across releases."

---

**Coverage summary:** the 18 prompts span the full RE lifecycle — *inception → elicitation → analysis & modelling → specification → prioritisation & negotiation → validation → management* — applied end-to-end to the ProcureFlow (PAMS) product.
