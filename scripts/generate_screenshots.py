#!/usr/bin/env python3
"""
Generate screenshots for README documentation
"""
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

async def generate_screenshots():
    """Generate screenshots using playwright"""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Installing playwright...")
        os.system("pip install playwright")
        os.system("playwright install chromium")
        from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1600, 'height': 900})
        
        # Wait for server to be ready
        await asyncio.sleep(3)
        
        # Screenshot 1: Dashboard
        print("📸 Capturing dashboard screenshot...")
        try:
            await page.goto('http://localhost:5000/', timeout=10000)
            await page.wait_for_load_state('networkidle', timeout=10000)
            await page.screenshot(path='docs/images/dashboard.png', full_page=True)
            print("✅ Dashboard screenshot saved")
        except Exception as e:
            print(f"❌ Dashboard screenshot failed: {e}")
        
        # Screenshot 2: Swagger UI
        print("📸 Capturing Swagger UI screenshot...")
        try:
            await page.goto('http://localhost:5000/api/docs/', timeout=10000)
            await page.wait_for_load_state('networkidle', timeout=10000)
            await asyncio.sleep(2)  # Wait for Swagger UI to render
            await page.screenshot(path='docs/images/swagger-ui.png', full_page=True)
            print("✅ Swagger UI screenshot saved")
        except Exception as e:
            print(f"❌ Swagger UI screenshot failed: {e}")
        
        # Screenshot 3: API Status
        print("📸 Capturing API response screenshot...")
        try:
            await page.goto('http://localhost:5000/api/status', timeout=10000)
            await page.wait_for_load_state('networkidle', timeout=10000)
            await page.screenshot(path='docs/images/compliance-report.png')
            print("✅ API response screenshot saved")
        except Exception as e:
            print(f"❌ API response screenshot failed: {e}")
        
        await browser.close()
        print("\n🎉 All screenshots generated successfully!")

if __name__ == '__main__':
    asyncio.run(generate_screenshots())
