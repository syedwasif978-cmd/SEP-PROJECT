from models.purchase_order import PurchaseOrder
from config.db import db
import json

def create_po(vendor_id, items):
    po = PurchaseOrder(vendor_id=vendor_id, items=json.dumps(items), total=sum(i.get('price',0)*i.get('qty',1) for i in items))
    db.session.add(po); db.session.commit()
    return po
