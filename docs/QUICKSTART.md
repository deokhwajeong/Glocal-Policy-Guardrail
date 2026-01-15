# Quick Start Guide - Glocal Policy Guardrail
## 🚀 Quick Start (Run in 5 Minutes)
### Step 1: Environment Setup
```bash
# Clone repository
git clone https://github.com/deokhwajeong/Glocal-Policy-Guardrail.git
cd Glocal-Policy-Guardrail
pip install -r requirements.txt
```
### 2:
```bash
python main.py
```
** :**
```
╔══════════════════════════════════════════════════════════════════════╗
║  🌍 GLOCAL POLICY GUARDRAIL - COMPLIANCE SCANNER                     ║
╚══════════════════════════════════════════════════════════════════════╝
✅ Policy Database Loaded Successfully
   Supported Countries: Saudi_Arabia, Spain, South_Korea, United_States, ...
🧪 Test Case: test_case_1
...
📊 FINAL TEST SUMMARY
Total Tests: 10
✅ Passed: 7
Success Rate: 70.0%
```
### 3:
```bash
python main.py --interactive
```
---
## 💡
### Python
```python
from src.compliance_scanner import ComplianceGuardrail
guardrail = ComplianceGuardrail()
my_content = {
    'title': ' ',
    'description': '   ',
    'genre': 'Sports',
    'tags': ['poker', 'gambling'],
    'features': []
}
# Saudi Arabia
result = guardrail.check_deployment('Saudi_Arabia', my_content)
print(result)
# 🔴 CRITICAL: Found 2 violation(s) in Saudi_Arabia
#   1. [CRITICAL] FORBIDDEN_KEYWORD: Forbidden keyword 'poker' detected
```
---
## 📋
### 1.
`test_data/my_test.yaml`  :
```yaml
my_custom_test:
  country: "South_Korea"
  content_metadata:
    title: " "
    description: " "
    genre: "Drama"
    tags: ["drama"]
    age_rating_system: "KMRB"
    age_rating: "15"
    features: ["real_name_verification", "youth_protection_system", "korean_subtitle_availability"]
  expected_result: "PASS"
```
### 2.
```python
test_cases = load_test_cases("test_data/my_test.yaml")
```
---
## 🌍
### `config/policy_rules.yaml` :
```yaml
Brazil:
  country_name: ""
  region: "South America"
  forbidden_keywords:
    - "illegal_gambling"
    - "drug_trafficking"
  ad_restrictions:
    gambling_ads: "restricted_to_licensed_entities"
    alcohol_ads:
      restriction_type: "content_warning"
      required_disclaimer: "Beba com moderação"
  age_rating_system: "DEJUS"
  mandatory_compliance:
    - "lgpd_compliance"  # Lei Geral de Proteção de Dados
  violation_severity: "MEDIUM"
```
### :
```python
result = guardrail.check_deployment('Brazil', my_content)
```
---
## 📊
###  JSON  :
```bash
cat reports/compliance_report.json
python -m json.tool reports/compliance_report.json
```
###  :
```json
{
  "generated_at": "2026-01-13T01:29:11",
  "total_deployments": 10,
  "results": [
    {
      "status": "CRITICAL",
      "country": "Saudi_Arabia",
      "violation_count": 6,
      "violations": [...]
    }
  ]
}
```
---
## 🔧
### 1.
```python
from datetime import datetime
#   2   ()
ad_schedule = {
    'ad_type': 'gambling_ads',
    'scheduled_time': '2026-01-13T02:00:00'
}
result = guardrail.check_deployment(
    'Spain',
    content_metadata,
    ad_schedule=ad_schedule,
    current_time=datetime(2026, 1, 13, 2, 0, 0)
)
# PASS
```
### 2.
```python
deployments = [
    {'country': 'USA', 'content_metadata': content1},
    {'country': 'Germany', 'content_metadata': content2},
    {'country': 'Japan', 'content_metadata': content3}
]
results = guardrail.batch_check(deployments)
report = guardrail.generate_compliance_report(results)
print(report)
```
### 3.
```python
from src.analytics import generate_full_analytics_report
analytics_report = generate_full_analytics_report(results)
print(analytics_report)
```
---
## 🐛
### : "Policy database not found"
**:**
```bash
# Check current directory
pwd
# config
ls config/
python -c "from src.compliance_scanner import ComplianceGuardrail; g = ComplianceGuardrail()"
```
### : "YAML  "
**:**
```bash
# YAML
python -c "import yaml; yaml.safe_load(open('config/policy_rules.yaml'))"
```
---
## 📈
1. **CI/CD **: GitHub Actions
2. ** **: Flask/Django
3. **API **: REST API
4. **AI **: LLM
---
## 💬
- 📧 : [your-email]
- 💼  : https://github.com/deokhwajeong/Glocal-Policy-Guardrail/issues
- 📚  : [README.md](README.md)
**Happy Coding! 🚀**
