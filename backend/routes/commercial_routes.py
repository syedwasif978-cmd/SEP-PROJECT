from flask import Blueprint, request, jsonify
from config.db import db
from models.commercial_approval import CommercialApproval
from models.purchase_requisition import PurchaseRequisition
from utils.helpers import to_dict

commercial_bp = Blueprint('commercial', __name__)


@commercial_bp.route('/', methods=['GET'])
def list_approvals():
    """Get all commercial approvals."""
    try:
        items = CommercialApproval.query.order_by(CommercialApproval.created_at.desc()).all()
        return jsonify([to_dict(i) for i in items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@commercial_bp.route('/pending', methods=['GET'])
def list_pending_prs():
    """Get pending PRs for commercial approval (PRS with status 'recommended')."""
    try:
        prs = PurchaseRequisition.query.filter_by(status='recommended').all()
        return jsonify([to_dict(p) for p in prs])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@commercial_bp.route('/', methods=['POST'])
def create_approval():
    """Create a commercial approval record."""
    try:
        data = request.get_json() or {}
        pr_id = data.get('pr_id')
        if not pr_id:
            return jsonify({'error': 'pr_id required'}), 400
        a = CommercialApproval(pr_id=pr_id, approver=data.get('approver', 'system'), decision=data.get('decision', 'approved'), comments=data.get('comments'))
        db.session.add(a)
        db.session.commit()
        return jsonify(to_dict(a)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@commercial_bp.route('/decision', methods=['POST'])
def commercial_decision():
    """Record commercial approval/rejection decision on a PR."""
    try:
        data = request.get_json() or {}
        pr_id = data.get('pr_id')
        approve = data.get('approve', True)
        if not pr_id:
            return jsonify({'error': 'pr_id required'}), 400
        pr = PurchaseRequisition.query.get(pr_id)
        if not pr:
            return jsonify({'error': 'PR not found'}), 404
        decision = 'approved' if approve else 'rejected'
        pr.status = decision
        a = CommercialApproval(pr_id=pr_id, approver='commercial_dept', decision=decision, comments='Commercial decision')
        db.session.add(a)
        db.session.commit()
        return jsonify({'status': 'success', 'pr_id': pr_id, 'decision': decision})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
