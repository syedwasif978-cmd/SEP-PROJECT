from flask import Blueprint, request, jsonify
from config.db import db
from models.quotation import Quotation
from models.order import Order
from utils.helpers import to_dict

quotation_bp = Blueprint('quotations', __name__)

@quotation_bp.route('/', methods=['POST'])
def submit_quotation():
    """UC-02: Vendor submits quotation"""
    try:
        data = request.get_json() or {}
        quotation = Quotation(
            order_id=data.get('order_id'),
            vendor_id=data.get('vendor_id'),
            unit_price=float(data.get('unit_price', 0)),
            total_price=float(data.get('total_price', 0)),
            delivery_days=data.get('delivery_days', 0),
            notes=data.get('notes', '')
        )
        db.session.add(quotation)
        # Update order status
        order = Order.query.get(data.get('order_id'))
        if order:
            order.status = 'quotation_requested'
        db.session.commit()
        return jsonify({
            'quotation': to_dict(quotation),
            'message': '✓ Quotation submitted by vendor'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quotation_bp.route('/', methods=['GET'])
def list_quotations():
    """Get all quotations"""
    try:
        quotations = Quotation.query.order_by(Quotation.created_at.desc()).all()
        return jsonify([to_dict(q) for q in quotations])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quotation_bp.route('/order/<string:order_id>', methods=['GET'])
def get_order_quotations(order_id):
    """UC-05: Get all quotations for an order (for comparison)"""
    try:
        quotations = Quotation.query.filter_by(order_id=order_id).all()
        return jsonify([to_dict(q) for q in quotations])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quotation_bp.route('/<string:quotation_id>/approve', methods=['POST'])
def approve_quotation(quotation_id):
    """UC-05: Commercial approves quotation"""
    try:
        quotation = Quotation.query.get(quotation_id)
        if not quotation:
            return jsonify({'error': 'Quotation not found'}), 404
        quotation.status = 'approved'
        db.session.commit()
        return jsonify({
            'quotation': to_dict(quotation),
            'message': '✓ Quotation approved. Ready for PO issuance.'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quotation_bp.route('/<string:quotation_id>/reject', methods=['POST'])
def reject_quotation(quotation_id):
    """Reject a quotation"""
    try:
        quotation = Quotation.query.get(quotation_id)
        if not quotation:
            return jsonify({'error': 'Quotation not found'}), 404
        quotation.status = 'rejected'
        db.session.commit()
        return jsonify({
            'quotation': to_dict(quotation),
            'message': '✗ Quotation rejected.'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
