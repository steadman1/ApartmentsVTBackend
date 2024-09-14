import os
from flask import Blueprint, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from server import db
from server.images.models import Image
from flask import current_app as app

images_bp = Blueprint("images", __name__, url_prefix="/images")

# Set the folder where uploaded images will be stored
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Ensure file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@images_bp.route('/upload', methods=['POST'])
def upload_image():
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Secure the filename and save it
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Get user_id and post_id from the form data
        user_id = request.form.get('user_id')  # Assumes user ID is sent with request
        post_id = request.form.get('post_id')  # Optional

        # Create a new Image object and store in the database
        image = Image(
            post_id=post_id,
            user_id=user_id,
            url=f'/images/uploads/{filename}',  # The URL for the uploaded image
            location=file_path  # The location of the file on the server
        )

        db.session.add(image)
        db.session.commit()

        flash('Image successfully uploaded and associated with post!')
        return redirect(url_for('images.upload_image'))  # Redirect to a success page

    flash('Invalid file type')
    return redirect(request.url)

# Route to serve uploaded files
@images_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

