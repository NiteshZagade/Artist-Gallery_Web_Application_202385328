from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enums import CategoryEnum, StyleEnum, SubjectEnum, MediumEnum, MaterialEnum, OrientationEnum
from utils import format_datetime, get_value_from_label, generate_unique_product_id

db = SQLAlchemy()

class Artwork(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), nullable=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=True)    
    category = db.Column(db.Integer, nullable=False)
    style = db.Column(db.Integer, nullable=False)
    material = db.Column(db.Integer, nullable=False)
    medium = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.Integer, nullable=False)
    orientation = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    offer_price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    imageurl = db.Column(db.String(255), nullable=True)
    is_trending = db.Column(db.Boolean, default=False)
    is_festival_offer = db.Column(db.Boolean, default=False)
    is_blockbuster_deal = db.Column(db.Boolean, default=False)
    search_count = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime, default=datetime.today())
    created_by = db.Column(db.Integer, nullable=False)
    modified_on = db.Column(db.DateTime, nullable=True, onupdate=datetime.today())
    modified_by = db.Column(db.Integer, nullable=False)
    
    #region Format date
    @property
    def formatted_created_on(self):
        return format_datetime(self.created_on)

    @property
    def formatted_modified_on(self):
        return format_datetime(self.modified_on)
    #endregion
    
    #region  Enum to get the value from the stored Enum
    @staticmethod
    def get_category_type_value(category_type_string):
        return get_value_from_label(CategoryEnum, category_type_string)
    
    @staticmethod
    def get_style_type_value(style_type_string):
        return get_value_from_label(StyleEnum, style_type_string)
    
    @staticmethod
    def get_subject_type_value(subject_type_string):
        return get_value_from_label(SubjectEnum, subject_type_string)
    
    @staticmethod
    def get_medium_type_value(medium_type_string):
        return get_value_from_label(MediumEnum, medium_type_string)
    
    @staticmethod
    def get_material_type_value(material_type_string):
        return get_value_from_label(MaterialEnum, material_type_string)
    
    @staticmethod
    def get_orientation_type_value(orientation_type_string):
        return get_value_from_label(OrientationEnum, orientation_type_string)
    #endregion
    
    #region Reverse mapping to get the string value from the stored integer
    @property
    def get_category_type_string(self):    
        return CategoryEnum.reverse_mapping()[self.category]        
    
    @property
    def get_style_type_string(self):        
        return StyleEnum.reverse_mapping()[self.style]
    
    @property
    def get_subject_type_string(self):        
        return SubjectEnum.reverse_mapping()[self.subject]
    
    @property
    def get_medium_type_string(self):        
        return MediumEnum.reverse_mapping()[self.medium]
    
    @property
    def get_material_type_string(self):
        return MaterialEnum.reverse_mapping()[self.material]
    
    @property
    def get_orientation_type_string(self):        
        return OrientationEnum.reverse_mapping()[self.orientation]
    #endregion
                    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'category_string': self.get_category_type_string,
            'style': self.style,
            'style_string': self.get_style_type_string,
            'material': self.material,
            'material_string': self.get_material_type_string,
            'medium': self.medium,
            'medium_string': self.get_medium_type_string,
            'subject': self.subject,
            'subject_string': self.get_subject_type_string,
            'orientation': self.orientation,
            'orientation_string': self.get_orientation_type_string,
            'size': self.size,
            'price': self.price,
            'offer_price': self.offer_price,
            'discount': self.discount,
            'quantity': self.quantity,            
            'avilable_for_sale': (True, False) [self.quantity <= 0],
            'imageurl': self.imageurl,
            'is_trending': self.is_trending,
            'is_festival_offer': self.is_festival_offer,
            'is_blockbuster_deal': self.is_blockbuster_deal,
            'search_count': self.search_count,
            'created_on': self.formatted_created_on,
            'created_by': self.created_by,
            'modified_on': self.formatted_modified_on if self.modified_on else None,
            'modified_by': self.modified_by
        }


def before_insert_listener(mapper, connection, target):
    # Get the last product inserted today
    today = datetime.today().strftime('%d%m%y')
    last_product_id = Artwork.query.filter(Artwork.product_id.like(f"PRD-%-{today}-%")).order_by(Artwork.id.desc()).first()
    
    target.product_id = generate_unique_product_id(last_product_id, today, 'PRD')
    
# event added to run before_insert_listener
from sqlalchemy import event
event.listen(Artwork, 'before_insert', before_insert_listener)

class ArtworkReviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    artwork_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.today())
    created_by = db.Column(db.Integer, nullable=False)
    
    @property
    def formatted_created_on(self):
        return format_datetime(self.created_on)

    def to_dict(self):
        return {
            'id': self.id,
            'artwork_id': self.artwork_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_on': self.formatted_created_on,
            'created_by': self.created_by
        }
    