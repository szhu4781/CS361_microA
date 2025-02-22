from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configuring upload folder and allowed file formats
UPLOAD_FOLDER = 'uploads'
SUFFIX = {'png', 'jpg', 'jpeg', 'svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the image folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check for allowed file format
def file_format(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in SUFFIX

# Endpoint to upload an image
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400
    file = request.files['image']
    event_id = request.form.get('event_id')

    # Check if the file format is correct
    # if it's correct, then image is uploaded and stored in a folder
    # Return the image url if successful
    if file and file_format(file.filename):
        filename = f"{event_id}_{file.filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = f"/{UPLOAD_FOLDER}/{filename}"
        return jsonify({'image_url': image_url}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

#Endpoint for getting the image
@app.route('/get_image', methods=['GET'])
def get_image():
    event_id = request.args.get('event_id')

    for suffix in SUFFIX:
        filename = f"{event_id}.{suffix}"
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Check for the existing image in the image folder
        if os.path.exists(img_path):
            return jsonify({'image_url': img_path}), 200
        else:
            return jsonify({'error': 'Image not found'}), 404

#Endpoint for removing image
@app.route('/remove_image', methods=['POST'])
def remove_image():
    event_id = request.form.get('event_id')

    for suffix in SUFFIX:
        filename = f"{event_id}.{suffix}"
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check for the existing image in the image folder
        if os.path.exists(img_path):
            os.remove(img_path)
            return jsonify({'message': 'Image removed succesfully'}), 200
        else:
            return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
