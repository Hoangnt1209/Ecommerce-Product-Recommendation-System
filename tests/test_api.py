from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_sample_users_endpoint():
    response = client.get("/sample-users")
    assert response.status_code == 200
    assert "users" in response.json()

def test_recommend_endpoint():
    payload = {
        "user_id": "TEST_USER_123",
        "top_k": 5,
        "model_type": "hybrid"
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "TEST_USER_123"
    assert len(data["recommendations"]) <= 5

def test_explain_endpoint():
    response = client.get("/explain?user_id=TEST_USER_123&asin=TEST_ASIN")
    assert response.status_code == 200
    assert "explanation_type" in response.json()

def test_fairness_endpoint():
    response = client.get("/fairness")
    assert response.status_code == 200
    assert "catalog_coverage_pct" in response.json()

def test_recommend_content_endpoint():
    payload = {
        "user_id": "TEST_USER_123",
        "top_k": 3,
        "model_type": "content"
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Content" in data["model_used"] or data["is_cold_start"]

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
