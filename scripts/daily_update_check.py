#!/usr/bin/env python3
"""
Daily Policy Update Checker
일일 정책 업데이트 확인 스케줄러

Usage:
  python scripts/daily_update_check.py
  
For automated scheduling:
  # Linux/Mac crontab
  0 9 * * * /usr/bin/python3 /path/to/daily_update_check.py
  
  # Windows Task Scheduler
  Run daily at 9:00 AM
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.policy_auto_updater import PolicyUpdateMonitor, PolicyAutoUpdater
from datetime import datetime
import logging

# 로깅 설정
log_dir = Path(__file__).parent.parent / "reports"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f"update_check_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def send_notification(updates: list, report: str):
    """
    업데이트 알림 전송 (이메일, Slack 등)
    
    TODO: 실제 구현 시 SMTP 또는 Slack webhook 사용
    """
    if not updates:
        logger.info("No notifications to send - no updates detected")
        return
    
    # 간단한 파일 알림
    notification_file = log_dir / f"ALERT_updates_detected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(notification_file, 'w', encoding='utf-8') as f:
        f.write("⚠️  REGULATORY UPDATES DETECTED\n")
        f.write("=" * 70 + "\n\n")
        f.write(report)
        f.write("\n\n")
        f.write("ACTION REQUIRED:\n")
        f.write("1. Review updates in reports/policy_updates.json\n")
        f.write("2. Consult with legal team\n")
        f.write("3. Update config/policy_rules.yaml if necessary\n")
        f.write("4. Run compliance tests\n")
    
    logger.warning(f"⚠️  ALERT: {len(updates)} regulatory updates detected!")
    logger.info(f"Alert saved to: {notification_file}")
    
    # TODO: 실제 이메일 전송
    # send_email(
    #     to="compliance-team@company.com",
    #     subject=f"Regulatory Update Alert - {len(updates)} changes detected",
    #     body=report
    # )


def main():
    """메인 실행 함수"""
    logger.info("=" * 70)
    logger.info("DAILY REGULATORY UPDATE CHECK")
    logger.info("=" * 70)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 모니터 초기화
        monitor = PolicyUpdateMonitor()
        logger.info(f"Initialized monitor with {len(monitor.sources)} sources")
        
        # 업데이트 확인
        logger.info("Checking for regulatory updates...")
        updates = monitor.check_for_updates()
        
        # 리포트 생성
        report = monitor.generate_update_report(updates)
        
        # 로그 저장
        monitor.save_update_log(updates)
        
        # 콘솔 출력
        print("\n" + report + "\n")
        
        # 업데이트 발견 시 알림
        if updates:
            send_notification(updates, report)
            
            # 정책 업데이트 제안 생성
            updater = PolicyAutoUpdater()
            
            logger.info("Generating policy update suggestions...")
            suggestions = []
            
            for update in updates:
                suggestion = updater.suggest_policy_update(update)
                if suggestion:
                    suggestions.append(suggestion)
            
            if suggestions:
                logger.info(f"Generated {len(suggestions)} policy update suggestions")
                
                # 제안사항 저장
                suggestion_file = log_dir / f"policy_suggestions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                import json
                with open(suggestion_file, 'w', encoding='utf-8') as f:
                    json.dump(suggestions, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Suggestions saved to: {suggestion_file}")
        else:
            logger.info("✅ No regulatory updates detected - all clear!")
        
        logger.info("=" * 70)
        logger.info("Daily check completed successfully")
        logger.info(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error during update check: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
