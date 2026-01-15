#!/usr/bin/env python3
"""
Regulatory Change Tracking System
규제 변경사항 추적 및 버전 관리 시스템

규제 업데이트의 변경사항을 추적하고 히스토리를 관리합니다.
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
import logging
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PolicyChange:
    """Policy change record"""
    timestamp: str
    country: str
    change_type: str  # 'update', 'new', 'deprecated'
    field: str
    old_value: Optional[str]
    new_value: str
    source: str
    source_url: str
    confidence: str  # 'high', 'medium', 'low'
    approved: bool = False
    applied: bool = False
    reviewer: Optional[str] = None


class ChangeTracker:
    """Change tracking system"""
    
    def __init__(self, history_path: str = "reports/change_history"):
        self.history_path = Path(history_path)
        self.history_path.mkdir(parents=True, exist_ok=True)
        
        self.changes_file = self.history_path / "changes.json"
        self.versions_file = self.history_path / "versions.json"
        
        self.changes = self._load_changes()
        self.versions = self._load_versions()
    
    def _load_changes(self) -> List[Dict]:
        """변경 기록 로드"""
        if self.changes_file.exists():
            with open(self.changes_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle both old format (list) and new format (dict with 'changes' key)
                if isinstance(data, dict) and 'changes' in data:
                    return data['changes']
                elif isinstance(data, list):
                    return data
        return []
    
    def _load_versions(self) -> List[Dict]:
        """버전 히스토리 로드"""
        if self.versions_file.exists():
            with open(self.versions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle both old format (list) and new format (dict with 'versions' key)
                if isinstance(data, dict) and 'versions' in data:
                    return data['versions']
                elif isinstance(data, list):
                    return data
        return []
    
    def record_change(self, change: PolicyChange):
        """변경사항 기록"""
        self.changes.append(asdict(change))
        self._save_changes()
        
        logger.info(f"Change recorded: {change.country} - {change.field}")
    
    def _save_changes(self):
        """변경 기록 저장"""
        with open(self.changes_file, 'w', encoding='utf-8') as f:
            json.dump(self.changes, f, indent=2, ensure_ascii=False)
    
    def create_version_snapshot(self, policy_path: str = "config/policy_rules.yaml"):
        """현재 정책의 버전 스냅샷 생성"""
        try:
            with open(policy_path, 'r', encoding='utf-8') as f:
                policy_data = yaml.safe_load(f)
            
            # 정책 해시 생성
            policy_str = json.dumps(policy_data, sort_keys=True)
            policy_hash = hashlib.sha256(policy_str.encode()).hexdigest()
            
            version = {
                "version": len(self.versions) + 1,
                "timestamp": datetime.now().isoformat(),
                "hash": policy_hash,
                "changes_count": len([c for c in self.changes if c.get('applied') and not c.get('archived', False)])
            }
            
            self.versions.append(version)
            
            # 버전별 스냅샷 저장
            snapshot_file = self.history_path / f"snapshot_v{version['version']}.yaml"
            with open(snapshot_file, 'w', encoding='utf-8') as f:
                yaml.dump(policy_data, f, allow_unicode=True, sort_keys=False)
            
            # 버전 목록 저장
            with open(self.versions_file, 'w', encoding='utf-8') as f:
                json.dump(self.versions, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Version snapshot created: v{version['version']}")
            return version
            
        except Exception as e:
            logger.error(f"Error creating version snapshot: {e}")
            return None
    
    def get_pending_changes(self) -> List[Dict]:
        """승인 대기 중인 변경사항 조회"""
        return [c for c in self.changes if not c.get('approved', False)]
    
    def get_approved_changes(self) -> List[Dict]:
        """승인된 변경사항 조회"""
        return [c for c in self.changes if c.get('approved', False) and not c.get('applied', False)]
    
    def approve_change(self, change_index: int, reviewer: str):
        """변경사항 승인"""
        if 0 <= change_index < len(self.changes):
            self.changes[change_index]['approved'] = True
            self.changes[change_index]['reviewer'] = reviewer
            self.changes[change_index]['approved_at'] = datetime.now().isoformat()
            self._save_changes()
            
            logger.info(f"Change approved by {reviewer}: {self.changes[change_index]}")
            return True
        return False
    
    def mark_applied(self, change_index: int):
        """변경사항 적용 완료 표시"""
        if 0 <= change_index < len(self.changes):
            self.changes[change_index]['applied'] = True
            self.changes[change_index]['applied_at'] = datetime.now().isoformat()
            self._save_changes()
            
            logger.info(f"Change marked as applied: {self.changes[change_index]}")
            return True
        return False
    
    def generate_change_report(self, days: int = 30) -> str:
        """변경사항 리포트 생성"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_changes = [
            c for c in self.changes
            if datetime.fromisoformat(c['timestamp']) > cutoff_date
        ]
        
        report = [
            "=" * 70,
            f"REGULATORY CHANGE REPORT (Last {days} days)",
            "=" * 70,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Changes: {len(recent_changes)}",
            "=" * 70,
            ""
        ]
        
        # 국가별 그룹화
        by_country = {}
        for change in recent_changes:
            country = change['country']
            if country not in by_country:
                by_country[country] = []
            by_country[country].append(change)
        
        for country, changes in sorted(by_country.items()):
            report.append(f"\n{country}:")
            report.append("-" * 70)
            
            for change in changes:
                status = "✓ Applied" if change.get('applied') else ("✓ Approved" if change.get('approved') else "⏳ Pending")
                report.append(f"  [{status}] {change['field']}")
                report.append(f"      Type: {change['change_type']}")
                report.append(f"      Source: {change['source']}")
                report.append(f"      Date: {change['timestamp'][:10]}")
                
                if change.get('approved'):
                    report.append(f"      Reviewer: {change.get('reviewer', 'N/A')}")
                
                report.append("")
        
        # 통계
        report.append("=" * 70)
        report.append("STATISTICS:")
        pending = len([c for c in recent_changes if not c.get('approved')])
        approved = len([c for c in recent_changes if c.get('approved') and not c.get('applied')])
        applied = len([c for c in recent_changes if c.get('applied')])
        
        report.append(f"  Pending:  {pending}")
        report.append(f"  Approved: {approved}")
        report.append(f"  Applied:  {applied}")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def diff_versions(self, version1: int, version2: int) -> Optional[Dict]:
        """두 버전 간 차이점 비교"""
        snapshot1 = self.history_path / f"snapshot_v{version1}.yaml"
        snapshot2 = self.history_path / f"snapshot_v{version2}.yaml"
        
        if not snapshot1.exists() or not snapshot2.exists():
            logger.error("One or both snapshot files not found")
            return None
        
        with open(snapshot1, 'r', encoding='utf-8') as f:
            data1 = yaml.safe_load(f)
        
        with open(snapshot2, 'r', encoding='utf-8') as f:
            data2 = yaml.safe_load(f)
        
        # 간단한 diff (실제로는 더 정교한 비교 필요)
        diff = {
            "version1": version1,
            "version2": version2,
            "added": {},
            "removed": {},
            "modified": {}
        }
        
        # TODO: 실제 diff 로직 구현
        
        return diff


