"""NFT Agentics — генерация 31 изображения через Pollinations.ai с градацией по редкости"""

import json, sys, time, requests
from urllib.parse import quote
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"

# Единый шаблон позы/фона/освещения
TEMPLATE = (
    "full body standing front view portrait of a robot mascot, "
    "centered symmetrical composition, arms relaxed at sides, "
    "pure dark gradient background dark grey to black, "
    "single soft key light from front-left, rim light from right, "
    "professional product photography style, clean render, sharp focus, "
    "uniform style across collection"
)

# Модификаторы качества по редкости
RARITY_MOD = {
    "legendary": "gold accents, glowing aura, ornate details, majestic, masterpiece quality",
    "epic": "silver accents, premium build, dramatic lighting, high quality detailed",
    "rare": "steel accents, solid build, industrial lighting, clean design, decent quality",
    "common": "bare metal, minimal details, utilitarian, flat lighting, basic quality",
}

# ─── Персонажи с редкостью и описанием ───
CHARACTERS = [
    # LEGENDARY
    ("Mentor-01", "legendary", "bronze robot with green patina, one large warm amber optical lens eye, old ribbed speaker chest, engraved gears and symbols on body, slightly tilted antenna"),
    ("Maverick-X7", "legendary", "chrome steel robot with red neon stripes, cowboy hat plate on head, face screen with cocky grin, laser cannon replacing one arm"),
    ("Seer-0mega", "legendary", "black titanium tall narrow robot, single red LED strip pulsing on face, faint purple glowing rune cracks, completely motionless"),
    # EPIC
    ("Sage-Core", "epic", "silver server-module robot, two green LED eyes, spinning cooling fan through chest grille, neatly organized wires visible"),
    ("Striker", "epic", "low squat military robot on tracks, matte battle-scarred armor, hydraulic manipulator arms, welded X7 number on bumper"),
    ("Dream-Weaver", "epic", "translucent acrylic robot with rainbow light pulsing inside, constantly changing colors, multiple appendages gesturing excitedly"),
    ("Jester-Bit", "epic", "harlequin-patterned robot with diamond plates, jester hat with blinking lights, trick buttons on chest, mischievous slouched posture"),
    ("Vanta", "epic", "perfectly black matte robot absorbing all light, barely visible outline, thin elegant frame, minimal features, completely silent presence"),
    # RARE
    ("Logician", "rare", "metallic blue robot with clean geometric design, chess-piece inspired head, digital display face showing logical symbols"),
    ("Volt", "rare", "yellow and black striped robot, crackling electricity between antennae, aggressive angular design, lightning bolt patterns on body"),
    ("Pixel", "rare", "blocky retro robot with visible pixel-grid texture, bright primary colors, square CRT screen face, chunky design like 8-bit era"),
    ("Forge-9", "rare", "dark heavy industrial robot with furnace-glow chest, thick armored plating, hammer-like hands, heat-resistant alloy body"),
    ("Anvil", "rare", "massive square-shouldered robot, dark grey industrial metal, thick support legs planted wide, no decoration, pure function"),
    ("Giggles", "rare", "pinkish aluminum robot with rounded edges, smile-shaped speaker on chest, antenna curled as question mark, bouncy posture"),
    ("Shade", "rare", "matte grey robot with smoothed edges, no sharp lines, moves silently, hard to focus eyes on, blends into background"),
    ("Nocturne", "rare", "dark purple robot with gold accents, two narrow vertical LED eyes, gramophone-shaped torso, elegant artistic design"),
    ("Riot", "rare", "welded scrap-metal robot, mismatched parts, peeling paint, graffiti on armor, looks homeless but has hacker antenna array"),
    # COMMON
    ("Old-Tin", "common", "rusty tin can robot on wheels, worn through on sides, squeaky joints, patched holes, looks ready to fall apart but functional"),
    ("Echo", "common", "empty mirror-polished shell robot, completely hollow inside, reflective surface, no visible internal components"),
    ("Spark", "common", "tiny yellow plastic robot with cracks, looks like a toy, one wheel slightly broken, eager posture despite small size"),
    ("Zest", "common", "bright neon orange robot, triangular non-standard body, moves in jerks, unpredictable shape, acid color"),
    ("Doodle", "common", "white robot covered in scribbles and drawings, marker-tip finger, constantly adding new doodles to own body"),
    ("Flux", "common", "liquid mercury-like robot body, constantly shifting shape, no fixed form, flows between solid and fluid states"),
    ("Rusty", "common", "reddish-brown rust covering entire body, one arm held by tape, shuffles, drags right leg, tired worn appearance"),
    ("Grit", "common", "rough unprocessed raw metal robot, no paint or polish, bare functional surface, minimal joints, pure utility"),
    ("Cog", "common", "neat factory-blue robot without flaws, simple working tool design, precise joints, clean uniform color, standard model"),
    ("Bounce", "common", "robot on single spring-leg, constantly bouncing and balancing, never still, pogo-stick body design"),
    ("Wacko", "common", "asymmetrical robot from mismatched colorful parts, one eye larger than other, looks assembled during power failure"),
    ("Noodle", "common", "soft silicone bendy robot, spaghetti-like tentacle arms constantly tangling, relaxed melted posture, no rigid parts"),
    ("Murmur", "common", "unremarkable grey robot blending into any background, barely audible speaker hiss, looks broken at first glance"),
    ("Bot-0", "common", "plain grey robot with no markings or decorations, nothing extra, basic model, reference design, featureless"),
]

def gen(char_name, rarity, desc, path):
    mod = RARITY_MOD[rarity]
    prompt = f"{TEMPLATE}, {desc}, {mod}"
    url = "https://image.pollinations.ai/prompt/" + quote(prompt)
    params = {"width": 1024, "height": 1024, "nologo": "true", "model": "flux"}
    try:
        r = requests.get(url, params=params, timeout=90)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(path, "wb") as f:
                f.write(r.content)
            return len(r.content)
    except:
        pass
    return 0

def main():
    IMAGES_DIR.mkdir(exist_ok=True)
    total = len(CHARACTERS)
    
    print(f"🎨 Генерация {total} изображений\n")
    
    done = 0
    for i, (name, rarity, desc) in enumerate(CHARACTERS, 1):
        slug = name.lower().replace(" ", "-").replace("_", "-")
        path = IMAGES_DIR / f"{slug}.png"
        
        if path.exists() and path.stat().st_size > 1000:
            print(f"[{i}/{total}] ⏭ {name} — уже есть")
            done += 1
            continue
        
        print(f"[{i}/{total}] 🎨 {name} [{rarity}]...", end=" ", flush=True)
        size = gen(name, rarity, desc, path)
        if size:
            print(f"✅ {size//1024}KB")
            done += 1
        else:
            print("❌")
        time.sleep(3)
    
    print(f"\n📊 Итог: {done}/{total}")

if __name__ == "__main__":
    main()
