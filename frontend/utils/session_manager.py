"""Session state management."""

import streamlit as st


def init_session_state():
    """Initialize session state with default values."""
    if "theme" not in st.session_state:
        st.session_state.theme = "Auto"
    
    if "language" not in st.session_state:
        st.session_state.language = "English"
    
    if "backend_url" not in st.session_state:
        st.session_state.backend_url = "http://localhost:8000"
    
    if "timeout" not in st.session_state:
        st.session_state.timeout = 30
    
    if "max_history" not in st.session_state:
        st.session_state.max_history = 20
    
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = None


def get_session_value(key: str, default=None):
    """Get value from session state."""
    return st.session_state.get(key, default)


def set_session_value(key: str, value):
    """Set value in session state."""
    st.session_state[key] = value
