"""Example usage of the Glocal Policy Guardrail framework."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from guardrail.rule_engine import RuleEngine, ValidationStatus


def example_korea_validation():
    """Example: Validate content for Korea deployment."""
    print("=" * 60)
    print("Example 1: Korea Content Validation")
    print("=" * 60)
    
    # Initialize rule engine
    engine = RuleEngine()
    
    # Example content that should PASS
    content_pass = {
        "title": "Family Adventure Movie",
        "description": "A heartwarming family adventure",
        "categories": ["family", "adventure"],
        "tags": ["family-friendly", "animation"],
        "rating": "ALL",
        "duration_minutes": 90,
        "subtitle_languages": ["ko", "en"],
        "audio_languages": ["en", "ko"],
        "ad_breaks": [
            {"timestamp_seconds": 1800, "duration_seconds": 60}
        ]
    }
    
    result = engine.validate_content(content_pass, "korea")
    print(f"\nContent: {content_pass['title']}")
    print(f"Status: {result.status.value}")
    print(f"Violations: {result.violations if result.violations else 'None'}")
    print(f"Warnings: {result.warnings if result.warnings else 'None'}")
    
    # Example content that should REJECT
    content_reject = {
        "title": "Gambling Documentary",
        "description": "A documentary about gambling culture",
        "categories": ["documentary", "unrated_gambling"],
        "tags": ["gambling", "casino"],
        "rating": "19",
        "duration_minutes": 60,
        "subtitle_languages": ["en"],  # Missing Korean subtitles
        "audio_languages": ["en"],
        "ad_breaks": []
    }
    
    result = engine.validate_content(content_reject, "korea")
    print(f"\nContent: {content_reject['title']}")
    print(f"Status: {result.status.value}")
    print(f"Violations:")
    for violation in result.violations:
        print(f"  - {violation}")


def example_saudi_arabia_validation():
    """Example: Validate content for Saudi Arabia deployment."""
    print("\n" + "=" * 60)
    print("Example 2: Saudi Arabia Content Validation")
    print("=" * 60)
    
    engine = RuleEngine()
    
    # Example content that should PASS
    content_pass = {
        "title": "Nature Documentary",
        "description": "Exploring the wonders of nature",
        "categories": ["documentary", "nature"],
        "tags": ["educational", "family"],
        "rating": "G",
        "duration_minutes": 45,
        "subtitle_languages": ["ar", "en"],
        "audio_languages": ["en", "ar"],
        "ad_breaks": [
            {"timestamp_seconds": 1200, "duration_seconds": 45}
        ]
    }
    
    result = engine.validate_content(content_pass, "saudi_arabia")
    print(f"\nContent: {content_pass['title']}")
    print(f"Status: {result.status.value}")
    print(f"Violations: {result.violations if result.violations else 'None'}")
    
    # Example content that should REJECT
    content_reject = {
        "title": "Dating Reality Show",
        "description": "A romantic dating show featuring alcohol",
        "categories": ["reality", "dating_shows"],
        "tags": ["romance", "dating", "alcohol"],
        "rating": "18",
        "duration_minutes": 60,
        "subtitle_languages": ["en"],  # Missing Arabic
        "audio_languages": ["en"],
        "ad_breaks": []
    }
    
    result = engine.validate_content(content_reject, "saudi_arabia")
    print(f"\nContent: {content_reject['title']}")
    print(f"Status: {result.status.value}")
    print(f"Violations:")
    for violation in result.violations:
        print(f"  - {violation}")


def example_ad_window_validation():
    """Example: Validate ad window restrictions."""
    print("\n" + "=" * 60)
    print("Example 3: Ad Window Restrictions")
    print("=" * 60)
    
    engine = RuleEngine()
    
    # Content with too many ads
    content = {
        "title": "Movie with Too Many Ads",
        "description": "A movie with excessive advertising",
        "categories": ["action"],
        "rating": "15",
        "duration_minutes": 60,  # 1 hour
        "subtitle_languages": ["ko"],
        "audio_languages": ["en"],
        "ad_breaks": [
            {"timestamp_seconds": 300, "duration_seconds": 100},   # Too long
            {"timestamp_seconds": 400, "duration_seconds": 60},    # Too close
            {"timestamp_seconds": 900, "duration_seconds": 60},
            {"timestamp_seconds": 1200, "duration_seconds": 60},
            {"timestamp_seconds": 1500, "duration_seconds": 60},
            {"timestamp_seconds": 1800, "duration_seconds": 60},
            {"timestamp_seconds": 2100, "duration_seconds": 60},
            {"timestamp_seconds": 2400, "duration_seconds": 60},
            {"timestamp_seconds": 2700, "duration_seconds": 60},
            {"timestamp_seconds": 3000, "duration_seconds": 60},
        ]
    }
    
    result = engine.validate_content(content, "korea")
    print(f"\nContent: {content['title']}")
    print(f"Status: {result.status.value}")
    print(f"Violations:")
    for violation in result.violations:
        print(f"  - {violation}")


if __name__ == "__main__":
    example_korea_validation()
    example_saudi_arabia_validation()
    example_ad_window_validation()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
