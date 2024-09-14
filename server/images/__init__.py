from flask import Blueprint

images_bp = Blueprint(
    "images",
    __name__,
    url_prefix="/images",
    template_folder="templates",
    static_folder="static"
)

from server.images import routes
