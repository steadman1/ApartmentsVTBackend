from flask import Flask
from server.db_config import Config, db


app = Flask(__name__)
app.config.from_object(Config)

from server.auth.models import User
from server.posts.models import Post

from server.auth import auth_bp
app.register_blueprint(auth_bp)

from server.images import images_bp
app.register_blueprint(images_bp)

from server.posts import posts_bp
app.register_blueprint(posts_bp)

with app.app_context():
    db.create_all()


@app.route('/', methods=["GET"])
def hello_world():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)