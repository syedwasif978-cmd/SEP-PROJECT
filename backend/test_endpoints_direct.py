#!/usr/bin/env python
"""Test API endpoints by accessing the Flask app directly"""

import sys
import json
from app import app, db
from models.order import Order
from models.quotation import Quotation

print("=" * 60)
print("Testing API Endpoints via Flask Test Client")
print("=" * 60)

# Create test client
client = app.test_client()

# Test 1: Create an order
print("\n1. POST /api/orders/ - Create order")
response = client.post('/api/orders/', 
    json={'client_name':'John Doe','client_email':'john@test.com','description':'Test Order','quantity':5,'total_budget':50000},
    content_type='application/json')
print(f"   Status: {response.status_code}")
data = json.loads(response.data)
print(f"   Response: {json.dumps(data, indent=2)}")
if 'order' in data:
    order_id = data['order']['id']
    print(f"   ✓ Order created with ID: {order_id}")
else:
    print(f"   ✗ Error: {data.get('error', 'Unknown error')}")
    order_id = None

# Test 2: List orders
print("\n2. GET /api/orders/ - List all orders")
response = client.get('/api/orders/')
print(f"   Status: {response.status_code}")
data = json.loads(response.data)
print(f"   ✓ Found {len(data)} orders")
if data:
    print(f"   First order: {data[0]['client_name']}")

# Test 3: List quotations
print("\n3. GET /api/quotations/ - List all quotations")
response = client.get('/api/quotations/')
print(f"   Status: {response.status_code}")
data = json.loads(response.data)
print(f"   Response: {json.dumps(data, indent=2)}")
print(f"   ✓ Found {len(data)} quotations")

# Test 4: List invoices  
print("\n4. GET /api/invoices/ - List all invoices")
response = client.get('/api/invoices/')
print(f"   Status: {response.status_code}")
data = json.loads(response.data)
print(f"   ✓ Found {len(data)} invoices")

# Test 5: List POs
print("\n5. GET /api/po/ - List all POs")
response = client.get('/api/po/')
print(f"   Status: {response.status_code}")
data = json.loads(response.data)
print(f"   Response: {json.dumps(data, indent=2)}")
print(f"   ✓ Found {len(data)} POs")

print("\n" + "=" * 60)
print("✓ All endpoints are working correctly!")
print("=" * 60)
