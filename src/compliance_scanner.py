"""
Glocal Policy Guardrail - Compliance Scanner Engine
국가별 법규 및 문화적 금기 사항 자동 검증 시스템

Author: [Your Name]
Purpose: EB1 Research - Policy-as-Code Framework for Global OTT Platforms
"""

import yaml
import re
from datetime import datetime, time
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ViolationSeverity(Enum):
    """위반 심각도 레벨"""
    CRITICAL = "CRITICAL"  # 배포 차단 필수
    HIGH = "HIGH"          # 즉시 수정 필요
    MEDIUM = "MEDIUM"      # 경고 후 배포 가능
    LOW = "LOW"            # 권고 사항


class ComplianceResult:
    """컴플라이언스 검사 결과"""
    def __init__(self, status: str, country: str, violations: List[Dict] = None):
        self.status = status  # PASS, WARNING, CRITICAL
        self.country = country
        self.violations = violations or []
        self.timestamp = datetime.now().isoformat()
    
    def add_violation(self, violation_type: str, message: str, severity: str, 
                     detected_content: str = None):
        """위반 사항 추가"""
        self.violations.append({
            "type": violation_type,
            "message": message,
            "severity": severity,
            "detected_content": detected_content,
            "timestamp": datetime.now().isoformat()
        })
        
        # 심각도에 따라 전체 상태 업데이트
        if severity in ["CRITICAL", "HIGH"] and self.status != "CRITICAL":
            self.status = "CRITICAL" if severity == "CRITICAL" else "WARNING"
    
    def to_dict(self) -> Dict:
        """결과를 딕셔너리로 변환"""
        return {
            "status": self.status,
            "country": self.country,
            "timestamp": self.timestamp,
            "violation_count": len(self.violations),
            "violations": self.violations
        }
    
    def __str__(self) -> str:
        """결과 출력"""
        if self.status == "PASS":
            return f"✅ PASS: Compliance check successful for {self.country}"
        
        output = [f"{'🔴' if self.status == 'CRITICAL' else '⚠️'} {self.status}: Found {len(self.violations)} violation(s) in {self.country}"]
        for idx, v in enumerate(self.violations, 1):
            output.append(f"  {idx}. [{v['severity']}] {v['type']}: {v['message']}")
            if v.get('detected_content'):
                output.append(f"     └─ Detected: '{v['detected_content']}'")
        
        return "\n".join(output)


