from server.config import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Basic details
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)  # Monthly rent in USD
    roommate_count = db.Column(db.Integer)
    summary = db.Column(db.Text)  # Short description of the sublease
    roommate_bio = db.Column(db.Text)  # Introduction to the roommates

    # Present pet types (array of strings)
    present_pet_types = db.Column(db.JSON)  # Requires SQLAlchemy 1.1+
    
    # Location details
    address = db.Column(db.String(255))  # Street address of the property
    
    # Commute times
    walk_time = db.Column(db.Integer)  # Minutes to campus by walking
    bike_time = db.Column(db.Integer)  # Minutes to campus by bike
    drive_time = db.Column(db.Integer)  # Minutes to campus by driving
    
    # Bus routes (array of strings)
    bus_routes_count = db.Column(db.Integer)
    
    # Preferences and attributes
    gender_preferences = db.Column(db.JSON)  # Array of strings (optional)
    nationalities = db.Column(db.JSON)  # Array of strings (optional)
    ada_accessible = db.Column(db.Boolean)  # Whether ADA accessible
    proximity_to_stores = db.Column(db.JSON)  # Array of strings
    
    # Lease and rent details
    rent_period_start = db.Column(db.Date)
    rent_period_end = db.Column(db.Date)
    lease_length = db.Column(db.String(50))  # e.g., "12 months"
    utilities_included = db.Column(db.JSON)  # Array of strings
    furnished = db.Column(db.Boolean)
    square_footage = db.Column(db.Integer)
    bathroom_count = db.Column(db.Integer)
    bedroom_count = db.Column(db.Integer)
    pets_allowed = db.Column(db.Boolean)
    deposit_required = db.Column(db.Integer)  # Security deposit amount
    lease_type = db.Column(db.String(50))  # e.g., "Sublease", "Full Lease"
    
    # Publication details
    post_published_date = db.Column(db.DateTime, default=datetime.utcnow)
    url_to_listing = db.Column(db.String(255))
    
    # Custom fields (dictionary)
    custom_fields = db.Column(db.JSON)
    
    # Relationship to images
    images = db.relationship('Image', backref='post')

    # Additional details
    apartment_complex_name = db.Column(db.String(255))
    period = db.Column(db.String(50))
    property_type = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Additional preferences and attributes
    smoking_allowed = db.Column(db.Boolean, default=False)
    parking_available = db.Column(db.Boolean, default=False)
    
    # Images URLs
    images_urls = db.Column(db.JSON)  # Stores a list of URLs as JSON

    favoriteListing = db.Column(db.Boolean)
    milesToCampus = db.Column(db.Float)
    languages = db.Column(db.JSON)


    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'price': self.price,
            'roommate_count': self.roommate_count,
            'summary': self.summary,
            'roommate_bio': self.roommate_bio,
            'present_pet_types': self.present_pet_types,
            'address': self.address,
            'walk_time': self.walk_time,
            'bike_time': self.bike_time,
            'drive_time': self.drive_time,
            'bus_routes_count': self.bus_routes_count,
            'gender_preferences': self.gender_preferences,
            'nationalities': self.nationalities,
            'ada_accessible': self.ada_accessible,
            'proximity_to_stores': self.proximity_to_stores,
            'rent_period_start': self.rent_period_start,
            'rent_period_end': self.rent_period_end,
            'lease_length': self.lease_length,
            'utilities_included': self.utilities_included,
            'furnished': self.furnished,
            'square_footage': self.square_footage,
            'bathroom_count': self.bathroom_count,
            'bedroom_count': self.bedroom_count,
            'pets_allowed': self.pets_allowed,
            'deposit_required': self.deposit_required,
            'lease_type': self.lease_type,
            'apartment_complex_name': self.apartment_complex_name,
            'period': self.period,
            'property_type': self.property_type,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'smoking_allowed': self.smoking_allowed,
            'parking_available': self.parking_available,
            'images_urls': self.images_urls,
            'favoriteListing': self.favoriteListing,
            'milesToCampus': self.milesToCampus,
            'url_to_listing': self.url_to_listing,
            'languages':self.languages
        }

    
    def __repr__(self):
        return f'<Post {self.title}>'
