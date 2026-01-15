#!/bin/bash
# systemd Service Installation Script
set -e
echo "======================================"
echo "Policy Guardrail Service Installation"
echo "======================================"
echo ""
# Check current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
echo "Project directory: $PROJECT_ROOT"
echo ""
# Create necessary directories
echo "Creating necessary directories..."
mkdir -p "$PROJECT_ROOT/reports/scheduler_logs"
mkdir -p "$PROJECT_ROOT/reports/source_hashes"
mkdir -p "$PROJECT_ROOT/reports/change_history"
# Python
echo "Installing Python dependencies..."
pip3 install -r "$PROJECT_ROOT/requirements.txt"
# Check .env file
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "WARNING: .env file not found!"
    echo "Copying .env.example to .env..."
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo "Please edit .env file with your configuration"
fi
# systemd
echo "Installing systemd service..."
sudo cp "$SCRIPT_DIR/policy-guardrail.service" /etc/systemd/system/
sudo sed -i "s|/workspaces/Glocal-Policy-Guardrail|$PROJECT_ROOT|g" /etc/systemd/system/policy-guardrail.service
# systemd
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload
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
