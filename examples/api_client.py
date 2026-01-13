"""Example API client for the Glocal Policy Guardrail service."""

import requests
import json


def validate_content_example():
    """Example of validating content via the API."""
    api_url = "http://localhost:8000"
    
    # Example content for Korea
    payload = {
        "content": {
            "title": "Family Animation",
            "description": "A fun family movie",
            "categories": ["animation", "family"],
            "tags": ["kids", "adventure"],
            "rating": "ALL",
            "duration_minutes": 90,
            "subtitle_languages": ["ko", "en"],
            "audio_languages": ["en"],
            "ad_breaks": [
                {"timestamp_seconds": 1800, "duration_seconds": 60}
            ]
        },
        "country": "korea"
    }
    
    print("Validating content for Korea...")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(f"{api_url}/validate", json=payload)
        response.raise_for_status()
        
        result = response.json()
        print("\nValidation Result:")
        print(json.dumps(result, indent=2))
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API server.")
        print("Make sure the API is running: python src/api.py")
    except requests.exceptions.RequestException as e:
        print(f"\nError: {e}")


def batch_validate_example():
    """Example of batch validation across multiple countries."""
    api_url = "http://localhost:8000"
    
    content = {
        "title": "International Documentary",
        "description": "A documentary suitable for global audiences",
        "categories": ["documentary"],
        "tags": ["education", "nature"],
        "rating": "G",
        "duration_minutes": 60,
        "subtitle_languages": ["ko", "ar", "en"],
        "audio_languages": ["en"],
        "ad_breaks": [
            {"timestamp_seconds": 1800, "duration_seconds": 45}
        ]
    }
    
    countries = ["korea", "saudi_arabia"]
    
    print("Batch validation across multiple countries...")
    
    try:
        response = requests.post(
            f"{api_url}/validate/batch",
            params={"countries": countries},
            json=content
        )
        response.raise_for_status()
        
        result = response.json()
        print("\nBatch Validation Results:")
        print(json.dumps(result, indent=2))
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API server.")
        print("Make sure the API is running: python src/api.py")
    except requests.exceptions.RequestException as e:
        print(f"\nError: {e}")


def list_policies_example():
    """Example of listing available policies."""
    api_url = "http://localhost:8000"
    
    print("Fetching available policies...")
    
    try:
        response = requests.get(f"{api_url}/policies")
        response.raise_for_status()
        
        result = response.json()
        print("\nAvailable Policies:")
        print(json.dumps(result, indent=2))
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API server.")
        print("Make sure the API is running: python src/api.py")
    except requests.exceptions.RequestException as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Glocal Policy Guardrail - API Client Examples")
    print("=" * 60)
    print("\nNote: Start the API server first with:")
    print("  python src/api.py")
    print("\nOr using uvicorn:")
    print("  uvicorn src.api:app --reload")
    print("=" * 60)
    
    # Run examples
    print("\n1. List Available Policies")
    print("-" * 60)
    list_policies_example()
    
    print("\n\n2. Validate Single Content")
    print("-" * 60)
    validate_content_example()
    
    print("\n\n3. Batch Validation")
    print("-" * 60)
    batch_validate_example()
