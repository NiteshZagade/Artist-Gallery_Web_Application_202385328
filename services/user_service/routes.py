from flask import Blueprint, request, jsonify
from .models import db, User
from datetime import datetime
from werkzeug.security import generate_password_hash
from .auth import protect_route

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
@protect_route
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(fname=data['fname']
                    , lname=data['lname']
                    , username=data['username']
                    , email=data['email']
                    , password=hashed_password
                    , isactive=True
                    , user_type=User.get_user_type_value(data['usertype'])
                    , created_on=datetime.today()
                    , modified_on=datetime.today()
                    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/users', methods=['GET'])
@protect_route
def get_users():
    users = User.query.all()
    return jsonify([user.to_dic() for user in users])

@user_bp.route('/users/<int:id>', methods=['GET'])
@protect_route
def get_user_by_id(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dic())

@user_bp.route('/users/<int:id>', methods=['PUT'])
@protect_route
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.fname = data['fname']
    user.lname = data['lname']
    user.modified_by = data['modified_by']
    user.modified_on = datetime.today()
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@user_bp.route('/users/<int:id>/inactive', methods=['PUT'])
@protect_route
def inactive_user(id):
    user = User.query.get_or_404(id)
    user.isactive = False
    user.modified_on = datetime.today()
    db.session.commit()
    return jsonify({'message': 'User marked as inactive successfully'})

@user_bp.route('/users/<int:id>', methods=['DELETE'])
@protect_route
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@user_bp.route('/users/<int:id>/unlock', methods=['PUT'])
def unlock_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.failed_login_attempts = 0
    user.account_locked = False
    user.modified_by = data['modified_by']
    user.modified_on = datetime.today()
    db.session.commit()
    return jsonify({'message': 'User unlocked successfully'})