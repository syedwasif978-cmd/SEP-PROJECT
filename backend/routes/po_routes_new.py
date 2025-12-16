from flask import Blueprint, request, jsonify
from config.db import db
from models.quotation import Quotation
from models.order import Order
from utils.helpers import to_dict
import uuid
from datetime import datetime

po_bp_new = Blueprint('po_new', __name__)

# Simple in-memory PO storage for demo (ideally use database model)
pos_store = {}

@po_bp_new.route('/', methods=['POST'])
def issue_po():
    """UC-03: Issue Purchase Order from approved quotation"""
    try:
        data = request.get_json() or {}
        quotation_id = data.get('quotation_id')
        
        quotation = Quotation.query.get(quotation_id)
        if not quotation:
            return jsonify({'error': 'Quotation not found'}), 404
        
        if quotation.status != 'approved':
            return jsonify({'error': 'Only approved quotations can be issued as PO'}), 400
        
        # Create PO record
        po_id = str(uuid.uuid4())
        po_number = f"PO-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        po_data = {
            'id': po_id,
            'quotation_id': quotation_id,
            'order_id': quotation.order_id,
            'vendor_id': quotation.vendor_id,
            'po_number': po_number,
            'total_amount': quotation.total_price,
            'delivery_days': quotation.delivery_days,
            'status': 'issued',
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Store in memory for demo
        pos_store[po_id] = po_data
        
        # Update quotation to mark PO issued
        quotation.status = 'po_issued'
        db.session.commit()
        
        return jsonify({
            'po': po_data,
            'message': f'✓ Purchase Order {po_number} issued to {quotation.vendor_id}. Ready for fulfillment.'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@po_bp_new.route('/', methods=['GET'])
def list_pos():
    """List all POs (filter by order_id if provided)"""
    try:
        order_id = request.args.get('order_id')
        
        if order_id:
            # Filter POs by order_id
            filtered_pos = [po for po in pos_store.values() if po['order_id'] == order_id]
            return jsonify(filtered_pos)
        else:
            # Return all POs
            return jsonify(list(pos_store.values()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@po_bp_new.route('/<string:po_id>', methods=['GET'])
def get_po(po_id):
    """Get PO details"""
    try:
        if po_id in pos_store:
            return jsonify(pos_store[po_id])
        return jsonify({'error': 'PO not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500