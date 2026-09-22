"""Styling utilities."""

import streamlit as st


def set_page_config():
    """Set page configuration and styling."""
    st.set_page_config(
        page_title="Banking Support AI",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Custom CSS
    custom_css = """
    <style>
    :root {
        --primary-color: #0066cc;
        --secondary-color: #00cc99;
        --background-color: #f5f5f5;
        --text-color: #333333;
    }
    
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        border-radius: 0.25rem;
    }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)


def apply_custom_theme():
    """Apply custom theme based on user preference."""
    if "theme" not in st.session_state:
        st.session_state.theme = "Auto"
    
    # Apply theme settings
    # This would typically be handled through Streamlit's theme configuration
    pass
