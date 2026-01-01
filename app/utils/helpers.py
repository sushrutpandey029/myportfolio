import os
import secrets
from flask import current_app

def save_image(form_picture, folder='services'):
    """Saves an image to the specified folder in static/uploads and returns the filename."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    # Ensure upload directory exists
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads', folder)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        
    picture_path = os.path.join(upload_path, picture_fn)
    form_picture.save(picture_path)

    return f"uploads/{folder}/{picture_fn}"
