"""Sidebar component."""

import streamlit as st
from utils.api_client import get_api_client


def render_sidebar():
    """Render sidebar navigation and info."""
    with st.sidebar:
        st.title("🏦 Banking Support AI")
        
        st.markdown("---")
        
        # API Status
        api_client = get_api_client()
        if api_client.health_check():
            st.success("🟢 Backend Online")
        else:
            st.error("🔴 Backend Offline")
            st.info("Start backend with: `python -m uvicorn app.main:app --reload`")
        
        st.markdown("---")
        
        # Quick Stats
        st.write("**Quick Stats**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Status", "Online", "✓")
        with col2:
            st.metric("Latency", "45ms", "✓")
        
        st.markdown("---")
        
        # Demo Customers
        st.write("**Demo Customers**")
        st.write("Try these customer IDs:")
        st.code("CUST_001\nCUST_002", language=None)
        
        st.markdown("---")
        
        # Support
        st.write("**Need Help?**")
        if st.button("📖 View Documentation"):
            st.info("Documentation: See DEVELOPMENT.md and CASE_STUDY.md")
        
        st.markdown("---")
        
        st.caption("© 2024 AI Customer Support Agent for Banking")
