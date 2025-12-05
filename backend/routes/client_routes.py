from flask import Blueprint, request, jsonify
from config.db import db
from models.client_confirmation import ClientConfirmation
from utils.helpers import to_dict

client_bp = Blueprint('client', __name__)


@client_bp.route('/', methods=['GET'])
def list_confirmations():
    """Get all client confirmations."""
    try:
        items = ClientConfirmation.query.order_by(ClientConfirmation.created_at.desc()).all()
        return jsonify([to_dict(i) for i in items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@client_bp.route('/confirmations', methods=['GET'])
def list_confirmations_alias():
    """Alias endpoint for /confirmations (to support frontend)."""
    try:
        items = ClientConfirmation.query.order_by(ClientConfirmation.created_at.desc()).all()
        return jsonify([to_dict(i) for i in items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@client_bp.route('/', methods=['POST'])
def create_confirmation():
    """Create a client confirmation record."""
    try:
        data = request.get_json() or {}
        po_id = data.get('po_id')
        if not po_id:
            return jsonify({'error': 'po_id required'}), 400
        c = ClientConfirmation(po_id=po_id, status=data.get('status', 'delivered'))
        db.session.add(c)
        db.session.commit()
        return jsonify(to_dict(c)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@client_bp.route('/<string:confirmation_id>/confirm', methods=['POST'])
def confirm_delivery(confirmation_id):
    """Mark a delivery as confirmed by client."""
    try:
        c = ClientConfirmation.query.get(confirmation_id)
        if not c:
            return jsonify({'error': 'not found'}), 404
        c.status = 'confirmed'
        db.session.commit()
        return jsonify(to_dict(c))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@client_bp.route('/<string:confirmation_id>', methods=['GET'])
def get_confirmation(confirmation_id):
    try:
        c = ClientConfirmation.query.get(confirmation_id)
        if not c:
            return jsonify({'error': 'not found'}), 404
        return jsonify(to_dict(c))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@client_bp.route('/<string:confirmation_id>', methods=['PUT'])
def update_confirmation(confirmation_id):
    try:
        c = ClientConfirmation.query.get(confirmation_id)
        if not c:
            return jsonify({'error': 'not found'}), 404
        data = request.get_json() or {}
        c.status = data.get('status', c.status)
        c.po_id = data.get('po_id', c.po_id)
        db.session.commit()
        return jsonify(to_dict(c))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@client_bp.route('/<string:confirmation_id>', methods=['DELETE'])
def delete_confirmation(confirmation_id):
    try:
        c = ClientConfirmation.query.get(confirmation_id)
        if not c:
            return jsonify({'error': 'not found'}), 404
        db.session.delete(c)
        db.session.commit()
        return jsonify({'deleted': confirmation_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