class ChangeReviewSystem:
    """변경사항 검토 시스템"""
    
    def __init__(self):
        self.tracker = ChangeTracker()
    
    def review_pending_changes(self):
        """대기 중인 변경사항 검토"""
        pending = self.tracker.get_pending_changes()
        
        if not pending:
            print("✅ No pending changes to review")
            return
        
        print("=" * 70)
        print(f"PENDING CHANGES REVIEW ({len(pending)} items)")
        print("=" * 70)
        print()
        
        for idx, change in enumerate(pending):
            print(f"{idx + 1}. {change['country']} - {change['field']}")
            print(f"   Type: {change['change_type']}")
            print(f"   Source: {change['source']}")
            print(f"   Date: {change['timestamp'][:10]}")
            print(f"   Confidence: {change['confidence']}")
            print()
            
            if change.get('old_value'):
                print(f"   Old: {change['old_value']}")
            print(f"   New: {change['new_value']}")
            print()
            print(f"   URL: {change['source_url']}")
            print("-" * 70)
        
        print()
        print("To approve changes, use the web dashboard or CLI tool")
    
    def interactive_review(self):
        """대화형 검토 모드"""
        pending = self.tracker.get_pending_changes()
        
        if not pending:
            print("✅ No pending changes to review")
            return
        
        for idx, change in enumerate(pending):
            print("\n" + "=" * 70)
            print(f"Change {idx + 1}/{len(pending)}")
            print("=" * 70)
            print(f"Country: {change['country']}")
            print(f"Field: {change['field']}")
            print(f"Type: {change['change_type']}")
            print(f"Source: {change['source']}")
            print(f"URL: {change['source_url']}")
            print()
            
            if change.get('old_value'):
                print(f"Current: {change['old_value']}")
            print(f"Proposed: {change['new_value']}")
            print()
            
            response = input("Approve this change? (y/n/s to skip): ").lower().strip()
            
            if response == 'y':
                reviewer = input("Your name: ").strip()
                if self.tracker.approve_change(idx, reviewer):
                    print("✅ Change approved!")
            elif response == 's':
                continue
            else:
                print("❌ Change rejected/skipped")


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Change Tracking System')
    parser.add_argument('--report', type=int, default=30, help='Generate report for last N days')
    parser.add_argument('--review', action='store_true', help='Review pending changes')
    parser.add_argument('--interactive', action='store_true', help='Interactive review mode')
    parser.add_argument('--snapshot', action='store_true', help='Create version snapshot')
    
    args = parser.parse_args()
    
    tracker = ChangeTracker()
    
    if args.snapshot:
        version = tracker.create_version_snapshot()
        if version:
            print(f"✅ Snapshot created: v{version['version']}")
    
    if args.report:
        report = tracker.generate_change_report(days=args.report)
        print(report)
    
    if args.interactive:
        reviewer = ChangeReviewSystem()
        reviewer.interactive_review()
    elif args.review:
        reviewer = ChangeReviewSystem()
        reviewer.review_pending_changes()


if __name__ == "__main__":
    main()
