"""Customer info page."""

import streamlit as st

from components.customer_lookup import render_customer_lookup


def main():
    """Customer info page main function."""
    st.set_page_config(page_title="Customer Info", layout="wide")
    st.title("👤 Customer Information")
    
    render_customer_lookup()


if __name__ == "__main__":
    main()
