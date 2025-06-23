
import streamlit as st
import base64
import pandas as pd
import math

st.set_page_config(layout="wide", page_title="MoneyBall Phil: Basketball Simulator")

# Set background
def set_background(image_path):
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""<style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>""",
        unsafe_allow_html=True
    )

# Load background image
set_background("basketball_background.png")

# Load logo
st.image("moneyball_logo.png", width=200)

st.title("🏀 MoneyBall Phil: Basketball Player Prop Simulator")

st.markdown("This simulator calculates the **true probability**, **expected value (EV%)**, and **hit zone** for PRA and Points props.")

player_data = []
top_board = pd.DataFrame()

# Conversion from American odds to implied probability
def american_to_implied(odds):
    if odds < 0:
        return abs(odds) / (abs(odds) + 100)
    else:
        return 100 / (odds + 100)

# Simulate binomial hit probability
def simulate_probability(avg, stat_total, usage_pct):
    prob = avg * (usage_pct / 100)
    return min(prob, 1.0)

# Classify zone based on true probability
def classify_zone(true_prob):
    if true_prob >= 0.80:
        return "🔥 Elite"
    elif true_prob >= 0.70:
        return "🟢 Strong"
    elif true_prob >= 0.60:
        return "🟡 Moderate"
    else:
        return "🔴 Bad"

st.header("🧾 Player Input")
with st.form("player_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Player Name")
        avg = st.number_input("Projected Hit Rate", min_value=0.0, max_value=1.0, format="%.4f")
        stat_total = st.number_input("Projected PRA or Points", min_value=0)
    with col2:
        usage_pct = st.number_input("Usage %", min_value=0.0, max_value=100.0, value=20.0)
        over_odds = st.number_input("Over Odds (American)", value=-110)
        under_odds = st.number_input("Under Odds (American)", value=-110)
    with col3:
        prop_type = st.radio("Prop Type", ["PRA", "Points"])
        submit = st.form_submit_button("Simulate Player")

    if submit:
        true_prob = simulate_probability(avg, stat_total, usage_pct)
        implied_over = american_to_implied(over_odds)
        implied_under = american_to_implied(under_odds)
        ev_over = round((true_prob - implied_over) * 100, 2)
        ev_under = round(((1 - true_prob) - implied_under) * 100, 2)
        zone = classify_zone(true_prob)

        result = {
            "Player": name,
            "Prop": prop_type,
            "True %": round(true_prob * 100, 1),
            "Over EV%": ev_over,
            "Under EV%": ev_under,
            "Zone": zone
        }
        player_data.append(result)

        st.success(f"{name} ({prop_type}) — True: {true_prob:.1%} | Zone: {zone}")

# Show Top Board
if player_data:
    top_board = pd.DataFrame(player_data)
    top_board = top_board.sort_values(by="True %", ascending=False)
    st.subheader("🏆 Top Player Board")
    st.dataframe(top_board, use_container_width=True)

# Parlay Builder
st.header("🧮 Parlay Evaluator")
with st.form("parlay_form"):
    parlay_true = st.number_input("True Parlay Probability %", min_value=0.0, max_value=100.0)
    parlay_odds = st.number_input("Parlay Odds (American)", value=+100)
    calc = st.form_submit_button("Evaluate Parlay")
    if calc:
        implied_parlay = american_to_implied(parlay_odds)
        ev_parlay = round((parlay_true/100 - implied_parlay) * 100, 2)
        st.markdown(f"**True %:** {parlay_true:.2f}%  
**Implied %:** {implied_parlay*100:.2f}%  
**EV%:** {ev_parlay:.2f}%")
        if parlay_true >= 80:
            st.success("🔥 This is an ELITE parlay!")
        elif parlay_true >= 70:
            st.info("🟢 Strong parlay!")
        elif parlay_true >= 60:
            st.warning("🟡 Moderate risk.")
        else:
            st.error("🔴 Risky parlay.")
