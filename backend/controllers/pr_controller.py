from models.purchase_requisition import PurchaseRequisition
from config.db import db

def list_prs():
    return PurchaseRequisition.query.all()

def create_pr(item, qty, requester):
    pr = PurchaseRequisition(item=item, qty=qty, requester=requester)
    db.session.add(pr); db.session.commit()
    return pr
