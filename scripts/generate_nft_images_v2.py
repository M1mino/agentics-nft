#!/usr/bin/env python3
"""Generate 1000 NFT images from agent icons + metadata."""

import json
import os
from PIL import Image, ImageDraw, ImageFont

# Config
ICON_DIR = "images"
OUT_DIR = "images/nft"
MAPPING_FILE = "scripts/nft_mapping.json"
METADATA_DIR = "metadata/nfts"
OUT_SIZE = 768  # keep original icon size

# Rarity colors
RARITY = {
    3: {"name": "Legendary", "color": "#FFD700", "glow": "#B8860B"},
    2: {"name": "Epic", "color": "#9B59B6", "glow": "#6C3483"},
    1: {"name": "Rare", "color": "#3498DB", "glow": "#1A5276"},
    0: {"name": "Common", "color": "#95A5A6", "glow": "#566573"},
}

def load_nft_mapping():
    """Load NFT ID → agent name mapping"""
    with open(MAPPING_FILE) as f:
        return json.load(f)

def get_nft_rarity(nft_id):
    """Get rarity from metadata attributes"""
    meta_file = os.path.join(METADATA_DIR, f"{nft_id}.json")
    if not os.path.exists(meta_file):
        return 0  # default common
    with open(meta_file) as f:
        meta = json.load(f)
    for attr in meta.get("attributes", []):
        if attr.get("trait_type") == "Rarity":
            rarity_map = {"Legendary": 3, "Epic": 2, "Rare": 1, "Common": 0}
            return rarity_map.get(attr["value"], 0)
    return 0

def get_agent_icon(agent_name):
    """Load agent icon PNG"""
    # Normalize: nft_mapping has "Mentor-01" → file "mentor-01.png"
    fname = agent_name.lower().replace(" ", "-") + ".png"
    path = os.path.join(ICON_DIR, fname)
    if os.path.exists(path):
        return Image.open(path).convert("RGBA")
    # Try direct match
    path2 = os.path.join(ICON_DIR, agent_name + ".png")
    if os.path.exists(path2):
        return Image.open(path2).convert("RGBA")
    return None

def create_nft_image(nft_id, agent_name, rarity_tier):
    """Create a composited NFT image with agent icon + rarity frame"""
    w, h = OUT_SIZE, OUT_SIZE
    
    # Load agent icon
    icon = get_agent_icon(agent_name)
    if icon is None:
        print(f"  ⚠️ No icon for {agent_name}, skipping #{nft_id}")
        return None
    
    rarity = RARITY[rarity_tier]
    
    # Create canvas
    img = Image.new("RGBA", (w, h), (20, 20, 30, 255))
    draw = ImageDraw.Draw(img)
    
    # Rarity glow border (gradient-like by drawing multiple rectangles)
    border_w = 12
    for i in range(border_w, 0, -1):
        alpha = int(30 + (border_w - i) * 15)  # 30..210
        try:
            r, g, b = tuple(int(rarity["glow"].lstrip("#")[j:j+2], 16) for j in (0, 2, 4))
            draw.rectangle(
                [i, i, w-i-1, h-i-1],
                outline=(r, g, b, alpha),
                width=1
            )
        except:
            pass
    
    # Inner ring
    inner_color = tuple(int(rarity["color"].lstrip("#")[j:j+2], 16) for j in (0, 2, 4))
    draw.rectangle([border_w, border_w, w-border_w-1, h-border_w-1], 
                   outline=(*inner_color, 60), width=2)
    
    # Place icon (centered, at 80% size)
    icon_size = int(w * 0.8)
    icon_resized = icon.resize((icon_size, icon_size), Image.LANCZOS)
    x_offset = (w - icon_size) // 2
    y_offset = (h - icon_size) // 2
    img.paste(icon_resized, (x_offset, y_offset), icon_resized)
    
    # Load font
    try:
        font_num = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_rarity = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_num = ImageFont.load_default()
        font_name = ImageFont.load_default()
        font_rarity = ImageFont.load_default()
    
    # Bottom bar — semi-transparent
    draw.rectangle([0, h-80, w, h], fill=(0, 0, 0, 160))
    
    # NFT number
    draw.text((w//2, h-70), f"#{nft_id}", fill=(255, 255, 255, 220),
              anchor="mt", font=font_num)
    
    # Agent name
    draw.text((w//2, h-40), agent_name, fill=(*inner_color, 220),
              anchor="mt", font=font_name)
    
    # Rarity badge — top right
    badge_w, badge_h = 130, 32
    bx, by = w - badge_w - 15, 15
    draw.rounded_rectangle([bx, by, bx+badge_w, by+badge_h], radius=8,
                           fill=(*inner_color, 180))
    draw.text((bx + badge_w//2, by + badge_h//2), rarity["name"],
              fill=(255, 255, 255, 230), anchor="mm", font=font_rarity)
    
    # Watermark/social
    draw.text((15, h-25), "@agenticsai", fill=(255, 255, 255, 80), font=font_rarity)
    
    return img

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    mapping = load_nft_mapping()
    total = len(mapping)
    
    print(f"🎨 Generating {total} NFT images...")
    print(f"   Icons: {ICON_DIR}/")
    print(f"   Output: {OUT_DIR}/")
    print()
    
    success = 0
    errors = 0
    
    # Sort by NFT ID for consistent output
    nft_ids = sorted(mapping.keys(), key=int)
    
    for i, nft_id in enumerate(nft_ids):
        agent_name = mapping[nft_id]
        rarity_tier = get_nft_rarity(nft_id)
        
        img = create_nft_image(nft_id, agent_name, rarity_tier)
        if img is None:
            errors += 1
            continue
        
        out_path = os.path.join(OUT_DIR, f"{nft_id}.png")
        img.save(out_path, "PNG")
        success += 1
        
        if (i+1) % 100 == 0:
            print(f"  ✅ {i+1}/{total} — {success} generated")
    
    print(f"\n{'='*40}")
    print(f"✅ Done: {success}/{total} images generated")
    print(f"❌ Errors: {errors}")
    print(f"📁 Output: {OUT_DIR}/")

if __name__ == "__main__":
    main()
