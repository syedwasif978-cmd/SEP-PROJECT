from config.db import db
from datetime import datetime
import uuid

class AccountEntry(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    po_id = db.Column(db.String, db.ForeignKey('purchase_orders.id'))
    amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String, default='pending')  # pending, paid
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
