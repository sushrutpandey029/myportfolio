"""
Helper Utilities Module
Common helper functions used across the application:
- Image Upload & Processing
- File Management
- Data Formatting
"""

# =========================================
# STANDARD LIBRARY IMPORTS
# =========================================
import os
import secrets

# =========================================
# THIRD-PARTY IMPORTS
# =========================================
from flask import current_app


# =========================================
# IMAGE HANDLING FUNCTIONS
# =========================================

def save_image(form_picture, folder='services'):
    """
    Save an uploaded image to the specified folder.
    
    Args:
        form_picture: FileStorage object from form
        folder: Target folder name within static/uploads
        
    Returns:
        str: Relative path to saved image
    """
    # Generate unique filename
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    # Ensure upload directory exists
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads', folder)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        
    # Save file
    picture_path = os.path.join(upload_path, picture_fn)
    form_picture.save(picture_path)

    return f"uploads/{folder}/{picture_fn}"
