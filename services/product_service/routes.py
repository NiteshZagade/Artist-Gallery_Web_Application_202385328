from datetime import datetime
from flask import Blueprint, request, jsonify
from enums import CategoryEnum, StyleEnum, SubjectEnum, MediumEnum, MaterialEnum, OrientationEnum
from .models import db, Artwork, ArtworkReviews
from utils import get_value_from_label
from sqlalchemy import func

artwork_bp = Blueprint('artwork', __name__)

# Create a new artwork
@artwork_bp.route('/artworks', methods=['POST'])
def add_artwork():
    data = request.get_json()
    
    #region data level validation
    category_type = Artwork.get_category_type_value(data['category'])
    if category_type == 0:
        return jsonify({'message': 'Category type does not exist in system'}), 400
    
    style_type = Artwork.get_style_type_value(data['style'])
    if style_type == 0:
        return jsonify({'message': 'Style type does not exist in system'}), 400
    
    material_type = Artwork.get_material_type_value(data['material'])
    if material_type == 0:
        return jsonify({'message': 'Material type does not exist in system'}), 400
    
    medium_type = Artwork.get_medium_type_value(data['medium'])
    if medium_type == 0:
        return jsonify({'message': 'Medium type does not exist in system'}), 400
    
    subject_type = Artwork.get_subject_type_value(data['subject'])
    if subject_type == 0:
        return jsonify({'message': 'Subject type does not exist in system'}), 400
    
    orientation_type = Artwork.get_orientation_type_value(data['orientation'])
    if orientation_type == 0:
        return jsonify({'message': 'Orientation type does not exist in system'}), 400
    #endregion
    
    cal_offer_price = 0
    if data['discount'] > 0:
        cal_offer_price = (data['price'] - ((data['price'] * data['discount']) / 100))
    
    new_artwork = Artwork(
          title=data['title']
        , description=data['description']
        , category=category_type
        , style=style_type
        , material=material_type
        , medium=medium_type
        , subject=subject_type
        , orientation=orientation_type
        , size=data['size']
        , price=data['price']
        , discount=data['discount']
        , offer_price=cal_offer_price
        , quantity=data['quantity']
        , imageurl=data['imageurl']
        , is_trending=data.get('is_trending', False)
        , is_festival_offer=data.get('is_festival_offer', False)
        , is_blockbuster_deal=data.get('is_blockbuster_deal', False)
        , search_count=data.get('search_count', 0)
        , created_on=datetime.today()
        , created_by=data['created_by']
        , modified_by=data['created_by']
        )
    db.session.add(new_artwork)
    
    db.session.commit()
    return jsonify({'message': 'Artwork added successfully'}), 201

# Get all artworks
@artwork_bp.route('/artworks', methods=['GET'])
def get_artworks():
    artworks = Artwork.query.all()
    return jsonify([artwork.to_dict() for artwork in artworks])

# Get a specific artwork by ID
@artwork_bp.route('/artworks/<int:id>', methods=['GET'])
def get_artwork(id):
    artwork = Artwork.query.get_or_404(id)
    return jsonify(artwork.to_dict()), 200

@artwork_bp.route('/artworks/<int:id>/check_availability', methods=['POST'])
def check_availability(id):
    data = request.get_json()
    artwork = Artwork.query.get_or_404(id)
    if artwork.quantity >= data.get('quantity', 1):
        return jsonify({'available': True, 'artwork': artwork.to_dict()})
    else:
        return jsonify({'available': False, 'message': 'Not enough stock'}), 400

@artwork_bp.route('/artworks/<int:id>/update_stock', methods=['PUT'])
def update_stock(id):
    data = request.get_json()
    artwork = Artwork.query.get_or_404(id)
    
    if artwork.quantity >= data['quantity']:
        artwork.quantity -= data['quantity']
        artwork.modified_on = datetime.today()
        artwork.modified_by = data['modified_by']
        db.session.commit()
        return jsonify({'message': 'Stock updated successfully'})
    else:
        return jsonify({'message': 'Not enough stock to update'}), 400        

@artwork_bp.route('/artworks/<int:id>/add_stock', methods=['PUT'])
def add_stock(id):
    data = request.get_json()
    artwork = Artwork.query.get_or_404(id)
    
    artwork.quantity=artwork.quantity if data.get('quantity', 0) == 0 else data.get('quantity', 0)
    artwork.price=artwork.price if data.get('price', 0.00) == 0.00 else data.get('price', 0.00)
    artwork.discount=artwork.discount if data.get('discount', 0) == 0 else data.get('discount', 0)
    
    cal_offer_price = 0
    if artwork.discount > 0:
        cal_offer_price = (artwork.price - ((artwork.price * artwork.discount) / 100))
    
    artwork.offer_price=artwork.offer_price if cal_offer_price == 0 else cal_offer_price
    artwork.modified_on=datetime.today()
    artwork.modified_by=data['modified_by']
    db.session.commit()
    
    return jsonify({'message': 'Stock updated successfully'})

