#!/usr/bin/env python3
"""
Notification System for Regulatory Updates
규제 업데이트 알림 시스템

이메일, Slack, Discord 등으로 업데이트 알림을 전송합니다.
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from datetime import datetime
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationConfig:
    """알림 설정"""
    
    def __init__(self, config_file: str = "config/notifications.yaml"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """설정 로드"""
        if self.config_file.exists():
            import yaml
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        # 기본 설정
        return {
            "email": {
                "enabled": False,
                "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
                "smtp_port": int(os.getenv("SMTP_PORT", "587")),
                "sender": os.getenv("EMAIL_SENDER", ""),
                "password": os.getenv("EMAIL_PASSWORD", ""),
                "recipients": os.getenv("EMAIL_RECIPIENTS", "").split(",")
            },
            "slack": {
                "enabled": False,
                "webhook_url": os.getenv("SLACK_WEBHOOK_URL", "")
            },
            "discord": {
                "enabled": False,
                "webhook_url": os.getenv("DISCORD_WEBHOOK_URL", "")
            }
        }


class EmailNotifier:
    """이메일 알림"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.enabled = config.get("enabled", False)
    
    def send(self, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """이메일 전송"""
        if not self.enabled:
            logger.info("Email notifications disabled")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config['sender']
            msg['To'] = ', '.join(self.config['recipients'])
            
            # 텍스트 버전
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # HTML 버전 (있는 경우)
            if html_body:
                msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # SMTP 연결 및 전송
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['sender'], self.config['password'])
                server.send_message(msg)
            
            logger.info(f"Email sent to {len(self.config['recipients'])} recipients")
            return True
            
        except Exception as e:
            logger.error(f"Email send error: {e}")
            return False


class SlackNotifier:
    """Slack 알림"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.enabled = config.get("enabled", False)
        self.webhook_url = config.get("webhook_url", "")
    
    def send(self, message: str, blocks: Optional[List[Dict]] = None) -> bool:
        """Slack 메시지 전송"""
        if not self.enabled or not self.webhook_url:
            logger.info("Slack notifications disabled or not configured")
            return False
        
        try:
            payload = {"text": message}
            
            if blocks:
                payload["blocks"] = blocks
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Slack notification sent successfully")
                return True
            else:
                logger.error(f"Slack error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Slack send error: {e}")
            return False
    
    def format_update_message(self, updates: List[Dict]) -> List[Dict]:
        """업데이트 메시지를 Slack 블록 형식으로 포맷"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🔔 Regulatory Update Alert"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{len(updates)} new regulatory update(s) detected*\n_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"
                }
            },
            {"type": "divider"}
        ]
        
        for idx, update in enumerate(updates[:10]):  # 최대 10개만 표시
            country = update.get('country', 'Unknown')
            source = update.get('source', 'Unknown')
            title = update.get('title', 'No title')
            link = update.get('link', update.get('url', ''))
            
            block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{idx+1}. {country} - {source}*\n{title}"
                }
            }
            
            if link:
                block["accessory"] = {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "View"},
                    "url": link
                }
            
            blocks.append(block)
        
        if len(updates) > 10:
            blocks.append({
                "type": "context",
                "elements": [{
                    "type": "mrkdwn",
                    "text": f"_... and {len(updates) - 10} more updates_"
                }]
            })
        
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "context",
            "elements": [{
                "type": "mrkdwn",
                "text": "Review and approve changes in the dashboard"
            }]
        })
        
        return blocks


