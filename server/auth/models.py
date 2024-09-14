from server.db_config import db

class User(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic user information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    password_salt = db.Column(db.String(20), nullable=False)
    
    # Additional user details
    bio = db.Column(db.Text, nullable=True)
    nationality = db.Column(db.String(60), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)  # URL to profile picture
    
    # Relationship to posts
    posts = db.relationship('Post', backref='user')
    
    def __repr__(self):
        return f'<User {self.username}>'
