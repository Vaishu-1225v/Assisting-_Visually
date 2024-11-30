import streamlit as st
from PIL import Image
import pytesseract
import pyttsx3
import google.generativeai as genai
import threading  # Add threading module for running speech synthesis in a separate thread

# Set path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Soberr\AppData\Local\Tesseract-OCR\tesseract.exe'  

# Initialize Google Generative AI with API Key
genai.configure(api_key="AIzaSyDUDkjE1JHK3GkY8-_Es1j7qs6LMffWsmI")

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Set up Streamlit page
st.set_page_config(page_title="VisionAid", layout="wide")
st.title("AI Powered Solution for Assisting Visually Impaired Individuals")
st.sidebar.title("🔧 Available Features")
st.sidebar.markdown("""
- Scene Interpretation
- Speech Conversion
- Object & Obstacle Recognition
""")

# Functions for processing the tasks

def extract_text_from_image(image: Image) -> str:
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)

def text_to_speech(text: str) -> None:
    """Converts the given text to speech, running in a separate thread to avoid blocking."""
    def speak():
        engine.say(text)
        engine.runAndWait()

    # Run the speak function in a separate thread
    thread = threading.Thread(target=speak)
    thread.start()

def generate_scene_description(input_prompt: str, image_data: list) -> str:
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def prepare_image_data(uploaded_file) -> list:
    """Prepares the uploaded image data for processing."""
    if uploaded_file is not None:
        image_data = [{
            "mime_type": uploaded_file.type,
            "data": uploaded_file.getvalue()
        }]
        return image_data
    else:
        raise FileNotFoundError("No file uploaded.")

# UI Components for Image Upload and Interaction
uploaded_file = st.file_uploader("📤 Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Interaction buttons for tasks
col1, col2, col3 = st.columns(3)
scene_button = col1.button("🔍 Describe Scene")
ocr_button = col2.button("📝 Extract Text")
tts_button = col3.button("🔊 Text-to-Speech")

# Input Prompt for Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
"""

# Main logic for handling user interaction
if uploaded_file:
    image_data = prepare_image_data(uploaded_file)

    # Scene description functionality
    if scene_button:
        with st.spinner("Generating scene description..."):
            scene_description = generate_scene_description(input_prompt, image_data)
            st.subheader("Scene Description")
            st.write(scene_description)

    # OCR functionality for text extraction
    if ocr_button:
        with st.spinner("Extracting text from image..."):
            extracted_text = extract_text_from_image(image)
            st.subheader("Extracted Text")
            st.write(extracted_text)

    # Text-to-Speech conversion for extracted text
    if tts_button:
        with st.spinner("Converting text to speech..."):
            extracted_text = extract_text_from_image(image)
            if extracted_text.strip():
                text_to_speech(extracted_text)  # Run in separate thread
                st.success("Text-to-Speech Conversion Completed!")
            else:
                st.warning("No text found in the image.")

else:
    st.info("Please upload an image to begin.")
  
# Footer with credits
st.markdown("""
    <hr>
    <footer style="text-align:center;">
        <p><strong>© VisionAid | Built with ❤ using Streamlit</strong></p>
    </footer>
""", unsafe_allow_html=True)
