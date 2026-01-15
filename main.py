"""
Glocal Policy Guardrail - Main Execution & Demo
실제 테스트 시나리오를 실행하는 메인 프로그램
"""

import sys
import os
import yaml
from datetime import datetime

# 상대 경로 import를 위한 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.compliance_scanner import ComplianceGuardrail, ComplianceResult
from src.analytics import generate_full_analytics_report, ComplianceAnalytics


def load_test_cases(test_file_path: str = "test_data/sample_deployments.yaml"):
    """테스트 케이스 로드"""
    try:
        with open(test_file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Test file not found: {test_file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"❌ Invalid YAML format: {e}")
        return None


def run_test_case(guardrail: ComplianceGuardrail, test_name: str, test_data: dict):
    """개별 테스트 케이스 실행"""
    print(f"\n{'='*70}")
    print(f"🧪 Test Case: {test_name}")
    print(f"{'='*70}")
    
    country = test_data.get('country')
    content_metadata = test_data.get('content_metadata', {})
    ad_schedule = test_data.get('ad_schedule')
    expected_result = test_data.get('expected_result', 'UNKNOWN')
    
    # 광고 스케줄이 있는 경우 시간 파싱
    current_time = None
    if ad_schedule and 'scheduled_time' in ad_schedule:
        current_time = datetime.fromisoformat(ad_schedule['scheduled_time'])
        print(f"📅 Scheduled Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 컴플라이언스 검사 실행
    result = guardrail.check_deployment(
        country=country,
        content_metadata=content_metadata,
        ad_schedule=ad_schedule,
        current_time=current_time
    )
    
    # 결과 출력
    print(f"\n📋 Content Details:")
    print(f"   Title: {content_metadata.get('title', 'N/A')}")
    print(f"   Genre: {content_metadata.get('genre', 'N/A')}")
    print(f"   Country: {country}")
    
    print(f"\n{result}")
    
    # 예상 결과와 비교
    test_passed = result.status == expected_result
    if test_passed:
        print(f"\n✅ TEST PASSED: Expected '{expected_result}', Got '{result.status}'")
    else:
        print(f"\n❌ TEST FAILED: Expected '{expected_result}', Got '{result.status}'")
    
    return test_passed, result


def run_all_tests():
    """모든 테스트 케이스 실행"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║  🌍 GLOCAL POLICY GUARDRAIL - COMPLIANCE SCANNER                     ║
║  Policy-as-Code Framework for Global OTT Platforms                   ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    # 가드레일 초기화
    try:
        guardrail = ComplianceGuardrail()
        print(f"✅ Policy Database Loaded Successfully")
        print(f"   Supported Countries: {', '.join(guardrail.supported_countries)}")
    except Exception as e:
        print(f"❌ Failed to initialize guardrail: {e}")
        return
    
    # 테스트 케이스 로드
    test_cases = load_test_cases()
    if not test_cases:
        print("❌ No test cases loaded. Exiting.")
        return
    
    # 모든 테스트 실행
    test_results = {}
    passed_count = 0
    failed_count = 0
    
    for test_name, test_data in test_cases.items():
        if not isinstance(test_data, dict):
            continue
        
        test_passed, result = run_test_case(guardrail, test_name, test_data)
        test_results[test_name] = {
            'passed': test_passed,
            'result': result
        }
        
        if test_passed:
            passed_count += 1
        else:
            failed_count += 1
    
    # 최종 요약
    print(f"\n\n{'='*70}")
    print("📊 FINAL TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Total Tests: {passed_count + failed_count}")
    print(f"✅ Passed: {passed_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"Success Rate: {(passed_count / (passed_count + failed_count) * 100):.1f}%")
    print(f"{'='*70}\n")
    
    # 위반 통계
    print("\n📈 VIOLATION STATISTICS BY COUNTRY:")
    print(f"{'='*70}")
    
    country_violations = {}
    for test_name, data in test_results.items():
        result = data['result']
        country = result.country
        
        if country not in country_violations:
            country_violations[country] = {
                'total_checks': 0,
                'violations': 0,
                'critical': 0,
                'warning': 0
            }
        
        country_violations[country]['total_checks'] += 1
        if result.status != 'PASS':
            country_violations[country]['violations'] += len(result.violations)
            if result.status == 'CRITICAL':
                country_violations[country]['critical'] += 1
            else:
                country_violations[country]['warning'] += 1
    
    for country, stats in sorted(country_violations.items()):
        print(f"\n{country}:")
        print(f"  Total Checks: {stats['total_checks']}")
        print(f"  Violations Found: {stats['violations']}")
        print(f"  🔴 Critical: {stats['critical']}")
        print(f"  ⚠️  Warnings: {stats['warning']}")
    
    print(f"\n{'='*70}")
    print("✨ Testing Complete!")
    
    # 고급 분석 리포트 생성
    print("\n\n")
    print("🎨 Generating Advanced Analytics Report...")
    print("="*70)
    
    # 결과를 딕셔너리로 변환
    results_dict = {name: data['result'] for name, data in test_results.items()}
    
    # 전체 분석 리포트 출력
    analytics_report = generate_full_analytics_report(results_dict)
    print(analytics_report)
    
    # JSON 내보내기
    analytics = ComplianceAnalytics()
    export_path = "reports/compliance_report.json"
    
    # reports 디렉토리 생성
    import os
    os.makedirs("reports", exist_ok=True)
    
    print("\n" + analytics.export_to_json(results_dict, export_path))
    print("="*70)


def run_interactive_demo():
    """대화형 데모 모드"""
    print("\n🎮 Interactive Demo Mode")
    print("="*70)
    
    guardrail = ComplianceGuardrail()
    
    while True:
        print("\nSelect a country to test:")
        for idx, country in enumerate(guardrail.supported_countries, 1):
            print(f"  {idx}. {country}")
        print("  0. Exit")
        
        try:
            choice = input("\nEnter number: ").strip()
            if choice == '0':
                print("👋 Goodbye!")
                break
            
            country = guardrail.supported_countries[int(choice) - 1]
            
            # 간단한 테스트 콘텐츠 입력
            title = input("\nEnter content title: ").strip()
            description = input("Enter content description: ").strip()
            
            content_metadata = {
                'title': title,
                'description': description,
                'genre': 'General',
                'tags': [],
                'features': []
            }
            
            result = guardrail.check_deployment(country, content_metadata)
            print(f"\n{result}")
            
        except (ValueError, IndexError):
            print("❌ Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        run_interactive_demo()
    else:
        run_all_tests()
