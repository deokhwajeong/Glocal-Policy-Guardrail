#!/bin/bash
# Docker Deployment Script
set -e
echo "======================================"
echo "Policy Guardrail Docker Deployment"
echo "======================================"
echo ""
# Check .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before running!"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit..."
fi
# Check Docker installation
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi
echo "✅ Docker and Docker Compose are installed"
echo ""
echo "Building Docker image..."
docker-compose build
echo ""
echo "======================================"
echo "Deployment Options"
echo "======================================"
echo ""
echo "1. Start scheduler only (background)"
echo "2. Start scheduler + web dashboard"
echo "3. Stop all services"
echo "4. View logs"
echo "5. Restart services"
echo ""
read -p "Select option (1-5): " option
case $option in
    1)
        echo "Starting scheduler..."
        docker-compose up -d policy-guardrail
        echo ""
        echo "✅ Scheduler started in background"
        echo "Check logs: docker-compose logs -f policy-guardrail"
        ;;
    2)
        echo "Starting scheduler and dashboard..."
        docker-compose up -d
        echo ""
        echo "✅ Services started"
        echo "Dashboard available at: http://localhost:5000"
        echo "Check logs: docker-compose logs -f"
        ;;
    3)
        echo "Stopping all services..."
        docker-compose down
        echo "✅ All services stopped"
        ;;
    4)
        docker-compose logs -f
        ;;
    5)
        echo "Restarting services..."
        docker-compose restart
        echo "✅ Services restarted"
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac
echo ""
echo "======================================"
echo "Useful Commands"
echo "======================================"
echo ""
echo "Check status:      docker-compose ps"
echo "View logs:         docker-compose logs -f"
echo "Stop services:     docker-compose down"
echo "Restart:           docker-compose restart"
echo "Rebuild:           docker-compose build --no-cache"
echo ""
