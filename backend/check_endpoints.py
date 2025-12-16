#!/usr/bin/env python3
"""Check all API endpoints and test them"""
from app import app
from config.db import db

with app.app_context():
    print("\n" + "="*70)
    print("REGISTERED API ENDPOINTS")
    print("="*70)
    
    endpoints = {}
    for rule in app.url_map.iter_rules():
        if 'api' in rule.rule:
            methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
            if rule.rule not in endpoints:
                endpoints[rule.rule] = methods
    
    for endpoint in sorted(endpoints.keys()):
        print(f"{endpoints[endpoint]:8} {endpoint}")
    
    print("\n" + "="*70)
    print("TESTING ENDPOINTS")
    print("="*70)
    
    with app.test_client() as client:
        # Test Orders
        print("\n1. Test GET /api/orders/")
        response = client.get('/api/orders/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test Quotations
        print("\n2. Test GET /api/quotations/")
        response = client.get('/api/quotations/')
        print(f"   Status: {response.status_code}")
        
        # Test Invoices
        print("\n3. Test GET /api/invoices/")
        response = client.get('/api/invoices/')
        print(f"   Status: {response.status_code}")
        
        # Test Tax
        print("\n4. Test GET /api/tax/records")
        response = client.get('/api/tax/records')
        print(f"   Status: {response.status_code}")
        
        # Test PO
        print("\n5. Test GET /api/po/")
        response = client.get('/api/po/')
        print(f"   Status: {response.status_code}")
        
        print("\n" + "="*70)
