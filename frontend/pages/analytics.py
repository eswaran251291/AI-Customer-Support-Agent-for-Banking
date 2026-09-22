"""Analytics page."""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import get_api_client


def render_analytics():
    """Render analytics from the live backend metrics."""
    st.title("📊 Analytics & Insights")

    api_client = get_api_client()
    summary = api_client.get_analytics_summary()
    if "error" in summary:
        st.error(summary["error"])
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Conversations", summary["total_conversations"])
    with col2:
        st.metric("Resolved Issues", summary["resolved_conversations"])
    with col3:
        st.metric("Escalated Issues", summary["escalated_conversations"])
    with col4:
        st.metric("Automation Rate", f"{summary['automation_rate']:.0%}")

    st.subheader("Conversation Trends")
    trend_data = api_client.get_analytics_trends()
    trends = trend_data.get("trends", [])
    col1, col2 = st.columns(2)
    with col1:
        df = pd.DataFrame(trends)
        fig = px.line(df, x="date", y="conversations", title="Conversations Over Time")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        categories = api_client.get_analytics_categories().get("categories", [])
        category_data = pd.DataFrame(categories)
        fig = px.pie(category_data, values="count", names="intent", title="Intent Distribution")
        st.plotly_chart(fig, use_container_width=True)


def main():
    """Analytics page main function."""
    st.set_page_config(page_title="Analytics", layout="wide")
    render_analytics()


if __name__ == "__main__":
    main()
