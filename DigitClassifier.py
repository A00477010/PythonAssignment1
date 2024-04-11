import streamlit as st
from matplotlib import pyplot as plt
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps, ImageEnhance
import numpy as np
from PIL import Image
import numpy as np
from PIL import Image, ImageOps

# Load your trained model
# Ensure your model is saved in the same directory as your app or provide the full path.
MODEL_PATH = 'digit_classifier.h5'
model = load_model(MODEL_PATH)


def preprocess_image(image):
    if image.mode == 'RGBA':
        image = image.convert('RGBA')
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image = background.convert('L')  # Convert to grayscale
    elif image.mode in ['LA', 'P']:
        image = ImageOps.grayscale(image.convert('RGBA'))

    # Apply a contrast enhancement
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Factor of 2 increases contrast

    # Resize the image to 28x28 pixels, maintaining aspect ratio
    aspect_ratio = min(28 / image.size[0], 28 / image.size[1])
    new_size = (int(image.size[0] * aspect_ratio), int(image.size[1] * aspect_ratio))
    image = image.resize(new_size, Image.Resampling.LANCZOS)

    # Create a 28x28 white background
    background = Image.new('L', (28, 28), 255)
    # Calculate padding to center the image
    padding = ((28 - new_size[0]) // 2, (28 - new_size[1]) // 2)
    background.paste(image, padding)

    # Convert to NumPy array
    image_array = np.asarray(background)

    # Apply threshold to help with binarization
    threshold = 128  # This is a common default value, adjust if necessary
    image_array = (image_array > threshold) * 255

    # Normalize the pixel values
    image_array = image_array.astype(np.float32) / 255.0

    # Add channel and batch dimensions
    image_array = np.expand_dims(image_array, axis=-1)
    image_array = np.expand_dims(image_array, axis=0)

    return image_array


st.title("Digit Classifier")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("Classifying...")

    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)
    prediction = predictions.argmax()
    st.write(f'Prediction: {prediction}')

    # Convert predictions to a more readable format
    readable_predictions = [f'{prob:.4f}' for prob in predictions[0]]

    # Create a dataframe for a nicer table display
    import pandas as pd
    probs_df = pd.DataFrame({
        'Digit': list(range(10)),
        'Probability': readable_predictions
    })

    # Display the probabilities as a table
    st.dataframe(probs_df.style.highlight_max(subset=['Probability'], axis=0, color='yellow'))

