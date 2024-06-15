import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image


# Function to load and preprocess the image.
def load_image(image_path):
    
    # Load the image.
    image = Image.open(image_path)
    
    # Resize the image.
    img = image.resize((224, 224))
 
    # Convert image to numpy array.
    img_array = np.array(img)

    # Normalize the image array.
    img_array = img_array / 255.0
    
    # Add a batch dimension.
    image_tensor = np.expand_dims(img_array, axis=0)
    
    return image_tensor





def predict_image(model, image_path):
    
    
    # Load and preprocess the image
    image_tensor = load_image(image_path)
    
    # Predict the class probabilities
    probability_prediction = model.predict( image_tensor)

    # # Round up probabilities
    # prediction = np.round(probability_prediction)
    rounded_probability = [prob for prob in probability_prediction[0][0]]
    
    return round(rounded_probability, 4) 

