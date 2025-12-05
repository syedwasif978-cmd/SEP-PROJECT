from flask import Blueprint, request, jsonify
from config.db import db
from models.vendor import Vendor
from utils.helpers import to_dict

vendor_bp = Blueprint('vendors', __name__)


@vendor_bp.route('/', methods=['GET'])
def list_vendors():
    vendors = Vendor.query.all()
    return jsonify([to_dict(v) for v in vendors])


@vendor_bp.route('/', methods=['POST'])
def create_vendor():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    v = Vendor(name=name, contact=data.get('contact'), rating=data.get('rating', 0))
    db.session.add(v); db.session.commit()
    return jsonify(to_dict(v)), 201


@vendor_bp.route('/<string:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    v = Vendor.query.get(vendor_id)
    if not v:
        return jsonify({'error': 'not found'}), 404
    return jsonify(to_dict(v))


@vendor_bp.route('/<string:vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    v = Vendor.query.get(vendor_id)
    if not v:
        return jsonify({'error': 'not found'}), 404
    data = request.get_json() or {}
    v.name = data.get('name', v.name)
    v.contact = data.get('contact', v.contact)
    v.rating = data.get('rating', v.rating)
    db.session.commit()
    return jsonify(to_dict(v))


@vendor_bp.route('/<string:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    v = Vendor.query.get(vendor_id)
    if not v:
        return jsonify({'error': 'not found'}), 404
    try:
        db.session.delete(v)
        db.session.commit()
        return jsonify({'deleted': vendor_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
