"""NFT Agentics — тест единого стиля через Pollinations.ai"""

import json, sys, time, requests
from urllib.parse import quote
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"

# Жёсткий шаблон — одинаковая поза, фон, освещение для всех
TEMPLATE = (
    "full body standing front view portrait of a robot mascot, "
    "centered symmetrical composition, arms relaxed at sides, "
    "pure dark gradient background dark grey to black, "
    "single soft key light from front-left, rim light from right, "
    "professional product photography style, clean render, sharp focus, "
    "uniform style across collection, collectible NFT character design"
)

PROMPTS = {
    "Mentor-01": TEMPLATE + ", bronze robot with green patina, one large warm amber optical lens eye, old ribbed speaker chest, engraved gears and symbols on body, slightly tilted antenna",
    "Maverick-X7": TEMPLATE + ", chrome steel robot with red neon stripes, cowboy hat plate on head, face screen with cocky grin, laser cannon replacing one arm",
    "Seer-0mega": TEMPLATE + ", black titanium tall narrow robot, single red LED strip pulsing on face, faint purple glowing rune cracks, completely motionless",
}

def gen(name, prompt, path):
    url = "https://image.pollinations.ai/prompt/" + quote(prompt)
    params = {"width": 1024, "height": 1024, "nologo": "true", "model": "flux"}
    try:
        r = requests.get(url, params=params, timeout=90)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(path, "wb") as f:
                f.write(r.content)
            return r.content
    except Exception as e:
        print(f"    ошибка: {e}")
    return None

def main():
    IMAGES_DIR.mkdir(exist_ok=True)
    
    # Очищаем старые тестовые
    for f in IMAGES_DIR.glob("*.png"):
        f.unlink()
    
    for name, prompt in PROMPTS.items():
        slug = name.lower().replace(" ", "-")
        path = IMAGES_DIR / f"{slug}.png"
        print(f"🎨 {name}...", end=" ", flush=True)
        data = gen(name, prompt, path)
        if data:
            print(f"✅ {len(data)//1024}KB")
        else:
            print("❌")
        time.sleep(3)
    
    print("\nРезультаты:")
    for f in sorted(IMAGES_DIR.glob("*.png")):
        print(f"  {f.name}: {f.stat().st_size//1024}KB")

if __name__ == "__main__":
    main()
