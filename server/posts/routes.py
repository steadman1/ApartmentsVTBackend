from server.posts import posts_bp
from server.auth.models import User
from server.posts.models import Post  # Import the Post model
from server.config import db  # Import the database object
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from datetime import datetime
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


@posts_bp.route('/create_post', methods=['POST'])
@jwt_required()
def create_post():
    # Get JSON data from the request
    data = request.get_json()

    try:
        user_id = get_jwt_identity()  # Get the user_id from the JWT token
        
        # Create a new Post object from the JSON data
        new_post = Post(
            user_id=user_id,
            title=data['title'],
            price=data['price'],
            roommate_count=data.get('roommate_count'),
            summary=data.get('summary'),
            roommate_bio=data.get('roommate_bio'),
            present_pet_types=data.get('present_pet_types', []),
            address=data.get('address'),
            walk_time=data.get('walk_time'),
            bike_time=data.get('bike_time'),
            drive_time=data.get('drive_time'),
            bus_routes=data.get('bus_routes', []),
            gender_preferences=data.get('gender_preferences', []),
            nationalities=data.get('nationalities', []),
            ada_accessible=data.get('ada_accessible'),
            proximity_to_stores=data.get('proximity_to_stores', []),
            rent_period_start=datetime.strptime(data.get('rent_period_start'), '%Y-%m-%d') if data.get('rent_period_start') else None,
            rent_period_end=datetime.strptime(data.get('rent_period_end'), '%Y-%m-%d') if data.get('rent_period_end') else None,
            lease_length=data.get('lease_length'),
            utilities_included=data.get('utilities_included', []),
            furnished=data.get('furnished'),
            square_footage=data.get('square_footage'),
            bathroom_count=data.get('bathroom_count'),
            bedroom_count=data.get('bedroom_count'),
            pets_allowed=data.get('pets_allowed'),
            deposit_required=data.get('deposit_required'),
            lease_type=data.get('lease_type'),
            apartment_complex_name=data.get('apartment_complex_name'),
            period=data.get('period'),
            property_type=data.get('property_type'),
            smoking_allowed=data.get('smoking_allowed'),
            parking_available=data.get('parking_available'),
            images_urls=data.get('images_urls', []),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            favoriteListing=data.get('favoriteListing', False),
            milesToCampus=data.get('milesToCampus')
        )

        # Add the new post to the database session
        db.session.add(new_post)
        db.session.commit()

        # Return a success message
        return jsonify({"message": "Post created successfully!", "post_id": new_post.id}), 201

    except Exception as e:
        # If there's an error, roll back the transaction and return an error message
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@posts_bp.route('/test', methods=["POST"])
@jwt_required()
def test():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify(msg=f"{user.username}"), 200
