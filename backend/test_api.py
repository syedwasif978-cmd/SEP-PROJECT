import requests
import json

print("=" * 50)
print("Testing API Endpoints")
print("=" * 50)

# Test 1: Create an order
print("\n1. POST /api/orders/ - Create order")
resp = requests.post('http://127.0.0.1:5000/api/orders/', 
    json={'client_name':'John Doe','client_email':'john@test.com','description':'Test Order','quantity':5,'total_budget':50000})
print(f"   Status: {resp.status_code}")
order_data = resp.json()
print(f"   Response: {json.dumps(order_data, indent=2)}")
order_id = order_data.get('order', {}).get('id') if 'order' in order_data else None
print(f"   Order ID: {order_id}")

# Test 2: List orders
print("\n2. GET /api/orders/ - List all orders")
resp = requests.get('http://127.0.0.1:5000/api/orders/')
print(f"   Status: {resp.status_code}")
print(f"   Found {len(resp.json())} orders")

# Test 3: List quotations
print("\n3. GET /api/quotations/ - List all quotations")
resp = requests.get('http://127.0.0.1:5000/api/quotations/')
print(f"   Status: {resp.status_code}")
print(f"   Response: {json.dumps(resp.json(), indent=2)}")

# Test 4: List invoices
print("\n4. GET /api/invoices/ - List all invoices")
resp = requests.get('http://127.0.0.1:5000/api/invoices/')
print(f"   Status: {resp.status_code}")
print(f"   Response: {json.dumps(resp.json(), indent=2)}")

# Test 5: List POs
print("\n5. GET /api/po/ - List all POs")
resp = requests.get('http://127.0.0.1:5000/api/po/')
print(f"   Status: {resp.status_code}")
print(f"   Response: {json.dumps(resp.json(), indent=2)}")

print("\n" + "=" * 50)
print("✓ All endpoints are responding!")
print("=" * 50)
