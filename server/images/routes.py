from server.images import images_bp
import os
from flask import request, jsonify, send_file, current_app
from server.config import db
from server.images.models import Image
from server.posts.models import Post
from server.auth.models import User
from flask_jwt_extended import get_jwt_identity, jwt_required

# Set the folder where uploaded images will be stored
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@images_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_image():
    try: 
        data = request.json()
    except:
        data = []
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    image_id = Image.query.count() + 1

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    extension = file.filename.rsplit('.', 1)[1].lower()

    if file and extension in ALLOWED_EXTENSIONS:
        filename = str(image_id) + f".{extension}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if 'post_id' in data:
            post_id = data['post_id']
            post = Post.query.get(post_id)
            image = Image(
                post=post,
                user=user,
                url=f'/images/{filename}',  # The URL for the uploaded image
                location=file_path  # The location of the file on the server
            )
        else:
            image = Image(
                user=user,
                url=f'/images/{filename}',  # The URL for the uploaded image
                location=file_path  # The location of the file on the server
            )


        # Create a new Image object and store in the database


        db.session.add(image)
        db.session.commit()

        return jsonify({"success": f"{request.host_url}images/{filename}"}), 200

    return jsonify(msg="Invalid file type"), 400

# Route to serve uploaded files
@images_bp.route('/<filename>')
def uploaded_file(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    return send_file(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), mimetype=f'image/{extension}')

