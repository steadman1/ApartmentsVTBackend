from server.posts import posts_bp
from server.auth.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify


@posts_bp.route('/test', methods=["POST"])
@jwt_required()
def test():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify(msg=f"{user.username}"), 200
    