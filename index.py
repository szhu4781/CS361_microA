from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for images
image_storage = {}

# Upload image endpoint
@app.route('/upload_image', methods=['POST'])
def upload_image():
    event_id = request.form.get('event_id')
    image_file = request.files.get('image')

    if not event_id or not image_file:
        return jsonify({"error": "missing event_id and image"}), 404

    # Save the image
    image_storage[event_id] = image_file.read()
    return jsonify({"image_url": f"https://cs-361-micro-a.vercel.app/get_image?event_id={event_id}"}), 200

# Get image endpoint
@app.route('/get_image', methods=['GET'])
def get_image():
    event_id = request.args.get('event_id')

    if event_id not in image_storage:
        return jsonify({"error": "Image not found"}), 404

    return jsonify({"image_url": f"https://cs-361-micro-a.vercel.app/get_image?event_id={event_id}"}), 200

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