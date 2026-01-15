"""
Unit tests for policy auto-updater
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.policy_auto_updater import PolicyUpdateMonitor, RegulatorySource


@pytest.fixture
def monitor():
    """Create policy update monitor instance"""
    return PolicyUpdateMonitor()


class TestPolicyUpdateMonitor:
    def test_monitor_initialization(self, monitor):
        """Test monitor initializes with sources"""
        assert monitor is not None
        assert len(monitor.sources) > 0
    
    def test_sources_have_required_fields(self, monitor):
        """Test all sources have required fields"""
        for source in monitor.sources:
            assert 'country' in source
            assert 'name' in source
            assert 'url' in source
            assert 'type' in source
    
    def test_source_types_valid(self, monitor):
        """Test all source types are valid"""
        valid_types = ['rss', 'web', 'api']
        for source in monitor.sources:
            assert source['type'] in valid_types
    
    def test_check_updates_returns_list(self, monitor):
        """Test check_updates returns a list"""
        results = monitor.check_updates()
        assert isinstance(results, list)
    
    def test_regulatory_source_dataclass(self):
        """Test RegulatorySource dataclass"""
        source = RegulatorySource(
            country="Test Country",
            name="Test Source",
            url="https://example.com",
            type="rss"
        )
        assert source.country == "Test Country"
        assert source.url == "https://example.com"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
