from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Local Storage Path
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")  # Store images in the "uploads" directory
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the directory if it doesn't exist

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Upload image endpoint
@app.route('/upload_image', methods=['POST'])
def upload_image():
    event_id = request.form.get('event_id')
    image_file = request.files.get('image')

    if not event_id or not image_file:
        return jsonify({"error": "missing event_id and image"}), 400

    # Secure filename
    filename = secure_filename(image_file.filename)
    storage_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Save image locally
    try:
        image_file.save(storage_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save image: {str(e)}"}), 500

    # Return image name for database storage
    return jsonify({"image_name": filename}), 200

# Remove image endpoint
@app.route('/remove_image', methods=['POST'])
def remove_image():
    image_name = request.form.get('image_name')

    if not image_name:
        return jsonify({"error": "missing image_name"}), 400

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)

    # Check if the file exists before deleting
    if os.path.exists(image_path):
        try:
            os.remove(image_path)
            return jsonify({"message": "Image removed successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to delete image: {str(e)}"}), 500
    else:
        return jsonify({"error": "Image not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)