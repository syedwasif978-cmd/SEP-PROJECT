from config.db import db
from datetime import datetime
import uuid

class Order(db.Model):
    """UC-01: Client places order to Commercial Department"""
    __tablename__ = 'orders'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_name = db.Column(db.String, nullable=False)
    client_email = db.Column(db.String)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.String, default='placed')  # placed, submitted_to_commercial, quotation_requested
    total_budget = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
