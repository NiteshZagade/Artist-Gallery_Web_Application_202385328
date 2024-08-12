from flask import Blueprint, request, jsonify
from .models import db, User
from .auth import create_token, protect_route
from .config import Config
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

login_bp = Blueprint('login', __name__)

@login_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'User with this email already exists'}), 400
    
    user_type = User.get_user_type_value(data['usertype'])
    if user_type == 0:
        return jsonify({'message': 'User type does not exist in system'}), 400
    
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(        
        fname=data['fname'], 
        lname=data['lname'],
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        isactive=True,
        user_type = user_type,
        created_on=datetime.today(),        
        modified_on=datetime.today()
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@login_bp.route('/login', methods=['POST'])
def login():
    from flask import request
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user:
        if user.account_locked:
            return jsonify({'message': 'Account locked due to too many failed login attempts'}), 403
    
        if check_password_hash(user.password, data['password']):
            user.failed_login_attempts = 0
            user.modified_on = datetime.today()
            db.session.commit()
            
            token = create_token(identity=user.id)
            return jsonify({
                'token': token,
                'user': user.to_dic()
            })
        else:
            user.failed_login_attempts += 1
            user.last_failed_login_attempt_on = datetime.today()
            if user.failed_login_attempts >= Config.MAX_FAILED_LOGIN_ATTEMPTS:
                user.account_locked = True
                user.account_locked_on = datetime.today()
            db.session.commit()
            return jsonify({'message': 'Invalid credentials'}), 401
    return jsonify({'message': 'Invalid credentials'}), 401

@login_bp.route('/users/<int:id>/change-password', methods=['PUT'])
@protect_route
def change_password(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    
    if not check_password_hash(user.password, data['old_password']):
        return jsonify({'message': 'Old password is incorrect'}), 400
    
    user.password = generate_password_hash(data['new_password'], method='pbkdf2:sha256')
    user.modified_by = data['modified_by']
    user.modified_on = datetime.today()
    db.session.commit()
    return jsonify({'message': 'Password changed successfully'})