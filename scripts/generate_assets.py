"""Generate agentics brand assets: logo, OG preview, banner"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

OUTPUT = "/root/.openclaw/workspace/nft-ai-agents/miniapp/assets"
os.makedirs(OUTPUT, exist_ok=True)

GOLD = (212, 168, 67)
GOLD_LIGHT = (247, 232, 170)
GOLD_DARK = (184, 134, 45)
DARK = (10, 10, 26)
DARK2 = (18, 18, 42)

def draw_robot(draw, cx, cy, size, color=GOLD, alpha=255):
    """Draw a simple robot face"""
    half = size // 2
    fill = (color[0], color[1], color[2], min(255, alpha))
    # Head
    draw.rounded_rectangle([cx-half, cy-half, cx+half, cy+half], radius=size//4, fill=fill)
    # Eyes
    eye_r = max(2, size // 14)
    draw.ellipse([cx-size//4-eye_r, cy-size//6-eye_r, cx-size//4+eye_r, cy-size//6+eye_r], fill=(0,0,0,min(255,alpha)))
    draw.ellipse([cx+size//4-eye_r, cy-size//6-eye_r, cx+size//4+eye_r, cy-size//6+eye_r], fill=(0,0,0,min(255,alpha)))
    # Mouth
    mouth_w = size // 3
    mouth_h = max(2, size // 20)
    draw.rectangle([cx-mouth_w//2, cy+size//6, cx+mouth_w//2, cy+size//6+mouth_h], fill=(0,0,0,min(255,alpha)))
    # Antenna
    ant_h = size // 4
    draw.rectangle([cx-2, cy-half-ant_h, cx+2, cy-half], fill=(*color, min(200,alpha)))
    draw.ellipse([cx-4, cy-half-ant_h-4, cx+4, cy-half-ant_h+4], fill=(255, 50, 50, min(255,alpha)))

def make_logo():
    """512x512 app icon"""
    img = Image.new('RGBA', (512, 512), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    # Background circle
    draw.ellipse([10, 10, 502, 502], fill=(*DARK2, 255))
    # Gold ring
    draw.ellipse([20, 20, 492, 492], outline=(*GOLD, 60), width=3)
    # Robot
    draw_robot(draw, 256, 240, 200, GOLD)
    # "A" letter
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
    except:
        font = ImageFont.load_default()
    draw.text((256, 430), "A", fill=(*GOLD_LIGHT, 255), font=font, anchor="mm")
    img.save(f"{OUTPUT}/logo.png")
    print(f"✅ Logo: {OUTPUT}/logo.png ({img.size})")

def make_og_preview():
    """1280x640 OG preview for links"""
    img = Image.new('RGBA', (1280, 640), DARK + (255,))
    draw = ImageDraw.Draw(img)
    # Gradient overlay
    for y in range(640):
        alpha = int(40 * (1 - y/640))
        draw.line([(0, y), (1280, y)], fill=(*GOLD, alpha))
    # Gold line
    draw.rectangle([0, 300, 1280, 304], fill=(*GOLD, 200))
    # Robot row
    positions = [(160, 260), (320, 250), (480, 240), (640, 230), (800, 240), (960, 250), (1120, 260)]
    for i, (x, y) in enumerate(positions):
        size = 60 + (3 - abs(i - 3)) * 15
        draw_robot(draw, x, y, size, GOLD if i in (2,3,4) else GOLD_DARK)
    # Title
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    draw.text((640, 370), "AGENTICS", fill=(*GOLD_LIGHT, 255), font=font_title, anchor="mm")
    draw.text((640, 430), "AI Robot Mascots on TON", fill=(*GOLD, 180), font=font_sub, anchor="mm")
    draw.text((640, 480), "30 unique AI agents — Each with their own personality", fill=(200,200,200,150), font=font_sub, anchor="mm")
    img.save(f"{OUTPUT}/og-preview.png")
    print(f"✅ OG Preview: {OUTPUT}/og-preview.png ({img.size})")

def make_banner():
    """1200x400 collection banner for GetGems"""
    img = Image.new('RGBA', (1200, 400), DARK + (255,))
    draw = ImageDraw.Draw(img)
    # Left: robots group
    positions = [(180, 200), (280, 190), (370, 200)]
    for i, (x, y) in enumerate(positions):
        draw_robot(draw, x, y, 70 + i*10, [GOLD, GOLD, GOLD_DARK][i])
    # Right: text
    try:
        font_t = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        font_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except:
        font_t = ImageFont.load_default()
        font_s = ImageFont.load_default()
    draw.text((600, 120), "AGENTICS", fill=(*GOLD_LIGHT, 255), font=font_t, anchor="mm")
    draw.text((600, 180), "AI Robot Mascots", fill=(*GOLD, 180), font=font_s, anchor="mm")
    draw.text((600, 215), "Collect. Activate. Converse.", fill=(200,200,200,120), font=font_s, anchor="mm")
    # Gold accent line
    draw.rectangle([550, 240, 650, 244], fill=(*GOLD, 200))
    img.save(f"{OUTPUT}/banner.png")
    print(f"✅ Banner: {OUTPUT}/banner.png ({img.size})")

def make_bg_pattern():
    """Background tile for web"""
    img = Image.new('RGBA', (200, 200), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    # Subtle grid dots
    for x in range(0, 200, 20):
        for y in range(0, 200, 20):
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(*GOLD, 8))
    # Small robot silhouette
    draw_robot(draw, 100, 100, 30, GOLD, 15)
    img.save(f"{OUTPUT}/bg-pattern.png")
    print(f"✅ BG Pattern: {OUTPUT}/bg-pattern.png ({img.size})")

if __name__ == "__main__":
    make_logo()
    make_og_preview()
    make_banner()
    make_bg_pattern()
    print("\n🎨 All assets generated!")
