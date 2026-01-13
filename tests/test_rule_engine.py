"""Unit tests for the Rule Engine."""

import sys
from pathlib import Path
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from guardrail.rule_engine import RuleEngine, ValidationStatus


@pytest.fixture
def rule_engine():
    """Create a rule engine instance."""
    return RuleEngine()


class TestKoreaPolicy:
    """Test Korea policy validation."""
    
    def test_valid_content_passes(self, rule_engine):
        """Test that valid content passes Korea validation."""
        content = {
            "title": "Family Movie",
            "description": "A family-friendly film",
            "categories": ["family"],
            "rating": "ALL",
            "duration_minutes": 90,
            "subtitle_languages": ["ko"],
            "audio_languages": ["en"],
            "ad_breaks": []
        }
        
        result = rule_engine.validate_content(content, "korea")
        assert result.status == ValidationStatus.PASS
        assert len(result.violations) == 0
    
    def test_forbidden_keyword_rejects(self, rule_engine):
        """Test that forbidden keywords trigger rejection."""
        content = {
            "title": "Gambling Documentary",
            "description": "About gambling",
            "categories": ["documentary"],
            "rating": "19",
            "subtitle_languages": ["ko"],
            "ad_breaks": []
        }
        
        result = rule_engine.validate_content(content, "korea")
        assert result.status == ValidationStatus.REJECT
        assert any("gambling" in v.lower() for v in result.violations)
    
    def test_forbidden_category_rejects(self, rule_engine):
        """Test that forbidden categories trigger rejection."""
        content = {
            "title": "Test Content",
            "categories": ["adult_content"],
            "rating": "19",
            "subtitle_languages": ["ko"],
            "ad_breaks": []
        }
        
        result = rule_engine.validate_content(content, "korea")
        assert result.status == ValidationStatus.REJECT
        assert any("forbidden categories" in v.lower() for v in result.violations)
    
    def test_missing_korean_subtitles_rejects(self, rule_engine):
        """Test that missing Korean subtitles triggers rejection."""
        content = {
            "title": "Foreign Film",
            "categories": ["drama"],
            "rating": "15",
            "subtitle_languages": ["en"],  # Missing Korean
            "ad_breaks": []
        }
        
        result = rule_engine.validate_content(content, "korea")
        assert result.status == ValidationStatus.REJECT
        assert any("korean" in v.lower() or "ko" in v.lower() for v in result.violations)
    
    def test_invalid_rating_rejects(self, rule_engine):
        """Test that invalid ratings trigger rejection."""
        content = {
            "title": "Test Movie",
            "categories": ["action"],
            "rating": "R",  # Not a valid Korean rating
            "subtitle_languages": ["ko"],
            "ad_breaks": []
        }
        
        result = rule_engine.validate_content(content, "korea")
        assert result.status == ValidationStatus.REJECT
        assert any("rating" in v.lower() for v in result.violations)


class TestSaudiArabiaPolicy:
    """Test Saudi Arabia policy validation."""
    
    def test_valid_content_passes(self, rule_engine):
        """Test that valid content passes Saudi Arabia validation."""
        content = {
            "title": "Nature Documentary",
            "description": "Beautiful nature scenes",
            "categories": ["documentary"],
            "rating": "G",
            "duration_minutes": 60,
            "subtitle_languages": ["ar", "en"],
            "audio_languages": ["en"],
            "ad_breaks": []
        }
        
        result = rule_engine.validate_content(content, "saudi_arabia")
        assert result.status == ValidationStatus.PASS
        assert len(result.violations) == 0
    
    def test_forbidden_alcohol_keyword_rejects(self, rule_engine):
        """Test that alcohol-related content is rejected."""
        content = {
            "title": "Wine Documentary",
            "description": "About alcohol production",
            "categories": ["documentary"],
            "rating": "18",
            "subtitle_languages": ["ar"],
            "ad_breaks": []
        }
        
        result = rule_engine.validate_content(content, "saudi_arabia")
        assert result.status == ValidationStatus.REJECT
        assert any("alcohol" in v.lower() for v in result.violations)
    
    def test_dating_show_category_rejects(self, rule_engine):
        """Test that dating shows are rejected."""
        content = {
            "title": "Dating Show",
            "categories": ["dating_shows"],
            "rating": "15",
            "subtitle_languages": ["ar"],
            "ad_breaks": []
        }
        
        result = rule_engine.validate_content(content, "saudi_arabia")
        assert result.status == ValidationStatus.REJECT
        assert any("forbidden categories" in v.lower() for v in result.violations)
    
    def test_missing_arabic_subtitles_rejects(self, rule_engine):
        """Test that missing Arabic subtitles triggers rejection."""
        content = {
            "title": "Foreign Film",
            "categories": ["drama"],
            "rating": "PG",
            "subtitle_languages": ["en"],  # Missing Arabic
            "ad_breaks": []
        }
        
        result = rule_engine.validate_content(content, "saudi_arabia")
        assert result.status == ValidationStatus.REJECT
        assert any("arabic" in v.lower() or "ar" in v.lower() for v in result.violations)


