import pkgutil
import importlib.util

# Compatibility: some Python versions remove pkgutil.get_loader; Flask internals expect it.
if not hasattr(pkgutil, 'get_loader'):
    def _get_loader(name):
        spec = importlib.util.find_spec(name)
        return getattr(spec, 'loader', None) if spec is not None else None
    pkgutil.get_loader = _get_loader

from flask import Flask, send_from_directory, jsonify, request
from config.db import db
from routes.pr_routes import pr_bp
from routes.vendor_routes import vendor_bp
from routes.negotiation_routes import negotiation_bp
from routes.po_routes import po_bp
from routes.commercial_routes import commercial_bp
from routes.account_routes import account_bp
from routes.tax_routes import tax_bp
from routes.client_routes import client_bp
from routes.warehouse_routes import warehouse_bp
from routes import dashboard_routes

import os

# Resolve frontend absolute path so static files are served regardless of cwd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'Frontend'))
if not os.path.isdir(FRONTEND_DIR):
    # fallback to project root 'Frontend' (case variations on some environments)
    FRONTEND_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', '..', 'Frontend'))

# Note: frontend folder name is 'Frontend' in the project root. Use that as static folder.
app = Flask('sep_project', static_folder=FRONTEND_DIR, static_url_path='/')
app.config.from_object('config.settings.Config')
db.init_app(app)

# register blueprints
app.register_blueprint(pr_bp, url_prefix='/api/pr')
app.register_blueprint(vendor_bp, url_prefix='/api/vendors')
app.register_blueprint(negotiation_bp, url_prefix='/api/negotiation')
app.register_blueprint(po_bp, url_prefix='/api/po')
app.register_blueprint(commercial_bp, url_prefix='/api/commercial')
app.register_blueprint(account_bp, url_prefix='/api/accounts')
app.register_blueprint(tax_bp, url_prefix='/api/tax')
app.register_blueprint(client_bp, url_prefix='/api/client')
app.register_blueprint(warehouse_bp, url_prefix='/api/warehouse')
app.register_blueprint(dashboard_routes.bp, url_prefix='/api')

# serve frontend static files
@app.route('/')
def index():
    return app.send_static_file('dashboard.html')


# SPA fallback: if a non-API route is requested, return the dashboard so
# the frontend can handle client-side routing. For API routes we return
# normal 404 responses.
@app.errorhandler(404)
def handle_404(e):
    # If the path looks like an API call, return JSON 404
    if request.path.startswith('/api'):
        return jsonify({'error': 'not found'}), 404
    # Otherwise serve the frontend entrypoint so users can navigate directly
    return app.send_static_file('dashboard.html')

if __name__ == '__main__':
    # Open default browser after server starts
    import threading, webbrowser, time

    def _open_browser_later(url):
        # Wait briefly for the server to start
        time.sleep(1.0)
        try:
            webbrowser.open_new(url)
        except Exception:
            pass

    url = 'http://127.0.0.1:5000/'
    threading.Thread(target=_open_browser_later, args=(url,), daemon=True).start()

    # Run the Flask development server. use_reloader=False prevents double browser opens.
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
