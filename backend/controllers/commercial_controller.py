from models.purchase_requisition import PurchaseRequisition
from config.db import db

def get_pending():
    return PurchaseRequisition.query.filter_by(status='pending').all()

def decision(pr_id, approve):
    pr = PurchaseRequisition.query.get(pr_id)
    if not pr: return False
    pr.status = 'approved' if approve else 'rejected'
    db.session.commit()
    return True
