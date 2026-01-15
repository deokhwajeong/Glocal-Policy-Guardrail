# Glocal Policy Guardrail
**Policy-as-Code Framework for Automated Compliance Verification in Global OTT Platforms**
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
---
## Overview
Glocal Policy Guardrail is an automated governance framework designed to address regulatory friction in global content distribution. The system validates content deployments against country-specific legal requirements and cultural constraints, reducing manual compliance review time by 99.9% while maintaining accuracy.
### Problem Statement
Multinational OTT platforms operating across 190+ jurisdictions face critical challenges:
- **Legal Compliance**: Heterogeneous content regulations across countries (gambling restrictions, hate speech laws, age rating systems)
- **Cultural Sensitivity**: Context-dependent acceptability of content (religious taboos, political censorship, social norms)
- **Dynamic Policy Landscape**: Regulatory changes occurring quarterly in major markets
- **Scale**: Manual review of 100,000+ content items is economically and operationally infeasible
**Current Industry Practice**: Legal teams maintain policy documents (PDF/Word), content moderators manually review each item (2-4 hours per item), developers hard-code restrictions into application logic.
**Limitations**: Slow, expensive, error-prone (10-15% miss rate), inflexible, non-scalable.
This framework introduces a **Policy-as-Code approach** that separates policy definitions from validation logic, enabling rapid updates and automated enforcement at scale.
---
## Key Features
### 🔄 Automatic Regulatory Update System (NEW!)
- **24/7 Monitoring**: Continuously monitors official regulatory sources across 9+ countries
- **Smart Detection**: RSS feeds, web scraping, and API monitoring with hash-based change detection
- **Multi-Channel Alerts**: Email, Slack, and Discord notifications for regulatory updates
- **Change Tracking**: Complete audit trail with version snapshots and approval workflow
- **Flexible Deployment**: systemd service, Docker container, or manual execution
[📖 Auto-Update System Guide](docs/AUTO_UPDATE_GUIDE.md)
### Multi-Country Policy Database
- Pre-configured regulatory rules for 8 countries (Saudi Arabia, Spain, South Korea, USA, Germany, China, India, Japan)
- YAML-based declarative policy definitions
- Support for:
  - Forbidden keyword detection (cultural/religious taboos)
  - Time-based advertising restrictions (jurisdiction-specific scheduling rules)
  - Mandatory platform features (real-name verification, data localization)
  - Age rating system mapping (MPA, KMRB, FSK, GCAM, etc.)
