"""
Example API client for testing the FastAPI endpoints
"""
import requests
import json


API_BASE_URL = "http://localhost:8000"


def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_list_policies():
    """Test list policies endpoint"""
    print("Listing available policies...")
    response = requests.get(f"{API_BASE_URL}/policies")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_validate_saudi():
    """Test validation for Saudi Arabia"""
    print("Validating content for Saudi Arabia...")
    
    request_data = {
        "metadata": {
            "title": "Family Show",
            "description": "Wholesome entertainment",
            "features": [
                "parental_controls",
                "content_filtering",
                "prayer_time_notifications"
            ],
            "local_content_percentage": 35,
            "ad_duration_minutes": 2
        },
        "target_countries": ["SA"]
    }
    
    response = requests.post(f"{API_BASE_URL}/validate", json=request_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_deployment_check():
    """Test deployment readiness check"""
    print("Testing deployment readiness for multiple countries...")
    
    request_data = {
        "metadata": {
            "title": "Global Streaming App",
            "description": "Entertainment platform",
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
    
    response = requests.post(f"{API_BASE_URL}/deployment-check", json=request_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_forbidden_content():
    """Test validation with forbidden content"""
    print("Testing forbidden content detection...")
    
    metadata = {
        "title": "Casino Games",
        "description": "Gambling and betting platform",
        "features": []
    }
    
    response = requests.post(f"{API_BASE_URL}/validate/SA", json=metadata)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Glocal Policy Guardrail - API Client Examples")
    print("=" * 60)
    print("\nMake sure the API server is running:")
    print("  python -m glocal_guardrail.api")
    print("\nor:")
    print("  uvicorn glocal_guardrail.api:app --reload")
    print("\n" + "=" * 60 + "\n")
    
    try:
        test_health()
        test_list_policies()
        test_validate_saudi()
        test_deployment_check()
        test_forbidden_content()
        
        print("=" * 60)
        print("All API tests completed!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API server.")
        print("Please start the server first with:")
        print("  python -m glocal_guardrail.api")
