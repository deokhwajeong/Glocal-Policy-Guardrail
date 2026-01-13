#!/usr/bin/env python3
"""
Regulatory Update Scheduler
규제 업데이트 자동 스케줄러

Usage:
  python update_scheduler.py --check-now
  python update_scheduler.py --schedule
  python update_scheduler.py --report
"""

import argparse
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.policy_auto_updater import PolicyUpdateMonitor, PolicyAutoUpdater


def check_updates_now():
    """즉시 업데이트 확인"""
    print("🔍 Checking for regulatory updates...")
    print("=" * 70)
    
    monitor = PolicyUpdateMonitor()
    updates = monitor.check_for_updates()
    
    if not updates:
        print("✅ No updates detected. All policies are current.")
        return
    
    # 리포트 생성
    report = monitor.generate_update_report(updates)
    print(report)
    
    # 로그 저장
    monitor.save_update_log(updates)
    
    # 정책 제안 생성
    print("\n🤖 Generating policy update suggestions...")
    updater = PolicyAutoUpdater()
    
    suggestions = []
    for update in updates:
        suggestion = updater.suggest_policy_update(update)
        if suggestion:
            suggestions.append(suggestion)
    
    if suggestions:
        print(f"\n📋 Generated {len(suggestions)} policy update suggestions")
        print("Review required in: reports/policy_updates.json")
    
    return updates


def generate_report():
    """업데이트 리포트 생성"""
    import json
    
    log_path = "reports/policy_updates.json"
    
    if not os.path.exists(log_path):
        print("No update logs found.")
        return
    
    with open(log_path, 'r', encoding='utf-8') as f:
        logs = json.load(f)
    
    if not logs:
        print("No updates recorded.")
        return
    
    print("=" * 70)
    print("REGULATORY UPDATE HISTORY")
    print("=" * 70)
    print()
    
    # 최근 10개 로그
    recent_logs = logs[-10:]
    
    for log in recent_logs:
        timestamp = log.get('timestamp', 'Unknown')
        count = log.get('updates_count', 0)
        
        print(f"📅 {timestamp}")
        print(f"   Updates: {count}")
        
        if count > 0:
            for update in log.get('updates', []):
                print(f"   - {update['source']} ({update['country']})")
        
        print()


def setup_schedule():
    """스케줄 설정 (cron job 또는 systemd timer)"""
    print("📅 Setting up automatic update schedule...")
    print()
    
    # Cron job 예제 생성
    cron_command = "0 9 * * 1 cd /path/to/Glocal-Policy-Guardrail && python update_scheduler.py --check-now"
    
    print("To set up automatic checks, add this to your crontab:")
    print(f"  {cron_command}")
    print()
    print("Or use:")
    print("  crontab -e")
    print()
    
    # GitHub Actions 예제
    github_actions = """
# .github/workflows/regulatory_check.yml
name: Regulatory Update Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
  workflow_dispatch:  # Allow manual trigger

jobs:
  check-updates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Check for regulatory updates
        run: python update_scheduler.py --check-now
      
      - name: Upload update report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: update-report
          path: reports/policy_updates.json
      
      - name: Create Issue if updates found
        if: steps.check.outputs.updates_found == 'true'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '🚨 Regulatory Update Detected',
              body: 'Automated check found regulatory updates. Review required.',
              labels: ['regulatory-update', 'needs-review']
            })
"""
    
    print("GitHub Actions workflow:")
    print(github_actions)


def main():
    parser = argparse.ArgumentParser(description="Regulatory Update Scheduler")
    parser.add_argument('--check-now', action='store_true', 
                       help='Check for updates immediately')
    parser.add_argument('--report', action='store_true',
                       help='Generate update history report')
    parser.add_argument('--schedule', action='store_true',
                       help='Show how to set up automatic scheduling')
    
    args = parser.parse_args()
    
    if args.check_now:
        check_updates_now()
    elif args.report:
        generate_report()
    elif args.schedule:
        setup_schedule()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
