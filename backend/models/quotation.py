from config.db import db
from datetime import datetime
import uuid

class Quotation(db.Model):
    """UC-02: Submission of Quotation by vendors"""
    __tablename__ = 'quotations'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String, db.ForeignKey('orders.id'), nullable=False)
    vendor_id = db.Column(db.String, db.ForeignKey('vendors.id'), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    delivery_days = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    status = db.Column(db.String, default='submitted')  # submitted, under_review, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
