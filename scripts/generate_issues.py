#!/usr/bin/env python3
"""
Generate initial GitHub issues from backlog

This script creates GitHub issues for Sprint 1 stories.
Requires: gh CLI tool or GitHub token
"""
import json
import subprocess
from pathlib import Path

def load_sprint_data():
    """Load sprint data from JSON"""
    with open('sprints.json', 'r') as f:
        return json.load(f)

def create_github_issue(story):
    """Create a GitHub issue using gh CLI"""
    title = f"{story['id']}: {story['title']}"
    
    # Build issue body
    body_parts = [
        f"## Description",
        story['description'],
        "",
        f"## Type: `{story['type']}`",
        f"## Priority: `{story['priority']}`",
        f"## Story Points: `{story['points']}`",
        "",
        "## Acceptance Criteria"
    ]
    
    for criterion in story.get('acceptance_criteria', []):
        body_parts.append(f"- [ ] {criterion}")
    
    if 'tasks' in story:
        body_parts.extend([
            "",
            "## Tasks"
        ])
        for task in story['tasks']:
            body_parts.append(f"- [ ] {task}")
    
    body_parts.extend([
        "",
        "---",
        f"**Sprint**: Sprint 1",
        f"**Epic**: EP-001 Testing & Quality Assurance"
    ])
    
    body = "\n".join(body_parts)
    
    # Create labels
    labels = [story['type'], story['priority'], 'sprint-1']
    
    # Print issue for preview
    print(f"\n{'='*80}")
    print(f"Creating Issue: {title}")
    print(f"Labels: {', '.join(labels)}")
    print(f"{'='*80}")
    print(body)
    print(f"{'='*80}\n")
    
    # Uncomment to actually create issues
    # Requires gh CLI: brew install gh
    # gh auth login first
    
    # cmd = [
    #     'gh', 'issue', 'create',
    #     '--title', title,
    #     '--body', body,
    #     '--label', ','.join(labels)
    # ]
    # 
    # try:
    #     result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    #     print(f"✅ Created: {result.stdout.strip()}")
    #     return result.stdout.strip()
    # except subprocess.CalledProcessError as e:
    #     print(f"❌ Error: {e.stderr}")
    #     return None
    
    return f"[DRY RUN] Would create: {title}"

def main():
    """Main execution"""
    print("=" * 80)
    print("GITHUB ISSUE GENERATOR - SPRINT 1 BACKLOG")
    print("=" * 80)
    print()
    print("This script will create GitHub issues for Sprint 1 stories.")
    print("Currently in DRY RUN mode - no issues will be created.")
    print()
    print("To actually create issues:")
    print("  1. Install GitHub CLI: brew install gh (or apt install gh)")
    print("  2. Authenticate: gh auth login")
    print("  3. Uncomment the gh commands in this script")
    print()
    print("=" * 80)
    print()
    
    # Load data
    data = load_sprint_data()
    sprint1 = data['sprint_1']
    
    print(f"Sprint {sprint1['sprint_number']}: {sprint1['goal']}")
    print(f"Duration: {sprint1['start_date']} to {sprint1['end_date']}")
    print(f"Total Stories: {len(sprint1['stories'])}")
    print(f"Total Points: {sprint1['metrics']['planned_points']}")
    print()
    
    # Generate issues
    created_issues = []
    for story in sprint1['stories']:
        issue_url = create_github_issue(story)
        if issue_url:
            created_issues.append(issue_url)
    
    print()
    print("=" * 80)
    print(f"SUMMARY: {len(created_issues)} issues processed")
    print("=" * 80)
    
    # Save issue URLs for reference
    if created_issues:
        output = {
            'sprint': 'Sprint 1',
            'created_at': '2026-01-15',
            'issues': created_issues
        }
        
        with open('generated_issues.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✅ Issue URLs saved to generated_issues.json")

if __name__ == '__main__':
    main()
