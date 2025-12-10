from flask import Blueprint, request, jsonify
from config.db import db
from models.account import AccountEntry
from utils.helpers import to_dict

account_bp = Blueprint('accounts', __name__)


@account_bp.route('/', methods=['GET'])
def list_accounts():
    """Get all account entries."""
    try:
        items = AccountEntry.query.order_by(AccountEntry.created_at.desc()).all()
        return jsonify([to_dict(i) for i in items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@account_bp.route('/pending', methods=['GET'])
def list_pending_payments():
    """Get all pending payment account entries."""
    try:
        items = AccountEntry.query.filter_by(status='pending').order_by(AccountEntry.created_at.desc()).all()
        return jsonify([to_dict(i) for i in items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@account_bp.route('/', methods=['POST'])
def create_account():
    """Create a new account entry."""
    try:
        data = request.get_json() or {}
        po_id = data.get('po_id')
        amount = data.get('amount', 0.0)
        if not po_id:
            return jsonify({'error': 'po_id required'}), 400
        a = AccountEntry(po_id=po_id, amount=amount, status=data.get('status', 'pending'))
        db.session.add(a)
        db.session.commit()
        return jsonify({'account': to_dict(a), 'message': 'Invoice created — sent to Accounts for processing'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@account_bp.route('/<string:account_id>/pay', methods=['POST'])
def mark_paid(account_id):
    """Mark an account entry as paid."""
    try:
        acc = AccountEntry.query.get(account_id)
        if not acc:
            return jsonify({'error': 'not found'}), 404
        acc.status = 'paid'
        db.session.commit()
        return jsonify({'account': to_dict(acc), 'message': 'Payment completed — transaction closed and recorded in Accounts'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@account_bp.route('/<string:account_id>', methods=['GET'])
def get_account(account_id):
    try:
        a = AccountEntry.query.get(account_id)
        if not a:
            return jsonify({'error': 'not found'}), 404
        return jsonify(to_dict(a))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@account_bp.route('/<string:account_id>', methods=['PUT'])
def update_account(account_id):
    try:
        a = AccountEntry.query.get(account_id)
        if not a:
            return jsonify({'error': 'not found'}), 404
        data = request.get_json() or {}
        a.amount = data.get('amount', a.amount)
        a.status = data.get('status', a.status)
        db.session.commit()
        return jsonify(to_dict(a))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@account_bp.route('/<string:account_id>', methods=['DELETE'])
def delete_account(account_id):
    try:
        a = AccountEntry.query.get(account_id)
        if not a:
            return jsonify({'error': 'not found'}), 404
        db.session.delete(a)
        db.session.commit()
        return jsonify({'deleted': account_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
