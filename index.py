from flask import Flask, request, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)

# Configuring upload folder and allowed file formats
SUFFIX = {'png', 'jpg', 'jpeg', 'svg'}

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")  # Set your Supabase URL as an environment variable
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")  # Set your Supabase Anon Key as an environment variable

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Check for allowed file format
def file_format(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in SUFFIX

@app.route('/')
def home():
    return "Welcome to the Image Upload API!"

# Endpoint to upload an image
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400
    file = request.files['image']
    event_id = request.form.get('event_id')

    if file and file_format(file.filename):
        # Generate the filename
        filename = f"{event_id}_{file.filename}"

        # Upload file to Supabase Storage
        bucket = "mybucket"
        try:
            # Upload file to Supabase
            response = supabase.storage.from_(bucket).upload(filename, file)
            if response.status_code == 200:
                # If the upload is successful, return the URL to the image
                image_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{filename}"
                return jsonify({'image_url': image_url}), 200
            else:
                return jsonify({'error': 'Failed to upload image'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

# Endpoint for getting the image
@app.route('/get_image', methods=['GET'])
def get_image():
    event_id = request.args.get('event_id')

    for suffix in SUFFIX:
        filename = f"{event_id}.{suffix}"

        # Check if image exists in Supabase storage
        try:
            # Get the URL of the image from Supabase
            bucket = "mybucket"
            file_url = supabase.storage.from_(bucket).get_public_url(filename)

            if file_url:
                return jsonify({'image_url': file_url}), 200
            else:
                return jsonify({'error': 'Image not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Endpoint for removing image
@app.route('/remove_image', methods=['POST'])
def remove_image():
    event_id = request.form.get('event_id')

    for suffix in SUFFIX:
        filename = f"{event_id}.{suffix}"
        try:
            bucket = "mybucket"
            response = supabase.storage.from_(bucket).remove([filename])

            if response.status_code == 200:
                return jsonify({'message': 'Image removed successfully'}), 200
            else:
                return jsonify({'error': 'Failed to remove image'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
