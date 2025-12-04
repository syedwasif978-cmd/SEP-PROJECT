from config.db import db
import uuid

class WarehouseItem(db.Model):
    __tablename__ = 'warehouse_items'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sku = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    qty = db.Column(db.Integer, default=0)
