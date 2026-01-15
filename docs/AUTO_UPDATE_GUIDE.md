# 자동 규제 업데이트 시스템 가이드

국가별 규제사항을 항상 최신으로 유지하는 완전 자동화 시스템입니다.

## 📋 목차

1. [시스템 개요](#시스템-개요)
2. [주요 기능](#주요-기능)
3. [빠른 시작](#빠른-시작)
4. [배포 방법](#배포-방법)
5. [설정 가이드](#설정-가이드)
6. [사용 방법](#사용-방법)
7. [모니터링](#모니터링)

## 🎯 시스템 개요

이 시스템은 다음 국가들의 규제를 자동으로 모니터링합니다:
- 🇺🇸 미국 (FCC, FTC)
- 🇰🇷 한국 (방송통신심의위원회, 개인정보보호위원회)
- 🇩🇪 독일 (BfDI, KJM)
- 🇪🇺 유럽연합 (EDPB)
- 🇪🇸 스페인 (DGOJ, AEPD)
- 🇨🇳 중국 (국가광전총국)
- 🇸🇦 사우디아라비아 (GCAM)
- 🇮🇳 인도 (MIB)
- 🇯🇵 일본

## ✨ 주요 기능

### 1. 자동 모니터링
- **일일 체크**: 매일 오전 9시 (KST) 실행
- **주간 체크**: 매주 월요일 오전 10시 실행
- **월간 체크**: 매월 1일 오전 11시 실행

### 2. 스마트 변경 감지
- RSS 피드 자동 파싱
- 웹사이트 콘텐츠 스크래핑 (BeautifulSoup4)
- API 엔드포인트 모니터링
- 해시 기반 변경 감지

### 3. 알림 시스템
- **이메일**: SMTP를 통한 이메일 알림
- **Slack**: Webhook을 통한 실시간 알림
- **Discord**: Webhook을 통한 실시간 알림

### 4. 변경사항 추적
- 모든 변경사항 기록 및 히스토리 관리
- 버전별 스냅샷 저장
- 승인 워크플로우
- 변경사항 비교 (diff)

### 5. 24/7 운영
- systemd 서비스로 실행
- Docker 컨테이너로 실행
- 자동 재시작 및 오류 복구

## 🚀 빠른 시작

### 사전 요구사항
```bash
# Python 3.11 이상
python3 --version

# pip 설치 확인
pip3 --version
```

### 1단계: 의존성 설치
```bash
cd /workspaces/Glocal-Policy-Guardrail
pip3 install -r requirements.txt
```

### 2단계: 환경 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (이메일, Slack, Discord 설정)
nano .env
```

### 3단계: 알림 설정
```bash
# config/notifications.yaml 편집
nano config/notifications.yaml

# 사용할 알림 채널을 enabled: true로 설정
```

### 4단계: 테스트 실행
```bash
# 즉시 업데이트 체크 (테스트)
python3 src/auto_scheduler.py --daily
```

## 📦 배포 방법

### 방법 1: systemd 서비스 (Linux 서버)

```bash
# 설치 스크립트 실행
sudo bash deployment/install_service.sh

# 서비스 시작
sudo systemctl start policy-guardrail

# 서비스 상태 확인
sudo systemctl status policy-guardrail

# 로그 보기
sudo journalctl -u policy-guardrail -f
```

### 방법 2: Docker (권장)

```bash
# Docker Compose로 실행
bash deployment/docker_deploy.sh

# 또는 수동으로 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f policy-guardrail

# 상태 확인
docker-compose ps
```

### 방법 3: 수동 실행 (개발/테스트)

```bash
# 백그라운드로 실행
nohup python3 src/auto_scheduler.py --daemon > logs/scheduler.log 2>&1 &

# 프로세스 확인
ps aux | grep auto_scheduler
```

## ⚙️ 설정 가이드

### 규제 소스 추가 ([config/regulatory_sources.yaml](config/regulatory_sources.yaml))

```yaml
sources:
  - country: "Country_Name"
    name: "Source Name"
    url: "https://example.com/news"
    method: "rss"  # 또는 "scrape", "api"
    language: "en"
    check_frequency: "daily"  # 또는 "weekly", "monthly"
```

### 알림 설정 ([config/notifications.yaml](config/notifications.yaml))

#### 이메일 설정
```yaml
email:
  enabled: true
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender: "your-email@gmail.com"
  password: "your-app-password"
  recipients:
    - "admin@example.com"
```

**Gmail 앱 비밀번호 생성 방법:**
1. Google 계정 설정 → 보안
2. 2단계 인증 활성화
3. 앱 비밀번호 생성
4. 생성된 비밀번호를 .env 파일에 입력

#### Slack 설정
```yaml
slack:
  enabled: true
  webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

**Slack Webhook 생성 방법:**
1. Slack 워크스페이스 → Apps & integrations
2. "Incoming Webhooks" 검색
3. Add to Slack
4. 채널 선택 및 Webhook URL 복사

#### Discord 설정
```yaml
discord:
  enabled: true
  webhook_url: "https://discord.com/api/webhooks/YOUR/WEBHOOK/URL"
```

**Discord Webhook 생성 방법:**
1. Discord 서버 설정 → 연동
2. Webhooks 메뉴
3. 새 Webhook 생성
4. Webhook URL 복사

## 📖 사용 방법

### 수동 업데이트 체크

```bash
# 일일 소스 체크
python3 src/auto_scheduler.py --daily

# 주간 소스 체크
python3 src/auto_scheduler.py --weekly

# 월간 소스 체크
python3 src/auto_scheduler.py --monthly

# 테스트 실행
python3 src/auto_scheduler.py --test
```

### 변경사항 검토

```bash
# 대기 중인 변경사항 확인
python3 src/change_tracker.py --review

# 대화형 검토 모드
python3 src/change_tracker.py --interactive

# 변경사항 리포트 (최근 30일)
python3 src/change_tracker.py --report 30

# 버전 스냅샷 생성
python3 src/change_tracker.py --snapshot
```

### 알림 테스트

```bash
# 알림 시스템 테스트
python3 src/notification_system.py
```

## 📊 모니터링

### 로그 위치

```bash
# 스케줄러 로그
reports/scheduler_logs/

# systemd 로그
sudo journalctl -u policy-guardrail -f

# Docker 로그
docker-compose logs -f policy-guardrail
```

### 리포트 파일

```bash
# 업데이트 로그
reports/policy_updates.json

# 변경사항 기록
reports/change_history/changes.json

# 버전 히스토리
reports/change_history/versions.json

# 소스 해시
reports/source_hashes/
```

### 상태 확인

```bash
# systemd 서비스 상태
sudo systemctl status policy-guardrail

# Docker 컨테이너 상태
docker-compose ps

# 프로세스 확인
ps aux | grep auto_scheduler
```

## 🔧 문제 해결

### 스케줄러가 실행되지 않는 경우

```bash
# 로그 확인
tail -f reports/scheduler_logs/*.log

# Python 경로 확인
which python3

# 의존성 재설치
pip3 install -r requirements.txt --force-reinstall
```

### 알림이 전송되지 않는 경우

```bash
# 알림 설정 확인
cat config/notifications.yaml

# .env 파일 확인
cat .env

# 수동 테스트
python3 src/notification_system.py
```

### 웹사이트 스크래핑 실패

```bash
# User-Agent 헤더 확인
# src/policy_auto_updater.py의 _check_website 함수 참조

# 타임아웃 설정 조정
# requests.get(..., timeout=30)
```

## 🔐 보안 고려사항

1. **.env 파일 보호**
   ```bash
   chmod 600 .env
   # .env 파일을 .gitignore에 추가
   ```

2. **API 키 관리**
   - 환경변수 사용
   - AWS Secrets Manager / Azure Key Vault 사용 권장

3. **네트워크 보안**
   - HTTPS 사용
   - VPN 환경에서 실행 (중국 등)

## 📈 향후 개선사항

- [ ] AI/LLM 기반 규제 변경사항 자동 분석
- [ ] 다국어 번역 자동화
- [ ] 웹 대시보드 UI 개선
- [ ] GraphQL API 제공
- [ ] 규제 영향도 자동 평가
- [ ] A/B 테스트 기반 정책 최적화

## 🤝 기여

이슈 및 개선 제안은 GitHub Issues에 등록해주세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

---

**문의사항**: 프로젝트 관리자에게 문의하세요.
