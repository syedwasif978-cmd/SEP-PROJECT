from flask import Blueprint, request, jsonify
from config.db import db
from models.tax_record import TaxRecord
from models.invoice import Invoice
from utils.helpers import to_dict

tax_bp = Blueprint('taxes', __name__)

@tax_bp.route('/calculate-cost', methods=['POST'])
def calculate_cost():
    """UC-06: Cost Calculation (Tax Department → Accounts)"""
    try:
        data = request.get_json() or {}
        invoice_id = data.get('invoice_id')
        tax_rate = float(data.get('tax_rate', 0)) / 100  # percentage to decimal
        
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        # Calculate tax
        tax_amount = invoice.base_amount * tax_rate
        
        # Update invoice
        invoice.tax_amount = tax_amount
        invoice.total_amount = invoice.base_amount + tax_amount - invoice.withholding_tax
        
        # Record calculation
        tax_record = TaxRecord(
            invoice_id=invoice_id,
            order_id=invoice.order_id,
            base_amount=invoice.base_amount,
            tax_rate=tax_rate * 100,
            tax_amount=tax_amount,
            calculation_type='cost_calc'
        )
        db.session.add(tax_record)
        db.session.commit()
        return jsonify({
            'invoice': to_dict(invoice),
            'message': f'✓ Cost calculated. Tax: {tax_amount} applied'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tax_bp.route('/calculate-withholding-tax', methods=['POST'])
def calculate_withholding_tax():
    """UC-07: Withholding Tax Calculation (FBR Compliance)"""
    try:
        data = request.get_json() or {}
        invoice_id = data.get('invoice_id')
        withholding_rate = float(data.get('withholding_rate', 0)) / 100  # percentage to decimal
        
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        # Calculate withholding tax
        withholding_amount = invoice.base_amount * withholding_rate
        
        # Update invoice
        invoice.withholding_tax = withholding_amount
        invoice.total_amount = invoice.base_amount + invoice.tax_amount - withholding_amount
        
        # Record calculation
        tax_record = TaxRecord(
            invoice_id=invoice_id,
            order_id=invoice.order_id,
            base_amount=invoice.base_amount,
            withholding_tax_rate=withholding_rate * 100,
            withholding_tax_amount=withholding_amount,
            calculation_type='withholding_tax'
        )
        db.session.add(tax_record)
        db.session.commit()
        return jsonify({
            'invoice': to_dict(invoice),
            'message': f'✓ Withholding tax calculated: {withholding_amount} (FBR compliant)'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tax_bp.route('/records', methods=['GET'])
def get_tax_records():
    """Retrieve all tax records"""
    try:
        records = TaxRecord.query.order_by(TaxRecord.created_at.desc()).all()
        return jsonify([to_dict(r) for r in records])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tax_bp.route('/records/<string:invoice_id>', methods=['GET'])
def get_invoice_tax_records(invoice_id):
    """Get tax records for specific invoice"""
    try:
        records = TaxRecord.query.filter_by(invoice_id=invoice_id).all()
        return jsonify([to_dict(r) for r in records])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