class DiscordNotifier:
    """Discord 알림"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.enabled = config.get("enabled", False)
        self.webhook_url = config.get("webhook_url", "")
    
    def send(self, message: str, embeds: Optional[List[Dict]] = None) -> bool:
        """Discord 메시지 전송"""
        if not self.enabled or not self.webhook_url:
            logger.info("Discord notifications disabled or not configured")
            return False
        
        try:
            payload = {"content": message}
            
            if embeds:
                payload["embeds"] = embeds
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                logger.info("Discord notification sent successfully")
                return True
            else:
                logger.error(f"Discord error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Discord send error: {e}")
            return False
    
    def format_update_embeds(self, updates: List[Dict]) -> List[Dict]:
        """업데이트를 Discord embed 형식으로 포맷"""
        embeds = []
        
        # 메인 embed
        main_embed = {
            "title": "🔔 Regulatory Update Alert",
            "description": f"{len(updates)} new regulatory update(s) detected",
            "color": 0xFF6B35,  # 주황색
            "timestamp": datetime.now().isoformat(),
            "footer": {
                "text": "Glocal Policy Guardrail"
            }
        }
        embeds.append(main_embed)
        
        # 각 업데이트별 embed (최대 10개)
        for update in updates[:10]:
            country = update.get('country', 'Unknown')
            source = update.get('source', 'Unknown')
            title = update.get('title', 'No title')
            link = update.get('link', update.get('url', ''))
            
            embed = {
                "title": f"{country} - {source}",
                "description": title,
                "color": 0x4ECDC4,  # 청록색
            }
            
            if link:
                embed["url"] = link
            
            embeds.append(embed)
            
            # Discord는 최대 10개의 embed만 허용
            if len(embeds) >= 10:
                break
        
        return embeds


class NotificationManager:
    """통합 알림 관리자"""
    
    def __init__(self, config_file: str = "config/notifications.yaml"):
        config = NotificationConfig(config_file).config
        
        self.email = EmailNotifier(config.get("email", {}))
        self.slack = SlackNotifier(config.get("slack", {}))
        self.discord = DiscordNotifier(config.get("discord", {}))
    
    def notify_updates(self, updates: List[Dict]) -> Dict[str, bool]:
        """모든 채널로 업데이트 알림 전송"""
        results = {}
        
        if not updates:
            logger.info("No updates to notify")
            return results
        
        # 이메일 알림
        email_subject = f"[Regulatory Alert] {len(updates)} New Updates Detected"
        email_body = self._format_email_body(updates)
        email_html = self._format_email_html(updates)
        
        results['email'] = self.email.send(email_subject, email_body, email_html)
        
        # Slack 알림
        slack_message = f"🔔 {len(updates)} new regulatory updates detected"
        slack_blocks = self.slack.format_update_message(updates)
        
        results['slack'] = self.slack.send(slack_message, slack_blocks)
        
        # Discord 알림
        discord_message = f"**🔔 Regulatory Update Alert**\n{len(updates)} new updates detected"
        discord_embeds = self.discord.format_update_embeds(updates)
        
        results['discord'] = self.discord.send(discord_message, discord_embeds)
        
        return results
    
    def _format_email_body(self, updates: List[Dict]) -> str:
        """이메일 본문 (텍스트) 포맷"""
        lines = [
            "=" * 70,
            "REGULATORY UPDATE NOTIFICATION",
            "=" * 70,
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Updates: {len(updates)}",
            "=" * 70,
            ""
        ]
        
        for idx, update in enumerate(updates, 1):
            lines.append(f"{idx}. {update.get('country', 'Unknown')} - {update.get('source', 'Unknown')}")
            lines.append(f"   Title: {update.get('title', 'No title')}")
            
            link = update.get('link', update.get('url', ''))
            if link:
                lines.append(f"   Link: {link}")
            
            lines.append(f"   Detected: {update.get('detected_at', 'N/A')}")
            lines.append("")
        
        lines.extend([
            "=" * 70,
            "Please review these updates in the policy dashboard.",
            "=" * 70
        ])
        
        return "\n".join(lines)
    
    def _format_email_html(self, updates: List[Dict]) -> str:
        """이메일 본문 (HTML) 포맷"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h1 {{ color: #2c3e50; }}
                .update {{ margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-left: 4px solid #FF6B35; }}
                .update-title {{ font-weight: bold; color: #34495e; }}
                .update-link {{ color: #3498db; text-decoration: none; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; }}
            </style>
        </head>
        <body>
            <h1>🔔 Regulatory Update Alert</h1>
            <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Total Updates:</strong> {len(updates)}</p>
            <hr>
        """
        
        for idx, update in enumerate(updates, 1):
            country = update.get('country', 'Unknown')
            source = update.get('source', 'Unknown')
            title = update.get('title', 'No title')
            link = update.get('link', update.get('url', ''))
            
            html += f"""
            <div class="update">
                <div class="update-title">{idx}. {country} - {source}</div>
                <p>{title}</p>
            """
            
            if link:
                html += f'<p><a href="{link}" class="update-link">View Details →</a></p>'
            
            html += f"""
                <p style="color: #7f8c8d; font-size: 12px;">
                    Detected: {update.get('detected_at', 'N/A')}
                </p>
            </div>
            """
        
        html += """
            <div class="footer">
                <p>Please review and approve these updates in the policy dashboard.</p>
                <p><em>Glocal Policy Guardrail - Automated Regulatory Monitoring</em></p>
            </div>
        </body>
        </html>
        """
        
        return html


def main():
    """테스트용 메인 함수"""
    # 테스트 업데이트 데이터
    test_updates = [
        {
            "country": "South_Korea",
            "source": "개인정보보호위원회",
            "title": "개인정보보호법 시행령 일부개정령(안) 입법예고",
            "link": "https://www.pipc.go.kr/np/default/page.do?mCode=D010030000",
            "detected_at": datetime.now().isoformat()
        },
        {
            "country": "United_States",
            "source": "FCC",
            "title": "New COPPA Guidelines for Digital Platforms",
            "link": "https://www.fcc.gov/news",
            "detected_at": datetime.now().isoformat()
        }
    ]
    
    manager = NotificationManager()
    results = manager.notify_updates(test_updates)
    
    print("\n" + "=" * 70)
    print("NOTIFICATION TEST RESULTS")
    print("=" * 70)
    for channel, success in results.items():
        status = "✅ Sent" if success else "❌ Failed"
        print(f"{channel.capitalize()}: {status}")
    print("=" * 70)


if __name__ == "__main__":
    main()
