#!/usr/bin/env python3
"""
Create realistic dashboard screenshot images using PIL
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_realistic_dashboard(filename='dashboard.png', width=1600, height=1400):
    """Create a realistic dashboard image"""
    # Create image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        heading_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        title_font = heading_font = normal_font = small_font = ImageFont.load_default()
    
    y_offset = 0
    
    # Header with gradient
    for y in range(120):
        r = int(30 + (42 - 30) * y / 120)
        g = int(60 + (82 - 60) * y / 120)
        b = int(114 + (152 - 114) * y / 120)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
    
    # Header text
    draw.text((width//2 - 250, 30), "🌍 Glocal Policy Guardrail", font=title_font, fill='white')
    draw.text((width//2 - 200, 80), "Real-time Compliance Monitoring Dashboard", font=small_font, fill='#e0e0e0')
    y_offset = 120
    
    # Stats cards
    card_y = y_offset + 30
    card_width = 350
    card_height = 120
    gap = 30
    cards = [
        ("15", "Countries Monitored", (72, 187, 120)),
        ("3", "Critical Violations", (245, 101, 101)),
        ("127", "Active Rules", (237, 137, 54)),
        ("70%", "Compliance Rate", (72, 187, 120))
    ]
    
    x_start = 50
    for i, (value, label, color) in enumerate(cards):
        x = x_start + (card_width + gap) * i
        # Card background
        draw.rectangle([(x, card_y), (x + card_width, card_y + card_height)], fill='white', outline='#e0e0e0', width=2)
        # Left border
        draw.rectangle([(x, card_y), (x + 5, card_y + card_height)], fill=color)
        # Value
        draw.text((x + 20, card_y + 20), value, font=title_font, fill='#2d3748')
        # Label
        draw.text((x + 20, card_y + 75), label, font=small_font, fill='#718096')
    
    y_offset = card_y + card_height + 50
    
    # Section: Recent Compliance Checks
    draw.text((50, y_offset), "Recent Compliance Checks", font=heading_font, fill='#2d3748')
    draw.rectangle([(50, y_offset + 40), (width - 50, y_offset + 42)], fill='#667eea')
    y_offset += 60
    
    # Table header
    table_y = y_offset
    draw.rectangle([(50, table_y), (width - 50, table_y + 40)], fill='#4a5568')
    headers = [("Content ID", 70), ("Title", 250), ("Country", 500), ("Status", 700), ("Violations", 900), ("Timestamp", 1050)]
    for header, x_pos in headers:
        draw.text((x_pos, table_y + 10), header, font=normal_font, fill='white')
    
    # Table rows
    rows = [
        ("SHOW-2024-001", "Vegas Nights", "Saudi Arabia", "CRITICAL", "6", "2026-01-15 14:30"),
        ("MOVIE-2024-078", "Tech Documentary", "United States", "COMPLIANT", "0", "2026-01-15 14:25"),
        ("SHOW-2024-045", "Drama Series", "South Korea", "HIGH", "2", "2026-01-15 14:20"),
        ("MOVIE-2024-091", "Action Film", "Germany", "COMPLIANT", "0", "2026-01-15 14:15"),
        ("SHOW-2024-033", "Reality Show", "Spain", "HIGH", "1", "2026-01-15 14:10"),
    ]
    
    row_y = table_y + 40
    for row_data in rows:
        # Alternate row color
        if rows.index(row_data) % 2 == 0:
            draw.rectangle([(50, row_y), (width - 50, row_y + 40)], fill='#f7fafc')
        else:
            draw.rectangle([(50, row_y), (width - 50, row_y + 40)], fill='white')
        
        # Row data
        content_id, title, country, status, violations, timestamp = row_data
        draw.text((70, row_y + 10), content_id, font=small_font, fill='#2d3748')
        draw.text((250, row_y + 10), title, font=small_font, fill='#2d3748')
        draw.text((500, row_y + 10), country, font=small_font, fill='#2d3748')
        
        # Status badge
        status_colors = {
            "CRITICAL": ("#fed7d7", "#c53030"),
            "HIGH": ("#feebc8", "#c05621"),
            "COMPLIANT": ("#c6f6d5", "#276749")
        }
        bg, fg = status_colors.get(status, ("#e2e8f0", "#4a5568"))
        badge_x = 700
        draw.rounded_rectangle([(badge_x, row_y + 8), (badge_x + 100, row_y + 32)], radius=12, fill=bg)
        draw.text((badge_x + 10, row_y + 10), status, font=small_font, fill=fg)
        
        draw.text((900, row_y + 10), violations, font=small_font, fill='#2d3748')
        draw.text((1050, row_y + 10), timestamp, font=small_font, fill='#2d3748')
        
        # Border
        draw.line([(50, row_y + 40), (width - 50, row_y + 40)], fill='#e2e8f0', width=1)
        row_y += 40
    
    y_offset = row_y + 40
    
    # Section: Violation Heatmap
    draw.text((50, y_offset), "Violation Heatmap by Country", font=heading_font, fill='#2d3748')
    draw.rectangle([(50, y_offset + 40), (width - 50, y_offset + 42)], fill='#667eea')
    y_offset += 60
    
    # Bar chart
    countries = [
        ("Saudi Arabia", 6, (102, 126, 234)),
        ("South Korea", 2, (246, 173, 85)),
        ("Germany", 2, (246, 173, 85)),
        ("Spain", 1, (251, 211, 141)),
        ("China", 1, (251, 211, 141)),
        ("United States", 0, (154, 230, 180)),
        ("Japan", 0, (154, 230, 180)),
    ]
    
    max_violations = 6
    bar_y = y_offset
    for country, violations, color in countries:
        # Country label
        draw.text((70, bar_y + 5), country, font=normal_font, fill='#4a5568')
        
        # Bar
        bar_width = int((violations / max_violations) * 900) if violations > 0 else 40
        draw.rounded_rectangle([(300, bar_y), (300 + bar_width, bar_y + 30)], radius=5, fill=color)
        
        # Value
        draw.text((310, bar_y + 5), f"{violations} violation{'s' if violations != 1 else ''}", font=normal_font, fill='white')
        
        bar_y += 45
    
    # Save image
    os.makedirs('docs/images', exist_ok=True)
    img.save(f'docs/images/{filename}')
    print(f"✅ Created: docs/images/{filename}")

def create_swagger_ui(filename='swagger-ui.png', width=1600, height=1000):
    """Create a Swagger UI screenshot"""
    img = Image.new('RGB', (width, height), color='#fafafa')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        heading_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        mono_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
    except:
        title_font = heading_font = normal_font = mono_font = ImageFont.load_default()
    
    # Header
    draw.rectangle([(0, 0), (width, 60)], fill='#1b1b1b')
    draw.text((30, 15), "Glocal Policy Guardrail API", font=heading_font, fill='white')
    
    # API Info section
    y = 80
    draw.rectangle([(50, y), (width - 50, y + 150)], fill='white', outline='#e8e8e8', width=1)
    draw.text((70, y + 20), "Glocal Policy Guardrail API", font=title_font, fill='#3b4151')
    draw.text((70, y + 60), "Version 1.0.0", font=normal_font, fill='#89bf04')
    draw.text((70, y + 95), "Policy-as-Code framework for automated compliance verification", font=normal_font, fill='#666')
    draw.text((70, y + 120), "across 15+ countries", font=normal_font, fill='#666')
    
    # Endpoints
    y = 260
    endpoints = [
        ("GET", "/api/status", "Get system status", (97, 175, 254)),
        ("POST", "/api/compliance/scan", "Scan content for compliance", (73, 204, 144)),
        ("GET", "/api/compliance/report", "Get compliance report", (97, 175, 254)),
        ("GET", "/api/regulatory/updates", "Get regulatory updates", (97, 175, 254)),
        ("POST", "/api/regulatory/check", "Check for new regulatory updates", (73, 204, 144)),
        ("GET", "/api/policy/countries", "List all supported countries", (97, 175, 254)),
    ]
    
    for method, path, desc, color in endpoints:
        # Endpoint container
        draw.rectangle([(50, y), (width - 50, y + 60)], fill='white', outline='#e8e8e8', width=1)
        
        # Method badge
        draw.rounded_rectangle([(70, y + 20), (140, y + 42)], radius=3, fill=color)
        draw.text((80, y + 22), method, font=normal_font, fill='white')
        
        # Path
        draw.text((160, y + 22), path, font=mono_font, fill='#3b4151')
        
        # Description
        draw.text((width - 400, y + 22), desc, font=normal_font, fill='#666')
        
        y += 70
    
    # Save image
    os.makedirs('docs/images', exist_ok=True)
    img.save(f'docs/images/{filename}')
    print(f"✅ Created: docs/images/{filename}")

if __name__ == '__main__':
    print("📸 Creating realistic dashboard screenshots...")
    create_realistic_dashboard()
    create_swagger_ui()
    print("\n✨ All screenshots created successfully!")
    print(f"\n👉 View them at:")
    print(f"   - docs/images/dashboard.png")
    print(f"   - docs/images/swagger-ui.png")
