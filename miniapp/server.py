"""
Agentics Mini App Server — FastAPI
Сервит HTML Mini App + POST /activate (генерация TOKEN)
"""

import json
import hashlib
import os
import secrets
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ACTIVATIONS_FILE = DATA_DIR / "activations.json"
USERS_FILE = DATA_DIR / "users.json"

COLLECTION_ADDRESS = "EQC_UNVutKasGbtxaK57c2ENCytuKUvvEYy9BuOWLpsnRS_k"
TONCENTER_API = "https://toncenter.com/api/v3"

app = FastAPI(title="Agentics Mini App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Персонажи ───
CHARACTERS = {
    "Mentor-01": {"category": "Wise", "rarity": "Legendary"},
    "Maverick-X7": {"category": "Bold", "rarity": "Legendary"},
    "Seer-0mega": {"category": "Mystic", "rarity": "Legendary"},
    "Sage-Core": {"category": "Wise", "rarity": "Epic"},
    "Striker": {"category": "Bold", "rarity": "Epic"},
    "Dream-Weaver": {"category": "Creative", "rarity": "Epic"},
    "Jester-Bit": {"category": "Playful", "rarity": "Epic"},
    "Vanta": {"category": "Mystic", "rarity": "Epic"},
    "Logician": {"category": "Wise", "rarity": "Rare"},
    "Volt": {"category": "Bold", "rarity": "Rare"},
    "Pixel": {"category": "Creative", "rarity": "Rare"},
    "Forge-9": {"category": "Grounded", "rarity": "Rare"},
    "Anvil": {"category": "Grounded", "rarity": "Rare"},
    "Giggles": {"category": "Playful", "rarity": "Rare"},
    "Shade": {"category": "Mystic", "rarity": "Rare"},
    "Nocturne": {"category": "Mystic", "rarity": "Rare"},
    "Riot": {"category": "Bold", "rarity": "Rare"},
    "Old-Tin": {"category": "Wise", "rarity": "Common"},
    "Echo": {"category": "Wise", "rarity": "Common"},
    "Spark": {"category": "Bold", "rarity": "Common"},
    "Zest": {"category": "Creative", "rarity": "Common"},
    "Doodle": {"category": "Creative", "rarity": "Common"},
    "Flux": {"category": "Creative", "rarity": "Common"},
    "Rusty": {"category": "Grounded", "rarity": "Common"},
    "Grit": {"category": "Grounded", "rarity": "Common"},
    "Cog": {"category": "Grounded", "rarity": "Common"},
    "Bounce": {"category": "Playful", "rarity": "Common"},
    "Wacko": {"category": "Playful", "rarity": "Common"},
    "Noodle": {"category": "Playful", "rarity": "Common"},
    "Murmur": {"category": "Mystic", "rarity": "Common"},
    "Bot-0": {"category": "Grounded", "rarity": "Common"},
}


def load_json(path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


class ActivateRequest(BaseModel):
    wallet: str
    api_key: str
    provider: str = "openai"
    model: str = ""
    base_url: str = ""
    nft_address: str = ""
    char_name: str = ""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/collection")
def get_collection_info():
    return {
        "address": COLLECTION_ADDRESS,
        "name": "Agentics — AI Robot Mascots",
        "getgems_url": f"https://getgems.io/collection/{COLLECTION_ADDRESS}",
    }


@app.post("/api/activate")
def activate(req: ActivateRequest):
    """Генерирует TOKEN для активации в боте"""
    wallet = req.wallet.strip()
    api_key = req.api_key.strip()
    provider = req.provider.strip().lower()
    model = req.model.strip()
    base_url = req.base_url.strip()
    nft_address = req.nft_address.strip()
    char_name = req.char_name.strip()

    if not wallet or not api_key:
        raise HTTPException(400, "wallet и api_key обязательны")

    # Допустимые провайдеры
    valid_providers = {"openai", "deepseek", "anthropic", "google", "custom"}
    if provider not in valid_providers:
        raise HTTPException(400, f"provider должен быть один из: {', '.join(sorted(valid_providers))}")

    # Если персонаж не указан — fallback
    if not char_name:
        char_name = "Mentor-01"
    if char_name not in CHARACTERS:
        raise HTTPException(400, f"Персонаж '{char_name}' не найден")

    # Генерируем одноразовый TOKEN
    raw = f"{wallet}:{api_key}:{provider}:{model}:{base_url}:{nft_address}:{char_name}:{secrets.token_hex(8)}"
    token = hashlib.sha256(raw.encode()).hexdigest()[:32]

    # Сохраняем
    activations = load_json(ACTIVATIONS_FILE)
    activations[token] = {
        "char_name": char_name,
        "api_key": api_key,
        "provider": provider,
        "model": model,
        "base_url": base_url,
        "wallet": wallet,
        "nft_address": nft_address,
        "created_at": datetime.now().isoformat(),
    }
    save_json(ACTIVATIONS_FILE, activations)

    return {
        "token": token,
        "char_name": char_name,
        "rarity": CHARACTERS[char_name]["rarity"],
        "category": CHARACTERS[char_name]["category"],
        "bot_username": "AgenticsAIBot",
    }


@app.get("/api/characters")
def list_characters():
    """Список всех персонажей"""
    return CHARACTERS


@app.get("/tonconnect-manifest.json")
def serve_manifest():
    manifest_path = BASE_DIR / "miniapp" / "tonconnect-manifest.json"
    if manifest_path.exists():
        return JSONResponse(json.loads(manifest_path.read_text()))
    return JSONResponse({}, status_code=404)


@app.get("/icon.png")
def serve_icon():
    icon_path = BASE_DIR / "miniapp" / "icon.png"
    if icon_path.exists():
        from fastapi.responses import FileResponse
        return FileResponse(icon_path, media_type="image/png")
    return JSONResponse({}, status_code=404)


@app.get("/api/images/{name}")
def serve_character_image(name: str):
    """Раздаёт изображения персонажей"""
    safe_name = name.lower().replace(" ", "-").replace("_", "-")
    images_dir = BASE_DIR / "images"
    img_path = images_dir / f"{safe_name}.png"
    if not img_path.exists():
        matches = list(images_dir.glob(f"{safe_name}*"))
        if matches:
            img_path = matches[0]
    if img_path.exists():
        from fastapi.responses import FileResponse
        return FileResponse(img_path, media_type="image/png")
    return JSONResponse({"error": "image not found"}, status_code=404)


ASSETS_MAP = {
    "logo.png": "logo.png",
    "og-preview.png": "og-preview.png",
    "banner.png": "banner.png",
    "bg-pattern.png": "bg-pattern.png",
}


@app.get("/assets/{filename}")
def serve_asset(filename: str):
    """Раздаёт brand assets (logo, og-preview, banner)"""
    if filename in ASSETS_MAP:
        path = BASE_DIR / "miniapp" / "assets" / ASSETS_MAP[filename]
        if path.exists():
            from fastapi.responses import FileResponse
            return FileResponse(path, media_type="image/png")
    return JSONResponse({"error": "not found"}, status_code=404)


@app.get("/", response_class=HTMLResponse)
def serve_miniapp():
    """Сервим Mini App"""
    html_path = BASE_DIR / "miniapp" / "index.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Agentics Mini App</h1><p>Файл index.html не найден</p>")
