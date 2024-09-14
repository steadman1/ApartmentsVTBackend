from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db_config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from posts import posts_bp
app.register_blueprint(posts_bp)

@app.route('/', methods=["GET"])
def hello_world():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)