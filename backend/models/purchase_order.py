from config.db import db
from datetime import datetime
import uuid
import json

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    vendor_id = db.Column(db.String, db.ForeignKey('vendors.id'))
    items = db.Column(db.Text)  # JSON string
    total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String, default='created')  # created, sent, received
    inspection = db.Column(db.String, nullable=True)  # pass, fail, pending
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
