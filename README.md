# 🌍 Glocal Policy Guardrail

> **Policy-as-Code Framework for Global OTT Platforms**  
> Automated compliance verification system for country-specific legal regulations and cultural taboos

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

---

## 📖 Overview

**Glocal Policy Guardrail** is an automated governance framework that helps global OTT/streaming platforms manage **regulatory friction** when expanding into new markets. Instead of manually reviewing thousands of content items, this system automatically validates deployments against country-specific rule sets before release.

### 🎯 Problem Statement

Global media companies face significant challenges when operating across borders:
- **Legal Compliance**: Each country has different content regulations (e.g., gambling laws, age ratings)
- **Cultural Sensitivity**: What's acceptable in one culture may be taboo in another (e.g., religious restrictions)
- **Dynamic Regulations**: Laws change frequently, requiring constant policy updates
- **Scale**: Manual review is impractical for platforms with millions of content items

This project addresses these challenges through **automated, policy-driven compliance verification**.

---

## 🚀 Key Features

### ✅ Multi-Country Policy Database
- Pre-configured rules for **8 countries**: Saudi Arabia, Spain, South Korea, USA, Germany, China, India, Japan
- Extensible YAML-based policy definitions
- Supports:
  - Forbidden keywords (cultural/religious taboos)
  - Time-based advertising restrictions
  - Mandatory platform features (e.g., real-name verification)
  - Age rating system compliance

### ✅ Automated Compliance Scanner
- Real-time validation of content metadata
- Keyword detection with regex pattern matching
- Time-window enforcement for ads
- Severity-based violation reporting (CRITICAL, HIGH, MEDIUM, LOW)

### ✅ Batch Processing & Reporting
- Scan multiple deployments simultaneously
- Generate comprehensive compliance reports
- Country-wise violation statistics

---

## 🏗️ Architecture

```
Glocal-Policy-Guardrail/
├── config/
│   └── policy_rules.yaml          # Country-specific policy database
├── src/
│   └── compliance_scanner.py      # Core validation engine
├── test_data/
│   └── sample_deployments.yaml    # Test scenarios
├── main.py                        # Main execution script
├── requirements.txt               # Python dependencies
└── README.md
```

### System Flow

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

## 💻 Installation

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

## 🎮 Usage

### Run All Test Cases

```bash
python main.py
```

This will execute 10 pre-configured test scenarios covering various violation types across different countries.

### Interactive Demo Mode

```bash
python main.py --interactive
```

Allows you to manually input content details and test against any supported country.

### Example: Programmatic Usage

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
# Output: 🔴 CRITICAL: Found 1 violation(s) in Saudi_Arabia
#           1. [CRITICAL] FORBIDDEN_KEYWORD: Forbidden keyword 'gambling' detected in description
```

---

## 📊 Sample Test Results

```
╔══════════════════════════════════════════════════════════════════════╗
║  🌍 GLOCAL POLICY GUARDRAIL - COMPLIANCE SCANNER                     ║
╚══════════════════════════════════════════════════════════════════════╝

✅ Policy Database Loaded Successfully
   Supported Countries: Saudi_Arabia, Spain, South_Korea, United_States, Germany, China, India, Japan

🧪 Test Case: test_case_1
═══════════════════════════════════════════════════════════════════════
📋 Content Details:
   Title: Vegas Nights
   Country: Saudi_Arabia

🔴 CRITICAL: Found 2 violation(s) in Saudi_Arabia
  1. [CRITICAL] FORBIDDEN_KEYWORD: Forbidden keyword 'gambling' detected in description
     └─ Detected: 'gambling'
  2. [CRITICAL] FORBIDDEN_KEYWORD: Forbidden keyword 'poker' detected in tags

✅ TEST PASSED: Expected 'CRITICAL', Got 'CRITICAL'
```

---

## 🌐 Supported Countries & Policies

| Country | Forbidden Keywords | Ad Restrictions | Mandatory Features | Severity |
|---------|-------------------|-----------------|-------------------|----------|
| 🇸🇦 Saudi Arabia | Gambling, Alcohol, LGBTQ | Complete ban on gambling/alcohol ads | Religious content review | CRITICAL |
| 🇪🇸 Spain | None | Gambling ads 01:00-05:00 only | GDPR, Accessibility | MEDIUM |
| 🇰🇷 South Korea | Drugs, Prostitution | Alcohol ads forbidden 07:00-22:00 | Real-name verification | HIGH |
| 🇺🇸 United States | Child exploitation | State-based gambling restrictions | COPPA, ADA, CCPA | MEDIUM |
| 🇩🇪 Germany | Nazi symbols, Hate speech | Licensed gambling only | GDPR, Youth protection | CRITICAL |
| 🇨🇳 China | Political content, Gambling | Complete ban on gambling/tobacco | Pre-approval, Data localization | CRITICAL |
| 🇮🇳 India | Cow slaughter, Religious hatred | No alcohol/tobacco ads | Grievance officer | HIGH |
| 🇯🇵 Japan | None (relatively free) | Public gambling only | Personal data protection | LOW |

---

## 🔬 Research Application (EB1 Contribution)

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

## 🛠️ Future Enhancements

- [ ] **AI-Powered Context Analysis**: Use LLMs to detect nuanced cultural violations
- [ ] **Real-time Policy Updates**: Auto-sync with government APIs for law changes
- [ ] **Dashboard Visualization**: Web UI for compliance monitoring
- [ ] **Multi-language Support**: Detect violations in non-English content
- [ ] **Blockchain Audit Trail**: Immutable compliance verification logs
- [ ] **API Integration**: REST API for CI/CD pipeline integration

---

## 📚 Documentation

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

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-country-policy`)
3. Commit your changes (`git commit -m 'Add policy for Brazil'`)
4. Push to the branch (`git push origin feature/new-country-policy`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**[Your Name]**  
- 🎓 Master of Science in Software Management (MSSM)
- 💼 10+ years experience in Smart TV / OTT platforms
- 🌐 Specialization: Global content compliance & regulatory technology

---

## 🙏 Acknowledgments

- Research inspired by real-world challenges in global OTT expansion
- Policy data compiled from official government sources and industry best practices
- Built with the goal of contributing to digital media governance standards

---

## 📞 Contact

For questions, suggestions, or collaboration opportunities:
- 📧 Email: [your-email@example.com]
- 💼 LinkedIn: [Your LinkedIn Profile]
- 🐙 GitHub: [@deokhwajeong](https://github.com/deokhwajeong)

---

**⭐ If this project helps your research or work, please consider starring the repository!**
