from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to get Gemini response
def get_gemini_response(input_text, image, prompt): 
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Function to handle uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit configuration
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

# User inputs
input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.")
    
    # Prepare image for Gemini API
    image_parts = input_image_setup(uploaded_file)
    
    # Generate and display Gemini response
    if st.button("Get Gemini Response"):
        prompt = "Describe the image"
        response = get_gemini_response(input_text, image_parts, prompt)
        st.write(response)
