#!/usr/bin/env python3
"""
Glocal Policy Guardrail - Quick Start Server
Run this script to start the API server quickly
"""
import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

if __name__ == "__main__":
    import uvicorn
    from glocal_guardrail.api import app
    
    # Get configuration from environment or use defaults
    host = os.getenv("GUARDRAIL_HOST", "127.0.0.1")
    port = int(os.getenv("GUARDRAIL_PORT", "8000"))
    
    print("=" * 60)
    print("Glocal Policy Guardrail API Server")
    print("=" * 60)
    print(f"Starting server on http://{host}:{port}")
    print(f"\nAPI Documentation: http://{host}:{port}/docs")
    print(f"OpenAPI Schema: http://{host}:{port}/openapi.json")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60 + "\n")
    
    uvicorn.run(app, host=host, port=port, log_level="info")
