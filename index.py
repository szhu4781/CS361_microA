from flask import Flask, request, jsonify
import os
from supabase import create_client, Client
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Supabase Configuration
SUPABASE_URL = "https://jqdqxziuzgfllzhaingt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpxZHF4eml1emdmbGx6aGFpbmd0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAxOTUxNTAsImV4cCI6MjA1NTc3MTE1MH0.c2iwEe1UKWgn1bR-LGnAC_RK0cdjWtZ2BHHQlpLOnBI"
BUCKET_NAME = "mybucket"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Upload image endpoint
@app.route('/upload_image', methods=['POST'])
def upload_image():
    event_id = request.form.get('event_id')
    image_file = request.files.get('image')

    if not event_id or not image_file:
        return jsonify({"error": "missing event_id and image"}), 404

    # Secure filename
    filename = secure_filename(image_file.filename)
    storage_path = f"{event_id}/{filename}"

    # Upload to Supabase Storage
    response = supabase.storage.from_(BUCKET_NAME).upload(storage_path, image_file)

    if response.status_code != 200:
        return jsonify({"error": "Failed to upload image"}), 500

    # Get public URL
    image_url = supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)

    return jsonify({"image_url": image_url}), 200

# Remove image endpoint
@app.route('/remove_image', methods=['POST'])
def remove_image():
    image_path = request.form.get('image_path')  # Should store this in the database

    if not image_path:
        return jsonify({"error": "missing image_path"}), 404

    # Delete from Supabase Storage
    response = supabase.storage.from_(BUCKET_NAME).remove([image_path])

    if response.status_code != 200:
        return jsonify({"error": "Failed to delete image"}), 500

    return jsonify({"message": "Image removed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
