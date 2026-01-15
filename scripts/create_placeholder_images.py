#!/usr/bin/env python3
"""
Create placeholder images for README documentation
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(filename, title, width=1600, height=900):
    """Create a placeholder image with text"""
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='#1a1b26')
    draw = ImageDraw.Draw(img)
    
    # Add gradient effect
    for y in range(height):
        r = int(26 + (89 - 26) * y / height)
        g = int(27 + (164 - 27) * y / height)
        b = int(38 + (218 - 38) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add title text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw centered title
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 50
    
    # Draw shadow
    draw.text((x + 4, y + 4), title, font=font, fill='#000000')
    # Draw text
    draw.text((x, y), title, font=font, fill='#7aa2f7')
    
    # Add subtitle
    subtitle = "Glocal Policy Guardrail"
    bbox = draw.textbbox((0, 0), subtitle, font=small_font)
    sub_width = bbox[2] - bbox[0]
    sub_x = (width - sub_width) // 2
    sub_y = y + text_height + 30
    draw.text((sub_x, sub_y), subtitle, font=small_font, fill='#9ece6a')
    
    # Add instruction at bottom
    instruction = f"Run 'python web_dashboard.py' to see the live {title.lower()}"
    bbox = draw.textbbox((0, 0), instruction, font=small_font)
    inst_width = bbox[2] - bbox[0]
    inst_x = (width - inst_width) // 2
    inst_y = height - 100
    draw.text((inst_x, inst_y), instruction, font=small_font, fill='#bb9af7')
    
    # Save image
    os.makedirs('docs/images', exist_ok=True)
    img.save(f'docs/images/{filename}')
    print(f"✅ Created: docs/images/{filename}")

if __name__ == '__main__':
    create_placeholder('dashboard.png', 'Web Dashboard UI')
    create_placeholder('swagger-ui.png', 'Swagger API Docs')
    print("\n📸 Placeholder images created successfully!")
    print("💡 To replace with real screenshots:")
    print("   1. Run: python web_dashboard.py")
    print("   2. Take screenshots at http://localhost:5000")
    print("   3. Save them as docs/images/dashboard.png and docs/images/swagger-ui.png")
