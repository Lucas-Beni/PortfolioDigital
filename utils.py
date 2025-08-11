import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, folder='uploads'):
    """Save uploaded file and return the filename"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        
        # Create upload path
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, filename)
        
        # Save and optimize image
        try:
            image = Image.open(file.stream)
            
            # Convert RGBA to RGB if necessary
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            
            # Resize if too large
            max_size = (1200, 1200)
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save with optimization
            image.save(file_path, optimize=True, quality=85)
            
            # Return relative path for database storage
            return f"{folder}/{filename}"
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
    
    return None

def delete_file(file_path):
    """Delete a file from the upload folder"""
    if file_path:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
        try:
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
        except Exception as e:
            print(f"Error deleting file: {e}")
    return False
