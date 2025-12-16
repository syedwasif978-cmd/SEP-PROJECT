# Procurement Workflow Visual Guide

## 🎯 The 8-Step Procurement Journey

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROCUREMENT MANAGEMENT SYSTEM                         │
│                         UC-01 through UC-08                              │
└─────────────────────────────────────────────────────────────────────────┘

STEP 1: PLACE ORDER (UC-01)
═══════════════════════════
┌──────────────────────┐
│   CLIENT            │
│                     │
│ Opens browser to:   │
│ /order.html         │
│                     │
│ Enters:             │
│ • Client name       │
│ • Email             │
│ • Order description │
│ • Quantity          │
│ • Budget            │
└──────────────────────┘
           │
           │ POST /api/orders/
           │
           ▼
┌──────────────────────┐
│   CREATE ORDER       │
│                     │
│ Order ID: uuid-123  │
│ Status: placed      │
│ ↓ submitted_to_     │
│   commercial        │
└──────────────────────┘


STEP 2: REQUEST QUOTATIONS (UC-02)
═══════════════════════════════════
┌──────────────────────┐     ┌──────────────┐
│   COMMERCIAL DEPT.   │────→│ Vendor List  │
│                     │     │ (email/call) │
│ Requests quotes from │     └──────────────┘
│ interested vendors   │
└──────────────────────┘
           ↑
           │
           └─ Data from Order


STEP 3: SUBMIT QUOTATIONS (UC-02)
══════════════════════════════════
Multiple Vendors Submit Bids:

VENDOR-001              VENDOR-002              VENDOR-003
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Unit Price:  │      │ Unit Price:  │      │ Unit Price:  │
│ PKR 8,500    │      │ PKR 8,200    │      │ PKR 8,800    │
│              │      │              │      │              │
│ Total:       │      │ Total:       │      │ Total:       │
│ PKR 425,000  │      │ PKR 410,000  │      │ PKR 440,000  │
│              │      │              │      │              │
│ Delivery:    │      │ Delivery:    │      │ Delivery:    │
│ 15 days      │      │ 20 days      │      │ 10 days      │
└──────────────┘      └──────────────┘      └──────────────┘
        │                     │                     │
        └─ POST /api/quotations/ ────────────────┘
                     │
                     ▼
           ┌──────────────────┐
           │  QUOTATIONS DB   │
           │  (stored & ready)│
           └──────────────────┘


STEP 4: COMPARE QUOTATIONS (UC-05)
═══════════════════════════════════
┌────────────────────────────────────────┐
│      COMMERCIAL COMPARISON PANEL       │
│                                        │
│  GET /api/quotations/order/{id}        │
│                                        │
│  ┌────────┐  ┌────────┐  ┌────────┐  │
│  │Vendor-1│  │Vendor-2│  │Vendor-3│  │
│  │        │  │        │  │        │  │
│  │PKR 425K│  │PKR 410K│◄─│PKR 440K│  │
│  │  15d   │  │  20d  ✓│  │  10d   │  │
│  │ Submit │  │Approve │  │ Submit │  │
│  └────────┘  └────────┘  └────────┘  │
│                  ▲                    │
│              SELECTED                 │
│           (Best Value)                │
└────────────────────────────────────────┘
        │
        └─ Approve ──→ POST /api/quotations/{id}/approve


STEP 5: ISSUE PURCHASE ORDER (UC-03)
════════════════════════════════════
┌──────────────────────────────┐
│   SELECTED VENDOR            │
│                             │
│   Vendor-002                │
│   PKR 410,000               │
│   Delivery: 20 days         │
│                             │
│   [ISSUE PO BUTTON]         │
│          ↓                  │
│   Status: PO Issued         │
│                             │
│   Warehouse receives        │
│   notification for delivery │
└──────────────────────────────┘


STEP 6: RECEIVE & INSPECT GOODS
═════════════════════════════════
┌──────────────────────────────┐
│   WAREHOUSE DEPARTMENT       │
│                             │
│   • Receives goods          │
│   • Checks against PO       │
│   • Records delivery challan│
│   • Updates system          │
│                             │
│   Status: Delivered         │
│                             │
│   Ready for invoice         │
└──────────────────────────────┘


STEP 7: CALCULATE COSTS & TAXES (UC-06 & UC-07)
════════════════════════════════════════════════
┌──────────────────────────────────────────────┐
│   TAX DEPARTMENT - COST CALCULATION          │
│   (UC-06: Cost | UC-07: Withholding Tax)    │
│                                             │
│   Base Amount:              PKR 410,000      │
│   ├─ Tax Rate: 17%          PKR 69,700      │
│   ├─ Withholding Rate: 5%   PKR 20,500      │
│   └─ Net Amount:            PKR 459,200     │
│                                             │
│   POST /api/tax/calculate-cost               │
│   POST /api/tax/calculate-withholding-tax    │
│                                             │
│   ✓ Tax records stored                       │
│   ✓ FBR compliant                            │
└──────────────────────────────────────────────┘


