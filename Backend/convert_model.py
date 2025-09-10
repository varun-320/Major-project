import tensorflow as tf
import os
import shutil

# Path to your old model
old_model_path = r"E:\MAJOR_PROJECT(srishti)\MobileNetv2.keras"
# Path to save the new model
new_model_path = r"E:\MAJOR_PROJECT(srishti)\MobileNetv2_tf215.keras"
# Temporary directory for SavedModel format
temp_dir = "temp_model"

try:
    # Create a temporary directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # Try to load and save in SavedModel format
    print("Attempting to load model...")
    model = tf.keras.models.load_model(old_model_path, compile=False)
    
    print("Saving model in SavedModel format...")
    tf.saved_model.save(model, temp_dir)
    
    print("Loading from SavedModel format...")
    loaded_model = tf.saved_model.load(temp_dir)
    
    print("Converting to Keras format...")
    keras_model = tf.keras.models.Model.from_config(model.get_config())
    keras_model.set_weights(model.get_weights())
    
    print("Saving final model...")
    keras_model.save(new_model_path, save_format='keras')
    
    print(f"Model successfully converted and saved to {new_model_path}")
    
except Exception as e:
    print(f"Error during conversion: {str(e)}")
    print("\nPlease try one of these solutions:")
    print("1. If you have the original training code, re-save the model with TensorFlow 2.15.0")
    print("2. Create a new virtual environment with Python 3.7 and TensorFlow 2.2.0")
    print("3. Contact the model creator for a version compatible with TensorFlow 2.15.0")

finally:
    # Clean up temporary directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir) 