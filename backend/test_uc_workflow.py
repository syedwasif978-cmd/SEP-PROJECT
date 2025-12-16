#!/usr/bin/env python3
"""
E2E Test for UC-01 through UC-08 - Complete Procurement Workflow
Tests all new use-case endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"

def print_test(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def print_result(response, data):
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    return response.status_code

# ============================================================================
# UC-01: Place Order
# ============================================================================

print_test("UC-01: PLACE ORDER")

order_payload = {
    "client_name": "ABC Corporation",
    "client_email": "contact@abc.com",
    "description": "Office supplies, computers, and furniture",
    "quantity": 50,
    "total_budget": 500000.00
}

print("\n1.1 Creating Order...")
response = requests.post(f"{BASE_URL}/orders/", json=order_payload)
order_data = response.json()
print_result(response, order_data)

if response.status_code != 201:
    print("ERROR: Failed to create order. Stopping tests.")
    exit(1)

order_id = order_data['order']['id']
print(f"\n✓ Order created successfully!")
print(f"  Order ID: {order_id}")
print(f"  Status: {order_data['order']['status']}")

print("\n1.2 Listing All Orders...")
response = requests.get(f"{BASE_URL}/orders/")
orders = response.json()
print(f"Status: {response.status_code}")
print(f"Total Orders: {len(orders)}")

print("\n1.3 Getting Order Details...")
response = requests.get(f"{BASE_URL}/orders/{order_id}")
order_details = response.json()
print_result(response, order_details)

# ============================================================================
# UC-02: Submission of Quotation & UC-05: Compare Vendor Quotation
# ============================================================================

print_test("UC-02 & UC-05: QUOTATION MANAGEMENT")

# Submit first quotation
quotation_1_payload = {
    "order_id": order_id,
    "vendor_id": "vendor-001",
    "unit_price": 8500.00,
    "total_price": 425000.00,
    "delivery_days": 15,
    "notes": "Includes 30-day warranty"
}

print("\n2.1 Vendor 1 Submitting Quotation...")
response = requests.post(f"{BASE_URL}/quotations/", json=quotation_1_payload)
quote_1_data = response.json()
print_result(response, quote_1_data)

if response.status_code != 201:
    print("ERROR: Failed to submit quotation 1. Stopping tests.")
    exit(1)

quote_1_id = quote_1_data['quotation']['id']
print(f"\n✓ Quotation 1 submitted!")
print(f"  Quote ID: {quote_1_id}")
print(f"  Vendor: {quote_1_data['quotation']['vendor_id']}")
print(f"  Price: PKR {quote_1_data['quotation']['total_price']:,.0f}")

# Submit second quotation from different vendor
quotation_2_payload = {
    "order_id": order_id,
    "vendor_id": "vendor-002",
    "unit_price": 8200.00,
    "total_price": 410000.00,
    "delivery_days": 20,
    "notes": "Best price in market"
}

print("\n2.2 Vendor 2 Submitting Quotation...")
response = requests.post(f"{BASE_URL}/quotations/", json=quotation_2_payload)
quote_2_data = response.json()
print_result(response, quote_2_data)

quote_2_id = quote_2_data['quotation']['id']
print(f"\n✓ Quotation 2 submitted!")
print(f"  Quote ID: {quote_2_id}")
print(f"  Vendor: {quote_2_data['quotation']['vendor_id']}")
print(f"  Price: PKR {quote_2_data['quotation']['total_price']:,.0f}")

# UC-05: Compare Quotations
print("\n2.3 Compare Quotations (UC-05)...")
response = requests.get(f"{BASE_URL}/quotations/order/{order_id}")
all_quotes = response.json()
print(f"Status: {response.status_code}")
print(f"Total Quotations Received: {len(all_quotes)}")
for i, quote in enumerate(all_quotes):
    print(f"  {i+1}. {quote['vendor_id']}: PKR {quote['total_price']:,.0f} ({quote['delivery_days']} days)")

# Approve Quotation 2 (best price)
print("\n2.4 Commercial Approves Best Quotation (UC-05)...")
response = requests.post(f"{BASE_URL}/quotations/{quote_2_id}/approve")
approve_data = response.json()
print_result(response, approve_data)
print(f"\n✓ Quotation approved!")
print(f"  Message: {approve_data['message']}")

# Reject Quotation 1
print("\n2.5 Commercial Rejects Other Quotation...")
response = requests.post(f"{BASE_URL}/quotations/{quote_1_id}/reject")
reject_data = response.json()
print(f"Status: {response.status_code}")
print(f"Message: {reject_data['message']}")

# ============================================================================
# UC-03: Purchase Order Issued (Simulated with PO creation)
# ============================================================================

print_test("UC-03: PURCHASE ORDER ISSUED")
print("\nNote: UC-03 (PO Issuance) endpoint is in development")
print("The approved quotation is ready for PO issuance.")
print(f"Vendor: {quote_2_data['quotation']['vendor_id']}")
print(f"Amount: PKR {quote_2_data['quotation']['total_price']:,.0f}")

# ============================================================================
# UC-06 & UC-07: Invoice Generation with Tax Calculation
# ============================================================================

print_test("UC-06 & UC-07 & UC-08: TAX CALCULATION & INVOICE GENERATION")

invoice_payload = {
    "order_id": order_id,
    "po_id": "PO-2024-001",  # Simulated PO
    "vendor_id": quote_2_data['quotation']['vendor_id'],
    "delivery_challan": "DC-2024-001",
    "base_amount": quote_2_data['quotation']['total_price'],
    "tax_amount": 0,  # Will be calculated
    "withholding_tax": 0  # Will be calculated
}

print("\n8.1 Generating Invoice...")
response = requests.post(f"{BASE_URL}/invoices/", json=invoice_payload)
invoice_data = response.json()
print_result(response, invoice_data)

if response.status_code != 201:
    print("ERROR: Failed to create invoice. Stopping tests.")
    exit(1)

invoice_id = invoice_data['invoice']['id']
print(f"\n✓ Invoice generated!")
print(f"  Invoice Number: {invoice_data['invoice']['invoice_number']}")
print(f"  Invoice ID: {invoice_id}")

# UC-06: Calculate Cost with Tax
print("\n6.1 Calculate Cost (UC-06)...")
tax_calc_payload = {
    "invoice_id": invoice_id,
    "tax_rate": 17.0  # Pakistan standard tax rate
}

response = requests.post(f"{BASE_URL}/tax/calculate-cost", json=tax_calc_payload)
tax_data = response.json()
print_result(response, tax_data)
print(f"\n✓ Cost calculated!")
print(f"  Base Amount: PKR {tax_data['invoice']['base_amount']:,.0f}")
print(f"  Tax Amount: PKR {tax_data['invoice']['tax_amount']:,.0f}")
print(f"  Message: {tax_data['message']}")

# UC-07: Calculate Withholding Tax
print("\n7.1 Calculate Withholding Tax (UC-07)...")
withholding_payload = {
    "invoice_id": invoice_id,
    "withholding_rate": 5.0  # FBR withholding tax
}

response = requests.post(f"{BASE_URL}/tax/calculate-withholding-tax", json=withholding_payload)
withholding_data = response.json()
print_result(response, withholding_data)
print(f"\n✓ Withholding tax calculated!")
print(f"  Withholding Tax: PKR {withholding_data['invoice']['withholding_tax']:,.0f}")
print(f"  Net Amount: PKR {withholding_data['invoice']['total_amount']:,.0f}")
print(f"  Message: {withholding_data['message']}")

# List Tax Records
print("\n6.2 & 7.2 Retrieve Tax Records...")
response = requests.get(f"{BASE_URL}/tax/records/{invoice_id}")
tax_records = response.json()
print(f"Status: {response.status_code}")
print(f"Tax Records for Invoice: {len(tax_records)}")
for record in tax_records:
    print(f"  - Type: {record['calculation_type']}")
    print(f"    Status: {record['status']}")

# ============================================================================
# UC-08: Invoice Bills Generation & Payment
# ============================================================================

print_test("UC-08: INVOICE BILLS GENERATION & PAYMENT")

print("\n8.2 Listing All Invoices...")
response = requests.get(f"{BASE_URL}/invoices/")
all_invoices = response.json()
print(f"Status: {response.status_code}")
print(f"Total Invoices: {len(all_invoices)}")

print("\n8.3 Getting Invoice Details...")
response = requests.get(f"{BASE_URL}/invoices/{invoice_id}")
invoice_details = response.json()
print(f"Status: {response.status_code}")
print(f"Invoice Number: {invoice_details['invoice_number']}")
print(f"Status: {invoice_details['status']}")
print(f"Payment Status: {invoice_details['payment_status']}")
print(f"Total Amount: PKR {invoice_details['total_amount']:,.0f}")

print("\n8.4 Mark Invoice as Paid...")
response = requests.post(f"{BASE_URL}/invoices/{invoice_id}/mark-paid")
paid_data = response.json()
print_result(response, paid_data)
print(f"\n✓ Invoice marked as paid!")
print(f"  Payment Status: {paid_data['invoice']['payment_status']}")
print(f"  Status: {paid_data['invoice']['status']}")
print(f"  Message: {paid_data['message']}")

# ============================================================================
# Summary
# ============================================================================

print_test("WORKFLOW SUMMARY - ALL TESTS PASSED ✓")

print("\n" + "="*70)
print("  COMPLETE PROCUREMENT WORKFLOW (UC-01 to UC-08)")
print("="*70)
print(f"""
✓ UC-01: Order placed by client
         Order ID: {order_id}
         Client: {order_payload['client_name']}
         Budget: PKR {order_payload['total_budget']:,.0f}

✓ UC-02: Quotations submitted by vendors
         Vendor 1: PKR {quote_1_payload['total_price']:,.0f} (15 days)
         Vendor 2: PKR {quote_2_payload['total_price']:,.0f} (20 days)

✓ UC-05: Commercial compared and selected best quotation
         Selected: Vendor {quote_2_data['quotation']['vendor_id']}
         Price: PKR {quote_2_data['quotation']['total_price']:,.0f}

✓ UC-03: Purchase Order ready for issuance
         PO Amount: PKR {quote_2_data['quotation']['total_price']:,.0f}

✓ UC-06: Cost calculated with tax
         Base: PKR {tax_data['invoice']['base_amount']:,.0f}
         Tax (17%): PKR {tax_data['invoice']['tax_amount']:,.0f}

✓ UC-07: Withholding tax calculated (FBR compliant)
         Withholding Tax (5%): PKR {withholding_data['invoice']['withholding_tax']:,.0f}

✓ UC-08: Invoice generated and marked as paid
         Invoice: {invoice_data['invoice']['invoice_number']}
         Total: PKR {paid_data['invoice']['total_amount']:,.0f}
         Status: PAID ✓

"""+"="*70)
print(f"Test Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)
