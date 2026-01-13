"""
Tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from glocal_guardrail.api import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_list_policies(client):
    """Test list policies endpoint"""
    response = client.get("/policies")
    assert response.status_code == 200
    data = response.json()
    assert "available_countries" in data
    assert len(data["available_countries"]) > 0


def test_validate_endpoint(client):
    """Test validation endpoint"""
    request_data = {
        "metadata": {
            "title": "Family App",
            "description": "Entertainment for all",
            "features": ["parental_controls", "content_filtering", "prayer_time_notifications"],
            "local_content_percentage": 35
        },
        "target_countries": ["SA"]
    }
    
    response = client.post("/validate", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "SA" in data["results"]


def test_validate_single_country(client):
    """Test single country validation endpoint"""
    metadata = {
        "title": "App",
        "description": "Test",
        "features": ["gdpr_compliance", "data_privacy_controls", "youth_protection_system", "opt_in_tracking"],
        "gdpr_compliant": True
    }
    
    response = client.post("/validate/DE", json=metadata)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "violations" in data


def test_validate_invalid_country(client):
    """Test validation with invalid country code"""
    metadata = {"title": "Test"}
    
    response = client.post("/validate/XX", json=metadata)
    assert response.status_code == 404


def test_deployment_check_pass(client):
    """Test deployment check that passes"""
    request_data = {
        "metadata": {
            "title": "Compliant App",
            "description": "Follows all rules",
            "features": [
                "parental_controls",
                "content_filtering",
                "prayer_time_notifications",
                "real_name_verification",
                "age_verification",
                "shutdown_system",
                "data_localization",
                "gdpr_compliance",
                "data_privacy_controls",
                "youth_protection_system",
                "opt_in_tracking"
            ],
            "real_name_verification_enabled": True,
            "gdpr_compliant": True,
            "data_stored_locally": True,
            "local_content_percentage": 35,
            "ad_duration_minutes": 2
        },
        "target_countries": ["SA", "KR", "DE"]
    }
    
    response = client.post("/deployment-check", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "overall_status" in data
    assert "deployment_ready" in data
    assert "results" in data


def test_deployment_check_reject(client):
    """Test deployment check that rejects"""
    request_data = {
        "metadata": {
            "title": "Casino App",
            "description": "Gambling and betting"
        },
        "target_countries": ["SA"]
    }
    
    response = client.post("/deployment-check", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["overall_status"] == "REJECT"
    assert data["deployment_ready"] is False
    assert len(data["non_compliant_countries"]) > 0
