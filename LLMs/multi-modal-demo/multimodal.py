import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(input_text, image, prompt):
    # Loading the model
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if the uploaded file is an image
    if uploaded_file is not None:
        # Read the image into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise ValueError("No image uploaded")

# Initialize Streamlit app
st.title("Gemini Multi-Modal Demo")

# Create input fields
input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Default system prompt
system_prompt = """
You are an expert in analyzing images and text. Provide a detailed description of the image and answer any questions based on the input prompt provided by the user.
"""

# Submit button
submit = st.button("Generate Response")

# Handle submission
if submit and input_text and uploaded_file:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, system_prompt)
        st.subheader("Response")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
elif submit:
    st.warning("Please provide both an input prompt and an image.")



