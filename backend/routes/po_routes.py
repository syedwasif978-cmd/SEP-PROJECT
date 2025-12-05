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
