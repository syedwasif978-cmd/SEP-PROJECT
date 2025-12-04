from config.db import db
import uuid

class TaxCalculation(db.Model):
    __tablename__ = 'tax_calculations'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = db.Column(db.Float)
    tax_amount = db.Column(db.Float)
