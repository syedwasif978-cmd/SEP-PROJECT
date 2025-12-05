from flask import Blueprint, request, jsonify
from config.db import db
from models.warehouse_item import WarehouseItem
from utils.helpers import to_dict

warehouse_bp = Blueprint('warehouse', __name__)


@warehouse_bp.route('/items', methods=['GET'])
def list_items():
    """Get all warehouse items."""
    try:
        items = WarehouseItem.query.all()
        return jsonify([to_dict(i) for i in items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@warehouse_bp.route('/items', methods=['POST'])
def create_item():
    """Create a warehouse item."""
    try:
        data = request.get_json() or {}
        sku = data.get('sku')
        name = data.get('name')
        qty = data.get('qty', 0)
        if not sku or not name:
            return jsonify({'error': 'sku and name required'}), 400
        item = WarehouseItem(sku=sku, name=name, qty=qty)
        db.session.add(item)
        db.session.commit()
        return jsonify(to_dict(item)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@warehouse_bp.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        it = WarehouseItem.query.get(item_id)
        if not it:
            return jsonify({'error': 'not found'}), 404
        return jsonify(to_dict(it))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@warehouse_bp.route('/items/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        it = WarehouseItem.query.get(item_id)
        if not it:
            return jsonify({'error': 'not found'}), 404
        data = request.get_json() or {}
        it.sku = data.get('sku', it.sku)
        it.name = data.get('name', it.name)
        it.qty = data.get('qty', it.qty)
        db.session.commit()
        return jsonify(to_dict(it))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@warehouse_bp.route('/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        it = WarehouseItem.query.get(item_id)
        if not it:
            return jsonify({'error': 'not found'}), 404
        db.session.delete(it)
        db.session.commit()
        return jsonify({'deleted': item_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
