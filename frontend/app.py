"""Main Streamlit frontend application."""

import streamlit as st
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface
from utils.styling import set_page_config
from pages.analytics import render_analytics
from components.customer_lookup import render_customer_lookup

# Set page configuration
set_page_config()

# Render sidebar and get selected page
page = st.sidebar.radio(
    "Navigation",
    ["Chat", "Customer Info", "Analytics", "Settings"],
    label_visibility="collapsed"
)

# Route to selected page
if page == "Chat":
    render_chat_interface()

elif page == "Customer Info":
    st.title("👤 Customer Information")
    render_customer_lookup()

elif page == "Analytics":
    render_analytics()

elif page == "Settings":
    st.title("⚙️ Settings")
    
    with st.form("settings_form"):
        theme = st.radio("Theme", ["Light", "Dark", "Auto"])
        language = st.selectbox("Language", ["English", "Spanish", "French"])
        backend_url = st.text_input("Backend URL", "http://localhost:8000")
        api_timeout = st.number_input("API Timeout (seconds)", 5, 120, 30)
        
        if st.form_submit_button("Save Settings"):
            st.success("Settings saved!")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🏦 Banking Support AI")
with col2:
    st.caption("v1.0.0")
with col3:
    st.caption("© 2024 All Rights Reserved")
