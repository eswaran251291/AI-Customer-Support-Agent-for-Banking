"""Settings page."""

import streamlit as st


def main():
    """Settings page main function."""
    st.set_page_config(page_title="Settings", layout="wide")
    st.title("⚙️ Settings")
    
    st.subheader("General Settings")
    
    # Theme setting
    theme = st.radio("Select Theme", ["Light", "Dark", "Auto"])
    st.session_state.theme = theme
    
    # Language setting
    language = st.selectbox("Select Language", ["English", "Spanish", "French", "Chinese"])
    st.session_state.language = language
    
    st.subheader("API Configuration")
    
    # Backend URL
    backend_url = st.text_input(
        "Backend URL",
        value="http://localhost:8000",
        help="URL of the backend API server"
    )
    st.session_state.backend_url = backend_url
    
    # Timeout
    timeout = st.number_input(
        "API Timeout (seconds)",
        value=30,
        min_value=5,
        max_value=120
    )
    st.session_state.timeout = timeout
    
    st.subheader("Chat Settings")
    
    # Max conversation history
    max_history = st.slider(
        "Maximum Conversation History",
        min_value=5,
        max_value=50,
        value=20,
        step=5
    )
    st.session_state.max_history = max_history
    
    # Response temperature
    temperature = st.slider(
        "AI Response Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Lower = more focused, Higher = more creative"
    )
    st.session_state.temperature = temperature
    
    # Save settings button
    if st.button("💾 Save Settings", type="primary"):
        st.success("Settings saved successfully!")
    
    st.divider()
    
    st.subheader("About")
    st.write(
        """
        **AI Customer Support Agent for Banking**
        
        Version: 1.0.0
        
        An intelligent customer support system powered by AI for banking institutions.
        """
    )


if __name__ == "__main__":
    main()
