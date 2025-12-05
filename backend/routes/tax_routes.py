from flask import Blueprint, request, jsonify
from config.db import db
from models.tax_calculation import TaxCalculation
from utils.helpers import to_dict

tax_bp = Blueprint('tax', __name__)


@tax_bp.route('/', methods=['GET'])
def list_tax():
    """Get all tax calculations."""
    try:
        items = TaxCalculation.query.all()
        return jsonify([to_dict(i) for i in items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tax_bp.route('/', methods=['POST'])
def calculate_tax():
    """Calculate tax on an amount."""
    try:
        data = request.get_json() or {}
        amount = data.get('amount')
        if amount is None:
            return jsonify({'error': 'amount required'}), 400
        # Simple tax calculation: 10% of amount
        tax_amount = round(float(amount) * 0.10, 2)
        t = TaxCalculation(amount=float(amount), tax_amount=tax_amount)
        db.session.add(t)
        db.session.commit()
        return jsonify(to_dict(t)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@tax_bp.route('/calc', methods=['POST'])
def calculate_tax_alias():
    """Alias endpoint for /calc (to support frontend)."""
    try:
        data = request.get_json() or {}
        amount = data.get('amount')
        if amount is None:
            return jsonify({'error': 'amount required'}), 400
        tax_amount = round(float(amount) * 0.10, 2)
        total_with_tax = round(float(amount) + tax_amount, 2)
        return jsonify({'amount': float(amount), 'tax_amount': tax_amount, 'total': total_with_tax})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tax_bp.route('/<string:tax_id>', methods=['GET'])
def get_tax(tax_id):
    try:
        t = TaxCalculation.query.get(tax_id)
        if not t:
            return jsonify({'error': 'not found'}), 404
        return jsonify(to_dict(t))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tax_bp.route('/<string:tax_id>', methods=['DELETE'])
def delete_tax(tax_id):
    try:
        t = TaxCalculation.query.get(tax_id)
        if not t:
            return jsonify({'error': 'not found'}), 404
        db.session.delete(t)
        db.session.commit()
        return jsonify({'deleted': tax_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