class TestAdWindowRestrictions:
    """Test advertisement window restrictions."""
    
    def test_korea_ad_duration_limit(self, rule_engine):
        """Test Korea max ad duration enforcement."""
        content = {
            "title": "Test Content",
            "categories": ["action"],
            "rating": "15",
            "duration_minutes": 120,
            "subtitle_languages": ["ko"],
            "ad_breaks": [
                {"timestamp_seconds": 1800, "duration_seconds": 100}  # Exceeds 90s limit
            ]
        }
        
        result = rule_engine.validate_content(content, "korea")
        assert result.status == ValidationStatus.REJECT
        assert any("exceeds maximum duration" in v.lower() for v in result.violations)
    
    def test_korea_min_interval_enforcement(self, rule_engine):
        """Test Korea minimum interval between ads."""
        content = {
            "title": "Test Content",
            "categories": ["action"],
            "rating": "15",
            "duration_minutes": 120,
            "subtitle_languages": ["ko"],
            "ad_breaks": [
                {"timestamp_seconds": 600, "duration_seconds": 60},
                {"timestamp_seconds": 800, "duration_seconds": 60}  # Too close (200s < 600s)
            ]
        }
        
        result = rule_engine.validate_content(content, "korea")
        assert result.status == ValidationStatus.REJECT
        assert any("too close" in v.lower() for v in result.violations)
    
    def test_saudi_arabia_ad_duration_limit(self, rule_engine):
        """Test Saudi Arabia max ad duration enforcement."""
        content = {
            "title": "Test Content",
            "categories": ["documentary"],
            "rating": "G",
            "duration_minutes": 60,
            "subtitle_languages": ["ar"],
            "ad_breaks": [
                {"timestamp_seconds": 1800, "duration_seconds": 70}  # Exceeds 60s limit
            ]
        }
        
        result = rule_engine.validate_content(content, "saudi_arabia")
        assert result.status == ValidationStatus.REJECT
        assert any("exceeds maximum duration" in v.lower() for v in result.violations)


class TestRuleEngineCore:
    """Test core rule engine functionality."""
    
    def test_load_policy_korea(self, rule_engine):
        """Test loading Korea policy."""
        policy = rule_engine.load_policy("korea")
        assert policy is not None
        assert "forbidden_content" in policy
        assert "rating_requirements" in policy
        assert "ad_windows" in policy
    
    def test_load_policy_saudi_arabia(self, rule_engine):
        """Test loading Saudi Arabia policy."""
        policy = rule_engine.load_policy("saudi_arabia")
        assert policy is not None
        assert "forbidden_content" in policy
        assert "rating_requirements" in policy
    
    def test_load_nonexistent_policy_raises_error(self, rule_engine):
        """Test that loading non-existent policy raises error."""
        with pytest.raises(FileNotFoundError):
            rule_engine.load_policy("nonexistent_country")
    
    def test_policy_caching(self, rule_engine):
        """Test that policies are cached after first load."""
        policy1 = rule_engine.load_policy("korea")
        policy2 = rule_engine.load_policy("korea")
        assert policy1 is policy2  # Same object due to caching
