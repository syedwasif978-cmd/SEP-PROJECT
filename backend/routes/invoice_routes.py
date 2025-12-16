from flask import Blueprint, request, jsonify
from config.db import db
from models.invoice import Invoice
from models.tax_record import TaxRecord
from utils.helpers import to_dict

invoice_bp = Blueprint('invoices', __name__)

@invoice_bp.route('/', methods=['POST'])
def create_invoice():
    """UC-08: Accounts generate invoice"""
    try:
        data = request.get_json() or {}
        # Generate invoice number (simple format: INV-{timestamp})
        import time
        invoice_number = f"INV-{int(time.time())}"
        
        invoice = Invoice(
            order_id=data.get('order_id'),
            po_id=data.get('po_id'),
            vendor_id=data.get('vendor_id'),
            delivery_challan=data.get('delivery_challan', ''),
            invoice_number=invoice_number,
            base_amount=float(data.get('base_amount', 0)),
            tax_amount=float(data.get('tax_amount', 0)),
            withholding_tax=float(data.get('withholding_tax', 0))
        )
        invoice.total_amount = invoice.base_amount + invoice.tax_amount - invoice.withholding_tax
        db.session.add(invoice)
        db.session.commit()
        return jsonify({
            'invoice': to_dict(invoice),
            'message': f'✓ Invoice {invoice_number} generated and forwarded to payment'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@invoice_bp.route('/', methods=['GET'])
def list_invoices():
    """Get all invoices"""
    try:
        invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
        return jsonify([to_dict(i) for i in invoices])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@invoice_bp.route('/<string:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """Get invoice details"""
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    return jsonify(to_dict(invoice))

@invoice_bp.route('/<string:invoice_id>/mark-paid', methods=['POST'])
def mark_invoice_paid(invoice_id):
    """Mark invoice as paid"""
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        invoice.payment_status = 'completed'
        from datetime import datetime
        invoice.payment_date = datetime.utcnow()
        invoice.status = 'paid'
        db.session.commit()
        return jsonify({
            'invoice': to_dict(invoice),
            'message': '✓ Invoice marked as paid. Transaction completed.'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@invoice_bp.route('/<string:invoice_id>/calculate-tax', methods=['POST'])
def calculate_invoice_tax(invoice_id):
    """UC-06 & UC-07: Calculate cost and withholding tax for invoice"""
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        data = request.get_json() or {}
        tax_rate = float(data.get('tax_rate', 0)) / 100  # convert percentage to decimal
        withholding_rate = float(data.get('withholding_rate', 0)) / 100
        
        # Calculate taxes
        tax_amount = invoice.base_amount * tax_rate
        withholding_amount = invoice.base_amount * withholding_rate
        
        invoice.tax_amount = tax_amount
        invoice.withholding_tax = withholding_amount
        invoice.total_amount = invoice.base_amount + tax_amount - withholding_amount
        
        # Create tax record
        tax_record = TaxRecord(
            invoice_id=invoice_id,
            order_id=invoice.order_id,
            base_amount=invoice.base_amount,
            tax_rate=tax_rate * 100,
            tax_amount=tax_amount,
            withholding_tax_rate=withholding_rate * 100,
            withholding_tax_amount=withholding_amount,
            net_amount=invoice.total_amount,
            calculation_type='cost_calc'
        )
        db.session.add(tax_record)
        db.session.commit()
        return jsonify({
            'invoice': to_dict(invoice),
            'message': '✓ Tax calculated and recorded'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
