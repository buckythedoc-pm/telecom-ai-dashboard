import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Telecom AI Dashboard", layout="wide")

st.title("📡 Telecom Customer 360 — AI Insights")

@st.cache_data
def load_data():
    df = pd.read_csv("telecom_data.csv")
    return df

df = load_data()

# ======================
# TABS
# ======================

tab1, tab2, tab3 = st.tabs([
    "📊 Executive Dashboard",
    "👤 Customer 360",
    "🤖 AI Insights"
])

# ======================
# TAB 1 — EXECUTIVE DASHBOARD
# ======================

with tab1:

    st.header("Executive Overview")

    total_customers = df["customer_id"].nunique()
    high_priority = df[df["priority"] == "High"].shape[0]
    avg_churn = round(df["churn_score"].mean(), 1)
    negative_sentiment = df[df["sentiment"] == "Negative"].shape[0]

    col1,

