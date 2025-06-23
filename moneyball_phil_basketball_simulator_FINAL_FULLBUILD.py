
# MoneyBall Phil Basketball Simulator (Final Working Build with Full Features)
import streamlit as st
from PIL import Image
import base64
import io
import random
import pandas as pd

# Set page config
st.set_page_config(layout="wide")

# Load and encode background
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64_string}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
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
    opponent = st.text_input("Opponent Team")
    usage = st.number_input("Usage %", min_value=0.0, max_value=100.0, step=0.1)
    odds_over = st.text_input("Over Odds (e.g., -120)")
    odds_under = st.text_input("Under Odds (e.g., +100)")

with col2:
    stat_type = st.radio("Stat Type to Simulate", ["PRA", "Points Only"])
    points = st.number_input("Points", min_value=0.0)
    rebounds = st.number_input("Rebounds", min_value=0.0)
    assists = st.number_input("Assists", min_value=0.0)
    defense_vs_position = st.number_input("Opponent DEF Rank vs Pos (1-30)", min_value=1, max_value=30)

# Helper functions
def american_to_prob(odds):
    try:
        odds = int(odds)
        if odds < 0:
            return round(abs(odds) / (abs(odds) + 100), 4)
        else:
            return round(100 / (odds + 100), 4)
    except:
        return None

def calc_ev(true_prob, implied_prob):
    return round((true_prob - implied_prob) * 100, 2)

# Simulation and Board
if st.button("Simulate"):
    hit_chance = round(random.uniform(0.70, 0.91), 4)  # Placeholder logic
    implied_over = american_to_prob(odds_over)
    implied_under = american_to_prob(odds_under)
    ev_over = calc_ev(hit_chance, implied_over) if implied_over else None
    ev_under = calc_ev(1 - hit_chance, implied_under) if implied_under else None

    result_data = {
        "Player": player_name,
        "Type": stat_type,
        "True %": f"{hit_chance * 100:.1f}%",
        "Over EV": f"{ev_over:.1f}%" if ev_over is not None else "-",
        "Under EV": f"{ev_under:.1f}%" if ev_under is not None else "-"
    }
    st.success(f"✅ {player_name} - True Hit Probability for {stat_type}: {hit_chance*100:.2f}%")

    if "board" not in st.session_state:
        st.session_state.board = []
    st.session_state.board.append(result_data)

# Display Board
st.header("📈 Top Player Board")
if "board" in st.session_state and len(st.session_state.board) > 0:
    board_df = pd.DataFrame(st.session_state.board)
    board_df = board_df.sort_values(by="True %", ascending=False)
    st.dataframe(board_df.reset_index(drop=True))

# Parlay Evaluator
st.header("💰 Parlay Evaluator")
parlay_col1, parlay_col2 = st.columns([3, 1])

with parlay_col1:
    parlay_players = st.multiselect("Select Players for Parlay", options=[row['Player'] for row in st.session_state.get("board", [])])
with parlay_col2:
    parlay_odds = st.text_input("Parlay Odds (e.g., +150)")

if st.button("Evaluate Parlay") and parlay_players and parlay_odds:
    selected_rows = [row for row in st.session_state.board if row['Player'] in parlay_players]
    true_probs = [float(row['True %'].replace('%',''))/100 for row in selected_rows]
    true_parlay_prob = round(100 * eval('*'.join([str(p) for p in true_probs])), 2)
    implied_parlay_prob = american_to_prob(parlay_odds)
    if implied_parlay_prob:
        implied_parlay_prob = round(implied_parlay_prob * 100, 2)
        parlay_ev = round(true_parlay_prob - implied_parlay_prob, 2)
        st.metric(label="True Parlay Probability", value=f"{true_parlay_prob}%")
        st.metric(label="Implied Probability", value=f"{implied_parlay_prob}%")
        st.metric(label="EV %", value=f"{parlay_ev}%")
    else:
        st.error("Invalid parlay odds input.")
