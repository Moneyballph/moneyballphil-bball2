
# Streamlit Basketball App
import streamlit as st
import base64
from PIL import Image

# Set page config
st.set_page_config(page_title="Moneyball Phil Basketball Simulator", layout="wide")

# Set background
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)

# Load background
set_background("ChatGPT Image Jun 22, 2025, 05_45_45 PM.png")

# Load logo
logo = Image.open("ChatGPT Image Jun 22, 2025, 05_53_13 PM.png")
st.image(logo, width=200)

st.title("🏀 Moneyball Phil: Basketball Prop Simulator")

st.write("This is a placeholder. Full app logic will go here...")
