"""Chat page."""

import streamlit as st

from components.chat_interface import render_chat_interface


def main():
    """Chat page main function."""
    st.set_page_config(page_title="Chat", layout="wide")
    st.title("💬 Chat with Support")
    
    render_chat_interface()


if __name__ == "__main__":
    main()
