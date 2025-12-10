from flask import Blueprint, request, jsonify
from config.db import db
from models.purchase_order import PurchaseOrder
from utils.helpers import to_dict
import json

po_bp = Blueprint('po', __name__)


@po_bp.route('/', methods=['GET'])
def list_pos():
    pos = PurchaseOrder.query.order_by(PurchaseOrder.created_at.desc()).all()
    return jsonify([to_dict(p) for p in pos])


@po_bp.route('/', methods=['POST'])
def create_po():
    data = request.get_json() or {}
    vendor_id = data.get('vendor_id')
    items = data.get('items', [])
    total = data.get('total', 0.0)
    if not vendor_id:
        return jsonify({'error': 'vendor_id required'}), 400
    po = PurchaseOrder(vendor_id=vendor_id, items=json.dumps(items), total=total)
    db.session.add(po); db.session.commit()
    return jsonify(to_dict(po)), 201


@po_bp.route('/<string:po_id>', methods=['GET'])
def get_po(po_id):
    po = PurchaseOrder.query.get(po_id)
    if not po:
        return jsonify({'error': 'not found'}), 404
    return jsonify(to_dict(po))


@po_bp.route('/<string:po_id>/receive', methods=['POST'])
def receive_po(po_id):
    """Mark PO as received and add items to warehouse."""
    try:
        po = PurchaseOrder.query.get(po_id)
        if not po:
            return jsonify({'error': 'not found'}), 404
        # mark received
        po.status = 'received'
        # add items to warehouse
        try:
            items = json.loads(po.items) if po.items else []
        except Exception:
            items = []
        from models.warehouse_item import WarehouseItem
        for it in items:
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
        return jsonify({'status': 'received', 'po_id': po_id, 'message': 'PO received — items transferred to Warehouse'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@po_bp.route('/<string:po_id>/inspect', methods=['POST'])
def inspect_po(po_id):
    """Set inspection result for a PO. If passed, create invoice (account entry)."""
    try:
        data = request.get_json() or {}
        result = data.get('result')  # 'pass' or 'fail'
        notes = data.get('notes')
        po = PurchaseOrder.query.get(po_id)
        if not po:
            return jsonify({'error': 'not found'}), 404
        po.inspection = result
        if result == 'pass':
            # create account invoice entry
            from models.account import AccountEntry
            amt = float(po.total or 0.0)
            a = AccountEntry(po_id=po.id, amount=amt, status='pending')
            db.session.add(a)
            msg = 'Inspection passed — invoice created and forwarded to Accounts'
        else:
            msg = 'Inspection failed — items flagged and vendor notified'
        db.session.commit()
        return jsonify({'po_id': po_id, 'inspection': result, 'message': msg})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@po_bp.route('/<string:po_id>/invoice', methods=['POST'])
def create_invoice_for_po(po_id):
    """Create an invoice/account entry for a PO explicitly."""
    try:
        po = PurchaseOrder.query.get(po_id)
        if not po:
            return jsonify({'error': 'not found'}), 404
        from models.account import AccountEntry
        amt = float(po.total or 0.0)
        a = AccountEntry(po_id=po.id, amount=amt, status='pending')
        db.session.add(a)
        db.session.commit()
        return jsonify({'invoice': to_dict(a), 'message': 'Invoice created — sent to Accounts for payment'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@po_bp.route('/<string:po_id>', methods=['PUT'])
def update_po(po_id):
    po = PurchaseOrder.query.get(po_id)
    if not po:
        return jsonify({'error': 'not found'}), 404
    data = request.get_json() or {}
    po.vendor_id = data.get('vendor_id', po.vendor_id)
    items = data.get('items')
    if items is not None:
        import json as _json
        po.items = _json.dumps(items)
    po.total = data.get('total', po.total)
    db.session.commit()
    return jsonify(to_dict(po))


@po_bp.route('/<string:po_id>', methods=['DELETE'])
def delete_po(po_id):
    po = PurchaseOrder.query.get(po_id)
    if not po:
        return jsonify({'error': 'not found'}), 404
    try:
        db.session.delete(po)
        db.session.commit()
        return jsonify({'deleted': po_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
