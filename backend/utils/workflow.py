from config.db import db
from models.purchase_requisition import PurchaseRequisition
from models.purchase_order import PurchaseOrder
from models.warehouse_item import WarehouseItem
from models.account import AccountEntry
import json
import uuid


def process_pr_full(pr_id):
    """Process a PR through the full automated workflow:
    - create PO from PR
    - mark PR.status='po_created'
    - mark PO as received and add warehouse items
    - mark inspection pass
    - create invoice and mark it paid
    Returns a summary dict.
    """
    summary = {'steps': []}
    pr = PurchaseRequisition.query.get(pr_id)
    if not pr:
        summary['error'] = 'PR not found'
        return summary
    # create PO
    items = [{
        'sku': getattr(pr, 'item', None),
        'name': getattr(pr, 'item', None),
        'qty': getattr(pr, 'qty', 1)
    }]
    po = PurchaseOrder(vendor_id=None, items=json.dumps(items), total=0.0)
    db.session.add(po)
    # update PR
    pr.status = 'po_created'
    db.session.commit()
    summary['steps'].append({'po_created': po.id})

    # receive PO: mark received and add items
    po.status = 'received'
    try:
        parsed = json.loads(po.items) if po.items else []
    except Exception:
        parsed = []
    for it in parsed:
        sku = it.get('sku') if isinstance(it, dict) else None
        name = it.get('name') if isinstance(it, dict) else str(it)
        qty = int(it.get('qty', 1)) if isinstance(it, dict) else 1
        if sku:
            existing = WarehouseItem.query.filter_by(sku=sku).first()
            if existing:
                existing.qty = (existing.qty or 0) + qty
            else:
                w = WarehouseItem(sku=sku, name=name, qty=qty)
                db.session.add(w)
    db.session.commit()
    summary['steps'].append({'po_received': po.id})

    # inspection pass
    po.inspection = 'pass'
    # create invoice/account entry
    amt = float(po.total or 0.0)
    a = AccountEntry(po_id=po.id, amount=amt, status='paid')
    db.session.add(a)
    db.session.commit()
    summary['steps'].append({'inspection': 'pass', 'invoice_id': a.id})

    # mark payment completed (already set to paid)
    summary['steps'].append({'payment': 'completed', 'account_id': a.id})
    return summary
