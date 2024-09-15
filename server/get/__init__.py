from flask import Blueprint

get_bp = Blueprint(
    "get",
    __name__,
    template_folder="templates",
    static_folder="static"
)

from server.get import routes