STEP 8: GENERATE INVOICE & PAYMENT (UC-08)
═══════════════════════════════════════════
┌──────────────────────────────────────────┐
│   ACCOUNTS DEPARTMENT                    │
│                                          │
│   Invoice Number: INV-1705315800         │
│   Date: 2024-01-15                       │
│                                          │
│   ┌────────────────────────────────────┐ │
│   │ Base Amount:    PKR 410,000        │ │
│   │ Tax (17%):      PKR 69,700         │ │
│   │ Withholding:    -PKR 20,500        │ │
│   │ ──────────────────────────────────│ │
│   │ Total Due:      PKR 459,200        │ │
│   └────────────────────────────────────┘ │
│                                          │
│   Status: Generated                      │
│   Payment: Pending                       │
│                                          │
│   POST /api/invoices/                    │
│   (Auto-create tax records)              │
│                                          │
│   [MARK AS PAID BUTTON]                  │
│          ↓                               │
│   Status: Paid                           │
│   Payment Date: [timestamp]              │
│   Payment Status: Completed              │
│                                          │
│   POST /api/invoices/{id}/mark-paid      │
│                                          │
│   ✓ WORKFLOW COMPLETE                    │
└──────────────────────────────────────────┘


═════════════════════════════════════════════════════════════════════════════
                              FULL WORKFLOW MAP
═════════════════════════════════════════════════════════════════════════════

┌──────────────┐
│ UC-01: Order │
└──────┬───────┘
       │ CREATE order
       ├─ Status: placed
       ├─ Status: submitted_to_commercial
       └─ Status: quotation_requested
              │
              ▼
┌──────────────────────┐
│ UC-02: Quotations    │
│ Request from Vendors │
└──────┬───────────────┘
       │ Multiple vendors
       │ POST /api/quotations/
       ├─ Status: submitted
       └─ Status: under_review
              │
              ▼
┌──────────────────────┐
│ UC-05: Compare       │
│ Select Best Quote    │
└──────┬───────────────┘
       │ GET /quotations/order/{id}
       │ Compare all vendor bids
       │ Select winner
       │ POST /approve
       └─ Status: approved
              │
              ▼
┌──────────────────────┐
│ UC-03: Issue PO      │
│ (In Development)     │
└──────┬───────────────┘
       │ Send to Warehouse
       │ Vendor notified
              │
              ▼
┌──────────────────────┐
│ Receive Goods        │
│ Delivery Challan     │
└──────┬───────────────┘
       │ Goods received
       │ Physical count
              │
              ▼
┌──────────────────────┐
│ UC-06: Cost Calc     │
│ Calculate Tax        │
└──────┬───────────────┘
       │ POST /tax/calculate-cost
       │ Apply tax rate (17%)
       │ Create tax record
              │
              ▼
┌──────────────────────┐
│ UC-07: Withholding   │
│ Calculate WHT        │
└──────┬───────────────┘
       │ POST /tax/calculate-withholding-tax
       │ Apply FBR rate (5%)
       │ Create tax record
       │ FBR Compliant ✓
              │
              ▼
┌──────────────────────┐
│ UC-08: Invoice       │
│ Generate Bill        │
└──────┬───────────────┘
       │ POST /api/invoices/
       │ Status: generated
       │ Payment: pending
              │
              ▼
┌──────────────────────┐
│ UC-08: Payment       │
│ Mark as Paid         │
└──────┬───────────────┘
       │ POST /mark-paid
       │ Status: paid
       │ Payment: completed
              │
              ▼
        ✓ WORKFLOW COMPLETE


═════════════════════════════════════════════════════════════════════════════
                              PAGE STRUCTURE
═════════════════════════════════════════════════════════════════════════════

DASHBOARD.HTML (Main Entry Point)
├─ Header (navigation)
├─ Sidebar (workflow links)
├─ Welcome Banner
├─ Quick Stats
│  ├─ Total Orders
│  ├─ Invoices Generated
│  ├─ Pending Quotations
│  └─ Awaiting Payment
├─ Workflow Grid (8 buttons)
│  ├─ 📝 Place Order (UC-01) → order.html
│  ├─ 💬 Quotation Management (UC-02, UC-05) → quotation.html
│  ├─ 📋 PO Issuance (UC-03) → Coming Soon
│  ├─ ✓ PR Approval (UC-04) → Legacy
│  ├─ ⚖️ Compare Quotes (UC-05) → quotation.html
│  ├─ 🧮 Calculate Cost (UC-06) → invoice.html
│  ├─ 🏛️ Withholding Tax (UC-07) → invoice.html
│  └─ 💵 Generate Invoice (UC-08) → invoice.html
└─ Recent Orders Table


ORDER.HTML (Place Order - UC-01)
├─ Workflow Indicator (Step 1 of 6)
├─ Client Information Section
│  ├─ Client Name
│  ├─ Email Address
├─ Order Details Section
│  ├─ Description
│  ├─ Quantity
│  └─ Total Budget
├─ Order Summary Panel
│  ├─ Items: [quantity]
│  └─ Budget: [amount]
└─ Submit Button


