"""
Regulatory Policy Auto-Update System
자동 규제 정책 업데이트 시스템

This module monitors official regulatory sources and automatically updates
the policy database when changes are detected.
"""

import requests
import feedparser
import hashlib
import yaml
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RegulatorySource:
    """규제 정보 출처"""
    country: str
    name: str
    url: str
    method: str  # 'rss', 'api', 'scrape', 'manual'
    language: str
    check_frequency: Optional[str] = None
    last_checked: Optional[str] = None
    last_hash: Optional[str] = None
    note: Optional[str] = None
    filter_keywords: Optional[List[str]] = None
    applies_to: Optional[List[str]] = None


class PolicyUpdateMonitor:
    """정책 업데이트 모니터링 시스템"""
    
    def __init__(self, config_path: str = "config/regulatory_sources.yaml"):
        self.sources = self._load_sources(config_path)
        self.update_log = []
    
    def _load_sources(self, path: str) -> List[RegulatorySource]:
        """규제 소스 설정 로드"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return [RegulatorySource(**source) for source in data.get('sources', [])]
        except FileNotFoundError:
            logger.warning(f"Sources config not found at {path}, using defaults")
            return self._get_default_sources()
    
    def _get_default_sources(self) -> List[RegulatorySource]:
        """기본 규제 소스 목록"""
        return [
            RegulatorySource(
                country="United_States",
                name="FCC News",
                url="https://www.fcc.gov/news-events/rss",
                method="rss",
                language="en"
            ),
            RegulatorySource(
                country="South_Korea",
                name="방송통신심의위원회",
                url="https://www.kocsc.or.kr/news/notice",
                method="scrape",
                language="ko"
            ),
            RegulatorySource(
                country="Germany",
                name="BfDI Press Releases",
                url="https://www.bfdi.bund.de/DE/Service/Presse/presse_node.html",
                method="scrape",
                language="de"
            ),
            # More sources to be added
        ]
    
    def check_for_updates(self) -> List[Dict]:
        """모든 소스에서 업데이트 확인"""
        updates = []
        
        for source in self.sources:
            try:
                if source.method == "rss":
                    update = self._check_rss_feed(source)
                elif source.method == "api":
                    update = self._check_api(source)
                elif source.method == "scrape":
                    update = self._check_website(source)
                else:
                    logger.info(f"Skipping manual source: {source.name}")
                    continue
                
                if update:
                    updates.append(update)
                    logger.info(f"✅ Update detected from {source.name}")
                else:
                    logger.info(f"ℹ️  No changes from {source.name}")
                    
            except Exception as e:
                logger.error(f"❌ Error checking {source.name}: {e}")
        
        return updates
    
    def _check_rss_feed(self, source: RegulatorySource) -> Optional[Dict]:
        """RSS 피드 확인"""
        try:
            feed = feedparser.parse(source.url)
            
            if not feed.entries:
                return None
            
            # 가장 최근 항목 가져오기
            latest = feed.entries[0]
            
            # 콘텐츠 해시 생성
            content = f"{latest.title}{latest.get('summary', '')}"
            current_hash = hashlib.md5(content.encode()).hexdigest()
            
            # 변경 감지
            if source.last_hash and source.last_hash == current_hash:
                return None
            
            return {
                "source": source.name,
                "country": source.country,
                "method": "rss",
                "title": latest.title,
                "summary": latest.get('summary', ''),
                "link": latest.get('link', ''),
                "published": latest.get('published', ''),
                "hash": current_hash,
                "detected_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"RSS feed error for {source.name}: {e}")
            return None
    
    def _check_api(self, source: RegulatorySource) -> Optional[Dict]:
        """API 엔드포인트 확인"""
        try:
            response = requests.get(source.url, timeout=10)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            current_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
            
            if source.last_hash and source.last_hash == current_hash:
                return None
            
            return {
                "source": source.name,
                "country": source.country,
                "method": "api",
                "data": data,
                "hash": current_hash,
                "detected_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"API error for {source.name}: {e}")
            return None
    
    def _check_website(self, source: RegulatorySource) -> Optional[Dict]:
        """웹사이트 스크래핑 (간단한 변경 감지)"""
        try:
            response = requests.get(source.url, timeout=10)
            
            if response.status_code != 200:
                return None
            
            # 간단한 콘텐츠 해시 (실제로는 BeautifulSoup 등으로 파싱 필요)
            current_hash = hashlib.md5(response.content).hexdigest()
            
            if source.last_hash and source.last_hash == current_hash:
                return None
            
            return {
                "source": source.name,
                "country": source.country,
                "method": "scrape",
                "url": source.url,
                "hash": current_hash,
                "detected_at": datetime.now().isoformat(),
                "note": "Content changed - manual review required"
            }
            
        except Exception as e:
            logger.error(f"Scraping error for {source.name}: {e}")
            return None
    
    def generate_update_report(self, updates: List[Dict]) -> str:
        """업데이트 리포트 생성"""
        if not updates:
            return "No regulatory updates detected."
        
        report = [
            "=" * 70,
            "REGULATORY UPDATE REPORT",
            "=" * 70,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Updates: {len(updates)}",
            "=" * 70,
            ""
        ]
        
        for idx, update in enumerate(updates, 1):
            report.append(f"{idx}. {update['source']} ({update['country']})")
            report.append(f"   Method: {update['method']}")
            
            if 'title' in update:
                report.append(f"   Title: {update['title']}")
            
            if 'link' in update:
                report.append(f"   Link: {update['link']}")
            
            report.append(f"   Detected: {update['detected_at']}")
            report.append("-" * 70)
        
        report.append("")
        report.append("ACTION REQUIRED:")
        report.append("1. Review each update for policy implications")
        report.append("2. Update config/policy_rules.yaml if necessary")
        report.append("3. Run compliance tests to verify changes")
        report.append("4. Document changes in version control")
        
        return "\n".join(report)
    
    def save_update_log(self, updates: List[Dict], filepath: str = "reports/policy_updates.json"):
        """업데이트 로그 저장"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "updates_count": len(updates),
            "updates": updates
        }
        
        # 기존 로그 읽기
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except FileNotFoundError:
            logs = []
        
        # 새 로그 추가
        logs.append(log_entry)
        
        # 저장 (최근 100개만 유지)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(logs[-100:], f, indent=2, ensure_ascii=False)
        
        logger.info(f"Update log saved to {filepath}")