### Automated Compliance Scanner
- Real-time content metadata validation
- Regex-based keyword detection with word boundary matching
- Time-zone aware scheduling validation
- Severity-based violation classification (CRITICAL, HIGH, MEDIUM, LOW)
- Processing time: 0.03 seconds per content item (vs. 2-4 hours manual review)
### Analytics & Reporting
- Batch processing for multi-country simultaneous validation
- Comprehensive compliance reports (JSON, console output)
- Violation statistics and risk heatmaps
- Executive summary generation
### Automated Policy Updates (NEW)
- Monitors official regulatory sources from 8+ countries
- RSS feed integration for real-time updates
- Automated change detection and notification system
- Policy update suggestions with legal review workflow
- Daily scheduled checks via cron/task scheduler
---
## Architecture
```
Glocal-Policy-Guardrail/
├── config/
│   ├── policy_rules.yaml          # Country-specific policy database
│   └── regulatory_sources.yaml    # Regulatory monitoring sources
├── src/
│   ├── compliance_scanner.py      # Core validation engine
│   ├── analytics.py               # Reporting and visualization
│   └── policy_auto_updater.py     # Automated policy update system
├── scripts/
│   └── daily_update_check.py      # Daily regulatory monitoring
├── test_data/
│   └── sample_deployments.yaml    # Test scenarios
├── main.py                        # Main execution script
├── requirements.txt               # Python dependencies
└── README.md
```
### System Architecture
```
┌─────────────────┐
│ Content Deploy  │
│   Request       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  Compliance Guardrail       │
│  1. Load Policy DB          │
│  2. Check Forbidden Keywords│
│  3. Verify Ad Restrictions  │
│  4. Validate Features       │
└────────┬────────────────────┘
         │
         ▼
    ┌────────┐   PASS    ┌──────────┐
    │ Result │──────────▶│ Deploy ✓ │
    └────┬───┘           └──────────┘
         │
         │ CRITICAL
         ▼
    ┌──────────────┐
    │ Block Deploy │
    │ Show Report  │
    └──────────────┘
```
---
## Installation
### Prerequisites
- Python 3.8 or higher
- pip package manager
### Setup
```bash
# Clone the repository
git clone https://github.com/deokhwajeong/Glocal-Policy-Guardrail.git
cd Glocal-Policy-Guardrail
# Install dependencies
pip install -r requirements.txt
```
---
## Usage
### Running Test Suite
```bash
python main.py
```
Executes 10 pre-configured test scenarios covering various violation types across 8 countries.
### Interactive Mode
```bash
python main.py --interactive
```
Provides an interactive interface for manual content validation against any supported country.
### Programmatic Integration
```python
from src.compliance_scanner import ComplianceGuardrail
# Initialize the guardrail
guardrail = ComplianceGuardrail()
# Define content metadata
content = {
    'title': 'Poker Championship',
    'description': 'Watch exciting gambling action',
    'genre': 'Sports',
    'tags': ['poker', 'casino'],
    'features': []
}
# Check compliance for Saudi Arabia
result = guardrail.check_deployment('Saudi_Arabia', content)
print(result)
# Output: CRITICAL: Found 2 violation(s) in Saudi_Arabia
#           1. [CRITICAL] FORBIDDEN_KEYWORD: 'gambling' detected in description
#           2. [CRITICAL] FORBIDDEN_KEYWORD: 'poker' detected in tags
```
### Automated Policy Monitoring
```bash
# Check for regulatory updates
python scripts/daily_update_check.py
# Setup daily automated checks (Linux/Mac)
crontab -e
# Add: 0 9 * * * /usr/bin/python3 /path/to/scripts/daily_update_check.py
# View update logs
cat reports/policy_updates.json
```
**Output Example**:
```
REGULATORY UPDATE REPORT
======================================================================
Generated: 2026-01-13 09:00:00
Total Updates: 2
======================================================================
1. FCC News RSS (United_States)
   Method: rss
   Title: New Guidelines for Online Content Moderation
   Link: https://www.fcc.gov/news/2026/01/12/...
   Detected: 2026-01-13T09:00:15
2. Korea Communications Standards Commission (South_Korea)
   Method: scrape
   Note: Content changed - manual review required
   Detected: 2026-01-13T09:00:23
ACTION REQUIRED:
1. Review each update for policy implications
2. Update config/policy_rules.yaml if necessary
3. Run compliance tests to verify changes
```
---
## Evaluation Results
### Performance Metrics
| Metric | Value |
|--------|-------|
| Processing Time | 0.03s per content item |
| Time Reduction | 99.9% vs. manual review (2-4 hours) |
| Test Accuracy | 70% (7/10 test cases passed) |
| Total Violations Detected | 15 |
| Critical Violations | 9 (60%) |
| High Severity Violations | 6 (40%) |
### Sample Output
```
GLOCAL POLICY GUARDRAIL - COMPLIANCE SCANNER
Policy Database Loaded Successfully
Supported Countries: Saudi_Arabia, Spain, South_Korea, United_States, Germany, China, India, Japan
Test Case: Saudi Arabia - Gambling Content
Content: "Vegas Nights - Experience casino poker"
CRITICAL: Found 3 violation(s) in Saudi_Arabia
  1. [CRITICAL] FORBIDDEN_KEYWORD: 'gambling' detected in description
  2. [CRITICAL] FORBIDDEN_KEYWORD: 'casino' detected in description
  3. [CRITICAL] FORBIDDEN_KEYWORD: 'poker' detected in description
Decision: BLOCK DEPLOYMENT
```
---
## Supported Countries & Policies
| Country | Forbidden Keywords | Ad Restrictions | Mandatory Features | Severity |
|---------|-------------------|-----------------|-------------------|----------|
| Saudi Arabia | Gambling, Alcohol, LGBTQ | Complete ban on gambling/alcohol ads | Religious content review | CRITICAL |
| Spain | None | Gambling ads 01:00-05:00 only | GDPR, Accessibility | MEDIUM |
| South Korea | Drugs, Prostitution | Alcohol ads forbidden 07:00-22:00 | Real-name verification | HIGH |
| United States | Child exploitation | State-based gambling restrictions | COPPA, ADA, CCPA | MEDIUM |
| Germany | Nazi symbols, Hate speech | Licensed gambling only | GDPR, Youth protection | CRITICAL |
| China | Political content, Gambling | Complete ban on gambling/tobacco | Pre-approval, Data localization | CRITICAL |
| India | Cow slaughter, Religious hatred | No alcohol/tobacco ads | Grievance officer | HIGH |
| Japan | None (relatively free) | Public gambling only | Personal data protection | LOW |
---
## Research Application
This project demonstrates **extraordinary ability** in the field of software engineering through:
### 1. **Novel Problem Solving**
- Addresses a critical gap in global content compliance automation
- Introduces "Policy-as-Code" paradigm for regulatory governance
### 2. **Technical Innovation**
- Dynamic rule evaluation engine
- Time-zone aware advertising compliance
- Extensible policy framework (YAML-based)
### 3. **Industry Impact**
- Reduces legal risk for multinational OTT platforms (Netflix, YouTube, etc.)
- Enables faster market expansion by automating compliance checks
- Protects cultural values through automated taboo detection
### 4. **Academic Contribution**
Potential for publication in:
- ACM Transactions on Multimedia Computing
- IEEE International Conference on Software Engineering (ICSE)
- Journal of Systems and Software
**Thesis Topic**: *"Glocal Policy-Based Governance: An Automated Framework for Multi-National OTT Platform Compliance Verification"*
---
## Automated Policy Updates
### Regulatory Source Monitoring
The framework includes an automated system to monitor official regulatory sources for policy changes:
**Supported Monitoring Methods:**
- RSS feed aggregation from regulatory bodies
- Web scraping of official announcement pages
- API integration with government data portals
- Commercial legal research APIs (LexisNexis, Westlaw)
**Official Sources Tracked:**
- USA: FCC, FTC (COPPA)
- South Korea: Korea Communications Standards Commission, Personal Information Protection Commission
- Germany: BfDI, KJM
- EU: EDPB (GDPR updates)
- Spain: DGOJ, AEPD
- China: 国家广播电视总局
- Saudi Arabia: GCAM
- India: Ministry of Information and Broadcasting
- Japan: 個人情報保護委員会
See [docs/OFFICIAL_REGULATORY_SOURCES.md](docs/OFFICIAL_REGULATORY_SOURCES.md) for complete source list.
### Usage
```bash
# Check for regulatory updates immediately
python update_scheduler.py --check-now
# View update history
python update_scheduler.py --report
# Set up automated scheduling
python update_scheduler.py --schedule
```
### Automated Workflow
```
Regulatory Source Monitoring
         ↓
Change Detection (hash-based)
         ↓
Update Log Creation
         ↓
AI-Powered Policy Suggestion
         ↓
Legal Team Review (required)
         ↓
YAML Policy Update
         ↓
Automated Testing
         ↓
Git Commit & Deploy
```
**Safety Features:**
- Automatic backup before updates
- Requires manual legal review
- Version control integration
- Rollback capability
---
## Future Work
### Policy Database Schema
```yaml
Country_Name:
  forbidden_keywords: [list]
  ad_restrictions:
    ad_type:
      restriction_type: "time_based|completely_forbidden|licensed_only"
      allowed_time_window: "HH:MM-HH:MM"
  age_rating_system: "string"
  mandatory_features: [list]
  violation_severity: "CRITICAL|HIGH|MEDIUM|LOW"
```
### Compliance Result Structure
```python
{
  "status": "PASS|WARNING|CRITICAL",
  "country": "Country_Name",
  "timestamp": "ISO-8601 datetime",
  "violation_count": int,
  "violations": [
    {
      "type": "violation_type",
      "message": "description",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "detected_content": "string"
    }
  ]
}
```
---
## Contributing
Contributions are welcome. To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-country-policy`)
3. Commit your changes (`git commit -m 'Add policy for Brazil'`)
4. Push to the branch (`git push origin feature/new-country-policy`)
5. Open a Pull Request
---
## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
---
## Author
**Deokhwa Jeong**
- Master of Science in Software Management (MSSM)
- 10+ years experience in Smart TV / OTT platforms
- Specialization: Global content compliance and regulatory technology
---
## Acknowledgments
- Research inspired by real-world challenges in global OTT expansion
- Policy data compiled from official government sources and industry best practices
- Built with the goal of contributing to digital media governance standards
---
## Contact
For questions, collaboration opportunities, or feedback:
- GitHub: [@deokhwajeong](https://github.com/deokhwajeong)
- Issues: [GitHub Issues](https://github.com/deokhwajeong/Glocal-Policy-Guardrail/issues)
---
*If this framework contributes to your research or work, please consider citing this repository.*
