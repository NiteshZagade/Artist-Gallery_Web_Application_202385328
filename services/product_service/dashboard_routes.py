from flask import Blueprint, request, jsonify
from .models import db, Artwork
from .order_proxy import get_cart_by_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    trending_products = Artwork.query.filter_by(is_trending=True).all()
    festival_offers = Artwork.query.filter_by(is_festival_offer=True).all()
    blockbuster_deals = Artwork.query.filter_by(is_blockbuster_deal=True).all()
    most_searched_products = Artwork.query.order_by(Artwork.search_count.desc()).limit(10).all()
    
    user_id = request.args.get('user_id')
    
    artwork_ids = []
    view_cart_response = get_cart_by_user(user_id)
       
    if view_cart_response.status_code == 200:
        artwork_datas = view_cart_response.json()        
        artwork_ids = [artwork["artwork_id"] for artwork in artwork_datas]
    
    cart_artworks = Artwork.query.filter(Artwork.id.in_(artwork_ids)).all()
    
    # Serialize artworks to a list of dictionaries
    artwork_list = [artwork.to_dict() for artwork in cart_artworks]
    
    return jsonify({
        'trending_products': [artwork.to_dict() for artwork in trending_products],
        'festival_offers': [artwork.to_dict() for artwork in festival_offers],
        'blockbuster_deals': [artwork.to_dict() for artwork in blockbuster_deals],
        'most_searched_products': [artwork.to_dict() for artwork in most_searched_products],
        'cart_items': [artwork for artwork in artwork_list]
    }), 200