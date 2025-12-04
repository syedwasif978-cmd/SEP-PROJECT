from config.db import db
import uuid, datetime

class ClientConfirmation(db.Model):
    __tablename__ = 'client_confirmations'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    po_id = db.Column(db.String, db.ForeignKey('purchase_orders.id'))
    status = db.Column(db.String, default='delivered')  # delivered, confirmed
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
