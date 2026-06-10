# 06 · Elicitation Instruments — Interview Script & Questionnaire

**Prompt 6** · *RE concept: elicitation instruments*

Concrete, ready-to-use instruments produced from the plan in [05-elicitation-plan.md](05-elicitation-plan.md).

---

## Part A — Interview script: Commercial Department Officer (STK-02)

**Goal:** surface how orders, quotation comparison and PO issuance *really* work, and the hidden rules behind vendor selection.
**Format:** semi-structured, 30–45 min, one interviewee (persona: Bilal Raza). Probes in *italics*.

**Warm-up**
1. Walk me through what happens from the moment a client places an order until you issue a purchase order. *(Let them narrate; don't interrupt.)*
2. Roughly how many orders and quotations do you handle in a typical week?

**Quotation handling**
3. How do you currently request quotations from vendors, and how do they reach you (phone, paper, WhatsApp, email)? *Which is most common?*
4. When you have several quotations for one order, how exactly do you compare them? *What do you write down, and where?*
5. Besides price, what else decides which vendor wins — delivery time, past reliability, payment terms? *Can you rank them?*
6. Has the cheapest quote ever **not** been chosen? *Why — and how did you justify that to management?*

**Approvals & hand-offs**
7. Who must approve before a PO can go out, and how is that approval recorded today?
8. What happens when a purchase requisition is **rejected** — where does it go, who is told?

**Pain points & wishes**
9. What part of this process wastes the most of your time or goes wrong most often?
10. If you had a system that did one thing perfectly for you, what would that one thing be?

*Closing:* "Is there anything about how this really works that I haven't asked about?"

---

## Part B — Interview script: Tax Department Officer (STK-05) *(supplementary)*

1. Which taxes apply to a typical vendor invoice here — sales/cost tax, withholding tax, anything else?
2. What rates do you currently apply, and how do you know they're the current FBR rates?
3. Walk me through how you calculate withholding tax on an invoice today. *What do you compute it on — gross or net?*
4. Where do you record what was deducted, and how do you prepare it for FBR filing?
5. When FBR changes a rate, how do you find out and update your process?
6. What's the riskiest part — where could an error cost the company a penalty?

---

## Part C — Questionnaire: Accounts & Tax Departments

**Goal:** quantify frequencies, errors and expectations across clerks (breadth). Mostly closed questions for easy analysis.
**Format:** self-administered, ~5 minutes. Scale = 1 (Strongly disagree) … 5 (Strongly agree) unless noted.

**Section 1 — About your work**
1. Which department are you in? ☐ Accounts ☐ Tax ☐ Both
2. On an average day, how many invoices do you process? ☐ 0–5 ☐ 6–15 ☐ 16–30 ☐ 30+

**Section 2 — Current process (rate 1–5)**
3. I can easily match an invoice to its purchase order and delivery challan today. `1 2 3 4 5`
4. Tax and withholding-tax amounts are calculated accurately in the current manual process. `1 2 3 4 5`
5. I often have to re-enter the same figures in more than one place. `1 2 3 4 5`
6. The current "paid / unpaid" status is reliable and up to date. `1 2 3 4 5`
7. I can quickly find a past invoice, challan or tax record when asked. `1 2 3 4 5`

**Section 3 — Errors & delays**
8. In the last month, how often did a tax/withholding calculation have to be corrected? ☐ Never ☐ 1–2 ☐ 3–5 ☐ 6+
9. The single biggest cause of delay in my work is: ☐ Missing documents ☐ Waiting for approvals ☐ Manual calculation ☐ Re-entering data ☐ Other: ____

**Section 4 — Expectations of the new system (rate 1–5)**
10. Automatically computing invoice total as *base + sales tax − withholding tax* would help me. `1 2 3 4 5`
11. A one-click "mark as paid" with automatic date stamping would help me. `1 2 3 4 5`
12. A searchable list of all tax records by invoice and period would help me. `1 2 3 4 5`
13. *(Open)* What is the one feature that would most reduce errors in your work? ______________

---

## Part D — Vendor mini-questionnaire (STK-04, external)

1. How do you currently receive purchase orders from TSE? ☐ Phone ☐ Paper ☐ Email ☐ WhatsApp
2. How do you submit your quotation and later your invoice? (free text)
3. How important is it to receive a clear, written PO with delivery date and terms? `1 2 3 4 5`
4. Would an online portal to submit quotes and view PO status be useful? ☐ Yes ☐ No ☐ Maybe

---

## How the answers feed the requirements

| Instrument question(s) | Feeds |
|------------------------|-------|
| A3–A6 (comparison & selection rules) | FR-08…FR-11 (quotation compare/select), BR rules in [07-functional-requirements.md](07-functional-requirements.md) |
| A7–A8, B (approvals, rejections) | UC-04 PR approval FRs; conflict log (doc 14) |
| C3–C7, C10–C12 | NFR usability/accuracy targets (doc 08) |
| C8, C9 | MoSCoW priority evidence (doc 13) |
| B1–B6 | Tax/withholding business rules & UC-06/UC-07 FRs |
| Data on every form | Data dictionary (doc 10) |
