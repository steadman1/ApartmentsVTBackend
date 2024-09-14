from flask import Flask
from example import example_bp

app = Flask(__name__)


app.register_blueprint(example_bp)

@app.route('/', methods=["GET"])
def hello_world():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)