#!/usr/bin/env python3
"""
System Integration Test
자동 규제 업데이트 시스템 통합 테스트

전체 시스템이 정상적으로 작동하는지 확인합니다.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """필수 모듈 임포트 테스트"""
    print("=" * 70)
    print("Testing Module Imports...")
    print("=" * 70)
    
    try:
        from src.policy_auto_updater import PolicyUpdateMonitor, PolicyAutoUpdater
        print("✅ policy_auto_updater imported")
    except Exception as e:
        print(f"❌ policy_auto_updater import failed: {e}")
        return False
    
    try:
        from src.auto_scheduler import RegulatoryUpdateScheduler
        print("✅ auto_scheduler imported")
    except Exception as e:
        print(f"❌ auto_scheduler import failed: {e}")
        return False
    
    try:
        from src.change_tracker import ChangeTracker
        print("✅ change_tracker imported")
    except Exception as e:
        print(f"❌ change_tracker import failed: {e}")
        return False
    
    try:
        from src.notification_system import NotificationManager
        print("✅ notification_system imported")
    except Exception as e:
        print(f"❌ notification_system import failed: {e}")
        return False
    
    return True


def test_dependencies():
    """의존성 패키지 테스트"""
    print("\n" + "=" * 70)
    print("Testing Dependencies...")
    print("=" * 70)
    
    packages = [
        "yaml",
        "requests",
        "feedparser",
        "bs4",
        "apscheduler",
        "dotenv"
    ]
    
    all_ok = True
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            all_ok = False
    
    return all_ok


def test_configuration():
    """설정 파일 테스트"""
    print("\n" + "=" * 70)
    print("Testing Configuration Files...")
    print("=" * 70)
    
    files = [
        "config/regulatory_sources.yaml",
        "config/policy_rules.yaml",
        "config/notifications.yaml"
    ]
    
    all_ok = True
    for file_path in files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"⚠️  {file_path} not found")
            all_ok = False
    
    # .env 파일 확인
    if Path(".env").exists():
        print("✅ .env")
    else:
        print("⚠️  .env not found (optional but recommended)")
    
    return all_ok


def test_monitor():
    """모니터링 시스템 테스트"""
    print("\n" + "=" * 70)
    print("Testing Update Monitor...")
    print("=" * 70)
    
    try:
        from src.policy_auto_updater import PolicyUpdateMonitor
        
        monitor = PolicyUpdateMonitor()
        print(f"✅ Monitor initialized with {len(monitor.sources)} sources")
        
        # 소스 출력
        print("\nConfigured sources:")
        by_country = {}
        for source in monitor.sources:
            if source.country not in by_country:
                by_country[source.country] = []
            by_country[source.country].append(source.name)
        
        for country, sources in sorted(by_country.items()):
            print(f"  {country}: {len(sources)} source(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Monitor test failed: {e}")
        return False


def test_directories():
    """필수 디렉토리 생성 테스트"""
    print("\n" + "=" * 70)
    print("Creating Necessary Directories...")
    print("=" * 70)
    
    directories = [
        "reports",
        "reports/scheduler_logs",
        "reports/source_hashes",
        "reports/change_history"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ {dir_path}")
    
    return True


def run_quick_test():
    """빠른 기능 테스트"""
    print("\n" + "=" * 70)
    print("Running Quick Functionality Test...")
    print("=" * 70)
    
    try:
        from src.policy_auto_updater import PolicyUpdateMonitor
        
        monitor = PolicyUpdateMonitor()
        print("✅ Monitor created")
        
        # 첫 번째 소스만 테스트
        if monitor.sources:
            test_source = monitor.sources[0]
            print(f"\nTesting first source: {test_source.name}")
            print(f"  Country: {test_source.country}")
            print(f"  Method: {test_source.method}")
            print(f"  URL: {test_source.url}")
            
            # 실제 체크는 시간이 걸릴 수 있으므로 스킵
            print("  (Actual check skipped for speed)")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 테스트 실행"""
    print("\n" + "=" * 70)
    print("GLOCAL POLICY GUARDRAIL - SYSTEM INTEGRATION TEST")
    print("=" * 70)
    print()
    
    results = []
    
    # 각 테스트 실행
    results.append(("Imports", test_imports()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Configuration", test_configuration()))
    results.append(("Directories", test_directories()))
    results.append(("Monitor", test_monitor()))
    results.append(("Quick Test", run_quick_test()))
    
    # 결과 요약
    print("\n" + "=" * 70)
    print("TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        if result:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_name}: FAILED")
            failed += 1
    
    print("=" * 70)
    print(f"Total: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Configure .env file with your credentials")
        print("2. Enable notifications in config/notifications.yaml")
        print("3. Run: python3 src/auto_scheduler.py --test")
        print("4. Deploy: bash deployment/docker_deploy.sh")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nTo install missing dependencies:")
        print("  pip3 install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
