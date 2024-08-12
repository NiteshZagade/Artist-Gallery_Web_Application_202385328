from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    order_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)  # amount in cents
    currency = db.Column(db.String(3), default='gbp')
    status = db.Column(db.String(50), nullable=False)
    stripe_charge_id = db.Column(db.String(200), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.today())