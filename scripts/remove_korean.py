"""
Remove all Korean text from codebase and replace with English
"""
import re
from pathlib import Path
# Define replacements
REPLACEMENTS = {
    # change_tracker.py
    "Regulatory Change Tracking and Version Management System": "Regulatory Change Tracking and Version Management System",
    "Tracks regulatory updates and manages change history.": "Tracks regulatory updates and manages change history.",
    "Load change records": "Load change records",
    "  ": "Load version history",
    " ": "Record change entry",
    "  ": "Save change records",
    "    ": "Create policy version snapshot",
    "  ": "Generate policy hash",
    "  ": "Save version snapshot",
    "  ": "Save version list",
    "    ": "Retrieve pending changes awaiting approval",
    "  ": "Retrieve approved changes",
    " ": "Approve change",
    "   ": "Mark change as applied",
    "  ": "Generate change report",
    " ": "Group by country",
    "": "Statistics",
    "    ": "Compare differences between two versions",
    " diff (    )": "Simple diff (more sophisticated comparison needed in practice)",
    " diff  ": "Implement actual diff logic",
    "  ": "Change Review System",
    "   ": "Review pending changes",
    "  ": "Interactive review mode",
    " ": "Main function",
    # update_scheduler.py
    "   ": "Automated Regulatory Update Scheduler",
    "  ": "Check for updates immediately",
    " ": "Generate report",
    " ": "Save log",
    "  ": "Generate policy proposal",
    "  ": "Generate update report",
    " 10 ": "Last 10 logs",
    "  (cron job  systemd timer)": "Schedule setup (cron job or systemd timer)",
    # analytics.py
    "Tool to visualize and analyze compliance check results": "Tool for visualizing and analyzing compliance inspection results",
    "Compliance check result analysis and visualization": "Compliance inspection result analysis and visualization",
    "Add result": "Add result",
    "    (ASCII )": "Generate country risk heatmap (ASCII art)",
    "   ": "Calculate average violation count",
    " ": "Generate heatmap",
    "    ": "Risk emoji based on violation count",
    "  ": "Classify by violation type",
    "  ": "Severity distribution chart",
    "  ": "Executive summary report",
    "  ": "Most risky countries",
    "JSON   ": "Export report in JSON format",
    "   ": "Generate comprehensive analysis report",
    # notification_system.py
    "Regulatory Update Notification System": "Regulatory Update Notification System",
    "Sends update notifications via Email, Slack, Discord, etc.": "Sends update notifications via email, Slack, Discord, etc.",
    " ": "Notification configuration",
    " ": "Load configuration",
    " ": "Default configuration",
    " ": "Email notification",
    " ": "Send email",
    " ": "Text version",
    " ": "if available",
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
