#!/usr/bin/env python3
"""
Capture dashboard screenshot using html2image
"""
from html2image import Html2Image
from pathlib import Path
import time

def capture_dashboard():
    """Capture dashboard HTML as image"""
    hti = Html2Image(output_path='docs/images')
    
    # Read HTML file
    html_path = Path('docs/images/demo_dashboard.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("📸 Capturing dashboard screenshot...")
    
    # Capture screenshot with larger size for better quality
    hti.screenshot(
        html_str=html_content,
        save_as='dashboard.png',
        size=(1600, 1400)
    )
    
    print("✅ Dashboard screenshot saved to docs/images/dashboard.png")
    
    # Create a simpler swagger UI screenshot
    swagger_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #fafafa;
                margin: 0;
                padding: 20px;
            }
            .swagger-container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 4px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            .swagger-header {
                background: #1b1b1b;
                color: white;
                padding: 20px 30px;
                font-size: 1.5em;
            }
            .api-info {
                padding: 30px;
                border-bottom: 1px solid #e8e8e8;
            }
            .api-title {
                font-size: 2em;
                color: #3b4151;
                margin-bottom: 10px;
            }
            .api-version {
                color: #89bf04;
                font-weight: bold;
            }
            .endpoint {
                border: 1px solid #e8e8e8;
                border-radius: 4px;
                margin: 15px 30px;
                overflow: hidden;
            }
            .endpoint-header {
                padding: 15px 20px;
                cursor: pointer;
                display: flex;
                align-items: center;
                background: white;
            }
            .endpoint-header:hover {
                background: #f7f7f7;
            }
            .method {
                font-weight: bold;
                padding: 5px 10px;
                border-radius: 3px;
                margin-right: 15px;
                font-size: 0.9em;
            }
            .method.get {
                background: #61affe;
                color: white;
            }
            .method.post {
                background: #49cc90;
                color: white;
            }
            .endpoint-path {
                font-family: monospace;
                color: #3b4151;
                font-size: 1.1em;
            }
            .endpoint-desc {
                color: #666;
                margin-left: auto;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="swagger-container">
            <div class="swagger-header">
                Glocal Policy Guardrail API
            </div>
            <div class="api-info">
                <div class="api-title">Glocal Policy Guardrail API</div>
                <div class="api-version">Version 1.0.0</div>
                <p style="color: #666; margin-top: 15px;">
                    Policy-as-Code framework for automated compliance verification across 15+ countries
                </p>
            </div>
            
            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-path">/api/status</span>
                    <span class="endpoint-desc">Get system status</span>
                </div>
            </div>
            
            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method post">POST</span>
                    <span class="endpoint-path">/api/compliance/scan</span>
                    <span class="endpoint-desc">Scan content for compliance</span>
                </div>
            </div>
            
            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-path">/api/compliance/report</span>
                    <span class="endpoint-desc">Get compliance report</span>
                </div>
            </div>
            
            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-path">/api/regulatory/updates</span>
                    <span class="endpoint-desc">Get regulatory updates</span>
                </div>
            </div>
            
            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method post">POST</span>
                    <span class="endpoint-path">/api/regulatory/check</span>
                    <span class="endpoint-desc">Check for new regulatory updates</span>
                </div>
            </div>
            
            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-path">/api/policy/countries</span>
                    <span class="endpoint-desc">List all supported countries</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    print("📸 Capturing Swagger UI screenshot...")
    hti.screenshot(
        html_str=swagger_html,
        save_as='swagger-ui.png',
        size=(1600, 1200)
    )
    
    print("✅ Swagger UI screenshot saved to docs/images/swagger-ui.png")
    print("\n✨ All screenshots captured successfully!")

if __name__ == '__main__':
    capture_dashboard()