class PolicyAutoUpdater:
    """정책 자동 업데이트 시스템"""
    
    def __init__(self, policy_path: str = "config/policy_rules.yaml"):
        self.policy_path = policy_path
        self.policy_db = self._load_policy()
    
    def _load_policy(self) -> Dict:
        """현재 정책 로드"""
        with open(self.policy_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def suggest_policy_update(self, regulatory_update: Dict) -> Optional[Dict]:
        """
        규제 업데이트를 기반으로 정책 변경 제안
        (실제로는 AI/LLM을 사용하여 자동 분석)
        """
        country = regulatory_update.get('country')
        
        if country not in self.policy_db:
            return None
        
        # 간단한 키워드 기반 제안 (실제로는 더 정교한 NLP 필요)
        suggestion = {
            "country": country,
            "current_policy": self.policy_db[country],
            "suggested_changes": [],
            "confidence": "low",
            "requires_legal_review": True
        }
        
        # 예: 제목에서 키워드 감지
        title = regulatory_update.get('title', '').lower()
        
        if 'gambling' in title or 'gaming' in title:
            suggestion['suggested_changes'].append({
                "field": "ad_restrictions.gambling_ads",
                "reason": "Gambling regulation update detected",
                "action": "Review and potentially update gambling ad restrictions"
            })
        
        if 'privacy' in title or 'data protection' in title:
            suggestion['suggested_changes'].append({
                "field": "mandatory_compliance",
                "reason": "Privacy regulation update detected",
                "action": "Review data protection requirements"
            })
        
        return suggestion if suggestion['suggested_changes'] else None
    
    def apply_policy_update(self, country: str, changes: Dict, backup: bool = True):
        """
        정책 업데이트 적용 (수동 승인 후)
        """
        if backup:
            # 백업 생성
            backup_path = f"{self.policy_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.policy_db, f, allow_unicode=True)
            logger.info(f"Backup created: {backup_path}")
        
        # 변경사항 적용
        if country in self.policy_db:
            self.policy_db[country].update(changes)
            
            # 저장
            with open(self.policy_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.policy_db, f, allow_unicode=True, sort_keys=False)
            
            logger.info(f"Policy updated for {country}")
        else:
            logger.error(f"Country {country} not found in policy database")


def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("REGULATORY POLICY AUTO-UPDATE SYSTEM")
    print("=" * 70)
    print()
    
    # 업데이트 모니터 초기화
    monitor = PolicyUpdateMonitor()
    
    print(f"Monitoring {len(monitor.sources)} regulatory sources...")
    print()
    
    # 업데이트 확인
    updates = monitor.check_for_updates()
    
    # 리포트 생성
    report = monitor.generate_update_report(updates)
    print(report)
    
    # 로그 저장
    if updates:
        monitor.save_update_log(updates)
        print()
        print("✅ Update log saved to reports/policy_updates.json")
        
        # 정책 업데이트 제안 생성
        updater = PolicyAutoUpdater()
        
        print()
        print("🤖 GENERATING POLICY UPDATE SUGGESTIONS...")
        print("=" * 70)
        
        for update in updates:
            suggestion = updater.suggest_policy_update(update)
            if suggestion:
                print(f"\nCountry: {suggestion['country']}")
                print(f"Confidence: {suggestion['confidence']}")
                print("Suggested Changes:")
                for change in suggestion['suggested_changes']:
                    print(f"  - {change['field']}: {change['action']}")
                print(f"Requires Legal Review: {suggestion['requires_legal_review']}")
    
    print()
    print("=" * 70)
    print("✨ Monitoring complete!")


if __name__ == "__main__":
    main()
