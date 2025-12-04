from config.db import db
import uuid

class BankCharge(db.Model):
    __tablename__ = 'bank_charges'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String)
    amount = db.Column(db.Float)
