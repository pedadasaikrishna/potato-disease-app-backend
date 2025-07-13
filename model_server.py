from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)
CORS(app)  # Allow frontend (port 5500) to access this backend

model = tf.keras.models.load_model('potato_disease_model.keras')
class_names = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(image_file.filename):
        return jsonify({'error': 'Invalid image format. Please use PNG or JPG'}), 400

    try:
        image = Image.open(image_file).convert('RGB').resize((256, 256))
        img_array = tf.keras.utils.img_to_array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]) * 100)

        return jsonify({'predicted_class': predicted_class, 'confidence': confidence})
    except UnidentifiedImageError:
        return jsonify({'error': 'Unable to process the image. Ensure it is a valid PNG or JPG.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
