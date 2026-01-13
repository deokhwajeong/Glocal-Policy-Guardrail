"""Integration tests for the FastAPI server."""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestAPIEndpoints:
    """Test API endpoint functionality."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "Glocal Policy Guardrail"
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_list_policies(self, client):
        """Test listing available policies."""
        response = client.get("/policies")
        assert response.status_code == 200
        data = response.json()
        assert "available_policies" in data
        assert "korea" in data["available_policies"]
        assert "saudi_arabia" in data["available_policies"]


class TestValidationEndpoint:
    """Test content validation endpoint."""
    
    def test_validate_korea_pass(self, client):
        """Test successful validation for Korea."""
        payload = {
            "content": {
                "title": "Family Movie",
                "description": "A family film",
                "categories": ["family"],
                "rating": "ALL",
                "duration_minutes": 90,
                "subtitle_languages": ["ko"],
                "audio_languages": ["en"],
                "ad_breaks": []
            },
            "country": "korea"
        }
        
        response = client.post("/validate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PASS"
        assert data["country"] == "korea"
        assert len(data["violations"]) == 0
    
    def test_validate_korea_reject(self, client):
        """Test rejection for Korea due to violations."""
        payload = {
            "content": {
                "title": "Gambling Show",
                "description": "About gambling",
                "categories": ["gambling"],
                "rating": "19",
                "subtitle_languages": ["en"],  # Missing Korean
                "ad_breaks": []
            },
            "country": "korea"
        }
        
        response = client.post("/validate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "REJECT"
        assert len(data["violations"]) > 0
    
    def test_validate_saudi_arabia_pass(self, client):
        """Test successful validation for Saudi Arabia."""
        payload = {
            "content": {
                "title": "Nature Documentary",
                "description": "Beautiful nature",
                "categories": ["documentary"],
                "rating": "G",
                "duration_minutes": 60,
                "subtitle_languages": ["ar"],
                "audio_languages": ["en"],
                "ad_breaks": []
            },
            "country": "saudi_arabia"
        }
        
        response = client.post("/validate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PASS"
        assert data["country"] == "saudi_arabia"
    
    def test_validate_saudi_arabia_reject(self, client):
        """Test rejection for Saudi Arabia."""
        payload = {
            "content": {
                "title": "Dating Show",
                "description": "A dating reality show",
                "categories": ["dating_shows"],
                "rating": "15",
                "subtitle_languages": ["en"],  # Missing Arabic
                "ad_breaks": []
            },
            "country": "saudi_arabia"
        }
        
        response = client.post("/validate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "REJECT"
        assert len(data["violations"]) > 0
    
    def test_validate_nonexistent_country(self, client):
        """Test validation with non-existent country policy."""
        payload = {
            "content": {
                "title": "Test Content",
                "categories": ["documentary"],
                "rating": "G",
                "ad_breaks": []
            },
            "country": "nonexistent"
        }
        
        response = client.post("/validate", json=payload)
        assert response.status_code == 404


class TestBatchValidation:
    """Test batch validation endpoint."""
    
    def test_batch_validate_multiple_countries(self, client):
        """Test batch validation across multiple countries."""
        payload = {
            "title": "International Documentary",
            "description": "A global documentary",
            "categories": ["documentary"],
            "rating": "G",
            "duration_minutes": 60,
            "subtitle_languages": ["ko", "ar", "en"],
            "audio_languages": ["en"],
            "ad_breaks": []
        }
        
        response = client.post(
            "/validate/batch",
            params={"countries": ["korea", "saudi_arabia"]},
            json=payload
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "summary" in data
        assert "korea" in data["results"]
        assert "saudi_arabia" in data["results"]
        assert data["summary"]["total"] == 2
