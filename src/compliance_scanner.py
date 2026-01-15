"""English docstring"""

import yaml
import re
from datetime import datetime, time
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ViolationSeverity(Enum):
 """English docstring"""
 CRITICAL = "CRITICAL" # English comment
 HIGH = "HIGH" # English comment
 MEDIUM = "MEDIUM" # English comment
 LOW = "LOW" # English comment


class ComplianceResult:
 """English docstring"""
 def __init__(self, status: str, country: str, violations: List[Dict] = None):
 self.status = status # PASS, WARNING, CRITICAL
 self.country = country
 self.violations = violations or []
 self.timestamp = datetime.now().isoformat()
 
 def add_violation(self, violation_type: str, message: str, severity: str, 
 detected_content: str = None):
 """English docstring"""
 self.violations.append({
 "type": violation_type,
 "message": message,
 "severity": severity,
 "detected_content": detected_content,
 "timestamp": datetime.now().isoformat()
 })
 
 # English comment
 if severity in ["CRITICAL", "HIGH"] and self.status != "CRITICAL":
 self.status = "CRITICAL" if severity == "CRITICAL" else "WARNING"
 
 def to_dict(self) -> Dict:
 """English docstring"""
 return {
 "status": self.status,
 "country": self.country,
 "timestamp": self.timestamp,
 "violation_count": len(self.violations),
 "violations": self.violations
 }
 
 def __str__(self) -> str:
 """English docstring"""
 if self.status == "PASS":
 return f"✅ PASS: Compliance check successful for {self.country}"
 
 output = [f"{'🔴' if self.status == 'CRITICAL' else '⚠️'} {self.status}: Found {len(self.violations)} violation(s) in {self.country}"]
 for idx, v in enumerate(self.violations, 1):
 output.append(f" {idx}. [{v['severity']}] {v['type']}: {v['message']}")
 if v.get('detected_content'):
 output.append(f" └─ Detected: '{v['detected_content']}'")
 
 return "\n".join(output)


