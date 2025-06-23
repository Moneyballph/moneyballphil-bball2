
import streamlit as st
from PIL import Image
import base64
import io

# Set page config
st.set_page_config(layout="wide")

# Load and encode background
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    css = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64_string}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Background image
set_background("arena_background.png")

# Logo
logo = Image.open("moneyball_logo.png")
st.image(logo, width=200)

# Title
st.markdown("<h1 style='text-align: center; color: white;'>MoneyBall Phil Basketball Simulator</h1>", unsafe_allow_html=True)

# Player input section
st.header("🏀 Player Input")
col1, col2 = st.columns(2)
with col1:
    player_name = st.text_input("Player Name")
    team = st.text_input("Team")
    position = st.selectbox("Position", ["PG", "SG", "SF", "PF", "C"])
with col2:
    opponent = st.text_input("Opponent Team")
    stat_type = st.radio("Stat Type to Simulate", ["PRA", "Points Only"])
    points = st.number_input("Points", min_value=0.0)
    rebounds = st.number_input("Rebounds", min_value=0.0)
    assists = st.number_input("Assists", min_value=0.0)
    defense_vs_position = st.number_input("Opponent DEF Rank vs Pos (1-30)", min_value=1, max_value=30)

# Simulate button
if st.button("Simulate"):
    import random
    hit_chance = random.uniform(0.55, 0.88)  # Placeholder logic
    st.success(f"✅ {player_name}'s true hit probability for {stat_type}: {round(hit_chance * 100, 2)}%")

# Top Player Board (placeholder)
st.header("📈 Top Player Board")
st.table({
    "Player": ["Sample A", "Sample B"],
    "Stat": ["PRA", "Points"],
    "Hit %": ["82.4%", "76.5%"],
})

# Parlay Evaluator (placeholder)
st.header("💰 Parlay Evaluator")
st.write("Coming soon: Evaluate 2-leg parlays based on real-time hit probabilities.")
