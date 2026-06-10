# 16 · Prototype Evaluation (Validation via Prototyping)

**Prompt 16** · *RE concept: prototyping as a validation technique*

The existing Flask + HTML application is treated as an **evolutionary prototype**. This document evaluates how showing each department page to stakeholders validates — or corrects — the captured requirements.

---

## 1. Prototype classification

| Aspect | Classification |
|--------|----------------|
| Type | **Evolutionary** (the prototype grows into the product) — not throwaway |
| Fidelity | **High-fidelity, functional** — real Flask API + SQLite, real workflow |
| Coverage | All 8 use cases have at least a page/endpoint |
| Purpose here | **Requirements validation** — confirm we understood the need, surface corrections early |

> Why evolutionary, not throwaway: the prototype already implements the data model and workflow; the productisation work (auth, PO persistence, tests) *extends* it rather than replacing it. This lowers cost (see [04-feasibility-study.md](04-feasibility-study.md)).

## 2. Page-by-page validation plan

For each page we record: what the stakeholder should confirm, and the likely **correction** the walkthrough will surface (a corrected requirement).

| Page (Frontend/) | Use case | Stakeholder | What they validate | Likely correction → requirement |
|------------------|----------|-------------|--------------------|---------------------------------|
| [order.html](../../Frontend/order.html) | UC-01 | Client/Commercial | Order fields match a real order | "We also need contact no. & delivery address" → extend Order (DEF-style change) |
| [quotation.html](../../Frontend/quotation.html) | UC-02/05 | Commercial | Quotations list & compare per order | "Show delivery days & rating next to price, and **flag cheapest**" → confirms FR-08 (DEF-02) |
| [po.html](../../Frontend/po.html) | UC-03 | Commercial | PO issued from approved quote | "PO disappears after restart" → confirms FR-18 (persist PO) |
| [pr.html](../../Frontend/pr.html) | UC-04 | PR | Raise/recommend/approve PR | "Need a **reason** field on reject + threshold rule" → confirms CONF-01 / FR-14 |
| [tax.html](../../Frontend/tax.html) | UC-06/07 | Tax | Sales & withholding calc on invoice | "Rate should come from a **current FBR list**, not typed each time" → confirms DEF-04 (TaxRate master) |
| [invoice.html](../../Frontend/invoice.html) | UC-08 | Accounts | Total = base+tax−WHT, mark paid | "Total computes correctly (✓); need linked **challan**" → confirms FR-25 |
| [accounts.html](../../Frontend/accounts.html) | UC-08 | Accounts | Pending payments & pay action | "Want a paid/unpaid filter" → R2 enhancement |
| [vendors.html](../../Frontend/vendors.html) | support | Commercial | Vendor master CRUD | "Add NTN no. for tax" → extend Vendor |
| [dashboard_new.html](../../Frontend/dashboard_new.html) | — | Management | One overview of all modules | "Counts should be **live** from DB" → confirms FR-33 |

## 3. Worked validation example (UC-07 Withholding Tax)

1. **Show:** the Tax officer opens `tax.html`, picks an invoice (base 60,000 PKR), enters 4.5%, runs withholding calculation.
2. **Observe:** system shows withholding = **2,700**, net payable = **57,300**, and writes a tax record (matches the UC-07 object diagram and AC-07.1).
3. **Validate:** officer confirms the math and the recording → **FR-27 validated**.
4. **Correction surfaced:** "I shouldn't have to *type* 4.5% — it should default to the current FBR rate." → **new requirement** (TaxRate master, DEF-04) captured without writing a single throwaway line.

This is the value of prototype-based validation: a 2-minute click-through replaces pages of speculative debate.

## 4. What prototyping confirmed vs corrected

| Confirmed (requirement was right) | Corrected (requirement refined) |
|-----------------------------------|---------------------------------|
| Invoice total formula (BR-02) | Tax rate should be data-driven (DEF-04) |
| Quotation-per-order comparison (FR-07) | Auto-flag cheapest must be explicit (DEF-02) |
| Approval-gated PO issuance (BR-01) | PO must be persisted (FR-18) |
| One-click mark-paid (FR-24) | Delivery challan needs to be an entity (FR-25) |
| Department-page structure fits real roles | Pages need login/role scoping (FR-35/36) |

## 5. Risks of evolutionary prototyping (and mitigation)

| Risk | Mitigation |
|------|------------|
| Prototype shortcuts harden into the product (e.g. in-memory PO, no auth) | Track them as **explicit requirements** (FR-18, FR-35/36) and MoSCoW-Must them for R1 |
| Stakeholders assume "it's basically done" | Communicate the **hardening backlog** (doc 13) and roadmap |
| UI polish distracts from missing non-functionals | Validate NFRs separately (doc 15), not just screens |

## 6. Outcome

The prototype is an effective **validation instrument**: it confirmed the core workflow requirements and surfaced five concrete corrections, all now captured in the FR/NFR set. It is suitable to **evolve** into Release 1 once the Must-have gaps (auth, PO persistence, tax-rate master, tests) are closed.

> Next: verification that the built product matches the (now validated) requirements is tracked through the test column of [17-traceability-matrix.md](17-traceability-matrix.md).
