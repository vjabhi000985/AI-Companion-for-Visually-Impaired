from streamlit_lottie import st_lottie
import requests
import streamlit as st

# Function to load and render Lottie animation
def render_animation():
    try:
        animation_response = requests.get('https://assets1.lottiefiles.com/packages/lf20_vykpwt8b.json')
        if animation_response.status_code == 200:
            animation_json = animation_response.json()
            st_lottie(animation_json, height=200, width=300)
        else:
            st.error("Failed to load animation!")
    except Exception as e:
        st.error(f"Error loading animation: {e}")