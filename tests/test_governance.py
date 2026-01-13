"""
Tests for governance module
"""
import pytest
from glocal_guardrail.governance import GovernanceEngine


@pytest.fixture
def governance():
    """Fixture for GovernanceEngine"""
    return GovernanceEngine()


def test_check_single_country_pass(governance):
    """Test single country check that passes"""
    metadata = {
        "title": "Family Show",
        "description": "Entertainment for everyone",
        "features": ["gdpr_compliance", "data_privacy_controls", "youth_protection_system", "opt_in_tracking"],
        "gdpr_compliant": True
    }
    
    result = governance.check_single_country(metadata, "DE")
    assert result.is_compliant() is True
    assert result.status == "PASS"


def test_check_single_country_reject(governance):
    """Test single country check that rejects"""
    metadata = {
        "title": "Gambling App",
        "description": "Casino games"
    }
    
    result = governance.check_single_country(metadata, "SA")
    assert result.is_compliant() is False
    assert result.status == "REJECT"


def test_check_multiple_countries(governance):
    """Test checking multiple countries"""
    metadata = {
        "title": "Streaming App",
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
        "local_content_percentage": 35
    }
    
    results = governance.check_compliance(metadata, ["SA", "KR", "DE"])
    
    assert len(results) == 3
    assert "SA" in results
    assert "KR" in results
    assert "DE" in results


def test_deployment_readiness_all_pass(governance):
    """Test deployment readiness when all countries pass"""
    metadata = {
        "title": "Universal App",
        "description": "Compliant everywhere",
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
    }
    
    report = governance.get_deployment_readiness(metadata, ["SA", "KR", "DE"])
    
    assert report["overall_status"] == "PASS"
    assert report["deployment_ready"] is True
    assert len(report["compliant_countries"]) == 3
    assert len(report["non_compliant_countries"]) == 0


def test_deployment_readiness_partial_reject(governance):
    """Test deployment readiness when some countries reject"""
    metadata = {
        "title": "Alcohol Store",
        "description": "Buy wine and beer online",
        "features": []
    }
    
    report = governance.get_deployment_readiness(metadata, ["SA", "DE"])
    
    assert report["overall_status"] == "REJECT"
    assert report["deployment_ready"] is False
    assert "SA" in report["non_compliant_countries"]  # Forbidden keywords


def test_invalid_country_code(governance):
    """Test handling invalid country code"""
    metadata = {"title": "Test"}
    
    result = governance.check_single_country(metadata, "XX")
    assert result.status == "REJECT"
    assert len(result.violations) > 0
