"""Chat interface component."""

import streamlit as st
from datetime import datetime
from typing import Optional
from utils.api_client import get_api_client
import uuid


def render_chat_interface():
    """Render the chat interface with backend integration."""
    
    # Initialize session state
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "customer_id" not in st.session_state:
        st.session_state.customer_id = None
    
    if "mfa_required" not in st.session_state:
        st.session_state.mfa_required = False
    
    if "api_status" not in st.session_state:
        st.session_state.api_status = "checking"
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("💬 Chat with Support Agent")
    with col2:
        if st.session_state.api_status == "ready":
            st.success("🟢 Online")
        elif st.session_state.api_status == "error":
            st.error("🔴 Offline")
        else:
            st.info("🟡 Checking...")
    
    # Customer ID input (in sidebar for cleaner UI)
    if "customer_id_input" not in st.session_state:
        st.session_state.customer_id_input = ""
    
    customer_id_input = st.text_input(
        "Enter Customer ID (optional):",
        value=st.session_state.customer_id_input,
        placeholder="e.g., CUST_001",
        key="customer_id_field"
    )
    
    if customer_id_input:
        st.session_state.customer_id = customer_id_input
        st.session_state.customer_id_input = customer_id_input
    
    # Display chat history
    st.write("---")
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show metadata for AI responses
                if message["role"] == "assistant" and "metadata" in message:
                    with st.expander("ℹ️ Details"):
                        metadata = message["metadata"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(f"Intent: {metadata.get('intent', 'unknown')}")
                            st.caption(f"Confidence: {metadata.get('confidence', 0):.0%}")
                        with col2:
                            if metadata.get("escalation_required"):
                                st.warning("⚠️ Requires escalation")
                            else:
                                st.success("✅ Can help directly")
    
    # Chat input area
    st.write("---")
    
    # Handle MFA requirement
    if st.session_state.mfa_required:
        st.warning("🔐 MFA Verification Required")
        mfa_token = st.text_input(
            "Enter MFA code:",
            type="password",
            placeholder="Enter 6-digit code or verification token"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Verify MFA", use_container_width=True):
                if mfa_token:
                    st.session_state.mfa_token = mfa_token
                    st.session_state.mfa_required = False
                    st.rerun()
                else:
                    st.error("Please enter MFA code")
        
        with col2:
            if st.button("✗ Cancel", use_container_width=True):
                st.session_state.mfa_required = False
                st.rerun()
    
    # Chat input
    user_input = st.chat_input(
        "Type your message here...",
        disabled=st.session_state.api_status == "error"
    )
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
        
        # Get API response
        try:
            api_client = get_api_client()
            
            # Check API health if not yet checked
            if st.session_state.api_status == "checking":
                if api_client.health_check():
                    st.session_state.api_status = "ready"
                else:
                    st.session_state.api_status = "error"
                    st.rerun()
            
            # Send message to backend
            with st.spinner("Processing your message..."):
                response = api_client.send_chat_message(
                    message=user_input,
                    customer_id=st.session_state.customer_id,
                    session_id=st.session_state.session_id,
                    mfa_token=st.session_state.get("mfa_token")
                )
            
            if "error" in response:
                st.error(f"Error: {response['error']}")
                st.session_state.api_status = "error"
            else:
                # Handle MFA requirement
                if response.get("requires_mfa"):
                    st.session_state.mfa_required = True
                    st.rerun()
                
                # Add bot response to history
                bot_message = {
                    "role": "assistant",
                    "content": response.get("message", "I couldn't process that request."),
                    "metadata": {
                        "intent": response.get("intent", "unknown"),
                        "confidence": response.get("confidence", 0),
                        "escalation_required": response.get("escalation_required", False),
                        "escalation_priority": response.get("escalation_priority"),
                        "suggested_specialist": response.get("suggested_specialist"),
                        "wait_time": response.get("wait_time_estimate")
                    }
                }
                
                st.session_state.messages.append(bot_message)
                
                # Display bot message
                with chat_container:
                    with st.chat_message("assistant"):
                        st.markdown(response.get("message", "Error processing request"))
                        
                        # Show escalation info if needed
                        if response.get("escalation_required"):
                            st.warning(
                                f"⚠️ Escalation Required\n\n"
                                f"Priority: {response.get('escalation_priority', 'Normal')}\n\n"
                                f"Specialist: {response.get('suggested_specialist', 'Support Specialist')}\n\n"
                                f"Wait time: {response.get('wait_time_estimate', '< 5 minutes')}"
                            )
                        
                        with st.expander("ℹ️ Details"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.caption(f"Intent: {response.get('intent', 'unknown')}")
                                st.caption(f"Confidence: {response.get('confidence', 0):.0%}")
                            with col2:
                                if response.get("escalation_required"):
                                    st.warning("⚠️ Requires escalation")
                                else:
                                    st.success("✅ Can help directly")
                
                st.rerun()
        
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            st.info("Make sure the backend is running: `python -m uvicorn app.main:app --reload`")
            st.session_state.api_status = "error"
    
    # Additional help section
    st.write("---")
    with st.expander("💡 Examples"):
        st.write("""
        Try asking:
        - "What's my account balance?"
        - "Show me my recent transactions"
        - "I want to transfer money"
        - "I lost my card"
        - "I think my account was hacked"
        """)
    
    # Session info
    with st.expander("📊 Session Info"):
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"Session ID: {st.session_state.session_id[:12]}...")
        with col2:
            st.caption(f"Messages: {len(st.session_state.messages)}")
        
        if st.session_state.customer_id:
            st.caption(f"Customer: {st.session_state.customer_id}")