# Update a specific artwork by ID
@artwork_bp.route('/artworks/<int:id>', methods=['PUT'])
def update_artwork(id):
    data = request.get_json()
    artwork = Artwork.query.get_or_404(id)
    artwork.title=data['title']
    artwork.description=data['description']
    artwork.category=CategoryEnum[data['category']]
    artwork.style=data['style']
    artwork.material=data['material']
    artwork.medium=data['medium']
    artwork.size=data['size']    
    artwork.price=data['price']
    artwork.rating=data['rating']
    artwork.imageurl=data['imageurl']
    artwork.is_trending = data['is_trending']
    artwork.is_festival_offer = data['is_festival_offer']
    artwork.is_blockbuster_deal = data['is_blockbuster_deal']
    artwork.search_count = data['search_count']
    artwork.modified_on=datetime.today()
    artwork.modified_by=data['modified_by']
    
    db.session.commit()
    return jsonify({'message': 'Artwork updated successfully'})

# Delete a specific artwork by ID
@artwork_bp.route('/artworks/<int:id>', methods=['DELETE'])
def delete_artwork(id):
    artwork = Artwork.query.get_or_404(id)
    db.session.delete(artwork)
    db.session.commit()
    return jsonify({'message': 'Artwork deleted successfully'})

# Search artwork on multiple conditions
@artwork_bp.route('/search', methods=['POST'])
def search_artworks():
    data = request.get_json()

    filters = request.json

    # Start with a base query
    query = Artwork.query    

    if 'category' in filters:
        query = query.filter(Artwork.category.in_([get_value_from_label(CategoryEnum, c) for c in filters['category']]))

    if 'style' in filters:
        query = query.filter(Artwork.style.in_([get_value_from_label(StyleEnum, s) for s in filters['style']]))
    
    if 'material' in filters:
        query = query.filter(Artwork.material.in_([get_value_from_label(MaterialEnum, m) for m in filters['material']]))
    
    if 'medium' in filters:
        query = query.filter(Artwork.medium.in_([get_value_from_label(MediumEnum, m) for m in filters['medium']]))
        
    if 'subject' in filters:
        query = query.filter(Artwork.subject.in_([get_value_from_label(SubjectEnum, s) for s in filters['subject']]))
    
    if 'orientation' in filters:
        query = query.filter(Artwork.orientation.in_([get_value_from_label(OrientationEnum, o) for o in filters['orientation']]))

    # Additional filters
    if 'title' in data:
        query = query.filter(Artwork.title.ilike(f"%{data['title']}%"))
         
    # Filter by size
    if 'size' in data:
        query = query.filter(Artwork.size == data['size'])
    
    # Filter by quantity range
    if 'quantity_min' in data:
        query = query.filter(Artwork.quantity >= data['quantity_min'])
    if 'quantity_max' in data:
        query = query.filter(Artwork.quantity <= data['quantity_max'])
        
    # Filter by price range
    if 'price_min' in data:
        query = query.filter(Artwork.price >= data['price_min'])
    if 'price_max' in data:
        query = query.filter(Artwork.price <= data['price_max'])
        
    # Filter by creation date range
    if 'created_on_from' in data:
        query = query.filter(Artwork.created_on >= data['created_on_from'])
    if 'created_on_to' in data:
        query = query.filter(Artwork.created_on <= data['created_on_to'])

    # Execute the query and get results
    artworks = query.all()

    # Serialize results
    results = [artwork.to_dict() for artwork in artworks]

    return jsonify(results), 200

def filter_query(query, filter_key, filter_values):
    if filter_values:
        enum_class = globals()[filter_key[0].upper() + filter_key[1:] + 'Enum']
        print(enum_class)
        query = query.filter(getattr(Artwork, filter_key).in_([enum_class(value) for value in filter_values]))
    return query

# Create a new artwork
@artwork_bp.route('/reviews', methods=['POST'])
def add_artwork_reviews():
    data = request.get_json()
    
    new_review = ArtworkReviews(
        artwork_id=data['artwork_id'],
        rating=data['rating'],
        comment=data['comment'],
        created_by=data['created_by'],
        created_on=datetime.today()
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Artwork review added successfully'}), 201

# Get all reviews for an artwork
@artwork_bp.route('/reviews/<int:artwork_id>', methods=['GET'])
def get_reviews(artwork_id):
    reviews = ArtworkReviews.query.filter_by(artwork_id=artwork_id).all()
    return jsonify([review.to_dict() for review in reviews])

# Get average rating of all reviews for an artwork
@artwork_bp.route('/artworks/<int:artwork_id>/average-rating', methods=['GET'])
def artwork_average_rating(artwork_id):
    average_rating = get_average_rating(artwork_id)
    return jsonify({'artwork_id': artwork_id, 'average_rating': average_rating})

def get_average_rating(artwork_id):
    average_rating = db.session.query(func.avg(ArtworkReviews.rating)).filter(ArtworkReviews.artwork_id == artwork_id).scalar()
    return round(average_rating, 2) if average_rating else 0.0