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

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)
    col2.metric("High Priority Customers", high_priority)
    col3.metric("Avg Churn Risk %", avg_churn)
    col4.metric("Negative Sentiment Cases", negative_sentiment)

    st.divider()

    col1, col2 = st.columns(2)

    fig1 = px.histogram(df, x="intent", title="Intent Distribution")
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(df, x="priority", title="Priority Segmentation")
    col2.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(
        df,
        x="sentiment_score",
        y="churn_score",
        color="priority",
        title="Churn Risk vs Sentiment"
    )

    st.plotly_chart(fig3, use_container_width=True)


# ======================
# TAB 2 — PLACEHOLDER (we build next)
# ======================

with tab2:
    st.header("Customer 360 View — Coming Next")

# ======================
# TAB 3 — PLACEHOLDER
# ======================

with tab3:
    st.header("AI Insights — Coming Next")
