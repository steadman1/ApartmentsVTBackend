from server.get import get_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.auth.models import User
from server.posts.models import Post
from flask import jsonify

@get_bp.route('/user')
@jwt_required()
def get_user():
    user = User.query.get(get_jwt_identity())
    if user:
        user_data = {
            "id": user.id,
            "username": user.username,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "phoneNumber": user.phone_number,
            "bio": user.bio,
            "nationality": user.nationality,
            "profilePictureURL": user.profile_picture,
            "userListings": user.posts,
            # "favoriteListings": [favorite_listing]
        }
        return jsonify(user_data)
    else:
        return jsonify({"error":"User not found"}), 404
    
@get_bp.route('/user/<id>')
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        user_data = {
            "id": user.id,
            "username": user.username,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "phoneNumber": user.phone_number,
            "bio": user.bio,
            "nationality": user.nationality,
            "profilePictureURL": user.profile_picture,
            "userListings": user.posts,
            # "favoriteListings": [favorite_listing]
        }
        return jsonify(user_data)
    else:
        return jsonify({"error":"User not found"}), 404
    
@get_bp.route('/posts/<id>')
def get_post(id):
    post = Post.query.get(id)
    if post:
        listing_data = {
            "id": post.id,
            "userID": post.user_id,
            "title": post.title,
            "apartmentComplexName": post.apartment_complex_name,
            "price": post.price,
            "period": post.period,
            "roommateCount": post.roommate_count,
            "summary": post.summary,
            "roommateBio": post.roommate_bio,
            "presentPetTypes": post.present_pet_types,
            "propertyType": post.property_type,
            "latitude": post.latitude,
            "longitude": post.longitude,
            "milesToCampus": post.milesToCampus,
            "walkTime": post.walk_time,
            "bikeTime": post.bike_time,
            "busRoutesCount": 3,
            "driveTime": post.drive_time,
            "gender": post.gender_preferences,
            "nationality": post.nationalities,
            "adaAccessible": post.ada_accessible,
            "proximityToStores": post.proximity_to_stores,
            "rentPeriodStart": post.rent_period_start.isoformat(),  # ISO 8601 formatted date
            "rentPeriodEnd": post.rent_period_end.isoformat(),
            "leaseLength": post.lease_length,
            "utilitiesIncluded": post.utilities_included,
            "furnished": post.furnished,
            "squareFootage": post.square_footage,
            "bathroomCount": post.bathroom_count,
            "bedroomCount": post.bedroom_count,
            "petsAllowed": post.pets_allowed,
            "postPublishedDate": post.post_published_date.isoformat(),
            "depositRequired": post.deposit_required,
            "leaseType": post.lease_type,
            "imagesURLs": post.images_urls,
            "urlToListing": post.url_to_listing,
            "smokingAllowed": post.smoking_allowed,
            "parkingAvailable": post.parking_available,
            "customFields": post.custom_fields
        }
        return jsonify(listing_data)
    else:
        return jsonify({"error":"Listing not found"}), 404