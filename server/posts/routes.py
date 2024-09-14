from server.posts import posts_bp
from server.auth.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from server.ai.ai_search import find_matching_listings  # Assuming this function exists

@posts_bp.route('/search', methods=['POST'])
def search_with_criteria():
    data = request.get_json()

    # Ensure data exists
    if not data:
        abort(400, description="No search criteria provided.")
    
    # Extract all criteria from the request data, ensuring correct types
    criteria = {
        "price": int(data.get('price')) if 'price' in data else None,  # Integer
        "furnished": data.get('furnished').lower() == 'true' if 'furnished' in data else None,  # Boolean
        "pets_allowed": data.get('pets_allowed').lower() == 'true' if 'pets_allowed' in data else None,  # Boolean
        "roommate_count": int(data.get('roommate_count')) if 'roommate_count' in data else None,  # Integer
        "ada_accessible": data.get('ada_accessible').lower() == 'true' if 'ada_accessible' in data else None,  # Boolean
        "gender_preferences": data.get('gender_preferences') if 'gender_preferences' in data else None,  # Array of strings
        "present_pet_types": data.get('present_pet_types') if 'present_pet_types' in data else None,  # Array of strings
        "walk_time": int(data.get('walk_time')) if 'walk_time' in data else None,  # Integer
        "bike_time": int(data.get('bike_time')) if 'bike_time' in data else None,  # Integer
        "drive_time": int(data.get('drive_time')) if 'drive_time' in data else None,  # Integer
        "bathroom_count": int(data.get('bathroom_count')) if 'bathroom_count' in data else None,  # Integer
        "bedroom_count": int(data.get('bedroom_count')) if 'bedroom_count' in data else None,  # Integer
        "lease_length": data.get('lease_length') if 'lease_length' in data else None,  # String
        "utilities_included": data.get('utilities_included') if 'utilities_included' in data else None,  # Array of strings
        "proximity_to_stores": data.get('proximity_to_stores') if 'proximity_to_stores' in data else None,  # Array of strings
        "bus_routes": data.get('bus_routes') if 'bus_routes' in data else None,  # Array of strings
        "nationalities": data.get('nationalities') if 'nationalities' in data else None,  # Array of strings
        "deposit_required": int(data.get('deposit_required')) if 'deposit_required' in data else None,  # Integer
        "lease_type": data.get('lease_type') if 'lease_type' in data else None,  # String
        "square_footage": int(data.get('square_footage')) if 'square_footage' in data else None  # Integer
    }

    # Filter out any criteria that are None
    criteria = {key: value for key, value in criteria.items() if value is not None}
    
    # Perform search using the find_matching_listings function
    results = find_matching_listings(criteria)

    if results:
        return jsonify({"success": True, "listings": results}), 200
    else:
        return jsonify({"success": False, "error": "No listings found."}), 404


@posts_bp.route('/test', methods=["POST"])
@jwt_required()
def test():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify(msg=f"{user.username}"), 200
    