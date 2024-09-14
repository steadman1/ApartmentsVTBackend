from server.auth import auth_bp
from server.db_config import db
from flask import request, jsonify
from werkzeug.security import generate_password_hash, gen_salt, check_password_hash
from server.auth.models import User

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

    return 200

@auth_bp.route("/login", methods=["POST"])
def login():
     data = request.get_json()
     if not 'email' in data or not 'password' in data:
          return jsonify({"error": "Missing required fields"}), 400
     
     email = data['email']
     user = User.query.filter_by(email=email).first()

     if not user:
          return jsonify({"error": "User not found"}), 404

     password = data['password'] + user.password_salt

     if check_password_hash(user.password_hash, password):
          pass