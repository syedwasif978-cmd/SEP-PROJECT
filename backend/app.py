from flask import Flask, send_from_directory, jsonify
from config.db import db
from routes.pr_routes import pr_bp
from routes.vendor_routes import vendor_bp
from routes.negotiation_routes import negotiation_bp
from routes.po_routes import po_bp
from routes.commercial_routes import commercial_bp
from routes.account_routes import account_bp
from routes.tax_routes import tax_bp
from routes.client_routes import client_bp
from routes import dashboard_routes

import os

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
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
app.register_blueprint(dashboard_routes.bp, url_prefix='/api')

# serve frontend static files
@app.route('/')
def index():
    return app.send_static_file('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
