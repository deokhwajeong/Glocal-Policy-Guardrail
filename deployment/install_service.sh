#!/bin/bash
# systemd 서비스 설치 스크립트

set -e

echo "======================================"
echo "Policy Guardrail Service Installation"
echo "======================================"
echo ""

# 현재 디렉토리 확인
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Project directory: $PROJECT_ROOT"
echo ""

# 필요한 디렉토리 생성
echo "Creating necessary directories..."
mkdir -p "$PROJECT_ROOT/reports/scheduler_logs"
mkdir -p "$PROJECT_ROOT/reports/source_hashes"
mkdir -p "$PROJECT_ROOT/reports/change_history"

# Python 의존성 설치
echo "Installing Python dependencies..."
pip3 install -r "$PROJECT_ROOT/requirements.txt"

# .env 파일 확인
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "WARNING: .env file not found!"
    echo "Copying .env.example to .env..."
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo "Please edit .env file with your configuration"
fi

# systemd 서비스 파일 복사
echo "Installing systemd service..."
sudo cp "$SCRIPT_DIR/policy-guardrail.service" /etc/systemd/system/

# 서비스 파일 내 경로 업데이트
sudo sed -i "s|/workspaces/Glocal-Policy-Guardrail|$PROJECT_ROOT|g" /etc/systemd/system/policy-guardrail.service

# systemd 리로드
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# 서비스 활성화
echo "Enabling service..."
sudo systemctl enable policy-guardrail.service

echo ""
echo "======================================"
echo "Installation completed!"
echo "======================================"
echo ""
echo "To start the service:"
echo "  sudo systemctl start policy-guardrail"
echo ""
echo "To check status:"
echo "  sudo systemctl status policy-guardrail"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u policy-guardrail -f"
echo ""
echo "To stop the service:"
echo "  sudo systemctl stop policy-guardrail"
echo ""
