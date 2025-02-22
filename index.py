from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# In-memory storage for images (for demonstration purposes)
image_storage = {}

# Upload image endpoint
@app.route('/upload_image', methods=['POST'])
def upload_image():
    event_id = request.form.get('event_id')
    image_file = request.files.get('image')

    if not event_id or not image_file:
        return jsonify({"error": "event_id and image are required"}), 400

    # Save the image (in-memory for demonstration)
    image_storage[event_id] = image_file.read()
    return jsonify({"image_url": f"http://localhost:5000/get_image?event_id={event_id}"}), 200

# Get image endpoint
@app.route('/get_image', methods=['GET'])
def get_image():
    event_id = request.args.get('event_id')

    if event_id not in image_storage:
        return jsonify({"error": "Image not found"}), 404

    return jsonify({"image_url": f"http://localhost:5000/get_image?event_id={event_id}"}), 200

# Remove image endpoint
@app.route('/remove_image', methods=['POST'])
def remove_image():
    event_id = request.form.get('event_id')

    if event_id not in image_storage:
        return jsonify({"error": "Image not found"}), 404

    del image_storage[event_id]
    return jsonify({"message": "Image removed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)