"""
Global Internet Access & Digital Divide Tracker - Dashboard
Week 6: Visual dashboard on top of the deployed FastAPI model

Run locally with:
    streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ---- Config ----
API_URL = "https://global-internet-digital-divide.onrender.com/predict"

st.set_page_config(page_title="Digital Divide Tracker", page_icon="🌍", layout="wide")

# ---- Load data (for the historical charts) ----
@st.cache_data
def load_data():
    df = pd.read_csv("digital_divide_clean.csv")
    return df

df = load_data()

# ---- Header ----
st.title("🌍 Global Internet Access & Digital Divide Tracker")
st.caption("MLOps pipeline: World Bank data → Random Forest → FastAPI → live prediction")

tab1, tab2 = st.tabs(["🔮 Live Prediction", "📊 Explore the Data"])

# ---- TAB 1: Live prediction via the deployed API ----
with tab1:
    st.subheader("Predict Digital Divide Risk")
    st.write("Enter a country's stats, or pick an existing country to auto-fill real values.")

    col1, col2 = st.columns([1, 2])

    with col1:
        country_pick = st.selectbox(
            "Auto-fill from a country's latest data (optional)",
            ["-- Manual entry --"] + sorted(df["country"].unique().tolist())
        )

    if country_pick != "-- Manual entry --":
        latest_row = df[df["country"] == country_pick].sort_values("year").iloc[-1]
        defaults = {
            "mobile_subs_per_100": float(latest_row["mobile_subs_per_100"]),
            "gdp_per_capita_usd": float(latest_row["gdp_per_capita_usd"]),
            "urban_pop_pct": float(latest_row["urban_pop_pct"]),
            "electricity_access_pct": float(latest_row["electricity_access_pct"]),
            "literacy_rate_pct": float(latest_row["literacy_rate_pct"]),
        }
    else:
        defaults = {
            "mobile_subs_per_100": 82.0,
            "gdp_per_capita_usd": 2600.0,
            "urban_pop_pct": 36.0,
            "electricity_access_pct": 99.0,
            "literacy_rate_pct": 76.0,
        }

    c1, c2, c3, c4, c5 = st.columns(5)
    mobile_subs = c1.number_input("Mobile subs / 100", value=defaults["mobile_subs_per_100"])
    gdp = c2.number_input("GDP per capita (USD)", value=defaults["gdp_per_capita_usd"])
    urban = c3.number_input("Urban population %", value=defaults["urban_pop_pct"])
    electricity = c4.number_input("Electricity access %", value=defaults["electricity_access_pct"])
    literacy = c5.number_input("Literacy rate %", value=defaults["literacy_rate_pct"])

    if st.button("Predict Risk", type="primary"):
        payload = {
            "mobile_subs_per_100": mobile_subs,
            "gdp_per_capita_usd": gdp,
            "urban_pop_pct": urban,
            "electricity_access_pct": electricity,
            "literacy_rate_pct": literacy,
        }
        try:
            with st.spinner("Calling the live API (may take up to a minute if it's waking up)..."):
                response = requests.post(API_URL, json=payload, timeout=90)
                response.raise_for_status()
                result = response.json()

            risk = result["predicted_risk"]
            probs = result["class_probabilities"]

            color = {"Low Risk": "green", "Medium Risk": "orange", "High Risk": "red"}[risk]
            st.markdown(f"### Predicted Risk: :{color}[{risk}]")

            prob_df = pd.DataFrame(list(probs.items()), columns=["Risk Tier", "Probability"])
            fig = px.bar(prob_df, x="Risk Tier", y="Probability", color="Risk Tier",
                         color_discrete_map={"Low Risk": "green", "Medium Risk": "orange", "High Risk": "red"},
                         range_y=[0, 1])
            st.plotly_chart(fig, use_container_width=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Couldn't reach the API: {e}")

# ---- TAB 2: Explore historical data ----
with tab2:
    st.subheader("Internet Access Trends (2016-2025)")

    countries_selected = st.multiselect(
        "Select countries to compare",
        sorted(df["country"].unique().tolist()),
        default=["India", "United States", "Ethiopia", "Germany"]
    )

    if countries_selected:
        filtered = df[df["country"].isin(countries_selected)]
        fig2 = px.line(filtered, x="year", y="internet_access_pct", color="country",
                        markers=True, title="Internet Access % Over Time")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("2025 Snapshot: All Countries")
    latest_year = df["year"].max()
    snapshot = df[df["year"] == latest_year].sort_values("internet_access_pct")
    fig3 = px.bar(snapshot, x="internet_access_pct", y="country", orientation="h",
                  color="internet_access_pct", color_continuous_scale="RdYlGn",
                  title=f"Internet Access % by Country ({latest_year})")
    st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.caption("Data: World Bank Open Data | Model: Random Forest (90% accuracy) | "
           "[GitHub repo](https://github.com/ShravaniKolte/Global-Internet-Digital-Divide)")
