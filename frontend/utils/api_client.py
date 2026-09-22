"""API client for backend communication."""

import os
from typing import Any, Optional, Dict
import streamlit as st
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class APIClient:
    """API client for communicating with the backend."""
    
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        """Initialize API client."""
        self.base_url = base_url or os.getenv("BACKEND_URL", "http://localhost:8000")
        self.timeout = timeout or int(os.getenv("API_TIMEOUT", 30))
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request to backend."""
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make GET request."""
        return self._make_request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make POST request."""
        return self._make_request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make PUT request."""
        return self._make_request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._make_request("DELETE", endpoint, **kwargs)
    
    def health_check(self) -> bool:
        """Check backend health."""
        try:
            response = self.get("/health")
            return response.get("status") == "healthy"
        except Exception:
            return False
    
    def send_chat_message(
        self, 
        message: str, 
        customer_id: Optional[str] = None,
        session_id: Optional[str] = None,
        mfa_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send chat message to backend.
        
        Args:
            message: Customer message
            customer_id: Customer ID (optional)
            session_id: Conversation session ID
            mfa_token: MFA verification token
            
        Returns:
            Chat response with intent, message, escalation info
        """
        return self.post(
            "/api/v1/chat",
            json={
                "message": message,
                "customer_id": customer_id,
                "session_id": session_id,
                "mfa_token": mfa_token
            }
        )
    
    def get_customer_info(self, customer_id: str) -> Dict[str, Any]:
        """Get customer account information."""
        return self.get(f"/api/v1/customers/{customer_id}/info")
    
    def get_account_balance(self, customer_id: str) -> Dict[str, Any]:
        """Get customer account balance."""
        return self.get(f"/api/v1/customers/{customer_id}/balance")
    
    def get_transactions(self, customer_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get customer transaction history."""
        return self.get(f"/api/v1/customers/{customer_id}/transactions?limit={limit}")

    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get aggregate support metrics."""
        return self.get("/api/v1/analytics/summary")

    def get_analytics_trends(self, days: int = 7) -> Dict[str, Any]:
        """Get daily conversation counts."""
        return self.get(f"/api/v1/analytics/trends?days={days}")

    def get_analytics_categories(self) -> Dict[str, Any]:
        """Get intent category counts."""
        return self.get("/api/v1/analytics/categories")


@st.cache_resource
def get_api_client() -> APIClient:
    """Get or create API client instance."""
    return APIClient()
