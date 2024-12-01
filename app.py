import os
import base64
import io
from dotenv import load_dotenv
from PIL import Image
import pyttsx3
import pytesseract
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from spinner_animation import render_animation

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found! Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

# Set page title, favicon, and layout
st.set_page_config(
    page_title="Perceiva - AI Assistant for Visually Impaired",
    page_icon="👁️‍🗨️",
    layout="centered",
)

# Custom CSS
custom_css = """
<style>
/* General App Style */
body {
    font-family: 'Arial', sans-serif;
    background-color: #f9f9f9;
    color: #333;
    margin: 0;
    padding: 0;
}

/* Title Styling */
h1 {
    color: #ff4b4b;
    text-align: center;
    margin-bottom: 20px;
    font-size: 2.5em;
    text-shadow: 1px 1px 2px #ccc;
}

/* Sidebar Styling */
.sidebar .sidebar-content {
    background-color: #333;
    color: #fff;
    border-right: 2px solid #4CAF50;
}

.sidebar .sidebar-content h1, 
.sidebar .sidebar-content h2, 
.sidebar .sidebar-content h3 {
    color: #fff;
}

/* Buttons Styling */
button {
    background-color: #ff4b4b;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 15px;
    cursor: pointer;
    transition: opacity 0.3s ease;
}

button:hover {
    opacity: 0.8;
}

/* File Uploader Styling */
.css-1dp5vir {
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 15px;
}

/* Info and Warning Messages */
.st-warning {
    background-color: #fffbe5;
    color: #856404;
    border: 1px solid #ffeeba;
    border-radius: 5px;
    padding: 10px;
    font-size: 1.1em;
}
</style>
"""

# Apply Custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Initialize Chat Model
chat_model = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-1.5-pro")

# App Title
st.title("👁️‍🗨️Perceiva - AI Assistant for Visually Impaired")

# Helper: Text-to-Speech Conversion
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed
    engine.setProperty('volume', 1)  # Volume
    audio_file = "text-to-speech-local.mp3"
    
    try:
        engine.save_to_file(text, audio_file)
        engine.runAndWait()
        st.audio(audio_file, format="audio/mp3")
    except Exception as e:
        st.error(f"Audio generation failed: {e}")

# Feature 1: Real-Time Scene Understanding
def real_time_scene_understanding(image_base64):
    hmessage = HumanMessage(
        content=[{
            "type": "text", 
            "text": """You are a real-time scene interpreter for visually impaired users. Your task is to analyze and describe images vividly, empathetically, and without technical jargon. Focus on delivering concise, actionable information that enhances understanding and safety."""},
            {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
        ]
    )
    try:
        response = chat_model.invoke([hmessage])
        response_text = response.content
        st.write(response_text)
        text_to_speech(response_text)
    except Exception as e:
        st.error(f"Scene understanding failed: {e}")

# Feature 2: Text Extraction
def text_extraction(uploaded_image):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    try:
        extracted_text = pytesseract.image_to_string(uploaded_image)
        st.write(extracted_text)
        text_to_speech(extracted_text)
    except Exception as e:
        st.error(f"Text extraction failed: {e}")

# Feature 3: Object Detection
def object_detection(image_base64):
    hmessage = HumanMessage(
        content=[{
            "type": "text", 
            "text": """You are a visual accessibility specialist analyzing images to help visually impaired individuals navigate safely. Your goal is to provide detailed yet concise descriptions of visible objects and obstacles, prioritizing safety and situational awareness."""},
            {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
        ]
    )
    try:
        response = chat_model.invoke([hmessage])
        response_text = response.content
        st.write(response_text)
        text_to_speech(response_text)
    except Exception as e:
        st.error(f"Object detection failed: {e}")

# Feature 4: Personalized Assistance
def personal_assistance(image_base64):
    hmessage = HumanMessage(
        content=[{
            "type": "text", 
            "text": """As an assistive technology specialist, your role is to provide personalized, context-specific support for visually impaired users. Deliver clear, actionable descriptions to empower users with confidence and enhance accessibility."""},
            {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
        ]
    )
    try:
        response = chat_model.invoke([hmessage])
        response_text = response.content
        st.write(response_text)
        text_to_speech(response_text)
    except Exception as e:
        st.error(f"Personalized assistance failed: {e}")

# Upload and process the image
uploaded_image = st.file_uploader("📤Upload an image", type=["jpg", "jpeg", "png"])
    
# Feature selection
feature = st.sidebar.radio(
    "Select a functionality🔧:",
    [
        "Real-Time Scene Understanding",
        "Text-to-Speech Conversion",
        "Object Detection",
        "Personalized Assistance",
    ],
    index=0,
)

if uploaded_image:
    # Display uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Trigger corresponding feature
    if feature == "Real-Time Scene Understanding":
        if st.button("🔍 Run Scene Understanding"):
            with st.spinner("Please be patient..."):
                render_animation()
                real_time_scene_understanding(image_base64)
                
    elif feature == "Text-to-Speech Conversion":
        if st.button("📜 Convert Text-to-Speech"):
            with st.spinner("Please be patient..."):
                render_animation()
                text_extraction(image)
                
    elif feature == "Object Detection":
        if st.button("🕵️‍♂️ Run Object Detection"):
            with st.spinner("Please be patient..."):
                render_animation()
                object_detection(image_base64)
                
    elif feature == "Personalized Assistance":
        if st.button("ℹ️ Run Personalized Assistance"):
            with st.spinner("Please be patient..."):
                render_animation()
                personal_assistance(image_base64)

else:
    st.info("Please Upload Image to Proceed...!")        