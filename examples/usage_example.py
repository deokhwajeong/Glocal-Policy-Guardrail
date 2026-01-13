"""
Example usage of Glocal Policy Guardrail framework
"""
from glocal_guardrail.governance import GovernanceEngine


def example_saudi_arabia_validation():
    """Example: Validate content for Saudi Arabia"""
    print("=" * 60)
    print("Example 1: Saudi Arabia Validation")
    print("=" * 60)
    
    governance = GovernanceEngine()
    
    # Example metadata for a streaming app
    metadata = {
        "title": "Family Entertainment Hub",
        "description": "Wholesome content for all ages",
        "content_rating": "PG",
        "features": [
            "parental_controls",
            "content_filtering",
            "prayer_time_notifications"
        ],
        "local_content_percentage": 35,
        "ad_duration_minutes": 2,
        "ad_schedule": ["10:00", "14:00", "20:00"]  # Outside prayer times
    }
    
    result = governance.check_single_country(metadata, "SA")
    
    print(f"\nStatus: {result.status}")
    print(f"Compliant: {result.is_compliant()}")
    print(f"Violations: {len(result.violations)}")
    print(f"Warnings: {len(result.warnings)}")
    
    if result.violations:
        print("\nViolations:")
        for v in result.violations:
            print(f"  - [{v['rule']}] {v['message']}")
    
    return result


def example_multi_country_validation():
    """Example: Validate for multiple countries"""
    print("\n" + "=" * 60)
    print("Example 2: Multi-Country Deployment Check")
    print("=" * 60)
    
    governance = GovernanceEngine()
    
    # Example metadata for a globally compliant app
    metadata = {
        "title": "Global Streaming Platform",
        "description": "Entertainment for everyone worldwide",
        "content_rating": "PG",
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
        "local_content_percentage": 35,
        "real_name_verification_enabled": True,
        "gdpr_compliant": True,
        "data_stored_locally": True,
        "ad_duration_minutes": 2
    }
    
    report = governance.get_deployment_readiness(
        metadata,
        ["SA", "KR", "DE"]
    )
    
    print(f"\nOverall Status: {report['overall_status']}")
    print(f"Deployment Ready: {report['deployment_ready']}")
    print(f"Total Countries: {report['total_countries']}")
    print(f"Compliant: {', '.join(report['compliant_countries'])}")
    
    if report['non_compliant_countries']:
        print(f"Non-Compliant: {', '.join(report['non_compliant_countries'])}")
    
    print("\nPer-Country Results:")
    for country, result in report['results'].items():
        status_icon = "✓" if result['is_compliant'] else "✗"
        print(f"  {status_icon} {country}: {result['status']} ({result['violation_count']} violations)")
    
    return report


def example_forbidden_content():
    """Example: Content with forbidden keywords"""
    print("\n" + "=" * 60)
    print("Example 3: Forbidden Content Detection")
    print("=" * 60)
    
    governance = GovernanceEngine()
    
    # Example with forbidden keywords for Saudi Arabia
    metadata = {
        "title": "Casino Night Special",
        "description": "Experience the thrill of gambling and win big prizes",
        "tags": ["casino", "gambling", "betting"],
        "features": ["parental_controls"]
    }
    
    result = governance.check_single_country(metadata, "SA")
    
    print(f"\nStatus: {result.status}")
    print(f"Compliant: {result.is_compliant()}")
    
    if result.violations:
        print("\nViolations Detected:")
        for v in result.violations:
            print(f"  - {v['message']} (Severity: {v['severity']})")
    
    return result


def example_korea_real_name():
    """Example: South Korea real name verification"""
    print("\n" + "=" * 60)
    print("Example 4: South Korea Real Name Verification")
    print("=" * 60)
    
    governance = GovernanceEngine()
    
    # Example without real name verification (non-compliant)
    metadata_bad = {
        "title": "Social Media App",
        "description": "Connect with friends",
        "features": ["age_verification"],
        "real_name_verification_enabled": False
    }
    
    result_bad = governance.check_single_country(metadata_bad, "KR")
    print(f"\nWithout Real Name Verification: {result_bad.status}")
    
    # Example with real name verification (compliant)
    metadata_good = {
        "title": "Social Media App",
        "description": "Connect with friends",
        "features": [
            "real_name_verification",
            "age_verification",
            "shutdown_system",
            "data_localization"
        ],
        "real_name_verification_enabled": True,
        "data_stored_locally": True,
        "local_content_percentage": 25
    }
    
    result_good = governance.check_single_country(metadata_good, "KR")
    print(f"With Real Name Verification: {result_good.status}")
    
    return result_good


if __name__ == "__main__":
    # Run all examples
    example_saudi_arabia_validation()
    example_multi_country_validation()
    example_forbidden_content()
    example_korea_real_name()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