class ComplianceGuardrail:
    """정책 기반 컴플라이언스 가드레일 시스템"""
    
    def __init__(self, policy_db_path: str = "config/policy_rules.yaml"):
        """
        Args:
            policy_db_path: 정책 YAML 파일 경로
        """
        self.policy_db = self._load_policy_db(policy_db_path)
        self.supported_countries = list(self.policy_db.keys())
    
    def _load_policy_db(self, path: str) -> Dict:
        """정책 데이터베이스 로드"""
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
        배포 전 컴플라이언스 검사 수행
        
        Args:
            country: 대상 국가 (예: "South_Korea", "Saudi_Arabia")
            content_metadata: 콘텐츠 메타데이터
            ad_schedule: 광고 스케줄 정보 (선택)
            current_time: 현재 시간 (테스트용, 기본값: 현재)
        
        Returns:
            ComplianceResult: 검사 결과
        """
        # 국가 정책 확인
        if country not in self.policy_db:
            return ComplianceResult("WARNING", country, [{
                "type": "UNKNOWN_COUNTRY",
                "message": f"No policy found for {country}. Supported: {', '.join(self.supported_countries)}",
                "severity": "MEDIUM"
            }])
        
        policy = self.policy_db[country]
        result = ComplianceResult("PASS", country)
        
        # 1. 금지 키워드 검사
        self._check_forbidden_keywords(content_metadata, policy, result)
        
        # 2. 광고 제한사항 검사
        if ad_schedule:
            self._check_ad_restrictions(ad_schedule, policy, result, current_time)
        
        # 3. 필수 기능 검사
        self._check_mandatory_features(content_metadata, policy, result)
        
        # 4. 연령 등급 검사
        self._check_age_rating(content_metadata, policy, result)
        
        return result
    
    def _check_forbidden_keywords(self, content_metadata: Dict, policy: Dict, 
                                  result: ComplianceResult):
        """금지 키워드 검사"""
        forbidden_keywords = policy.get('forbidden_keywords', [])
        if not forbidden_keywords:
            return
        
        # 검사할 텍스트 필드들
        searchable_fields = ['title', 'description', 'tags', 'genre']
        
        for field in searchable_fields:
            if field not in content_metadata:
                continue
            
            text = str(content_metadata[field]).lower()
            
            for keyword in forbidden_keywords:
                # 정규식을 사용하여 단어 경계를 고려한 검색
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
        """광고 제한사항 검사"""
        ad_restrictions = policy.get('ad_restrictions', {})
        if not ad_restrictions:
            return
        
        current_time = current_time or datetime.now()
        ad_type = ad_schedule.get('ad_type', 'unknown')
        
        # 각 광고 타입별 제한사항 확인
        for restriction_key, restriction_value in ad_restrictions.items():
            if restriction_key not in ad_schedule.get('ad_type', ''):
                continue
            
            # 완전 금지
            if restriction_value == "completely_forbidden":
                result.add_violation(
                    violation_type="AD_COMPLETELY_FORBIDDEN",
                    message=f"{restriction_key} is completely forbidden in {result.country}",
                    severity="CRITICAL",
                    detected_content=ad_type
                )
            
            # 시간대 기반 제한
            elif isinstance(restriction_value, dict):
                if restriction_value.get('restriction_type') == 'time_based':
                    self._check_time_restriction(
                        restriction_value, current_time, result, restriction_key
                    )
    
    def _check_time_restriction(self, restriction: Dict, current_time: datetime, 
                               result: ComplianceResult, ad_type: str):
        """시간대 기반 광고 제한 검사"""
        allowed_window = restriction.get('allowed_time_window')
        forbidden_window = restriction.get('forbidden_time_window')
        
        current_hour_minute = current_time.time()
        
        if allowed_window:
            # 허용된 시간대만 명시 (예: "01:00-05:00")
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
            # 금지된 시간대 명시 (예: "07:00-22:00")
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
        """필수 기능 요구사항 검사"""
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
        """연령 등급 시스템 검사"""
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
        """
        여러 배포 대상을 일괄 검사
        
        Args:
            deployments: 배포 정보 리스트 (각각 country와 content_metadata 포함)
        
        Returns:
            국가별 검사 결과 딕셔너리
        """
        results = {}
        for idx, deployment in enumerate(deployments):
            country = deployment.get('country')
            content = deployment.get('content_metadata', {})
            ad_schedule = deployment.get('ad_schedule')
            
            result = self.check_deployment(country, content, ad_schedule)
            results[f"{country}_{idx}"] = result
        
        return results
    
    def generate_compliance_report(self, results: Dict[str, ComplianceResult]) -> str:
        """컴플라이언스 리포트 생성"""
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
            f"⚠️  Warnings: {warnings}",
            f"🔴 Critical: {critical}",
            "=" * 70,
            ""
        ]
        
        for deployment_id, result in results.items():
            report.append(str(result))
            report.append("-" * 70)
        
        return "\n".join(report)


def main():
    """메인 실행 함수 (데모)"""
    print("🌍 Glocal Policy Guardrail - Compliance Scanner")
    print("=" * 70)
    
    # 가드레일 초기화
    try:
        guardrail = ComplianceGuardrail()
        print(f"✅ Loaded policies for {len(guardrail.supported_countries)} countries")
        print(f"   Supported: {', '.join(guardrail.supported_countries)}\n")
    except Exception as e:
        print(f"❌ Error loading policy database: {e}")
        return
    
    # 테스트 케이스 실행은 test_data/sample_deployments.yaml 참조


if __name__ == "__main__":
    main()
