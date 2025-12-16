from config.db import db
from datetime import datetime
import uuid

class Invoice(db.Model):
    """UC-08: Invoice Bills Generation"""
    __tablename__ = 'invoices'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String, db.ForeignKey('orders.id'), nullable=False)
    po_id = db.Column(db.String, db.ForeignKey('purchase_orders.id'))
    vendor_id = db.Column(db.String, db.ForeignKey('vendors.id'), nullable=False)
    delivery_challan = db.Column(db.String)  # reference to delivery document
    invoice_number = db.Column(db.String, unique=True)
    base_amount = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, default=0.0)
    withholding_tax = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, default='generated')  # generated, verified, approved, paid
    payment_status = db.Column(db.String, default='pending')  # pending, partial, completed
    payment_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
