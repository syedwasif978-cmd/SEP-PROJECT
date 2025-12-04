from config.db import db
import uuid

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, nullable=False)
    contact = db.Column(db.String)
    rating = db.Column(db.Integer, default=0)
