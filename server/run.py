from server import create_app
from server.db_config import db

app = create_app()

if __name__ == '__main__':
    from server.auth.models import User
    from server.posts.models import Post
    from server.images.models import Image

    with app.app_context():
        db.create_all()

    app.run(debug=True)