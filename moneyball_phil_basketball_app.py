
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# Load assets
background_path = "images/background.png"
logo_path = "images/logo.png"

# Set page config and background
st.set_page_config(layout="wide")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url('{background_path}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

img.logo {{
    position: absolute;
    top: 10px;
    left: 10px;
    width: 150px;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.image(logo_path, width=150)

# App title
st.markdown("<h1 style='color:white;'>MoneyBall Phil Basketball Simulator</h1>", unsafe_allow_html=True)

# Mode toggle
mode = st.radio("Choose Simulation Type", ["PRA", "Points"], horizontal=True)

# Input form
with st.form("player_input"):
    col1, col2, col3 = st.columns(3)
    with col1:
        player_name = st.text_input("Player Name")
        position = st.selectbox("Position", ["PG", "SG", "SF", "PF", "C"])
    with col2:
        team = st.text_input("Team")
        opponent = st.selectbox("Opponent Team", ["LAL", "BOS", "DEN", "GSW", "MIA", "MIL", "NYK"])
    with col3:
        line = st.number_input(f"{mode} Line", min_value=0.0, value=25.0)
        team_def = st.number_input(f"{opponent} Avg {mode} Allowed to {position}s", min_value=0.0, value=24.5)

    submit = st.form_submit_button("Run Simulation")

# Run sim (placeholder logic)
if submit:
    base_mean = team_def
    simulated_avg = round(np.random.normal(base_mean, 4), 1)
    result = "Over" if simulated_avg > line else "Under"
    st.success(f"Simulated Avg: {simulated_avg} → **{result}** (Line: {line})")
