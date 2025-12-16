from flask import Blueprint, request, jsonify
from config.db import db
from models.order import Order
from utils.helpers import to_dict

order_bp = Blueprint('orders', __name__)

@order_bp.route('/', methods=['POST'])
def create_order():
    """UC-01: Client places order"""
    try:
        data = request.get_json() or {}
        order = Order(
            client_name=data.get('client_name', 'Unknown'),
            client_email=data.get('client_email', ''),
            description=data.get('description', ''),
            quantity=data.get('quantity', 1),
            total_budget=data.get('total_budget', 0.0)
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({
            'order': to_dict(order),
            'message': '✓ Order placed successfully. Submitted to Commercial Department.'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@order_bp.route('/', methods=['GET'])
def list_orders():
    """Get all orders"""
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return jsonify([to_dict(o) for o in orders])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<string:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(to_dict(order))

@order_bp.route('/<string:order_id>', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        data = request.get_json() or {}
        if 'status' in data:
            order.status = data['status']
        db.session.commit()
        return jsonify({
            'order': to_dict(order),
            'message': f'Order status updated to {order.status}'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
