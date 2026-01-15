"""
Remove all Korean text from codebase and replace with English
"""
import re
from pathlib import Path

# Define replacements
REPLACEMENTS = {
    # change_tracker.py
    "규제 변경사항 추적 및 버전 관리 시스템": "Regulatory Change Tracking and Version Management System",
    "규제 업데이트의 변경사항을 추적하고 히스토리를 관리합니다.": "Tracks regulatory updates and manages change history.",
    "변경 기록 로드": "Load change records",
    "버전 히스토리 로드": "Load version history",
    "변경사항 기록": "Record change entry",
    "변경 기록 저장": "Save change records",
    "현재 정책의 버전 스냅샷 생성": "Create policy version snapshot",
    "정책 해시 생성": "Generate policy hash",
    "버전별 스냅샷 저장": "Save version snapshot",
    "버전 목록 저장": "Save version list",
    "승인 대기 중인 변경사항 조회": "Retrieve pending changes awaiting approval",
    "승인된 변경사항 조회": "Retrieve approved changes",
    "변경사항 승인": "Approve change",
    "변경사항 적용 완료 표시": "Mark change as applied",
    "변경사항 리포트 생성": "Generate change report",
    "국가별 그룹화": "Group by country",
    "통계": "Statistics",
    "두 버전 간 차이점 비교": "Compare differences between two versions",
    "간단한 diff (실제로는 더 정교한 비교 필요)": "Simple diff (more sophisticated comparison needed in practice)",
    "실제 diff 로직 구현": "Implement actual diff logic",
    "변경사항 검토 시스템": "Change Review System",
    "대기 중인 변경사항 검토": "Review pending changes",
    "대화형 검토 모드": "Interactive review mode",
    "메인 함수": "Main function",
    
    # update_scheduler.py
    "규제 업데이트 자동 스케줄러": "Automated Regulatory Update Scheduler",
    "즉시 업데이트 확인": "Check for updates immediately",
    "리포트 생성": "Generate report",
    "로그 저장": "Save log",
    "정책 제안 생성": "Generate policy proposal",
    "업데이트 리포트 생성": "Generate update report",
    "최근 10개 로그": "Last 10 logs",
    "스케줄 설정 (cron job 또는 systemd timer)": "Schedule setup (cron job or systemd timer)",
    
    # analytics.py
    "컴플라이언스 검사 결과를 시각화하고 분석하는 도구": "Tool for visualizing and analyzing compliance inspection results",
    "컴플라이언스 검사 결과 분석 및 시각화": "Compliance inspection result analysis and visualization",
    "결과 추가": "Add result",
    "국가별 위험도 히트맵 생성 (ASCII 아트)": "Generate country risk heatmap (ASCII art)",
    "평균 위반 수 계산": "Calculate average violation count",
    "히트맵 생성": "Generate heatmap",
    "위반 수에 따른 위험도 이모지": "Risk emoji based on violation count",
    "위반 유형별 분류": "Classify by violation type",
    "심각도 분포 차트": "Severity distribution chart",
    "경영진용 요약 리포트": "Executive summary report",
    "가장 위험한 국가": "Most risky countries",
    "JSON 형식으로 리포트 내보내기": "Export report in JSON format",
    "전체 분석 리포트 생성": "Generate comprehensive analysis report",
    
    # notification_system.py
    "규제 업데이트 Notification system": "Regulatory Update Notification System",
    "이메일, Slack, Discord 등으로 업데이트 알림을 전송합니다.": "Sends update notifications via email, Slack, Discord, etc.",
    "알림 설정": "Notification configuration",
    "설정 로드": "Load configuration",
    "기본 설정": "Default configuration",
    "이메일 알림": "Email notification",
    "이메일 전송": "Send email",
    "텍스트 버전": "Text version",
    "있는 경우": "if available",
}

def remove_korean_from_file(file_path):
    """Remove Korean text from a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for korean, english in REPLACEMENTS.items():
            content = content.replace(korean, english)
        
        # Check if any changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {file_path}")
            return True
        else:
            return False
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    """Main function"""
    workspace_root = Path("/workspaces/Glocal-Policy-Guardrail")
    
    # Files to process
    files_to_process = [
        workspace_root / "src" / "change_tracker.py",
        workspace_root / "src" / "analytics.py",
        workspace_root / "src" / "notification_system.py",
        workspace_root / "update_scheduler.py",
    ]
    
    print("Removing Korean text from Python files...")
    print("=" * 60)
    
    updated_count = 0
    for file_path in files_to_process:
        if file_path.exists():
            if remove_korean_from_file(file_path):
                updated_count += 1
        else:
            print(f"⚠ File not found: {file_path}")
    
    print("=" * 60)
    print(f"\n✅ Complete! Updated {updated_count} files.")

if __name__ == "__main__":
    main()
