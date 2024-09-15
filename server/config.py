import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# This can be set using environment variables or directly here
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

class Config:
    UPLOAD_FOLDER = os.path.join(PARENT_DIR, 'image_uploads')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PARENT_DIR, 'main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To suppress a warning
    
    # General Flask settings
    SECRET_KEY = 'your_secret_key_here'

    # JWT-specific settings
    JWT_SECRET_KEY = 'your_jwt_secret_key_here'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)  # Access token valid for 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=90)  # Refresh token valid for 30 days
    JWT_ALGORITHM = 'HS256'  # Specify the signing algorithm (default: HS256)
    JWT_TOKEN_LOCATION = ['headers']  # Tokens will be accepted in the headers

db = SQLAlchemy()
jwt = JWTManager()