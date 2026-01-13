"""
Tests for policy loader module
"""
import pytest
from pathlib import Path
from glocal_guardrail.policy_loader import PolicyLoader, PolicyConfig


def test_load_saudi_arabia_policy():
    """Test loading Saudi Arabia policy"""
    loader = PolicyLoader()
    policy = loader.load_policy("SA")
    
    assert policy.country_code == "SA"
    assert policy.country_name == "Saudi Arabia"
    assert "gambling" in policy.forbidden_keywords
    assert "alcohol" in policy.forbidden_keywords
    assert len(policy.mandatory_features) > 0


def test_load_south_korea_policy():
    """Test loading South Korea policy"""
    loader = PolicyLoader()
    policy = loader.load_policy("KR")
    
    assert policy.country_code == "KR"
    assert policy.country_name == "South Korea"
    assert "real_name_verification" in policy.mandatory_features
    assert policy.compliance.get("requires_real_name") is True


def test_load_germany_policy():
    """Test loading Germany policy"""
    loader = PolicyLoader()
    policy = loader.load_policy("DE")
    
    assert policy.country_code == "DE"
    assert policy.country_name == "Germany"
    assert "nazi" in policy.forbidden_keywords
    assert "gdpr_compliance" in policy.mandatory_features


def test_invalid_country_code():
    """Test loading policy with invalid country code"""
    loader = PolicyLoader()
    
    with pytest.raises(ValueError):
        loader.load_policy("XX")


def test_policy_caching():
    """Test that policies are cached"""
    loader = PolicyLoader()
    
    policy1 = loader.load_policy("SA")
    policy2 = loader.load_policy("SA")
    
    assert policy1 is policy2  # Same object reference


def test_list_available_policies():
    """Test listing available policies"""
    loader = PolicyLoader()
    policies = loader.list_available_policies()
    
    assert "SA" in policies
    assert "KR" in policies
    assert "DE" in policies
    assert len(policies) == 3


def test_clear_cache():
    """Test clearing policy cache"""
    loader = PolicyLoader()
    
    policy1 = loader.load_policy("SA")
    loader.clear_cache()
    policy2 = loader.load_policy("SA")
    
    assert policy1 is not policy2  # Different objects after cache clear
