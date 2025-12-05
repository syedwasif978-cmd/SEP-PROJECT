from flask import Blueprint, jsonify

bp = Blueprint('dashboard', __name__)


@bp.route('/health')
def health():
    """Simple health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'SEP-PROJECT backend'})


@bp.route('/info')
def info():
    """Return a small info payload for the frontend to display."""
    return jsonify({'app': 'SEP-PROJECT', 'version': '1.0', 'notes': 'Simple backend for static frontend'})
