from flask import Blueprint, request, jsonify
from config.db import db
from models.purchase_requisition import PurchaseRequisition
from utils.helpers import to_dict

pr_bp = Blueprint('pr', __name__)


@pr_bp.route('/', methods=['GET'])
def list_prs():
    prs = PurchaseRequisition.query.order_by(PurchaseRequisition.created_at.desc()).all()
    return jsonify([to_dict(p) for p in prs])


@pr_bp.route('/', methods=['POST'])
def create_pr():
    try:
        data = request.get_json() or {}
        item = data.get('item') or data.get('item_sku')  # Support both field names
        qty = data.get('qty', 1)
        requester = data.get('requester', 'unknown')
        if not item:
            return jsonify({'error': 'item is required'}), 400
        pr = PurchaseRequisition(item=item, qty=qty, requester=requester)
        db.session.add(pr)
        db.session.commit()
        # Inform frontend where the PR is sent next
        return jsonify({'pr': to_dict(pr), 'message': 'Order received — transferred to Procurement (PR) department'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@pr_bp.route('/<string:pr_id>', methods=['GET'])
def get_pr(pr_id):
    pr = PurchaseRequisition.query.get(pr_id)
    if not pr:
        return jsonify({'error': 'not found'}), 404
    return jsonify(to_dict(pr))


@pr_bp.route('/<string:pr_id>', methods=['PUT'])
def update_pr(pr_id):
    pr = PurchaseRequisition.query.get(pr_id)
    if not pr:
        return jsonify({'error': 'not found'}), 404
    data = request.get_json() or {}
    pr.item = data.get('item', pr.item)
    pr.qty = data.get('qty', pr.qty)
    pr.requester = data.get('requester', pr.requester)
    pr.status = data.get('status', pr.status)
    db.session.commit()
    return jsonify(to_dict(pr))


@pr_bp.route('/<string:pr_id>', methods=['DELETE'])
def delete_pr(pr_id):
    """Delete a purchase requisition."""
    try:
        pr = PurchaseRequisition.query.get(pr_id)
        if not pr:
            return jsonify({'error': 'not found'}), 404
        db.session.delete(pr)
        db.session.commit()
        return jsonify({'deleted': pr_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@pr_bp.route('/<string:pr_id>/recommend', methods=['POST'])
def recommend_pr(pr_id):
    """Recommend a PR (set status to recommended)."""
    try:
        pr = PurchaseRequisition.query.get(pr_id)
        if not pr:
            return jsonify({'error': 'not found'}), 404
        pr.status = 'recommended'
        db.session.commit()
        return jsonify({'pr': to_dict(pr), 'message': 'PR recommended — transferred to Commercial department for decision'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@pr_bp.route('/<string:pr_id>/create_po', methods=['POST'])
def create_po_from_pr(pr_id):
    """Create a Purchase Order automatically from a PR's data.
    Request JSON may include `vendor_id` and `items` override.
    """
    try:
        pr = PurchaseRequisition.query.get(pr_id)
        if not pr:
            return jsonify({'error': 'PR not found'}), 404
        data = request.get_json() or {}
        vendor_id = data.get('vendor_id')
        items = data.get('items')
        # Default item structure from PR if items not provided
        if not items:
            items = [{
                'sku': getattr(pr, 'item', None),
                'name': getattr(pr, 'item', None),
                'qty': getattr(pr, 'qty', 1)
            }]
        total = data.get('total', 0.0)
        from models.purchase_order import PurchaseOrder
        import json
        po = PurchaseOrder(vendor_id=vendor_id or None, items=json.dumps(items), total=total)
        db.session.add(po)
        # mark PR as having a PO created
        pr.status = 'po_created'
        db.session.commit()
        return jsonify({'po_id': po.id, 'pr_id': pr.id, 'message': 'PO created from PR — sent to Vendor for fulfillment'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
