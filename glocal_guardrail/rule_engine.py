"""
Rule engine for validating content/app metadata against policy rules
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, time
from .policy_loader import PolicyConfig


class ValidationResult:
    """Represents the result of a policy validation"""
    
    def __init__(self, status: str, country_code: str):
        self.status = status  # 'PASS' or 'REJECT'
        self.country_code = country_code
        self.violations: List[Dict[str, str]] = []
        self.warnings: List[Dict[str, str]] = []
    
    def add_violation(self, rule: str, message: str, severity: str = "critical"):
        """Add a policy violation"""
        self.violations.append({
            "rule": rule,
            "message": message,
            "severity": severity
        })
        self.status = "REJECT"
    
    def add_warning(self, rule: str, message: str):
        """Add a policy warning"""
        self.warnings.append({
            "rule": rule,
            "message": message
        })
    
    def is_compliant(self) -> bool:
        """Check if the validation passed"""
        return self.status == "PASS"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "status": self.status,
            "country_code": self.country_code,
            "is_compliant": self.is_compliant(),
            "violations": self.violations,
            "warnings": self.warnings,
            "violation_count": len(self.violations),
            "warning_count": len(self.warnings)
        }
    
    def __repr__(self):
        return f"ValidationResult(status={self.status}, violations={len(self.violations)})"


class RuleEngine:
    """
    Core rule engine for validating content/app metadata against policies
    """
    
    def __init__(self, policy: PolicyConfig):
        self.policy = policy
    
    def validate(self, metadata: Dict[str, Any]) -> ValidationResult:
        """
        Validate content/app metadata against the loaded policy
        
        Args:
            metadata: Dictionary containing content/app metadata
        
        Returns:
            ValidationResult object with PASS or REJECT status
        """
        result = ValidationResult("PASS", self.policy.country_code)
        
        # Run all validation checks
        self._check_forbidden_keywords(metadata, result)
        self._check_content_rating(metadata, result)
        self._check_mandatory_features(metadata, result)
        self._check_advertising_compliance(metadata, result)
        self._check_youth_protection(metadata, result)
        self._check_regional_compliance(metadata, result)
        
        return result
    
    def _check_forbidden_keywords(self, metadata: Dict[str, Any], result: ValidationResult):
        """Check for forbidden keywords in content metadata"""
        forbidden = self.policy.forbidden_keywords
        if not forbidden:
            return
        
        # Check in various metadata fields
        searchable_fields = [
            metadata.get("title", ""),
            metadata.get("description", ""),
            " ".join(metadata.get("tags", [])),
            " ".join(metadata.get("keywords", []))
        ]
        
        content_text = " ".join(searchable_fields).lower()
        
        for keyword in forbidden:
            if keyword.lower() in content_text:
                result.add_violation(
                    "forbidden_keywords",
                    f"Forbidden keyword detected: '{keyword}'",
                    "critical"
                )
    
    def _check_content_rating(self, metadata: Dict[str, Any], result: ValidationResult):
        """Check content rating compliance"""
        rating_config = self.policy.content_rating
        if not rating_config:
            return
        
        content_rating = metadata.get("content_rating", "")
        minimum_age = rating_config.get("minimum_age", 0)
        prohibited_ratings = rating_config.get("prohibited_ratings", [])
        allowed_ratings = rating_config.get("allowed_ratings", [])
        
        # Check prohibited ratings
        if content_rating in prohibited_ratings:
            result.add_violation(
                "content_rating",
                f"Content rating '{content_rating}' is prohibited in {self.policy.country_name}",
                "critical"
            )
        
        # Check allowed ratings (if specified)
        if allowed_ratings and content_rating and content_rating not in allowed_ratings:
            result.add_violation(
                "content_rating",
                f"Content rating '{content_rating}' is not in allowed ratings: {allowed_ratings}",
                "high"
            )
        
        # Check minimum age
        content_age = metadata.get("minimum_age", 0)
        if content_age < minimum_age:
            result.add_warning(
                "content_rating",
                f"Content minimum age ({content_age}) is below country minimum ({minimum_age})"
            )
    
    def _check_mandatory_features(self, metadata: Dict[str, Any], result: ValidationResult):
        """Check for mandatory features"""
        mandatory = self.policy.mandatory_features
        if not mandatory:
            return
        
        app_features = metadata.get("features", [])
        
        for required_feature in mandatory:
            if required_feature not in app_features:
                result.add_violation(
                    "mandatory_features",
                    f"Missing mandatory feature: '{required_feature}'",
                    "high"
                )
    
    def _check_advertising_compliance(self, metadata: Dict[str, Any], result: ValidationResult):
        """Check advertising compliance"""
        ad_config = self.policy.advertising
        if not ad_config:
            return
        
        ad_duration = metadata.get("ad_duration_minutes", 0)
        max_duration = ad_config.get("max_duration_minutes", float('inf'))
        
        if ad_duration > max_duration:
            result.add_violation(
                "advertising",
                f"Ad duration ({ad_duration} min) exceeds maximum allowed ({max_duration} min)",
                "high"
            )
        
        # Check forbidden time windows
        ad_schedule = metadata.get("ad_schedule", [])
        forbidden_windows = ad_config.get("forbidden_time_windows", [])
        
        for ad_time in ad_schedule:
            for window in forbidden_windows:
                if self._time_in_window(ad_time, window.get("start"), window.get("end")):
                    reason = window.get("reason", "restricted period")
                    result.add_violation(
                        "advertising",
                        f"Ad scheduled during forbidden time window ({window['start']}-{window['end']}): {reason}",
                        "critical"
                    )
    
    def _check_youth_protection(self, metadata: Dict[str, Any], result: ValidationResult):
        """Check youth protection requirements"""
        youth_config = self.policy.youth_protection
        if not youth_config or not youth_config.get("enabled"):
            return
        
        # Check shutdown system (e.g., Korea's Cinderella law)
        if "shutdown_hours" in youth_config:
            access_times = metadata.get("youth_access_times", [])
            shutdown_start = youth_config["shutdown_hours"].get("start")
            shutdown_end = youth_config["shutdown_hours"].get("end")
            
            for access_time in access_times:
                if self._time_in_window(access_time, shutdown_start, shutdown_end):
                    applies_under = youth_config.get("applies_to_age_under", 16)
                    result.add_violation(
                        "youth_protection",
                        f"Youth access (under {applies_under}) during shutdown hours ({shutdown_start}-{shutdown_end})",
                        "critical"
                    )
    
    def _check_regional_compliance(self, metadata: Dict[str, Any], result: ValidationResult):
        """Check regional compliance requirements"""
        compliance = self.policy.compliance
        if not compliance:
            return
        
        # Check local content quota
        if compliance.get("requires_local_content_quota"):
            local_percentage = metadata.get("local_content_percentage", 0)
            required_percentage = compliance.get("local_content_percentage", 0)
            
            if local_percentage < required_percentage:
                result.add_violation(
                    "regional_compliance",
                    f"Local content percentage ({local_percentage}%) below required ({required_percentage}%)",
                    "high"
                )
        
        # Check real name verification (Korea)
        if compliance.get("requires_real_name"):
            if not metadata.get("real_name_verification_enabled", False):
                result.add_violation(
                    "regional_compliance",
                    "Real name verification is required but not enabled",
                    "critical"
                )
        
        # Check GDPR compliance (Germany)
        if compliance.get("requires_gdpr_compliance"):
            if not metadata.get("gdpr_compliant", False):
                result.add_violation(
                    "regional_compliance",
                    "GDPR compliance is required",
                    "critical"
                )
        
        # Check data localization (Korea)
        if compliance.get("data_must_be_stored_locally"):
            if not metadata.get("data_stored_locally", False):
                result.add_violation(
                    "regional_compliance",
                    "Data must be stored locally within the country",
                    "critical"
                )
    
    def _time_in_window(self, time_str: str, window_start: str, window_end: str) -> bool:
        """Check if a time falls within a time window"""
        try:
            check_time = datetime.strptime(time_str, "%H:%M").time()
            start = datetime.strptime(window_start, "%H:%M").time()
            end = datetime.strptime(window_end, "%H:%M").time()
            
            if start <= end:
                return start <= check_time <= end
            else:
                # Handle overnight windows (e.g., 23:00 - 01:00)
                return check_time >= start or check_time <= end
        except (ValueError, AttributeError):
            return False
