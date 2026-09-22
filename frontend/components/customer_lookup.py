"""Customer lookup component."""

import streamlit as st
from utils.api_client import get_api_client


def render_customer_lookup():
    """Render customer lookup interface."""
    # Search form
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search by customer ID, name, or email",
            placeholder="Enter customer details..."
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary")
    
    if search_button and search_query:
        customer = get_api_client().get_customer_info(search_query.strip())
        if "error" in customer or "detail" in customer:
            st.error(customer.get("error", customer.get("detail", "Customer not found")))
            return

        st.success(f"Found customer {customer['id']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Basic Information")
            st.write(f"**Name:** {customer['name']}")
            st.write(f"**Customer ID:** {customer['id']}")
            st.write(f"**Email:** {customer['email']}")
            st.write(f"**Account Status:** {customer['account_status']}")
        
        with col2:
            st.subheader("💼 Account Details")
            st.write(f"**Account Type:** {customer['account_type']}")
            st.write(f"**Account Number:** ****{customer['last_4_digits']}")
            st.write(f"**Balance:** ${customer['balance']}")
            st.write(f"**Member Since:** {customer['created_at']}")
        
        st.subheader("📞 Recent Interactions")
        interactions = [
            {"date": "2024-01-15", "type": "Chat", "issue": "Account Balance Query", "resolved": "Yes"},
            {"date": "2024-01-10", "type": "Phone", "issue": "Card Replacement", "resolved": "Yes"},
            {"date": "2024-01-05", "type": "Chat", "issue": "Transfer Limit", "resolved": "Yes"},
        ]
        
        for interaction in interactions:
            with st.expander(f"{interaction['date']} - {interaction['type']} - {interaction['issue']}"):
                st.write(f"**Type:** {interaction['type']}")
                st.write(f"**Issue:** {interaction['issue']}")
                st.write(f"**Status:** {'✅ Resolved' if interaction['resolved'] == 'Yes' else '⏳ Pending'}")