class ComplianceGuardrail:
 """English docstring"""
 
 def __init__(self, policy_db_path: str = "config/policy_rules.yaml"):
 """English docstring"""
 self.policy_db = self._load_policy_db(policy_db_path)
 self.supported_countries = list(self.policy_db.keys())
 
 def _load_policy_db(self, path: str) -> Dict:
 """English docstring"""
 try:
 with open(path, 'r', encoding='utf-8') as f:
 return yaml.safe_load(f)
 except FileNotFoundError:
 raise FileNotFoundError(f"Policy database not found at {path}")
 except yaml.YAMLError as e:
 raise ValueError(f"Invalid YAML format: {e}")
 
 def check_deployment(self, 
 country: str, 
 content_metadata: Dict,
 ad_schedule: Optional[Dict] = None,
 current_time: Optional[datetime] = None) -> ComplianceResult:
 """
 Check 
 
 Args:
 country: (English:
 content_metadata: 
 ad_schedule: ()
 current_time: (Test, English:
 
 Returns:
 ComplianceResult: Check Result
 """
 # English comment
 if country not in self.policy_db:
 return ComplianceResult("WARNING", country, [{
 "type": "UNKNOWN_COUNTRY",
 "message": f"No policy found for {country}. Supported: {', '.join(self.supported_countries)}",
 "severity": "MEDIUM"
 }])
 
 policy = self.policy_db[country]
 result = ComplianceResult("PASS", country)
 
 # 1. Check
 self._check_forbidden_keywords(content_metadata, policy, result)
 
 # 2. Check
 if ad_schedule:
 self._check_ad_restrictions(ad_schedule, policy, result, current_time)
 
 # 3. Check
 self._check_mandatory_features(content_metadata, policy, result)
 
 # 4. Check
 self._check_age_rating(content_metadata, policy, result)
 
 return result
 
 def _check_forbidden_keywords(self, content_metadata: Dict, policy: Dict, 
 result: ComplianceResult):
 """English docstring"""
 forbidden_keywords = policy.get('forbidden_keywords', [])
 if not forbidden_keywords:
 return
 
 # Check 
 searchable_fields = ['title', 'description', 'tags', 'genre']
 
 for field in searchable_fields:
 if field not in content_metadata:
 continue
 
 text = str(content_metadata[field]).lower()
 
 for keyword in forbidden_keywords:
 # English comment
 pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
 if re.search(pattern, text):
 severity = policy.get('violation_severity', 'HIGH')
 result.add_violation(
 violation_type="FORBIDDEN_KEYWORD",
 message=f"Forbidden keyword '{keyword}' detected in {field}",
 severity=severity,
 detected_content=keyword
 )
 
 def _check_ad_restrictions(self, ad_schedule: Dict, policy: Dict, 
 result: ComplianceResult, current_time: Optional[datetime]):
 """English docstring"""
 ad_restrictions = policy.get('ad_restrictions', {})
 if not ad_restrictions:
 return
 
 current_time = current_time or datetime.now()
 ad_type = ad_schedule.get('ad_type', 'unknown')
 
 # English comment
 for restriction_key, restriction_value in ad_restrictions.items():
 if restriction_key not in ad_schedule.get('ad_type', ''):
 continue
 
 # English comment
 if restriction_value == "completely_forbidden":
 result.add_violation(
 violation_type="AD_COMPLETELY_FORBIDDEN",
 message=f"{restriction_key} is completely forbidden in {result.country}",
 severity="CRITICAL",
 detected_content=ad_type
 )
 
 # English comment
 elif isinstance(restriction_value, dict):
 if restriction_value.get('restriction_type') == 'time_based':
 self._check_time_restriction(
 restriction_value, current_time, result, restriction_key
 )
 
 def _check_time_restriction(self, restriction: Dict, current_time: datetime, 
 result: ComplianceResult, ad_type: str):
 """English docstring"""
 allowed_window = restriction.get('allowed_time_window')
 forbidden_window = restriction.get('forbidden_time_window')
 
 current_hour_minute = current_time.time()
 
 if allowed_window:
 # English comment
 start_str, end_str = allowed_window.split('-')
 start_time = datetime.strptime(start_str, "%H:%M").time()
 end_time = datetime.strptime(end_str, "%H:%M").time()
 
 if not (start_time <= current_hour_minute <= end_time):
 result.add_violation(
 violation_type="AD_TIME_RESTRICTION",
 message=f"{ad_type} only allowed during {allowed_window}. Current: {current_time.strftime('%H:%M')}",
 severity="HIGH",
 detected_content=f"Scheduled at {current_time.strftime('%H:%M')}"
 )
 
 if forbidden_window:
 # English comment
 start_str, end_str = forbidden_window.split('-')
 start_time = datetime.strptime(start_str, "%H:%M").time()
 end_time = datetime.strptime(end_str, "%H:%M").time()
 
 if start_time <= current_hour_minute <= end_time:
 result.add_violation(
 violation_type="AD_TIME_RESTRICTION",
 message=f"{ad_type} forbidden during {forbidden_window}. Current: {current_time.strftime('%H:%M')}",
 severity="HIGH",
 detected_content=f"Scheduled at {current_time.strftime('%H:%M')}"
 )
 
 def _check_mandatory_features(self, content_metadata: Dict, policy: Dict, 
 result: ComplianceResult):
 """English docstring"""
 mandatory_features = policy.get('mandatory_features', [])
 if not mandatory_features:
 return
 
 available_features = content_metadata.get('features', [])
 
 for feature in mandatory_features:
 if feature not in available_features:
 result.add_violation(
 violation_type="MISSING_MANDATORY_FEATURE",
 message=f"Required feature '{feature}' is missing",
 severity="HIGH",
 detected_content=f"Available: {', '.join(available_features)}"
 )
 
 def _check_age_rating(self, content_metadata: Dict, policy: Dict, 
 result: ComplianceResult):
 """English docstring"""
 expected_system = policy.get('age_rating_system')
 if not expected_system:
 return
 
 content_rating_system = content_metadata.get('age_rating_system')
 
 if content_rating_system and content_rating_system != expected_system:
 result.add_violation(
 violation_type="INCORRECT_AGE_RATING_SYSTEM",
 message=f"Expected age rating system: {expected_system}, but got: {content_rating_system}",
 severity="MEDIUM",
 detected_content=content_rating_system
 )
 
 if not content_rating_system:
 result.add_violation(
 violation_type="MISSING_AGE_RATING",
 message=f"Age rating is required (system: {expected_system})",
 severity="MEDIUM"
 )
 
 def batch_check(self, deployments: List[Dict]) -> Dict[str, ComplianceResult]:
 """English docstring"""
 results = {}
 for idx, deployment in enumerate(deployments):
 country = deployment.get('country')
 content = deployment.get('content_metadata', {})
 ad_schedule = deployment.get('ad_schedule')
 
 result = self.check_deployment(country, content, ad_schedule)
 results[f"{country}_{idx}"] = result
 
 return results
 
 def generate_compliance_report(self, results: Dict[str, ComplianceResult]) -> str:
 """English docstring"""
 total = len(results)
 passed = sum(1 for r in results.values() if r.status == "PASS")
 warnings = sum(1 for r in results.values() if r.status == "WARNING")
 critical = sum(1 for r in results.values() if r.status == "CRITICAL")
 
 report = [
 "=" * 70,
 "GLOCAL POLICY GUARDRAIL - COMPLIANCE REPORT",
 "=" * 70,
 f"Total Deployments Checked: {total}",
 f"✅ Passed: {passed}",
 f"⚠️ Warnings: {warnings}",
 f"🔴 Critical: {critical}",
 "=" * 70,
 ""
 ]
 
 for deployment_id, result in results.items():
 report.append(str(result))
 report.append("-" * 70)
 
 return "\n".join(report)


def main():
 """English docstring"""
 print("🌍 Glocal Policy Guardrail - Compliance Scanner")
 print("=" * 70)
 
 # English comment
 try:
 guardrail = ComplianceGuardrail()
 print(f"✅ Loaded policies for {len(guardrail.supported_countries)} countries")
 print(f" Supported: {', '.join(guardrail.supported_countries)}\n")
 except Exception as e:
 print(f"❌ Error loading policy database: {e}")
 return
 
 # Test Execute test_data/sample_deployments.yaml 


if __name__ == "__main__":
 main()
