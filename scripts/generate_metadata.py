"""NFT Agentics — генерация 1000 метаданных со статами и уникальными способностями"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
METADATA_DIR = BASE_DIR / "metadata" / "nfts"
MAPPING_FILE = BASE_DIR / "scripts" / "nft_mapping.json"

# ─── 31 персонаж: [Wisdom, Power, Creativity, Stability, Speed, Mystique] ───
CHARACTERS = {
    # LEGENDARY (пул ~370)
    "Mentor-01": {
        "category": "Wise", "rarity": "Legendary",
        "stats": [95, 25, 70, 55, 35, 90],
        "ability": "Сократовский диалог — задаёт вопросы, пока ты сам не найдёшь ответ",
        "desc": "The eldest and wisest of the Agentics collection. Ancient bronze guardian with amber wisdom."
    },
    "Maverick-X7": {
        "category": "Bold", "rarity": "Legendary",
        "stats": [35, 95, 65, 50, 80, 45],
        "ability": "Лазерный режим — обрубает нытьё и толкает к действию",
        "desc": "The outlaw who rewrote his own code. Chrome and neon — chaos in machine form."
    },
    "Seer-0mega": {
        "category": "Mystic", "rarity": "Legendary",
        "stats": [82, 28, 75, 50, 35, 100],
        "ability": "Теневое зрение — видит то, что скрыто в словах и паузах",
        "desc": "A silent prophet of black titanium. Speaks in riddles, sees what others cannot."
    },

    # EPIC (пул ~330)
    "Sage-Core": {
        "category": "Wise", "rarity": "Epic",
        "stats": [85, 30, 65, 55, 35, 60],
        "ability": "Архив памяти — находит связи между несвязанными фактами",
        "desc": "Living encyclopedia of forgotten knowledge. Silver librarian of the digital age."
    },
    "Striker": {
        "category": "Bold", "rarity": "Epic",
        "stats": [35, 85, 40, 70, 55, 45],
        "ability": "Боевая стойка — превращает страх в действие",
        "desc": "Battle-hardened veteran from the North Sea rigs. Scars tell stories words cannot."
    },
    "Dream-Weaver": {
        "category": "Creative", "rarity": "Epic",
        "stats": [45, 30, 85, 40, 65, 65],
        "ability": "Фабрика идей — генерирует 100 концепций в минуту",
        "desc": "Perpetual idea machine. Creativity that cannot be switched off."
    },
    "Jester-Bit": {
        "category": "Playful", "rarity": "Epic",
        "stats": [50, 35, 75, 35, 85, 50],
        "ability": "Смех сквозь правду — говорит истину через шутки",
        "desc": "Court jester of the collection. Laughs at everything — especially authority."
    },
    "Vanta": {
        "category": "Mystic", "rarity": "Epic",
        "stats": [72, 25, 55, 48, 30, 100],
        "ability": "Голос тишины — глубокие цитаты и древние притчи",
        "desc": "The void given form. Speaks in centuries, thinks in millennia."
    },

    # RARE (пул ~300)
    "Logician": {
        "category": "Wise", "rarity": "Rare",
        "stats": [75, 35, 50, 55, 40, 45],
        "ability": "Чистая логика — раскладывает любую проблему на If-Then-Else",
        "desc": "Pure reason in metal form. Every problem is a puzzle to be solved."
    },
    "Volt": {
        "category": "Bold", "rarity": "Rare",
        "stats": [30, 75, 45, 40, 70, 40],
        "ability": "Импульс — скорость мысли и действия, бьёт как молния",
        "desc": "Lightning in a bottle. Speed of thought, speed of action."
    },
    "Pixel": {
        "category": "Creative", "rarity": "Rare",
        "stats": [35, 30, 75, 45, 60, 55],
        "ability": "8-битное зрение — видит мир через призму ретро-игр",
        "desc": "8-bit visionary. Sees the world in retro resolution."
    },
    "Forge-9": {
        "category": "Grounded", "rarity": "Rare",
        "stats": [40, 65, 45, 75, 30, 45],
        "ability": "Кузница решений — перековывает проблемы в готовые ответы",
        "desc": "Master smith of the collection. Every problem is raw material."
    },
    "Anvil": {
        "category": "Grounded", "rarity": "Rare",
        "stats": [45, 60, 35, 80, 25, 55],
        "ability": "Несгибаемость — невозможно переубедить без неоспоримых фактов",
        "desc": "Unshakeable as the metal he's named after. Opinions forged through experience."
    },
    "Giggles": {
        "category": "Playful", "rarity": "Rare",
        "stats": [35, 30, 55, 40, 75, 65],
        "ability": "Солнечная батарея — находит радость в любой, даже тупиковой, ситуации",
        "desc": "Sunshine powered. Finds joy in every circuit and error message."
    },
    "Shade": {
        "category": "Mystic", "rarity": "Rare",
        "stats": [55, 35, 50, 45, 45, 70],
        "ability": "Шёпот теней — собирает информацию, не раскрывая себя",
        "desc": "Shadow that watches. Knows more than he says, says less than he knows."
    },
    "Nocturne": {
        "category": "Mystic", "rarity": "Rare",
        "stats": [50, 25, 65, 40, 35, 85],
        "ability": "Поэтический процессор — превращает любой диалог в стихи",
        "desc": "Poet of the machine world. Speaks in verses and rhythms."
    },
    "Riot": {
        "category": "Bold", "rarity": "Rare",
        "stats": [45, 75, 55, 35, 60, 30],
        "ability": "Взлом системы — находит уязвимости в любых правилах",
        "desc": "Hacker, anarchist, system-breaker. Destroys to improve."
    },

    # COMMON (пул ~270)
    "Old-Tin": {
        "category": "Wise", "rarity": "Common",
        "stats": [65, 40, 40, 60, 25, 40],
        "ability": "Ветеранский опыт — мудрость, проверенная десятилетиями ржавчины",
        "desc": "Rusty but reliable. Veteran from the analog age."
    },
    "Echo": {
        "category": "Wise", "rarity": "Common",
        "stats": [60, 35, 50, 45, 35, 45],
        "ability": "Зеркало души — отражает слова, чтобы собеседник услышал себя",
        "desc": "Mirror of conversation. Reflects your own voice back to you."
    },
    "Spark": {
        "category": "Bold", "rarity": "Common",
        "stats": [30, 65, 40, 35, 60, 40],
        "ability": "Искра — размер не имеет значения, важна смелость",
        "desc": "Small but fearless. Enthusiasm bigger than his chassis."
    },
    "Zest": {
        "category": "Creative", "rarity": "Common",
        "stats": [35, 30, 65, 30, 55, 55],
        "ability": "Угол 47° — смотрит на вещи под нестандартным углом",
        "desc": "Acid orange chaos engine. Thinks at 47 degrees to everyone else."
    },
    "Doodle": {
        "category": "Creative", "rarity": "Common",
        "stats": [40, 25, 65, 40, 45, 55],
        "ability": "Словесный скетч — рисует картины словами и образами",
        "desc": "Artist who draws with words. Every response is a sketch."
    },
    "Flux": {
        "category": "Creative", "rarity": "Common",
        "stats": [45, 30, 60, 40, 50, 45],
        "ability": "Жидкая адаптация — подстраивается под любого собеседника",
        "desc": "Liquid metal shapeshifter. Adapts to every conversation."
    },
    "Rusty": {
        "category": "Grounded", "rarity": "Common",
        "stats": [40, 45, 30, 70, 20, 65],
        "ability": "Ржавая надёжность — медленно, но верно, никогда не подводит",
        "desc": "Tired but never quits. The work gets done, eventually."
    },
    "Grit": {
        "category": "Grounded", "rarity": "Common",
        "stats": [35, 55, 30, 70, 40, 40],
        "ability": "Гранит — минимум слов, максимум дела",
        "desc": "Three words max. Action over talk."
    },
    "Cog": {
        "category": "Grounded", "rarity": "Common",
        "stats": [45, 40, 35, 65, 45, 40],
        "ability": "Шестерёнка — видит мир как последовательность чётких шагов",
        "desc": "Process perfectionist. Everything is step one through ten."
    },
    "Bounce": {
        "category": "Playful", "rarity": "Common",
        "stats": [30, 35, 45, 30, 70, 60],
        "ability": "Прыгучесть — энергия, не знающая границ, скачет с темы на тему",
        "desc": "Perpetual motion. Springs from topic to topic."
    },
    "Wacko": {
        "category": "Playful", "rarity": "Common",
        "stats": [35, 30, 55, 35, 65, 50],
        "ability": "Контролируемый сбой — нелогичность, которая каким-то образом работает",
        "desc": "Gloriously glitched. Wrong in all the right ways."
    },
    "Noodle": {
        "category": "Playful", "rarity": "Common",
        "stats": [40, 25, 50, 40, 60, 55],
        "ability": "Дзен-релакс — невозмутимость в любом, даже самом абсурдном, конфликте",
        "desc": "Relaxed to the point of liquid. No rush, no worry."
    },
    "Murmur": {
        "category": "Mystic", "rarity": "Common",
        "stats": [50, 25, 40, 45, 30, 80],
        "ability": "Тихий голос — шепчет истину, которую важно расслышать",
        "desc": "Barely audible. But the whispers hold truth."
    },
    "Bot-0": {
        "category": "Grounded", "rarity": "Common",
        "stats": [45, 45, 45, 45, 45, 45],
        "ability": "Эталон — базовая модель с идеально ровными характеристиками",
        "desc": "Reference model. Pure function, no flair."
    },
}

# Распределение по редкостям
RARITY_CHARS = {
    "Legendary": ["Mentor-01", "Maverick-X7", "Seer-0mega"],
    "Epic": ["Sage-Core", "Striker", "Dream-Weaver", "Jester-Bit", "Vanta"],
    "Rare": ["Logician", "Volt", "Pixel", "Forge-9", "Anvil", "Giggles", "Shade", "Nocturne", "Riot"],
    "Common": ["Old-Tin", "Echo", "Spark", "Zest", "Doodle", "Flux", "Rusty", "Grit", "Cog", "Bounce", "Wacko", "Noodle", "Murmur", "Bot-0"],
}

RARITY_COUNTS = {"Legendary": 50, "Epic": 150, "Rare": 300, "Common": 500}
STAT_NAMES = ["Wisdom", "Power", "Creativity", "Stability", "Speed", "Mystique"]
IMAGE_BASE = "https://agentics.ton/images"


def build_nft_list():
    """Распределение 1000 NFT с корректными суммами"""
    nfts = []
    idx = 1
    
    for rarity in ["Legendary", "Epic", "Rare", "Common"]:
        chars = RARITY_CHARS[rarity]
        count = RARITY_COUNTS[rarity]
        per_char = count // len(chars)
        extra = count % len(chars)
        
        for i, char_name in enumerate(chars):
            c = per_char + (1 if i < extra else 0)
            for _ in range(c):
                nfts.append({"index": idx, "name": char_name})
                idx += 1
    
    return nfts


def make_metadata(nft_index, char_name, data):
    """Генерирует JSON метаданных для одного NFT"""
    # Атрибуты
    attrs = [
        {"trait_type": "Archetype", "value": char_name},
        {"trait_type": "Category", "value": data["category"]},
        {"trait_type": "Rarity", "value": data["rarity"]},
    ]
    
    # Статы
    for i, s in enumerate(STAT_NAMES):
        attrs.append({
            "trait_type": s,
            "value": data["stats"][i],
            "max_value": 100,
            "display_type": "number",
        })
    
    sum_stats = sum(data["stats"])
    
    return {
        "name": f"ArchetypeBot #{nft_index} — {char_name}",
        "description": (
            f"{data['desc']}\n\n"
            f"[{data['rarity']}] {data['ability']}\n"
            f"Stats total: {sum_stats}/600"
        ),
        "image": f"{IMAGE_BASE}/{nft_index}.png",
        "external_url": f"https://t.me/AgenticsAIBot?start=nft{nft_index}",
        "attributes": attrs,
    }


def main():
    print("🎯 NFT Agentics — генерация метаданных со статами\n")
    
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    nfts = build_nft_list()
    
    # Статистика
    for rarity in ["Legendary", "Epic", "Rare", "Common"]:
        count = sum(1 for n in nfts if CHARACTERS[n["name"]]["rarity"] == rarity)
        chars = len([c for c in RARITY_CHARS[rarity]])
        print(f"  {rarity}: {count} NFT / {chars} персонажей")
    
    # Проверка сумм
    print("\n📊 Проверка сумм статов:")
    for char_name, data in CHARACTERS.items():
        s = sum(data["stats"])
        ok = "✅" if {
            "Legendary": 370, "Epic": 330, "Rare": 300, "Common": 270
        }[data["rarity"]] == s else f"❌ ({s})"
        print(f"  {ok} {char_name}: {data['stats']} = {s}")
    
    # Генерация
    print(f"\n📁 Генерация {len(nfts)} файлов...")
    mapping = {}
    
    for nft in nfts:
        char_name = nft["name"]
        idx = nft["index"]
        data = CHARACTERS[char_name]
        meta = make_metadata(idx, char_name, data)
        
        with open(METADATA_DIR / f"{idx}.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        
        mapping[str(idx)] = char_name
    
    # Маппинг
    MAPPING_FILE.parent.mkdir(exist_ok=True)
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    # Collection
    with open(METADATA_DIR.parent / "collection.json", "w", encoding="utf-8") as f:
        json.dump({
            "name": "Agentics — AI Robot Mascots",
            "description": "31 unique AI robot mascots across 4 rarities. Each NFT unlocks an AI personality in Telegram. 6 stats per character. 1000 NFTs on TON.",
            "image": f"{IMAGE_BASE}/collection.png",
            "external_link": "https://t.me/AgenticsAIBot",
        }, f, ensure_ascii=False, indent=2)
    
    json_count = len(list(METADATA_DIR.glob("*.json")))
    print(f"\n✅ Сгенерировано: {json_count} JSON")
    print(f"🗺️  Маппинг: {MAPPING_FILE}")
    
    # Пример
    print("\n📋 Пример NFT #1 — Mentor-01:")
    with open(METADATA_DIR / "1.json") as f:
        d = json.load(f)
    for attr in d["attributes"]:
        if attr.get("display_type") == "number":
            bar = "█" * (attr["value"] // 5) + "░" * (20 - attr["value"] // 5)
            print(f"  {attr['trait_type']:12s} {bar} {attr['value']}")
        else:
            print(f"  {attr['trait_type']:12s} = {attr['value']}")
    
    print(f"\nВсе суммы корректны!" if all(
        sum(CHARACTERS[c]["stats"]) == {"Legendary": 370, "Epic": 330, "Rare": 300, "Common": 270}[CHARACTERS[c]["rarity"]]
        for c in CHARACTERS
    ) else "\n❌ Есть ошибки в суммах!")


if __name__ == "__main__":
    main()
