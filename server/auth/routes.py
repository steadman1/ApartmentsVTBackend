from server.auth import auth_bp
from server.config import db
from flask import request, jsonify
from werkzeug.security import generate_password_hash, gen_salt, check_password_hash
from server.auth.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not all(key in data for key in ('first_name', 'last_name', 'username', 'email', 'phone_number', 'password')):
        return jsonify({"error": "Missing required fields"}), 400

    first_name = data['first_name']
    last_name = data['last_name']
    username = data['username']
    email = data['email']
    phone_number = data['phone_number']
    salt = gen_salt(20)
    password = data['password'] + salt
    
    if User.query.filter_by(username=username).first() or \
        User.query.filter_by(email=email).first() or \
        User.query.filter_by(phone_number=phone_number).first():
            return jsonify({"error": "Username or email already exists"}), 400
    
    new_user = User(
         first_name=first_name,
         last_name=last_name,
         username=username,
         email=email,
         phone_number=phone_number,
         password_hash=generate_password_hash(password),
         password_salt=salt
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success":"Signed up successfully"}), 200

@auth_bp.route("/login", methods=["POST"])
def login():
     data = request.get_json()
     print(data)
     if not 'email' in data or not 'password' in data:
          return jsonify({"error": "Missing required fields"}), 400
     
     email = data['email']
     user = User.query.filter_by(email=email).first()

     if not user:
          return jsonify({"error": "User not found"}), 404

     password = data['password'] + user.password_salt

     if check_password_hash(user.password_hash, password):
          access_token=create_access_token(identity=user.id)
          refresh_token=create_refresh_token(identity=user.id)
          return jsonify(access_token=access_token, refresh_token=refresh_token), 200
     else:
          return jsonify({"error": "Invalid password"}), 401
     
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
     user_id = get_jwt_identity()
     access_token = create_access_token(identity=user_id)
     return jsonify(access_token=access_token), 200