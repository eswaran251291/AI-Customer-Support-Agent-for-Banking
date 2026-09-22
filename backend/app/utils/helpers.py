"""Helper functions."""

import uuid


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


def generate_customer_id() -> str:
    """Generate a unique customer ID."""
    return f"CUST_{uuid.uuid4().hex[:8].upper()}"
