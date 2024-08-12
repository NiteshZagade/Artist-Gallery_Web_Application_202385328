from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils import format_datetime

db = SQLAlchemy()

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    artwork_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.today())
    created_by = db.Column(db.Integer, nullable=False)
    modified_on = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())
    modified_by = db.Column(db.Integer, nullable=False)

    #region Format date
    @property
    def formatted_created_on(self):
        return format_datetime(self.created_on)

    @property
    def formatted_modified_on(self):
        return format_datetime(self.modified_on)
    #endregion

    def to_dict(self):
        return {
            'id': self.id
            , 'artwork_id': self.artwork_id
            , 'quantity': self.quantity
            , 'price': self.price
            , 'created_on': self.created_on
            , 'created_by': self.created_by
            , 'modified_on': self.modified_on
            , 'modified_by': self.modified_by
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(80), nullable=False, default='Pending')
    created_on = db.Column(db.DateTime, default=datetime.today())
    created_by = db.Column(db.Integer, nullable=False)
    modified_on = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())
    modified_by = db.Column(db.Integer, nullable=False)

    #region Format date
    @property
    def formatted_created_on(self):
        return format_datetime(self.created_on)

    @property
    def formatted_modified_on(self):
        return format_datetime(self.modified_on)
    #endregion

    def to_dict(self):
        return {
            'id': self.id
            , 'total_amount': self.total_amount
            , 'status': self.status
            , 'created_on': self.created_on
            , 'created_by': self.created_by
            , 'modified_on': self.modified_on
            , 'modified_by': self.modified_by
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    artwork_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.today())
    created_by = db.Column(db.Integer, nullable=False)
    modified_on = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())
    modified_by = db.Column(db.Integer, nullable=False)    
    
    #region Format date
    @property
    def formatted_created_on(self):
        return format_datetime(self.created_on)

    @property
    def formatted_modified_on(self):
        return format_datetime(self.modified_on)
    #endregion
    
    def to_dict(self):
        return {
            'id': self.id
            , 'order_id': self.order_id
            , 'artwork_id': self.artwork_id
            , 'quantity': self.quantity
            , 'price': self.price
            , 'created_on': self.created_on
            , 'created_by': self.created_by
            , 'modified_on': self.modified_on
            , 'modified_by': self.modified_by
        }