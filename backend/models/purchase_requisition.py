from config.db import db
from datetime import datetime
import uuid

class PurchaseRequisition(db.Model):
    __tablename__ = 'purchase_requisitions'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item = db.Column(db.String, nullable=False)
    qty = db.Column(db.Integer, default=1)
    requester = db.Column(db.String)
    status = db.Column(db.String, default='pending')  # pending, recommended, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
