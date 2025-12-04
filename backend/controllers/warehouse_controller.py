from models.warehouse_item import WarehouseItem
from config.db import db

def list_items():
    return WarehouseItem.query.all()
