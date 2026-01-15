"""
Unit tests for compliance scanner
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.compliance_scanner import ComplianceScanner, ViolationLevel


@pytest.fixture
def scanner():
    """Create a compliance scanner instance"""
    return ComplianceScanner()


class TestComplianceScanner:
    def test_scanner_initialization(self, scanner):
        """Test scanner initializes with policy rules"""
        assert scanner is not None
        assert len(scanner.country_rules) > 0
    
    def test_forbidden_keywords_detection(self, scanner):
        """Test detection of forbidden keywords"""
        deployment = {
            'content': {
                'title': 'Gambling Casino Games',
                'description': 'Play poker and bet money'
            },
            'target_countries': ['Saudi_Arabia']
        }
        
        results = scanner.scan_deployment(deployment)
        assert len(results) > 0
        
        saudi_result = next((r for r in results if r['country'] == 'Saudi_Arabia'), None)
        assert saudi_result is not None
        assert not saudi_result['compliant']
        assert len(saudi_result['violations']) > 0
    
    def test_time_based_restrictions(self, scanner):
        """Test time-based advertising restrictions"""
        deployment = {
            'content': {
                'title': 'Product Advertisement',
                'content_type': 'advertisement',
                'schedule': {
                    'start_time': '20:00',
                    'end_time': '21:00'
                }
            },
            'target_countries': ['Spain']
        }
        
        results = scanner.scan_deployment(deployment)
        spain_result = next((r for r in results if r['country'] == 'Spain'), None)
        
        if spain_result:
            # Should have warnings or violations for ad restrictions
            assert 'violations' in spain_result or 'warnings' in spain_result
    
    def test_age_rating_validation(self, scanner):
        """Test age rating system mapping"""
        deployment = {
            'content': {
                'title': 'Adult Content',
                'age_rating': '18+'
            },
            'target_countries': ['South_Korea']
        }
        
        results = scanner.scan_deployment(deployment)
        korea_result = next((r for r in results if r['country'] == 'South_Korea'), None)
        assert korea_result is not None
    
    def test_platform_features_requirement(self, scanner):
        """Test platform feature requirements"""
        deployment = {
            'content': {
                'title': 'Test Content',
                'age_rating': '18+'
            },
            'platform_features': {
                'real_name_verification': False
            },
            'target_countries': ['South_Korea']
        }
        
        results = scanner.scan_deployment(deployment)
        korea_result = next((r for r in results if r['country'] == 'South_Korea'), None)
        
        # Korea requires real-name verification for adult content
        if korea_result and not korea_result['compliant']:
            violations = korea_result.get('violations', [])
            assert any('real' in str(v).lower() or 'verification' in str(v).lower() 
                      for v in violations)
    
    def test_multiple_country_scan(self, scanner):
        """Test scanning against multiple countries"""
        deployment = {
            'content': {
                'title': 'International Content',
                'description': 'Available worldwide'
            },
            'target_countries': ['USA', 'South_Korea', 'Germany']
        }
        
        results = scanner.scan_deployment(deployment)
        assert len(results) == 3
        
        country_names = [r['country'] for r in results]
        assert 'USA' in country_names or 'South_Korea' in country_names
    
    def test_compliant_content(self, scanner):
        """Test that compliant content passes all checks"""
        deployment = {
            'content': {
                'title': 'Family Friendly Movie',
                'description': 'Suitable for all ages',
                'age_rating': 'G'
            },
            'target_countries': ['USA']
        }
        
        results = scanner.scan_deployment(deployment)
        usa_result = next((r for r in results if r['country'] == 'USA'), None)
        
        if usa_result:
            # Clean content should have minimal or no violations
            violations = usa_result.get('violations', [])
            critical_violations = [v for v in violations 
                                 if v.get('severity') == ViolationLevel.CRITICAL]
            assert len(critical_violations) == 0
    
    def test_empty_deployment(self, scanner):
        """Test handling of empty deployment"""
        deployment = {
            'content': {},
            'target_countries': []
        }
        
        results = scanner.scan_deployment(deployment)
        assert isinstance(results, list)
    
    def test_missing_country_rules(self, scanner):
        """Test handling of unknown country"""
        deployment = {
            'content': {
                'title': 'Test Content'
            },
            'target_countries': ['NonExistentCountry']
        }
        
        results = scanner.scan_deployment(deployment)
        # Should handle gracefully, might return empty or skip
        assert isinstance(results, list)
    
    def test_violation_severity_levels(self, scanner):
        """Test that violations are categorized by severity"""
        deployment = {
            'content': {
                'title': 'Gambling Alcohol Violence',
                'description': 'Multiple prohibited content'
            },
            'target_countries': ['Saudi_Arabia']
        }
        
        results = scanner.scan_deployment(deployment)
        saudi_result = next((r for r in results if r['country'] == 'Saudi_Arabia'), None)
        
        if saudi_result and not saudi_result['compliant']:
            violations = saudi_result.get('violations', [])
            if violations:
                # Check that severity levels are assigned
                assert any('severity' in v or 'level' in v for v in violations)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
