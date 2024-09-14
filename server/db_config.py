import os
from flask_sqlalchemy import SQLAlchemy

# This can be set using environment variables or directly here
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To suppress a warning

db = SQLAlchemy()