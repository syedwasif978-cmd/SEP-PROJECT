from flask import Blueprint, request, jsonify
from config.db import db
from models.vendor_negotiation import VendorNegotiation
from utils.helpers import to_dict

negotiation_bp = Blueprint('negotiation', __name__)


@negotiation_bp.route('/', methods=['GET'])
def list_negotiations():
    """Get all negotiations."""
    try:
        items = VendorNegotiation.query.order_by(VendorNegotiation.created_at.desc()).all()
        return jsonify([to_dict(i) for i in items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@negotiation_bp.route('/', methods=['POST'])
def create_negotiation():
    """Create a new negotiation."""
    try:
        data = request.get_json() or {}
        vendor_id = data.get('vendor_id')
        if not vendor_id:
            return jsonify({'error': 'vendor_id is required'}), 400
        n = VendorNegotiation(vendor_id=vendor_id, note=data.get('note'))
        db.session.add(n)
        db.session.commit()
        return jsonify(to_dict(n)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@negotiation_bp.route('/<string:vendor_id>', methods=['POST'])
def create_negotiation_for_vendor(vendor_id):
    """Create a negotiation for a specific vendor."""
    try:
        data = request.get_json() or {}
        n = VendorNegotiation(vendor_id=vendor_id, note=data.get('note', 'Initial negotiation'))
        db.session.add(n)
        db.session.commit()
        return jsonify(to_dict(n)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@negotiation_bp.route('/<string:neg_id>', methods=['GET'])
def get_negotiation(neg_id):
    try:
        n = VendorNegotiation.query.get(neg_id)
        if not n:
            return jsonify({'error': 'not found'}), 404
        return jsonify(to_dict(n))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@negotiation_bp.route('/<string:neg_id>', methods=['PUT'])
def update_negotiation(neg_id):
    try:
        n = VendorNegotiation.query.get(neg_id)
        if not n:
            return jsonify({'error': 'not found'}), 404
        data = request.get_json() or {}
        n.note = data.get('note', n.note)
        db.session.commit()
        return jsonify(to_dict(n))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@negotiation_bp.route('/<string:neg_id>', methods=['DELETE'])
def delete_negotiation(neg_id):
    try:
        n = VendorNegotiation.query.get(neg_id)
        if not n:
            return jsonify({'error': 'not found'}), 404
        db.session.delete(n)
        db.session.commit()
        return jsonify({'deleted': neg_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
