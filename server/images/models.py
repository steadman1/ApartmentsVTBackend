from server.config import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)  # URL to the image
    location = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<Image {self.url}>'