QUOTATION.HTML (UC-02, UC-05)
├─ Tab 1: Submit Quotation
│  ├─ Order ID (dropdown)
│  ├─ Order Details (auto-display)
│  ├─ Vendor ID
│  ├─ Unit Price
│  ├─ Total Price (auto-calculate)
│  ├─ Delivery Days
│  └─ Notes
├─ Tab 2: Compare Quotations
│  ├─ Order Selection
│  ├─ Quotation Cards Grid
│  │  ├─ Vendor Name & Status
│  │  ├─ Unit Price
│  │  ├─ Total Price (highlighted)
│  │  ├─ Delivery Days
│  │  ├─ Approve Button
│  │  └─ Reject Button
│  └─ Color-coded Status Badges
└─ Tab 3: History


INVOICE.HTML (UC-06, UC-07, UC-08)
├─ Tab 1: Generate Invoice
│  ├─ Order ID (dropdown)
│  ├─ PO ID (dropdown)
│  ├─ Vendor ID (auto-fill)
│  ├─ Delivery Challan
│  ├─ Base Amount
│  ├─ Tax Calculator Section
│  │  ├─ Tax Rate (%) [17]
│  │  ├─ Withholding Rate (%) [5]
│  │  ├─ Calculate Button
│  │  └─ Tax/Withholding fields (auto-fill)
│  ├─ Total Amount
│  └─ Generate Button
├─ Tab 2: Invoice List
│  └─ Invoice Cards Grid
│     ├─ Invoice Number & Status
│     ├─ Order & Vendor Info
│     ├─ Amount Breakdown
│     └─ Actions
└─ Tab 3: Payment Tracking
   └─ Unpaid Invoices
      └─ Mark as Paid Button


═════════════════════════════════════════════════════════════════════════════
                            API ENDPOINT SUMMARY
═════════════════════════════════════════════════════════════════════════════

ORDERS
  POST   /api/orders/                 Create order (UC-01)
  GET    /api/orders/                 List all orders
  GET    /api/orders/{id}             Get order details
  PUT    /api/orders/{id}             Update order status

QUOTATIONS
  POST   /api/quotations/             Submit quotation (UC-02)
  GET    /api/quotations/order/{id}   List by order (UC-05)
  POST   /api/quotations/{id}/approve Approve (UC-05)
  POST   /api/quotations/{id}/reject  Reject (UC-05)

INVOICES
  POST   /api/invoices/               Generate invoice (UC-08)
  GET    /api/invoices/               List invoices
  GET    /api/invoices/{id}           Get invoice details
  POST   /api/invoices/{id}/mark-paid Mark as paid (UC-08)

TAX
  POST   /api/tax/calculate-cost      Calculate cost tax (UC-06)
  POST   /api/tax/calculate-withholding-tax  Calculate withholding (UC-07)
  GET    /api/tax/records             List all tax records
  GET    /api/tax/records/{invoice_id} Get invoice tax records


═════════════════════════════════════════════════════════════════════════════
                         USER NOTIFICATION FLOW
═════════════════════════════════════════════════════════════════════════════

Action → API Request → Backend Processing → API Response → Toast Notification

✓ Success: Green toast, checkmark icon, auto-dismiss
✗ Error: Red toast, X icon, auto-dismiss
⚠ Warning: Yellow toast, warning icon, auto-dismiss
ℹ Info: Blue toast, info icon, auto-dismiss

Examples:
  ✓ "Order placed successfully. Submitted to Commercial Department."
  ✓ "Quotation approved. Ready for PO issuance."
  ✓ "Tax calculated. Withholding tax: PKR 21,250 (FBR compliant)"
  ✓ "Invoice marked as paid. Transaction completed."


═════════════════════════════════════════════════════════════════════════════
                              DATA FLOW SUMMARY
═════════════════════════════════════════════════════════════════════════════

FRONTEND                              BACKEND                      DATABASE
─────────────────────────────────────────────────────────────────────────────

User clicks
"Place Order"
    │
    ├─→ Form submission
         │
         └─→ POST /api/orders/
              │
              ├─→ Validate input
              ├─→ Create Order object
              ├─→ Save to DB ─────────→ INSERT INTO orders
              │
              ├─→ Set status: "placed"
              │
              ├─→ Return JSON response
              │   {order: {...}, message: "✓..."}
              │
              └─→ Parse response
                  Display toast
                  Reset form
                  Redirect to dashboard


Similar flow for all other endpoints (Quotations, Invoices, Tax Calculations)


═════════════════════════════════════════════════════════════════════════════
                           STATUS PROGRESSION MAP
═════════════════════════════════════════════════════════════════════════════

ORDER LIFECYCLE:
  placed → submitted_to_commercial → quotation_requested

QUOTATION LIFECYCLE:
  submitted → under_review → approved OR rejected

INVOICE LIFECYCLE:
  generated → verified → approved → paid

TAX_RECORD LIFECYCLE:
  calculated → verified → recorded

PAYMENT LIFECYCLE:
  pending → partial → completed


═════════════════════════════════════════════════════════════════════════════
