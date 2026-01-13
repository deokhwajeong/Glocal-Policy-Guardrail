# Quick Start Guide - Glocal Policy Guardrail

## 🚀 빠른 시작 (5분 안에 실행하기)

### 1단계: 환경 설정

```bash
# 저장소 클론
git clone https://github.com/deokhwajeong/Glocal-Policy-Guardrail.git
cd Glocal-Policy-Guardrail

# 의존성 설치
pip install -r requirements.txt
```

### 2단계: 첫 번째 테스트 실행

```bash
# 모든 테스트 케이스 실행
python main.py
```

**예상 출력:**
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

### 3단계: 대화형 모드 체험

```bash
# 직접 콘텐츠를 입력하며 테스트
python main.py --interactive
```

---

## 💡 예제 사용법

### Python 코드에서 직접 사용

```python
from src.compliance_scanner import ComplianceGuardrail

# 가드레일 초기화
guardrail = ComplianceGuardrail()

# 콘텐츠 메타데이터 정의
my_content = {
    'title': '포커 토너먼트',
    'description': '세계 최고의 포커 대회',
    'genre': 'Sports',
    'tags': ['poker', 'gambling'],
    'features': []
}

# 사우디아라비아에 배포 가능한지 검사
result = guardrail.check_deployment('Saudi_Arabia', my_content)

print(result)
# 🔴 CRITICAL: Found 2 violation(s) in Saudi_Arabia
#   1. [CRITICAL] FORBIDDEN_KEYWORD: Forbidden keyword 'poker' detected
```

---

## 📋 테스트 케이스 작성하기

### 1. 새로운 테스트 파일 생성

`test_data/my_test.yaml` 파일 생성:

```yaml
my_custom_test:
  country: "South_Korea"
  content_metadata:
    title: "내 드라마"
    description: "재미있는 드라마"
    genre: "Drama"
    tags: ["drama"]
    age_rating_system: "KMRB"
    age_rating: "15"
    features: ["real_name_verification", "youth_protection_system", "korean_subtitle_availability"]
  expected_result: "PASS"
```

### 2. 메인 코드에서 로드

```python
test_cases = load_test_cases("test_data/my_test.yaml")
```

---

## 🌍 새로운 국가 정책 추가하기

### `config/policy_rules.yaml`에 추가:

```yaml
Brazil:
  country_name: "브라질"
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

### 테스트:

```python
result = guardrail.check_deployment('Brazil', my_content)
```

---

## 📊 리포트 분석하기

### 생성된 JSON 리포트 확인:

```bash
# 리포트 보기
cat reports/compliance_report.json

# 예쁘게 포맷팅
python -m json.tool reports/compliance_report.json
```

### 리포트 구조:

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

## 🔧 고급 기능

### 1. 시간대별 광고 검증

```python
from datetime import datetime

# 스페인에서 새벽 2시에 도박 광고 (허용)
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

### 2. 일괄 검사

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

### 3. 분석 리포트 생성

```python
from src.analytics import generate_full_analytics_report

analytics_report = generate_full_analytics_report(results)
print(analytics_report)
```

---

## 🐛 문제 해결

### 문제: "Policy database not found"

**해결책:**
```bash
# 현재 디렉토리 확인
pwd

# config 디렉토리가 있는지 확인
ls config/

# 상대 경로가 맞는지 확인
python -c "from src.compliance_scanner import ComplianceGuardrail; g = ComplianceGuardrail()"
```

### 문제: "YAML 파싱 에러"

**해결책:**
```bash
# YAML 문법 검증
python -c "import yaml; yaml.safe_load(open('config/policy_rules.yaml'))"
```

---

## 📈 다음 단계

1. **CI/CD 통합**: GitHub Actions에 추가하여 자동 검증
2. **웹 대시보드**: Flask/Django로 시각화 대시보드 구축
3. **API 서버**: REST API로 변환하여 마이크로서비스화
4. **AI 확장**: LLM 통합으로 문맥 기반 검증 추가

---

## 💬 도움말

- 📧 이메일: [your-email]
- 💼 이슈 트래커: https://github.com/deokhwajeong/Glocal-Policy-Guardrail/issues
- 📚 전체 문서: [README.md](README.md)

**Happy Coding! 🚀**
