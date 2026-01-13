"""Rule Engine for validating content against country-specific policies."""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ValidationStatus(Enum):
    """Validation status enum."""
    PASS = "PASS"
    REJECT = "REJECT"


@dataclass
class ValidationResult:
    """Result of policy validation."""
    status: ValidationStatus
    country: str
    violations: List[str]
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "status": self.status.value,
            "country": self.country,
            "violations": self.violations,
            "warnings": self.warnings
        }


class RuleEngine:
    """Python-based validator for country-specific content rules."""
    
    def __init__(self, policies_dir: Optional[Path] = None):
        """Initialize the rule engine.
        
        Args:
            policies_dir: Directory containing policy YAML files
        """
        if policies_dir is None:
            policies_dir = Path(__file__).parent.parent.parent / "policies"
        self.policies_dir = Path(policies_dir)
        self.policies_cache: Dict[str, Dict[str, Any]] = {}
    
    def load_policy(self, country: str) -> Dict[str, Any]:
        """Load policy configuration for a specific country.
        
        Args:
            country: Country code (e.g., 'korea', 'saudi_arabia')
            
        Returns:
            Policy configuration dictionary
            
        Raises:
            FileNotFoundError: If policy file doesn't exist
            yaml.YAMLError: If policy file is invalid
        """
        if country in self.policies_cache:
            return self.policies_cache[country]
        
        policy_file = self.policies_dir / f"{country.lower()}.yaml"
        
        if not policy_file.exists():
            raise FileNotFoundError(f"Policy file not found for country: {country}")
        
        with open(policy_file, 'r', encoding='utf-8') as f:
            policy = yaml.safe_load(f)
        
        self.policies_cache[country] = policy
        return policy
    
    def validate_content(
        self,
        content: Dict[str, Any],
        country: str
    ) -> ValidationResult:
        """Validate content against country-specific policies.
        
        Args:
            content: Content metadata to validate
            country: Target country for validation
            
        Returns:
            ValidationResult with status and details
        """
        policy = self.load_policy(country)
        violations = []
        warnings = []
        
        # Check forbidden content
        if "forbidden_content" in policy:
            violations.extend(
                self._check_forbidden_content(content, policy["forbidden_content"])
            )
        
        # Check content rating requirements
        if "rating_requirements" in policy:
            rating_violations = self._check_rating_requirements(
                content, policy["rating_requirements"]
            )
            violations.extend(rating_violations)
        
        # Check ad window restrictions
        if "ad_windows" in policy:
            ad_violations = self._check_ad_windows(
                content, policy["ad_windows"]
            )
            violations.extend(ad_violations)
        
        # Check language requirements
        if "language_requirements" in policy:
            lang_violations = self._check_language_requirements(
                content, policy["language_requirements"]
            )
            violations.extend(lang_violations)
        
        # Check cultural restrictions
        if "cultural_restrictions" in policy:
            cultural_warnings = self._check_cultural_restrictions(
                content, policy["cultural_restrictions"]
            )
            warnings.extend(cultural_warnings)
        
        # Determine overall status
        status = ValidationStatus.REJECT if violations else ValidationStatus.PASS
        
        return ValidationResult(
            status=status,
            country=country,
            violations=violations,
            warnings=warnings
        )
    
    def _check_forbidden_content(
        self,
        content: Dict[str, Any],
        forbidden_rules: Dict[str, Any]
    ) -> List[str]:
        """Check for forbidden content types."""
        violations = []
        
        # Check forbidden keywords
        if "keywords" in forbidden_rules:
            content_text = " ".join([
                str(content.get("title", "")),
                str(content.get("description", "")),
                " ".join(content.get("tags", []))
            ]).lower()
            
            for keyword in forbidden_rules["keywords"]:
                if keyword.lower() in content_text:
                    violations.append(
                        f"Forbidden keyword detected: '{keyword}'"
                    )
        
        # Check forbidden categories
        if "categories" in forbidden_rules:
            content_categories = set(content.get("categories", []))
            forbidden_categories = set(forbidden_rules["categories"])
            
            overlap = content_categories & forbidden_categories
            if overlap:
                violations.append(
                    f"Forbidden categories detected: {', '.join(overlap)}"
                )
        
        return violations
    
    def _check_rating_requirements(
        self,
        content: Dict[str, Any],
        rating_rules: Dict[str, Any]
    ) -> List[str]:
        """Check content rating requirements."""
        violations = []
        
        if "required" in rating_rules and rating_rules["required"]:
            if "rating" not in content or not content["rating"]:
                violations.append("Content rating is required but not provided")
        
        if "allowed_ratings" in rating_rules:
            content_rating = content.get("rating", "")
            allowed_ratings = rating_rules["allowed_ratings"]
            
            if content_rating and content_rating not in allowed_ratings:
                violations.append(
                    f"Content rating '{content_rating}' is not allowed. "
                    f"Allowed ratings: {', '.join(allowed_ratings)}"
                )
        
        return violations
    
    def _check_ad_windows(
        self,
        content: Dict[str, Any],
        ad_rules: Dict[str, Any]
    ) -> List[str]:
        """Check advertising window restrictions."""
        violations = []
        
        ad_breaks = content.get("ad_breaks", [])
        
        # Check maximum ad duration
        if "max_duration_seconds" in ad_rules:
            max_duration = ad_rules["max_duration_seconds"]
            
            for idx, ad_break in enumerate(ad_breaks):
                duration = ad_break.get("duration_seconds", 0)
                if duration and duration > max_duration:
                    violations.append(
                        f"Ad break {idx + 1} exceeds maximum duration "
                        f"({duration}s > {max_duration}s)"
                    )
        
        # Check minimum interval between ads
        if "min_interval_seconds" in ad_rules and len(ad_breaks) > 1:
            min_interval = ad_rules["min_interval_seconds"]
            
            for i in range(1, len(ad_breaks)):
                prev_time = ad_breaks[i - 1].get("timestamp_seconds", 0)
                curr_time = ad_breaks[i].get("timestamp_seconds", 0)
                if prev_time and curr_time:
                    interval = curr_time - prev_time
                    
                    if interval < min_interval:
                        violations.append(
                            f"Ad breaks {i} and {i + 1} are too close "
                            f"({interval}s < {min_interval}s)"
                        )
        
        # Check maximum ads per hour
        if "max_per_hour" in ad_rules:
            content_duration = content.get("duration_minutes")
            if content_duration and content_duration > 0:
                hours = content_duration / 60
                ads_per_hour = len(ad_breaks) / hours if hours > 0 else 0
                
                if ads_per_hour > ad_rules["max_per_hour"]:
                    violations.append(
                        f"Too many ad breaks per hour "
                        f"({ads_per_hour:.1f} > {ad_rules['max_per_hour']})"
                    )
        
        return violations
    
    def _check_language_requirements(
        self,
        content: Dict[str, Any],
        language_rules: Dict[str, Any]
    ) -> List[str]:
        """Check language requirements."""
        violations = []
        
        if "required_subtitles" in language_rules:
            required_langs = set(language_rules["required_subtitles"])
            available_subtitles = set(content.get("subtitle_languages", []))
            
            missing_langs = required_langs - available_subtitles
            if missing_langs:
                violations.append(
                    f"Missing required subtitle languages: {', '.join(missing_langs)}"
                )
        
        if "required_audio" in language_rules:
            required_audio = set(language_rules["required_audio"])
            available_audio = set(content.get("audio_languages", []))
            
            missing_audio = required_audio - available_audio
            if missing_audio:
                violations.append(
                    f"Missing required audio languages: {', '.join(missing_audio)}"
                )
        
        return violations
    
    def _check_cultural_restrictions(
        self,
        content: Dict[str, Any],
        cultural_rules: Dict[str, Any]
    ) -> List[str]:
        """Check cultural restrictions (returns warnings, not violations)."""
        warnings = []
        
        if "sensitive_topics" in cultural_rules:
            content_text = " ".join([
                str(content.get("title", "")),
                str(content.get("description", ""))
            ]).lower()
            
            for topic in cultural_rules["sensitive_topics"]:
                if topic.lower() in content_text:
                    warnings.append(
                        f"Sensitive cultural topic detected: '{topic}'. "
                        "Manual review recommended."
                    )
        
        return warnings
