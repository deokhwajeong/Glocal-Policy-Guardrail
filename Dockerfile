FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 필요한 디렉토리 생성
RUN mkdir -p reports/scheduler_logs \
    reports/source_hashes \
    reports/change_history \
    config

# 환경변수 설정
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Seoul

# 스크립트 실행 권한 부여
RUN chmod +x deployment/*.sh

# 헬스체크
HEALTHCHECK --interval=1h --timeout=10s --start-period=5m --retries=3 \
    CMD python3 -c "import os; exit(0 if os.path.exists('reports/scheduler_logs') else 1)"

# 데이터 볼륨
VOLUME ["/app/reports", "/app/config"]

# 포트 노출 (웹 대시보드용)
EXPOSE 5000

# 기본 명령: 스케줄러 실행
CMD ["python3", "src/auto_scheduler.py", "--daemon"]
