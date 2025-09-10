import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os


def load_my_model(model_path):
    """
    Load the pre-trained model.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"The model file at {model_path} was not found.")
    return load_model(model_path)



def preprocess_image(image_path):
    """
    Preprocess the image for model prediction.
    """
    try:
        img = Image.open(image_path).convert("RGB").resize((150, 150))
        img_array = np.array(img) / 255.0
        return np.expand_dims(img_array, axis=0)
    except Exception as e:
        raise ValueError(f"Error processing the image: {e}")


def predict_plant(image_path, model):
    """
    Predict the plant class using the trained model.
    """
    try:
        img_array = preprocess_image(image_path)
        predictions = model.predict(img_array)
        plant_classes = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']  # Replace with actual class labels
        return plant_classes[np.argmax(predictions)]
    except Exception as e:
        raise ValueError(f"Error during prediction: {e}")


if __name__ == "__main__":
    # Update paths as necessary
    model_path = r"C:\\Users\\ASUS\Documents\\MAJOR_PROJECT\\MobileNetv2.keras"  # Using raw string to handle backslashes

    image_path = "C:\\Users\\ASUS\\Documents\\MAJOR_PROJECT\\test_images\\test_image.jpg"

    try:
        model = load_model(model_path)
        result = predict_plant(image_path, model)
        print(f"Predicted Plant: {result}")
    except Exception as e:
        print(e)



