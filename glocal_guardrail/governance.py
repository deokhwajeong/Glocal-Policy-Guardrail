"""
Governance logic for pre-deployment checks
"""
from typing import Dict, Any, List
from .policy_loader import PolicyLoader, PolicyConfig
from .rule_engine import RuleEngine, ValidationResult


class GovernanceEngine:
    """
    Pre-deployment check system that returns PASS or REJECT status
    based on regional compliance triggers
    """
    
    def __init__(self, policies_dir: str = None):
        self.policy_loader = PolicyLoader(policies_dir)
    
    def check_compliance(
        self, 
        metadata: Dict[str, Any], 
        target_countries: List[str]
    ) -> Dict[str, ValidationResult]:
        """
        Perform pre-deployment compliance check for multiple countries
        
        Args:
            metadata: Content/app metadata to validate
            target_countries: List of country codes to check against
        
        Returns:
            Dictionary mapping country codes to ValidationResult objects
        """
        results = {}
        
        for country_code in target_countries:
            try:
                policy = self.policy_loader.load_policy(country_code)
                engine = RuleEngine(policy)
                result = engine.validate(metadata)
                results[country_code] = result
            except (FileNotFoundError, ValueError) as e:
                # Create a REJECT result for missing/invalid policies
                result = ValidationResult("REJECT", country_code)
                result.add_violation(
                    "policy_error",
                    f"Policy validation error: {str(e)}",
                    "critical"
                )
                results[country_code] = result
        
        return results
    
    def check_single_country(
        self, 
        metadata: Dict[str, Any], 
        country_code: str
    ) -> ValidationResult:
        """
        Perform pre-deployment compliance check for a single country
        
        Args:
            metadata: Content/app metadata to validate
            country_code: Country code to check against (e.g., 'SA', 'KR', 'DE')
        
        Returns:
            ValidationResult object with PASS or REJECT status
        """
        try:
            policy = self.policy_loader.load_policy(country_code)
            engine = RuleEngine(policy)
            return engine.validate(metadata)
        except (FileNotFoundError, ValueError) as e:
            result = ValidationResult("REJECT", country_code)
            result.add_violation(
                "policy_error",
                f"Policy validation error: {str(e)}",
                "critical"
            )
            return result
    
    def get_deployment_readiness(
        self,
        metadata: Dict[str, Any],
        target_countries: List[str]
    ) -> Dict[str, Any]:
        """
        Get comprehensive deployment readiness report
        
        Args:
            metadata: Content/app metadata to validate
            target_countries: List of country codes to check against
        
        Returns:
            Dictionary with overall status and per-country results
        """
        results = self.check_compliance(metadata, target_countries)
        
        overall_status = "PASS"
        compliant_countries = []
        non_compliant_countries = []
        
        for country_code, result in results.items():
            if result.is_compliant():
                compliant_countries.append(country_code)
            else:
                non_compliant_countries.append(country_code)
                overall_status = "REJECT"
        
        return {
            "overall_status": overall_status,
            "deployment_ready": overall_status == "PASS",
            "total_countries": len(target_countries),
            "compliant_countries": compliant_countries,
            "non_compliant_countries": non_compliant_countries,
            "results": {
                country: result.to_dict() 
                for country, result in results.items()
            }
        }
