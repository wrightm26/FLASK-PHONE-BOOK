
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(50), nullable=False)
    last = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(75), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
