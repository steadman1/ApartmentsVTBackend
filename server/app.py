from flask import Flask

app = Flask(__name__)

from posts import posts_bp
app.register_blueprint(posts_bp)

@app.route('/', methods=["GET"])
def hello_world():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)