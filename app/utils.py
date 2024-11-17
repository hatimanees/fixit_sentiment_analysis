# app/utils.py
import os
from werkzeug.utils import secure_filename
import uuid


def save_uploaded_file(content, upload_folder):
    """Save content to a file and return the file path"""
    filename = f"{uuid.uuid4().hex}.txt"
    file_path = os.path.join(upload_folder, secure_filename(filename))

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return file_path