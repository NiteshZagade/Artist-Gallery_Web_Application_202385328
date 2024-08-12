from datetime import datetime
from flask import Blueprint, request, jsonify
from .product_proxy import check_product_availability, update_stock, get_artwork_by_id
from .models import db, Cart, Order, OrderItem

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    
    artwork_response = get_artwork_by_id(data['artwork_id'])    
    if artwork_response.status_code != 200:
        return jsonify({'message': 'Artwork not found'}), 404
    
    artwork_data = artwork_response.json()
    
    if artwork_data['quantity'] <= 0:
        return jsonify({'message': 'Not enough stock available'}), 400
            
    cart_item = Cart.query.filter_by(created_by=data['created_by'], artwork_id=data['artwork_id']).first()
    
    item_price = artwork_data['price'] if artwork_data['discount'] <= 0 else artwork_data['offer_price']
    
    if cart_item:
        cart_item.quantity += data.get('quantity', 1)
        cart_item.price = data.get('quantity', 1) * artwork_data['price']
    else:
        new_cart_item = Cart(
            artwork_id=artwork_data['id']
            , quantity=data.get('quantity', 1)
            , price = item_price * data.get('quantity', 1)
            , created_on=datetime.today()
            , created_by=data['created_by']
            , modified_on=datetime.today()
            , modified_by=data['created_by']
        )
        db.session.add(new_cart_item)
    db.session.commit()
    return jsonify({'message': 'Artwork added to cart successfully'}), 201

@order_bp.route('/cart/<int:created_by>', methods=['GET'])
def view_cart(created_by):
    cart_items = Cart.query.filter_by(created_by=created_by).all()
    return jsonify([item.to_dict() for item in cart_items])
    
@order_bp.route('/cart/<int:id>', methods=['PUT'])
def update_cart(id):
    data = request.get_json()
    
    cart_item = Cart.query.get_or_404(id)
    
    artwork_response = get_artwork_by_id(cart_item.artwork_id)
    if artwork_response.status_code != 200:
        return jsonify({'message': 'Artwork not found'}), 404
    
    artwork_data = artwork_response.json()
    
    if artwork_data['quantity'] <= data.get('quantity', 1):
        return jsonify({'message': 'Not enough stock available'}), 400
    
    item_price = artwork_data['price'] if artwork_data['discount'] <= 0 else artwork_data['offer_price']

    cart_item.quantity = data.get('quantity', 1)
    cart_item.price = data.get('quantity', 1) * item_price
    cart_item.modified_on=datetime.today()
    cart_item.modified_by=data['created_by']
    
    db.session.commit()
    return jsonify({'message': 'Cart item updated successfully'}), 200

@order_bp.route('/cart/<int:id>', methods=['DELETE'])
def delete_cart_item(id):
    cart_item = Cart.query.get_or_404(id)
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Cart item deleted successfully'}), 200

@order_bp.route('/create-order', methods=['POST'])
def create_order():
    data = request.get_json()
    created_by = data['created_by']
    
    # Get all items from the cart for this user
    cart_items = Cart.query.filter_by(created_by=created_by).all()
    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 400

    # Calculate total amount
    total_amount = sum(item.quantity * item.price for item in cart_items)

    # Create a new order
    new_order = Order(        
          total_amount = total_amount
        , status = 'Pending'
        , created_by=created_by
        , modified_by=created_by
        )
    db.session.add(new_order)
    db.session.flush()  # Flush to get the order ID

    # Create order items from the cart items
    for cart_item in cart_items:

        order_item = OrderItem(
            order_id=new_order.id
            , artwork_id=cart_item.artwork_id
            , quantity=cart_item.quantity
            , price=cart_item.price
            , created_by=created_by
            , modified_by=created_by
        )
        db.session.add(order_item)

    # Remove the items from the cart
    Cart.query.filter_by(created_by=created_by).delete()

    db.session.commit()

    return jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201

@order_bp.route('/orders/<int:created_by>', methods=['GET'])
def view_orders(created_by):
    orders = Order.query.filter_by(created_by=created_by).all()
    return jsonify([order.to_dict() for order in orders])
    
@order_bp.route('/order/<int:id>/status', methods=['PUT'])
def update_order_status(id):
    data = request.get_json()
    order = Order.query.get_or_404(id)
    status = data.get('status', order.status)
    
    new_status = ''
    # Check if the payment was successful
    if status == 'succeeded':
        # Update order status to PAID
        new_status = 'PAID'
    else:
        # Update order status to FAILED
        new_status = 'FAILED'
    
    if not new_status:
        return jsonify({'error': 'Order status is required'}), 400
    
    order.status = new_status
    db.session.commit()
    return jsonify({'message': 'Order status updated successfully'}), 200