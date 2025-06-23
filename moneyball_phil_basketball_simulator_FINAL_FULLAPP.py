
import streamlit as st
from PIL import Image

# Set page config
st.set_page_config(layout="wide")

# Load and set background and logo images
def set_background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = image_file.read()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string.decode('utf-8')}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Load assets
background_image = "basketball_arena_bg.png"
logo_image = Image.open("moneyball_logo_basketball.png")

# Display logo
st.image(logo_image, width=180)

# Set background
set_background(background_image)

# Title
st.title("🏀 MoneyBall Phil: Basketball Player Prop Simulator")

# Sidebar for input type
prop_type = st.sidebar.radio("Choose Prop Type", ["PRA", "Points Only"])

# Input fields
st.subheader("Enter Player Stats")
player_name = st.text_input("Player Name")
points = st.number_input("Points per Game", value=0.0)
rebounds = st.number_input("Rebounds per Game", value=0.0)
assists = st.number_input("Assists per Game", value=0.0)
usage_rate = st.number_input("Usage Rate (%)", min_value=0.0, max_value=100.0)
opponent_team = st.text_input("Opponent Team")
team_defense_rating = st.number_input("Defense vs Position Rating", value=1.0)
line = st.number_input("Prop Line", value=0.0)
odds = st.text_input("Sportsbook Odds (American)", value="-110")

# Simulation logic (simplified binomial for this version)
import numpy as np

def simulate_hit_probability(avg, line, std_dev=3.5):
    samples = np.random.normal(loc=avg, scale=std_dev, size=100000)
    return np.mean(samples > line)

def american_to_implied(odds):
    try:
        odds = int(odds)
        if odds < 0:
            return abs(odds) / (abs(odds) + 100)
        else:
            return 100 / (odds + 100)
    except:
        return 0.0

# Simulate
if st.button("Simulate Player"):
    if prop_type == "PRA":
        avg = points + rebounds + assists
    else:
        avg = points

    true_prob = simulate_hit_probability(avg, line)
    implied_prob = american_to_implied(odds)
    ev = round((true_prob - implied_prob) * 100, 2)

    st.markdown(f"**True Probability:** {true_prob:.2%}")
    st.markdown(f"**Implied Probability:** {implied_prob:.2%}")
    st.markdown(f"**Expected Value (EV):** {ev:+.2f}%")

    # Add to hit board
    if "hit_board" not in st.session_state:
        st.session_state.hit_board = []

    st.session_state.hit_board.append({
        "Player": player_name,
        "Prop Type": prop_type,
        "True %": f"{true_prob:.2%}",
        "Implied %": f"{implied_prob:.2%}",
        "EV %": f"{ev:+.2f}%"
    })

# Top Hit Board
if "hit_board" in st.session_state and st.session_state.hit_board:
    st.subheader("🔥 Top Player Board")
    st.table(st.session_state.hit_board)

# Parlay Evaluator
st.subheader("🎯 Parlay Evaluator")
player1_prob = st.number_input("Player 1 True Probability", min_value=0.0, max_value=1.0, step=0.01)
player2_prob = st.number_input("Player 2 True Probability", min_value=0.0, max_value=1.0, step=0.01)
player3_prob = st.number_input("Player 3 True Probability (Optional)", min_value=0.0, max_value=1.0, step=0.01)
parlay_odds = st.text_input("Parlay Odds (American)", "-110")

# Calculate parlay stats
if st.button("Evaluate Parlay"):
    probs = [p for p in [player1_prob, player2_prob, player3_prob] if p > 0]
    true_parlay = np.prod(probs)
    implied_parlay = american_to_implied(parlay_odds)
    parlay_ev = round((true_parlay - implied_parlay) * 100, 2)

    # Parlay zone
    if parlay_ev >= 10:
        zone = "🔥 Elite"
    elif parlay_ev >= 5:
        zone = "✅ Strong"
    elif parlay_ev >= 2:
        zone = "⚠️ Moderate"
    else:
        zone = "❌ Low"

    st.markdown(f"**True Parlay Probability:** {true_parlay:.2%}")
    st.markdown(f"**Implied Probability:** {implied_parlay:.2%}")
    st.markdown(f"**Parlay EV:** {parlay_ev:+.2f}%")
    st.markdown(f"**Parlay Zone:** {zone}")
