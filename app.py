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

    st.header("👤 Customer 360 View")

    # Sidebar filter
    st.sidebar.header("Filters")

    customer_id = st.sidebar.selectbox(
        "Select Customer",
        df["customer_id"].unique()
    )

    filtered_df = df[df["customer_id"] == customer_id]

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

    # Customer charts
    st.subheader("Customer Insights")

    fig = px.bar(
        filtered_df,
        x="customer_id",
        y="churn_score",
        title="Customer Churn Risk"
    )

    st.plotly_chart(fig, use_container_width=True)


# ======================
# TAB 3 — PLACEHOLDER
# ======================

with tab3:
    with tab3:

    st.header("🤖 AI Insights & Recommendations")

    st.subheader("Priority Distribution")

    fig1 = px.pie(
        df,
        names="priority",
        title="Customer Priority Segmentation"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    st.subheader("Churn Risk vs Sentiment Analysis")

    fig2 = px.scatter(
        df,
        x="sentiment_score",
        y="churn_score",
        color="priority",
        size="churn_score",
        title="Churn vs Sentiment Relationship"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("AI Retention Strategy Generator")

    customer_id_ai = st.selectbox(
        "Select Customer for AI Recommendation",
        df["customer_id"].unique(),
        key="ai_customer"
    )

    customer_data = df[df["customer_id"] == customer_id_ai].iloc[0]

    if st.button("Generate Retention Strategy"):

        churn = customer_data["churn_score"]
        intent = customer_data["intent"]
        sentiment = customer_data["sentiment"]

        # Simple AI logic (can replace with LLM later)
        if churn > 70:
            recommendation = "High churn risk detected. Offer personalized discount and priority technical support."
        elif churn > 40:
            recommendation = "Moderate churn risk. Provide proactive engagement and service check."
        else:
            recommendation = "Low churn risk. Maintain engagement with loyalty benefits."

        explanation = f"""
        AI Analysis:
        - Intent: {intent}
        - Sentiment: {sentiment}
        - Churn Score: {churn}%

        Recommended Action:
        {recommendation}
        """

        st.success(recommendation)
        st.info(explanation)

