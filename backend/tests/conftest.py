"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Provide a test client."""
    return TestClient(app)


@pytest.fixture
def mock_customer_data():
    """Provide mock customer data."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "account_status": "active",
    }
