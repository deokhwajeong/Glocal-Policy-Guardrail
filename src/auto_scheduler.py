#!/usr/bin/env python3
"""
Automatic Regulatory Update Scheduler
자동 규제 업데이트 스케줄러

24/7 자동 실행되며 설정된 주기에 따라 각 국가별 규제를 체크합니다.
"""

import sys
import os
from pathlib import Path
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import yaml
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.policy_auto_updater import PolicyUpdateMonitor, PolicyAutoUpdater
from src.notification_system import NotificationManager

# 로깅 설정
log_dir = Path(__file__).parent.parent / "reports" / "scheduler_logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"scheduler_{datetime.now().strftime('%Y%m')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RegulatoryUpdateScheduler:
    """Regulatory 업데이트 Auto scheduler"""
    
    def __init__(self, config_path: str = "config/regulatory_sources.yaml"):
        self.config_path = config_path
        self.scheduler = BlockingScheduler()
        self.monitor = PolicyUpdateMonitor(config_path)
        self.updater = PolicyAutoUpdater()
        self.notifier = NotificationManager()
        
        logger.info("Regulatory Update Scheduler initialized")
    
    def check_daily_sources(self):
        """일일 체크 소스 확인"""
        logger.info("=" * 70)
        logger.info("Running DAILY regulatory check...")
        logger.info("=" * 70)
        
        try:
            # 일일 체크 소스만 필터링
            daily_sources = [s for s in self.monitor.sources if s.check_frequency == "daily"]
            
            if not daily_sources:
                logger.info("No daily sources configured")
                return
            
            logger.info(f"Checking {len(daily_sources)} daily sources...")
            
            # 임시로 소스 교체
            original_sources = self.monitor.sources
            self.monitor.sources = daily_sources
            
            updates = self.monitor.check_for_updates()
            
            # 원래 소스 복원
            self.monitor.sources = original_sources
            
            if updates:
                self._process_updates(updates, "daily")
            else:
                logger.info("✅ No daily updates detected")
                
        except Exception as e:
            logger.error(f"Error in daily check: {e}", exc_info=True)
    
    def check_weekly_sources(self):
        """주간 체크 소스 확인"""
        logger.info("=" * 70)
        logger.info("Running WEEKLY regulatory check...")
        logger.info("=" * 70)
        
        try:
            weekly_sources = [s for s in self.monitor.sources if s.check_frequency == "weekly"]
            
            if not weekly_sources:
                logger.info("No weekly sources configured")
                return
            
            logger.info(f"Checking {len(weekly_sources)} weekly sources...")
            
            original_sources = self.monitor.sources
            self.monitor.sources = weekly_sources
            
            updates = self.monitor.check_for_updates()
            
            self.monitor.sources = original_sources
            
            if updates:
                self._process_updates(updates, "weekly")
            else:
                logger.info("✅ No weekly updates detected")
                
        except Exception as e:
            logger.error(f"Error in weekly check: {e}", exc_info=True)
    
    def check_monthly_sources(self):
        """월간 체크 소스 확인"""
        logger.info("=" * 70)
        logger.info("Running MONTHLY regulatory check...")
        logger.info("=" * 70)
        
        try:
            monthly_sources = [s for s in self.monitor.sources if s.check_frequency == "monthly"]
            
            if not monthly_sources:
                logger.info("No monthly sources configured")
                return
            
            logger.info(f"Checking {len(monthly_sources)} monthly sources...")
            
            original_sources = self.monitor.sources
            self.monitor.sources = monthly_sources
            
            updates = self.monitor.check_for_updates()
            
            self.monitor.sources = original_sources
            
            if updates:
                self._process_updates(updates, "monthly")
            else:
                logger.info("✅ No monthly updates detected")
                
        except Exception as e:
            logger.error(f"Error in monthly check: {e}", exc_info=True)
    
    def _process_updates(self, updates: list, frequency: str):
        """업데이트 처리"""
        logger.info(f"🔔 {len(updates)} update(s) detected from {frequency} check!")
        
        # 리포트 생성
        report = self.monitor.generate_update_report(updates)
        logger.info("\n" + report)
        
        # 로그 저장
        self.monitor.save_update_log(updates)
        
        # 정책 제안 생성
        logger.info("\n🤖 Generating policy update suggestions...")
        suggestions = []
        
        for update in updates:
            suggestion = self.updater.suggest_policy_update(update)
            if suggestion:
                suggestions.append(suggestion)
                logger.info(f"  - Suggestion generated for {update['country']}")
        
        if suggestions:
            # 제안 저장
            suggestions_file = Path("reports/policy_suggestions.json")
            suggestions_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                with open(suggestions_file, 'r') as f:
                    existing = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                existing = []
            
            existing.extend(suggestions)
            
            with open(suggestions_file, 'w') as f:
                json.dump(existing[-100:], f, indent=2, ensure_ascii=False)
            
            logger.info(f"📋 {len(suggestions)} suggestions saved to {suggestions_file}")
        
        # TODO: 알림 전송 (이메일, Slack 등)
        self._send_notifications(updates, frequency)
    
    def _send_notifications(self, updates: list, frequency: str):
        """알림 전송 (이메일, Slack, Discord)"""
        try:
            logger.info(f"📧 Sending notifications for {len(updates)} updates...")
            results = self.notifier.notify_updates(updates)
            
            for channel, success in results.items():
                if success:
                    logger.info(f"  ✅ {channel.capitalize()} notification sent")
                else:
                    logger.warning(f"  ⚠️  {channel.capitalize()} notification failed")
        except Exception as e:
            logger.error(f"Error sending notifications: {e}", exc_info=True)
    
    def setup_jobs(self):
        """스케줄 작업 설정"""
        logger.info("Setting up scheduled jobs...")
        
        # 일일 체크: 매일 오전 9시 (KST)
        self.scheduler.add_job(
            self.check_daily_sources,
            CronTrigger(hour=9, minute=0),
            id='daily_check',
            name='Daily Regulatory Check',
            replace_existing=True
        )
        logger.info("✓ Daily check scheduled: 09:00 KST")
        
        # 주간 체크: 매주 월요일 오전 10시
        self.scheduler.add_job(
            self.check_weekly_sources,
            CronTrigger(day_of_week='mon', hour=10, minute=0),
            id='weekly_check',
            name='Weekly Regulatory Check',
            replace_existing=True
        )
        logger.info("✓ Weekly check scheduled: Monday 10:00 KST")
        
        # 월간 체크: 매월 1일 오전 11시
        self.scheduler.add_job(
            self.check_monthly_sources,
            CronTrigger(day=1, hour=11, minute=0),
            id='monthly_check',
            name='Monthly Regulatory Check',
            replace_existing=True
        )
        logger.info("✓ Monthly check scheduled: 1st of month 11:00 KST")
        
        # 헬스 체크: 매 시간
        self.scheduler.add_job(
            self._health_check,
            IntervalTrigger(hours=1),
            id='health_check',
            name='Scheduler Health Check',
            replace_existing=True
        )
        logger.info("✓ Health check scheduled: Every hour")
    
    def _health_check(self):
        """스케줄러 상태 체크"""
        logger.info(f"[Health Check] Scheduler running - {datetime.now().isoformat()}")
        logger.info(f"  Total sources: {len(self.monitor.sources)}")
        logger.info(f"  Active jobs: {len(self.scheduler.get_jobs())}")
    
    def start(self):
        """스케줄러 시작"""
        logger.info("=" * 70)
        logger.info("REGULATORY UPDATE SCHEDULER STARTING")
        logger.info("=" * 70)
        logger.info(f"Total regulatory sources: {len(self.monitor.sources)}")
        logger.info("")
        
        self.setup_jobs()
        
        logger.info("")
        logger.info("Scheduler started successfully!")
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 70)
        
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("\nShutting down scheduler...")
            self.scheduler.shutdown()
            logger.info("Scheduler stopped.")


def main():
    """메인 함수"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Regulatory Update Scheduler')
    parser.add_argument('--test', action='store_true', help='Run test check immediately')
    parser.add_argument('--daily', action='store_true', help='Run daily check now')
    parser.add_argument('--weekly', action='store_true', help='Run weekly check now')
    parser.add_argument('--monthly', action='store_true', help='Run monthly check now')
    parser.add_argument('--daemon', action='store_true', help='Run as background daemon (default)')
    
    args = parser.parse_args()
    
    scheduler = RegulatoryUpdateScheduler()
    
    if args.test or args.daily:
        scheduler.check_daily_sources()
    elif args.weekly:
        scheduler.check_weekly_sources()
    elif args.monthly:
        scheduler.check_monthly_sources()
    else:
        # 기본: 데몬 모드로 실행
        scheduler.start()


if __name__ == "__main__":
    main()
