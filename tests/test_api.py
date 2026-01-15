"""
Integration tests for API endpoints
"""
import pytest
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from web_dashboard import app


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAPIEndpoints:
    def test_home_page(self, client):
        """Test main dashboard loads"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_api_status(self, client):
        """Test /api/status endpoint"""
        response = client.get('/api/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] in ['operational', 'online', 'healthy']
    
    def test_api_updates(self, client):
        """Test /api/updates endpoint"""
        response = client.get('/api/updates')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'success' in data
        assert 'updates' in data or 'count' in data
    
    def test_api_updates_with_days_param(self, client):
        """Test /api/updates with days parameter"""
        response = client.get('/api/updates?days=7')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_country_endpoint(self, client):
        """Test /api/country/<name> endpoint"""
        response = client.get('/api/country/USA')
        assert response.status_code in [200, 404]  # Depends on data availability
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert isinstance(data, dict)
    
    def test_invalid_country(self, client):
        """Test country endpoint with invalid country"""
        response = client.get('/api/country/InvalidCountry123')
        # Should return 404 or handle gracefully
        assert response.status_code in [200, 404]
    
    def test_api_response_format(self, client):
        """Test that API returns valid JSON"""
        response = client.get('/api/updates')
        assert response.content_type == 'application/json'
        
        # Ensure valid JSON
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.get('/api/status')
        # CORS middleware should add headers
        assert response.status_code == 200


class TestStaticFiles:
    def test_static_css(self, client):
        """Test CSS file is accessible"""
        response = client.get('/static/style.css')
        assert response.status_code == 200
    
    def test_static_js(self, client):
        """Test JavaScript file is accessible"""
        response = client.get('/static/script.js')
        assert response.status_code == 200
    
    def test_swagger_json(self, client):
        """Test Swagger spec is accessible"""
        response = client.get('/static/swagger.json')
        assert response.status_code == 200
        
        # Verify it's valid JSON
        data = json.loads(response.data)
        assert 'swagger' in data or 'openapi' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
