from models.client_confirmation import ClientConfirmation
from config.db import db

def list_confirmations():
    return ClientConfirmation.query.all()

def confirm(id):
    c = ClientConfirmation.query.get(id)
    if not c: return False
    c.status = 'confirmed'
    db.session.commit()
    return True
