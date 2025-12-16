from config.db import db
from datetime import datetime
import uuid

class TaxRecord(db.Model):
    """UC-06 & UC-07: Cost and Withholding Tax Calculations"""
    __tablename__ = 'tax_records'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String, db.ForeignKey('orders.id'))
    invoice_id = db.Column(db.String, db.ForeignKey('invoices.id'))
    base_amount = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, default=0.0)  # percentage
    tax_amount = db.Column(db.Float, default=0.0)
    withholding_tax_rate = db.Column(db.Float, default=0.0)  # FBR withholding tax
    withholding_tax_amount = db.Column(db.Float, default=0.0)
    net_amount = db.Column(db.Float, default=0.0)
    calculation_type = db.Column(db.String)  # 'cost_calc', 'withholding_tax'
    status = db.Column(db.String, default='calculated')  # calculated, verified, recorded
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
