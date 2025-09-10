from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from database import get_plant_info
from chatbot import get_chatbot_response
from model import load_my_model, predict_plant

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',  # prevents cross site request forgery
    SESSION_COOKIE_SECURE=False
)
# Allow localhost on any port

CORS(app, supports_credentials=True, origins=["http://localhost:*", "http://127.0.0.1:*"])

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model once
model = load_my_model("E:\\MAJOR_PROJECT(srishti)\\MobileNetv2.keras")

# Valid plant types (modify according to your model's classes)
VALID_PLANT_TYPES = {'rose', 'daisy', 'sunflower', 'tulip', 'dandelion'}  # Add your 5 flower types


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a PNG, JPG, or JPEG image.'}), 400

    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Predict plant
        plant_name = predict_plant(filepath, model)

        # Check if predicted plant is in valid types
        if plant_name.lower() not in VALID_PLANT_TYPES:
            return jsonify({'error': 'invalid_plant'}), 400

        # Get plant info
        plant_info = get_plant_info(plant_name)

        # Store in session for chatbot
        session['identified_plant'] = plant_name

        # Clean up
        os.remove(filepath)

        return jsonify({'name': plant_name, 'info': plant_info}), 200

    except Exception as e:
        # Clean up on error
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500


@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        print("Received data in /chatbot:", data)
        query = data.get('query', '')
        print("Query:", query)

        if not query:
            return jsonify({'error': 'No query provided'}), 400

        identified_plant = session.get('identified_plant')
        print("Identified plant from session:", identified_plant)

        if not identified_plant:
            return jsonify({'error': 'No plant identified yet'}), 400

        # Add context to query
        contextualized_query = f"Regarding the {identified_plant} plant, {query}"
        print("Contextualized query:", contextualized_query)
        response = get_chatbot_response(contextualized_query)
        print("Chatbot function returned:", response)

        return jsonify({'response': response}), 200

    except Exception as e:
        print("Error in chatbot route:", str(e))
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
