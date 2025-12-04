from models.account import AccountEntry
from config.db import db

def list_pending():
    return AccountEntry.query.filter_by(status='pending').all()

def mark_paid(aid):
    a = AccountEntry.query.get(aid)
    if not a: return False
    a.status = 'paid'
    db.session.commit()
    return True
