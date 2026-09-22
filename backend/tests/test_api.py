"""Backend API tests."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_chat_answers_known_faq():
    """Known FAQ messages are handled without external AI credentials."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "What is my account balance?"},
    )

    assert response.status_code == 200
    assert response.json()["intent"] == "account_balance"
    assert response.json()["requires_mfa"] is True


def test_chat_requires_mfa_before_sensitive_action():
    """Sensitive requests return an MFA challenge before processing."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "I want to transfer funds", "customer_id": "CUST_001"},
    )

    assert response.status_code == 200
    assert response.json()["requires_mfa"] is True
    assert response.json()["suggested_actions"] == ["request_mfa"]


def test_chat_rejects_invalid_mfa_token():
    """Invalid MFA tokens preserve the endpoint's 401 response."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "I want to transfer funds",
            "customer_id": "CUST_001",
            "mfa_token": "invalid",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid MFA token"


def test_chat_escalates_fraud_reports():
    """Fraud reports are escalated immediately to the fraud team."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "I see an unauthorized charge on my account"},
    )

    assert response.status_code == 200
    assert response.json()["escalation_required"] is True
    assert response.json()["suggested_specialist"] == "Fraud Team"


def test_analytics_endpoints_return_live_metrics():
    """Analytics endpoints expose metrics recorded by chat interactions."""
    summary = client.get("/api/v1/analytics/summary")
    trends = client.get("/api/v1/analytics/trends?days=3")
    categories = client.get("/api/v1/analytics/categories")

    assert summary.status_code == 200
    assert summary.json()["total_conversations"] >= 0
    assert trends.status_code == 200
    assert len(trends.json()["trends"]) == 3
    assert categories.status_code == 200
    assert "categories" in categories.json()
