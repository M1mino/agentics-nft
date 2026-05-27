"""Make a collage of all 31 agent NFT images, grouped by rarity"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

IMAGES_DIR = Path("/root/.openclaw/workspace/nft-ai-agents/images")
OUTPUT = "/root/.openclaw/workspace/nft-ai-agents/miniapp/assets/collage.png"

RARITY_ORDER = ["Legendary", "Epic", "Rare", "Common"]
RARITY_COLORS = {"Legendary": (212, 168, 67), "Epic": (138, 92, 245),
                 "Rare": (41, 182, 246), "Common": (140, 140, 140)}

# Map from filename base to (name, rarity)
CHARACTERS = {
    "mentor-01": ("Mentor-01", "Legendary"), "maverick-x7": ("Maverick-X7", "Legendary"),
    "seer-0mega": ("Seer-0mega", "Legendary"),
    "sage-core": ("Sage-Core", "Epic"), "striker": ("Striker", "Epic"),
    "dream-weaver": ("Dream-Weaver", "Epic"), "jester-bit": ("Jester-Bit", "Epic"),
    "vanta": ("Vanta", "Epic"),
    "logician": ("Logician", "Rare"), "volt": ("Volt", "Rare"), "pixel": ("Pixel", "Rare"),
    "forge-9": ("Forge-9", "Rare"), "anvil": ("Anvil", "Rare"), "giggles": ("Giggles", "Rare"),
    "shade": ("Shade", "Rare"), "nocturne": ("Nocturne", "Rare"), "riot": ("Riot", "Rare"),
    "old-tin": ("Old-Tin", "Common"), "echo": ("Echo", "Common"), "spark": ("Spark", "Common"),
    "zest": ("Zest", "Common"), "doodle": ("Doodle", "Common"), "flux": ("Flux", "Common"),
    "rusty": ("Rusty", "Common"), "grit": ("Grit", "Common"), "cog": ("Cog", "Common"),
    "bounce": ("Bounce", "Common"), "wacko": ("Wacko", "Common"), "noodle": ("Noodle", "Common"),
    "murmur": ("Murmur", "Common"), "bot-0": ("Bot-0", "Common"),
}

# Group by rarity
groups = {r: [] for r in RARITY_ORDER}
for fname, (name, rarity) in CHARACTERS.items():
    path = IMAGES_DIR / f"{fname}.png"
    if path.exists():
        groups[rarity].append((name, path))

# Layout: 4 rows (one per rarity), variable columns
cols = 8  # max columns
cell = 140
padding = 6
header = 30
margin = 16

total_width = cols * cell + (cols - 1) * padding + margin * 2

for rarity in RARITY_ORDER:
    count = len(groups[rarity])
    
print(f"Layout: {[(r, len(groups[r])) for r in RARITY_ORDER]}")

# Build image
rows_data = []
max_row_h = 0

for rarity in RARITY_ORDER:
    items = groups[rarity]
    if not items:
        continue
    n = len(items)
    ncols = min(cols, n)
    nrows = (n + ncols - 1) // ncols
    actual_cols = min(cols, n)
    row_w = actual_cols * cell + (actual_cols - 1) * padding
    row_h = nrows * cell + (nrows - 1) * padding + header
    rows_data.append((rarity, items, actual_cols, nrows, row_w, row_h))
    max_row_h = max(max_row_h, row_h)

total_w = cols * cell + (cols - 1) * padding + margin * 2
total_h = sum(r[5] for r in rows_data) + margin * 2 + (len(rows_data) - 1) * 8

img = Image.new('RGBA', (total_w, total_h), (10, 10, 26, 255))
draw = ImageDraw.Draw(img)

try:
    font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
except:
    font_name = ImageFont.load_default()
    font_small = font_name

y = margin
for rarity, items, ncols, nrows, row_w, row_h in rows_data:
    # Rarity header
    color = RARITY_COLORS[rarity]
    draw.text((margin, y), f"◆ {rarity.upper()}", fill=(*color, 255), font=font_name)
    y += header
    
    x_start = margin + (total_w - margin * 2 - ncols * cell - (ncols - 1) * padding) // 2
    
    x = x_start
    for idx, (name, path) in enumerate(items):
        try:
            icon = Image.open(path).convert("RGBA")
            icon = icon.resize((cell, cell), Image.LANCZOS)
            img.paste(icon, (x, y), icon)
        except:
            draw.rectangle([x, y, x+cell, y+cell], fill=(30, 30, 60))
        
        # Name below
        draw.text((x + cell//2, y + cell + 2), name, fill=(200, 200, 200, 200), font=font_small, anchor="mt")
        
        x += cell + padding
        if (idx + 1) % ncols == 0 and idx + 1 < len(items):
            x = x_start
            y += cell + padding
    
    y += cell + padding + 20

img.save(OUTPUT)
print(f"✅ Collage saved: {OUTPUT} ({img.size})")
