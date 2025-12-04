from config.db import db
import uuid, datetime

class CommercialApproval(db.Model):
    __tablename__ = 'commercial_approvals'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pr_id = db.Column(db.String, db.ForeignKey('purchase_requisitions.id'))
    approver = db.Column(db.String)
    decision = db.Column(db.String)  # approved/rejected
    comments = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
