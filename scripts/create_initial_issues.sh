#!/bin/bash
# Script to create initial issues for GitHub Project Kanban board
# Run this after creating your GitHub Project
echo "🚀 Creating initial issues for Glocal Policy Guardrail project..."
echo ""
# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed. Please install it first."
    exit 1
fi
# Check authentication
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub. Run 'gh auth login' first."
    exit 1
fi
# High Priority Features
echo "📌 Creating high priority issues..."
gh issue create \
  --title "Add automated testing for regulatory updates" \
  --body "Implement comprehensive test suite for policy update validation and compliance scanning.\n\n- Unit tests for core modules\n- Integration tests for API endpoints\n- End-to-end tests for update workflow" \
  --label "enhancement,high-priority,testing"
gh issue create \
  --title "Implement CI/CD pipeline with GitHub Actions" \
  --body "Set up automated deployment pipeline:\n\n- Automated testing on PR\n- Docker image building\n- Deployment to staging/production\n- Version tagging and releases" \
  --label "enhancement,high-priority,devops"
gh issue create \
  --title "Add API rate limiting and authentication" \
  --body "Implement security measures for production API:\n\n- API key authentication\n- Rate limiting per client\n- Request logging and monitoring\n- CORS configuration" \
  --label "enhancement,high-priority,security"
# Feature Requests
echo "✨ Creating feature request issues..."
gh issue create \
  --title "Email notification system for high-confidence updates" \
  --body "Build email notification system:\n\n- Configure SMTP settings\n- Create email templates\n- Schedule digest emails\n- Allow user preferences for notification frequency" \
  --label "enhancement,feature"
gh issue create \
  --title "Export compliance reports to PDF" \
  --body "Add PDF export functionality:\n\n- Generate formatted PDF reports\n- Include charts and statistics\n- Add company branding\n- Support custom date ranges" \
  --label "enhancement,feature"
gh issue create \
  --title "Add search and filter functionality to dashboard" \
  --body "Enhance dashboard with search capabilities:\n\n- Search by country, source, or keyword\n- Filter by confidence level and status\n- Date range filtering\n- Save custom filter presets" \
  --label "enhancement,feature,ui"
gh issue create \
  --title "Implement webhook integration for real-time updates" \
  --body "Add webhook support for external integrations:\n\n- Configurable webhook endpoints\n- Event filtering\n- Retry logic with exponential backoff\n- Webhook testing interface" \
  --label "enhancement,feature,api"
# Bug Fixes
echo "🐛 Creating bug tracking issues..."
gh issue create \
  --title "Review and optimize database queries" \
  --body "Performance optimization for data loading:\n\n- Profile slow queries\n- Add appropriate indexes\n- Implement caching strategy\n- Optimize JSON parsing" \
  --label "bug,performance"
gh issue create \
  --title "Improve mobile responsiveness of dashboard" \
  --body "Fix responsive design issues:\n\n- Test on mobile devices\n- Fix table overflow on small screens\n- Optimize touch interactions\n- Improve mobile navigation" \
  --label "bug,ui,mobile"
# Documentation
echo "📚 Creating documentation issues..."
gh issue create \
  --title "Create architecture diagram" \
  --body "Document system architecture:\n\n- Component diagram\n- Data flow diagram\n- Deployment architecture\n- Technology stack overview" \
  --label "documentation"
gh issue create \
  --title "Write deployment guide for AWS/Azure" \
  --body "Create cloud deployment guides:\n\n- AWS deployment with ECS/Fargate\n- Azure deployment with App Service\n- Database setup and migration\n- Environment configuration" \
  --label "documentation,devops"
gh issue create \
  --title "Create video demo for Netflix pitch" \
  --body "Produce professional demo video:\n\n- Script preparation\n- Screen recording of key features\n- Voice-over narration\n- Professional editing\n- Upload to YouTube/Vimeo" \
  --label "documentation,demo"
# DevOps
echo "🔧 Creating DevOps issues..."
gh issue create \
  --title "Set up monitoring and alerting" \
  --body "Implement production monitoring:\n\n- Application performance monitoring (APM)\n- Error tracking (Sentry/Rollbar)\n- Uptime monitoring\n- Slack/email alerts for critical issues" \
  --label "devops,monitoring"
gh issue create \
  --title "Configure automated backups" \
  --body "Set up backup strategy:\n\n- Daily database backups\n- Configuration file backups\n- Backup retention policy\n- Test restore procedures" \
  --label "devops,infrastructure"
gh issue create \
  --title "Add health check endpoints" \
  --body "Implement health monitoring:\n\n- /health endpoint for load balancer\n- Database connectivity check\n- External API dependency checks\n- Detailed status in /status endpoint" \
  --label "devops,api"
echo ""
echo "✅ Successfully created 15 initial issues!"
echo ""
echo "🎯 Next steps:"
echo "1. Create your GitHub Project at: https://github.com/users/deokhwajeong/projects/new"
echo "2. Link these issues to your project board"
echo "3. Organize them into columns: Backlog, Todo, In Progress, Done"
echo "4. Start working on high-priority items!"
echo ""
echo "📊 View all issues: https://github.com/deokhwajeong/Glocal-Policy-Guardrail/issues"
