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
            "milesToCampus": 2.0,
            "walkTime": 15,
            "bikeTime": 8,
            "busRoutesCount": 3,
            "driveTime": 5,
            "gender": ["Male"],
            "nationality": ["American"],
            "adaAccessible": True,
            "proximityToStores": ["Walmart", "Starbucks", "McDonald's"],
            "rentPeriodStart": "2023-09-14T00:00:00Z",  # ISO 8601 formatted date
            "rentPeriodEnd": "2024-09-14T00:00:00Z",
            "leaseLength": "12 months",
            "utilitiesIncluded": ["Water", "Electricity", "Internet"],
            "furnished": True,
            "squareFootage": 1200,
            "bathroomCount": 2,
            "bedroomCount": 2,
            "petsAllowed": True,
            "postPublishedDate": "2023-09-14T00:00:00Z",
            "depositRequired": 500,
            "leaseType": "Full Lease",
            "imagesURLs": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            "urlToListing": "https://example.com/listings/apartment1",
            "smokingAllowed": False,
            "parkingAvailable": True,
            "customFields": {
                "Pool": "Yes",
                "Gym": "Yes"
            }
        }