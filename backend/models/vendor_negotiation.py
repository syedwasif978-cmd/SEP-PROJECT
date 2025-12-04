from config.db import db
from datetime import datetime
import uuid

class VendorNegotiation(db.Model):
    __tablename__ = 'vendor_negotiations'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    vendor_id = db.Column(db.String, db.ForeignKey('vendors.id'))
    note = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
