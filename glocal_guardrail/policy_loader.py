"""
Policy configuration loader and validator
"""
import os
import yaml
from typing import Dict, Any, List, Optional
from pathlib import Path


class PolicyConfig:
    """Represents a country-specific policy configuration"""
    
    def __init__(self, config_data: Dict[str, Any]):
        self.country_code = config_data.get("country_code", "")
        self.country_name = config_data.get("country_name", "")
        self.forbidden_keywords = config_data.get("forbidden_keywords", [])
        self.content_rating = config_data.get("content_rating", {})
        self.advertising = config_data.get("advertising", {})
        self.mandatory_features = config_data.get("mandatory_features", [])
        self.youth_protection = config_data.get("youth_protection", {})
        self.compliance = config_data.get("compliance", {})
        self._raw_config = config_data
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key"""
        return self._raw_config.get(key, default)
    
    def __repr__(self):
        return f"PolicyConfig(country={self.country_name}, code={self.country_code})"


class PolicyLoader:
    """Loads and manages policy configurations from YAML files"""
    
    def __init__(self, policies_dir: Optional[str] = None):
        if policies_dir is None:
            # Default to policies directory in the package
            current_dir = Path(__file__).parent.parent
            policies_dir = current_dir / "policies"
        
        self.policies_dir = Path(policies_dir)
        self._policies_cache: Dict[str, PolicyConfig] = {}
    
    def load_policy(self, country_code: str) -> PolicyConfig:
        """
        Load a policy configuration for a specific country
        
        Args:
            country_code: ISO country code (e.g., 'SA', 'KR', 'DE')
        
        Returns:
            PolicyConfig object
        
        Raises:
            FileNotFoundError: If policy file doesn't exist
            ValueError: If policy file is invalid
        """
        # Check cache first
        if country_code in self._policies_cache:
            return self._policies_cache[country_code]
        
        # Map country codes to file names
        country_file_map = {
            "SA": "saudi_arabia.yaml",
            "KR": "south_korea.yaml",
            "DE": "germany.yaml",
        }
        
        filename = country_file_map.get(country_code)
        if not filename:
            raise ValueError(f"No policy configuration found for country code: {country_code}")
        
        policy_path = self.policies_dir / filename
        
        if not policy_path.exists():
            raise FileNotFoundError(f"Policy file not found: {policy_path}")
        
        with open(policy_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        if not config_data:
            raise ValueError(f"Empty or invalid policy file: {policy_path}")
        
        policy_config = PolicyConfig(config_data)
        self._policies_cache[country_code] = policy_config
        
        return policy_config
    
    def list_available_policies(self) -> List[str]:
        """List all available country codes"""
        # Derive from country_file_map to avoid duplication
        country_file_map = {
            "SA": "saudi_arabia.yaml",
            "KR": "south_korea.yaml",
            "DE": "germany.yaml",
        }
        return list(country_file_map.keys())
    
    def clear_cache(self):
        """Clear the policy cache"""
        self._policies_cache.clear()
