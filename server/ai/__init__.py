from flask import Blueprint

ai_bp = Blueprint('ai_bp', __name__)

# Import routes to register them with the blueprint
from . import routes
