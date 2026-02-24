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

# Sidebar
st.sidebar.header("Filters")

customer_id = st.sidebar.selectbox(
    "Select Customer",
    df["customer_id"].unique()
)

filtered_df = df[df["customer_id"] == customer_id]

# Metrics
st.subheader("Customer Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Churn Risk", f"{filtered_df['churn_score'].values[0]}%")
col2.metric("Sentiment", filtered_df['sentiment'].values[0])
col3.metric("Intent", filtered_df['intent'].values[0])
col4.metric("Priority", filtered_df['priority'].values[0])

st.divider()

st.subheader("Conversation Summary")
st.info(filtered_df["summary"].values[0])

st.subheader("Retention Recommendation")
st.success(filtered_df["retention_action"].values[0])

st.divider()

# Charts
st.subheader("Insights")

col1, col2 = st.columns(2)

fig1 = px.histogram(df, x="intent", title="Intent Distribution")
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.histogram(df, x="sentiment", title="Sentiment Distribution")
col2.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(
    df,
    x="sentiment_score",
    y="churn_score",
    color="priority",
    title="Churn vs Sentiment"
)

st.plotly_chart(fig3, use_container_width=True)
