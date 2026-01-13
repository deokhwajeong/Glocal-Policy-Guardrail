"""
Tests for rule engine module
"""
import pytest
from glocal_guardrail.policy_loader import PolicyLoader
from glocal_guardrail.rule_engine import RuleEngine, ValidationResult


@pytest.fixture
def saudi_policy():
    """Fixture for Saudi Arabia policy"""
    loader = PolicyLoader()
    return loader.load_policy("SA")


@pytest.fixture
def korea_policy():
    """Fixture for South Korea policy"""
    loader = PolicyLoader()
    return loader.load_policy("KR")


@pytest.fixture
def germany_policy():
    """Fixture for Germany policy"""
    loader = PolicyLoader()
    return loader.load_policy("DE")


def test_validation_result_pass():
    """Test ValidationResult with PASS status"""
    result = ValidationResult("PASS", "SA")
    assert result.is_compliant() is True
    assert len(result.violations) == 0


def test_validation_result_reject():
    """Test ValidationResult with violations"""
    result = ValidationResult("PASS", "SA")
    result.add_violation("test_rule", "Test violation")
    
    assert result.status == "REJECT"
    assert result.is_compliant() is False
    assert len(result.violations) == 1


def test_forbidden_keywords_saudi(saudi_policy):
    """Test forbidden keywords for Saudi Arabia"""
    engine = RuleEngine(saudi_policy)
    
    # Metadata with forbidden keyword
    metadata = {
        "title": "Casino Night",
        "description": "Fun gambling experience"
    }
    
    result = engine.validate(metadata)
    assert result.status == "REJECT"
    assert len(result.violations) > 0


def test_compliant_content_saudi(saudi_policy):
    """Test compliant content for Saudi Arabia"""
    engine = RuleEngine(saudi_policy)
    
    metadata = {
        "title": "Family Entertainment",
        "description": "Fun for all ages",
        "content_rating": "PG",
        "features": ["parental_controls", "content_filtering", "prayer_time_notifications"],
        "local_content_percentage": 35
    }
    
    result = engine.validate(metadata)
    assert result.status == "PASS"


def test_missing_mandatory_features_korea(korea_policy):
    """Test missing mandatory features for South Korea"""
    engine = RuleEngine(korea_policy)
    
    metadata = {
        "title": "Streaming App",
        "description": "Entertainment platform",
        "features": []  # Missing required features
    }
    
    result = engine.validate(metadata)
    assert result.status == "REJECT"
    assert any("mandatory_features" in v["rule"] for v in result.violations)


def test_real_name_verification_korea(korea_policy):
    """Test real name verification requirement for Korea"""
    engine = RuleEngine(korea_policy)
    
    # Without real name verification
    metadata = {
        "title": "App",
        "features": ["real_name_verification", "age_verification", "shutdown_system", "data_localization"],
        "real_name_verification_enabled": False,
        "data_stored_locally": True
    }
    
    result = engine.validate(metadata)
    assert result.status == "REJECT"


def test_gdpr_compliance_germany(germany_policy):
    """Test GDPR compliance for Germany"""
    engine = RuleEngine(germany_policy)
    
    # Without GDPR compliance
    metadata = {
        "title": "App",
        "features": ["gdpr_compliance", "data_privacy_controls", "youth_protection_system", "opt_in_tracking"],
        "gdpr_compliant": False
    }
    
    result = engine.validate(metadata)
    assert result.status == "REJECT"


def test_ad_duration_violation(saudi_policy):
    """Test ad duration violation"""
    engine = RuleEngine(saudi_policy)
    
    metadata = {
        "title": "App",
        "ad_duration_minutes": 10,  # Exceeds 3 minutes max
        "features": ["parental_controls", "content_filtering", "prayer_time_notifications"]
    }
    
    result = engine.validate(metadata)
    assert result.status == "REJECT"
    assert any("advertising" in v["rule"] for v in result.violations)


def test_ad_time_window_violation(saudi_policy):
    """Test ad scheduling during prayer times"""
    engine = RuleEngine(saudi_policy)
    
    metadata = {
        "title": "App",
        "ad_schedule": ["12:30"],  # During Dhuhr prayer time (12:00-13:00)
        "features": ["parental_controls", "content_filtering", "prayer_time_notifications"]
    }
    
    result = engine.validate(metadata)
    assert result.status == "REJECT"
    assert any("advertising" in v["rule"] for v in result.violations)


def test_local_content_quota(saudi_policy):
    """Test local content quota requirement"""
    engine = RuleEngine(saudi_policy)
    
    metadata = {
        "title": "App",
        "features": ["parental_controls", "content_filtering", "prayer_time_notifications"],
        "local_content_percentage": 15  # Below 30% requirement
    }
    
    result = engine.validate(metadata)
    assert result.status == "REJECT"
    assert any("regional_compliance" in v["rule"] for v in result.violations)


def test_forbidden_keywords_germany(germany_policy):
    """Test forbidden keywords for Germany"""
    engine = RuleEngine(germany_policy)
    
    metadata = {
        "title": "Historical Documentary",
        "description": "About nazi propaganda"  # Forbidden keyword
    }
    
    result = engine.validate(metadata)
    assert result.status == "REJECT"
    assert any("forbidden_keywords" in v["rule"] for v in result.violations)
