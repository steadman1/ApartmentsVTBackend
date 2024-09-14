from ..app import db
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Assuming a User model exists
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    # Other user fields like username, email, etc.

class Post(db.Model):
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to link to the user who created the post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    
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
    bus_routes = db.Column(db.JSON)
    
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
    images = db.relationship('Image', backref='post', lazy=True)
    
    def __repr__(self):
        return f'<Post {self.title}>'

class Image(db.Model):
    __tablename__ = 'image'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)  # URL to the image
    
    def __repr__(self):
        return f'<Image {self.url}>'
