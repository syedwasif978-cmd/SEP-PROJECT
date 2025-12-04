from config.db import db
import uuid, datetime

class PRApproval(db.Model):
    __tablename__ = 'pr_approvals'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pr_id = db.Column(db.String, db.ForeignKey('purchase_requisitions.id'))
    approver = db.Column(db.String)
    status = db.Column(db.String)
    comments = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
