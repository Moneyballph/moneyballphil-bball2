
# MoneyBall Phil Basketball Simulator (FINAL BUILD - June 23)
import streamlit as st
from PIL import Image
import base64
import random
import pandas as pd

st.set_page_config(layout="wide")

# Set full screen background
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        b64 = base64.b64encode(image_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("arena_background.png")

# App Title
st.markdown("<h1 style='text-align: center; color: white;'>MoneyBall Phil Basketball Simulator</h1>", unsafe_allow_html=True)

# Player Input Section
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
    sportsbook_line = st.number_input("Sportsbook Line (Points or PRA)", min_value=0.0)
with col2:
    stat_type = st.radio("Stat Type to Simulate", ["PRA", "Points Only"])
    points = st.number_input("Points", min_value=0.0)
    rebounds = st.number_input("Rebounds", min_value=0.0)
    assists = st.number_input("Assists", min_value=0.0)
    defense_vs_position = st.number_input("Opponent DEF Rank vs Pos (1-30)", min_value=1, max_value=30)

# Helper Functions
def american_to_prob(odds):
    try:
        odds = int(odds)
        if odds < 0:
            return abs(odds) / (abs(odds) + 100)
        else:
            return 100 / (odds + 100)
    except:
        return None

def calc_ev(true_prob, implied_prob):
    return round((true_prob - implied_prob) * 100, 2)

# Simulation Logic
if st.button("Simulate"):
    hit_chance = round(random.uniform(0.70, 0.91), 4)
    implied_over = american_to_prob(odds_over)
    implied_under = american_to_prob(odds_under)
    ev_over = calc_ev(hit_chance, implied_over) if implied_over else None
    ev_under = calc_ev(1 - hit_chance, implied_under) if implied_under else None

    result = {
        "Player": player_name,
        "Type": stat_type,
        "True %": f"{hit_chance * 100:.1f}%",
        "Line": sportsbook_line,
        "Over EV": f"{ev_over:.1f}%" if ev_over else "-",
        "Under EV": f"{ev_under:.1f}%" if ev_under else "-"
    }

    if "board" not in st.session_state:
        st.session_state.board = []
    st.session_state.board.append(result)

    st.success(f"{player_name} - True Hit Probability: {hit_chance * 100:.2f}%")

# Top Player Board
st.header("📈 Top Player Board")
if "board" in st.session_state:
    df = pd.DataFrame(st.session_state.board)
    df["True % Num"] = df["True %"].str.replace("%","").astype(float)
    df = df.sort_values(by="True % Num", ascending=False).drop(columns=["True % Num"])
    st.dataframe(df.reset_index(drop=True))

# Parlay Evaluator
st.header("💰 Parlay Evaluator")
c1, c2 = st.columns([3, 1])
with c1:
    parlay_players = st.multiselect("Select Players", [r["Player"] for r in st.session_state.get("board", [])])
with c2:
    parlay_odds = st.text_input("Parlay Odds (e.g., +145)")

if st.button("Evaluate Parlay") and parlay_players and parlay_odds:
    selected = [r for r in st.session_state.board if r["Player"] in parlay_players]
    probs = [float(r["True %"].replace("%", ""))/100 for r in selected]
    if probs:
        parlay_true = round(100 * eval("*".join([str(p) for p in probs])), 2)
        implied = american_to_prob(parlay_odds)
        if implied:
            implied_pct = round(implied * 100, 2)
            ev_parlay = round(parlay_true - implied_pct, 2)
            st.metric("True Parlay Probability", f"{parlay_true}%")
            st.metric("Implied Probability", f"{implied_pct}%")
            st.metric("EV %", f"{ev_parlay}%")
        else:
            st.error("Invalid odds")
