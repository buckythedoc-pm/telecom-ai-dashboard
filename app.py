import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

st.set_page_config(page_title="Telecom AI Dashboard", layout="wide")

st.title("📡 Telecom Customer 360 — AI Insights")

# =========================
# LOAD DATA FROM SUPABASE
# =========================

@st.cache_data
def load_data():
    conn = psycopg2.connect(
    host=st.secrets["SUPABASE_HOST"],
    database=st.secrets["SUPABASE_DB"],
    user=st.secrets["SUPABASE_USER"],
    password=st.secrets["SUPABASE_PASSWORD"],
    port=st.secrets["SUPABASE_PORT"],
    sslmode="require"
)

    query = """
    SELECT
        usp.user_id AS customer_id,
        usp.avg_confidence,
        usp.churn_risk,
        usp.churn_risk_label,
        usp.churn_reason,

        ra.sentiment,
        ra.retention_action,
        ra.priority,
        ra.department,
        ra.reason,
        ra.confidence_score

    FROM user_support_profile usp

    LEFT JOIN (
        SELECT DISTINCT ON (customer_id)
            customer_id,
            sentiment,
            retention_action,
            priority,
            department,
            reason,
            confidence_score,
            created_at
        FROM retention_actions
        ORDER BY customer_id, created_at DESC
    ) ra

    ON usp.user_id = ra.customer_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


df = load_data()

# ✅ RELOAD BUTTON (OUTSIDE FUNCTION)
if st.button("Reload Data"):
    st.cache_data.clear()
    st.rerun()


# ======================
# TABS
# ======================

tab1, tab2, tab3 = st.tabs([
    "📊 Executive Dashboard",
    "👤 Customer 360",
    "🤖 AI Insights"
])

# ======================
# TAB 1 — EXECUTIVE
# ======================

with tab1:

    st.header("Executive Overview")

    total_customers = df["customer_id"].nunique()
    high_priority = df[df["priority"] == "high"].shape[0]
    avg_churn = round(df["churn_risk"].mean(), 2)
    negative_sentiment = df[df["sentiment"] < 0].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)
    col2.metric("High Priority Customers", high_priority)
    col3.metric("Avg Churn Risk", avg_churn)
    col4.metric("Negative Sentiment Cases", negative_sentiment)

    st.divider()

    col1, col2 = st.columns(2)

    fig1 = px.histogram(df, x="priority", title="Priority Distribution")
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(df, x="department", title="Department Distribution")
    col2.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(
        df,
        x="sentiment",
        y="churn_risk",
        color="priority",
        title="Churn vs Sentiment"
    )

    st.plotly_chart(fig3, use_container_width=True)


# ======================
# TAB 2 — CUSTOMER 360
# ======================

with tab2:

    st.header("👤 Customer 360 View")

    customer_id = st.selectbox(
        "Select Customer",
        df["customer_id"].unique()
    )

    filtered_df = df[df["customer_id"] == customer_id].iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Churn Risk", round(filtered_df["churn_risk"], 2))
    col2.metric("Sentiment", round(filtered_df["sentiment"], 2))
    col3.metric("Priority", filtered_df["priority"])
    col4.metric("Confidence", filtered_df["confidence_score"])

    st.divider()

    st.subheader("Churn Reason")
    st.info(filtered_df["churn_reason"])

    st.subheader("Retention Recommendation")
    st.success(filtered_df["retention_action"])

    st.subheader("Department Handling")
    st.write(filtered_df["department"])


# ======================
# TAB 3 — AI INSIGHTS
# ======================

with tab3:

    st.header("🤖 AI Insights & Recommendations")

    fig1 = px.pie(
        df,
        names="priority",
        title="Customer Priority Segmentation"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    fig2 = px.scatter(
        df,
        x="sentiment",
        y="churn_risk",
        color="priority",
        size="churn_risk",
        title="Churn vs Sentiment Relationship"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("AI Retention Strategy Generator")

    customer_id_ai = st.selectbox(
        "Select Customer",
        df["customer_id"].unique(),
        key="ai_customer"
    )

    customer_data = df[df["customer_id"] == customer_id_ai].iloc[0]

    if st.button("Generate Retention Strategy"):

        churn = customer_data["churn_risk"]
        sentiment = customer_data["sentiment"]

        if churn > 0.75:
            recommendation = "High churn risk detected. Offer personalized discount and priority support."
        elif churn > 0.5:
            recommendation = "Moderate churn risk. Provide proactive engagement and service review."
        else:
            recommendation = "Low churn risk. Maintain engagement with loyalty benefits."

        explanation = f"""
        AI Analysis:
        - Sentiment Score: {sentiment}
        - Churn Risk: {churn}

        Recommended Action:
        {recommendation}
        """

        st.success(recommendation)
        st.info(explanation)
