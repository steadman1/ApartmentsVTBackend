from . import auth_bp
from ..db_config import db
from flask import request, jsonify
from werkzeug.security import generate_password_hash, gen_salt, check_password_hash
from server.auth.models import User

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data or not 'username' in data or not 'email' in data or not 'password' in data:
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