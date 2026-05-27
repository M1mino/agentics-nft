"""
Проверка владения NFT — 1 запрос к коллекции.
Получает все NFT коллекции → проверяет, владеет ли пользователь своим конкретным NFT.
Если конкретный NFT перепродана — бан.
"""

import json
import logging
from pathlib import Path
from datetime import datetime

import requests

# ─── Конфиг ───
TONCENTER_API = "https://testnet.toncenter.com/api/v3"  # testnet → mainnet при релизе
COLLECTION_ADDRESS = "EQC_UNVutKasGbtxaK57c2ENCytuKUvvEYy9BuOWLpsnRS_k"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.json"
BLACKLIST_FILE = DATA_DIR / "blacklist.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s CHECK_NFT %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def load_json(path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def get_collection_owners() -> dict[str, str]:
    """
    Один запрос к TON Center: получает все NFT коллекции.
    Возвращает {nft_address: owner_address}.
    """
    owners = {}
    offset = 0
    limit = 1000

    while True:
        url = (
            f"{TONCENTER_API}/nft/items"
            f"?collection_address={COLLECTION_ADDRESS}"
            f"&limit={limit}&offset={offset}"
        )
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code != 200:
                logger.error(f"TON Center вернул {resp.status_code}: {resp.text[:200]}")
                break

            data = resp.json()
            items = data.get("nft_items", [])

            if not items:
                break

            for item in items:
                addr = item.get("address", "").lower()
                owner = (
                    item.get("owner_address", {})
                    .get("address", "")
                    .lower()
                )
                if addr and owner:
                    owners[addr] = owner

            if len(items) < limit:
                break
            offset += limit

        except Exception as e:
            logger.error(f"Ошибка запроса к TON Center: {e}")
            break

    logger.info(f"Загружено NFT коллекции: {len(owners)} шт.")
    return owners


def main():
    users = load_json(USERS_FILE)
    blacklist = load_json(BLACKLIST_FILE)

    if not users:
        logger.info("Нет активных пользователей — проверка не требуется")
        return

    # 1 запрос — получаем все NFT коллекции с владельцами
    all_nfts = get_collection_owners()
    if not all_nfts:
        logger.warning("Не удалось получить данные коллекции — пропускаем проверку")
        return

    to_blacklist = {}

    for tg_id, user in users.items():
        if not user.get("activated"):
            continue

        nft_address = user.get("nft_address", "").strip().lower()
        if not nft_address:
            continue

        stored_wallet = user.get("wallet", "").strip().lower()

        # Проверяем ТОЛЬКО конкретный NFT пользователя
        current_owner = all_nfts.get(nft_address)

        if current_owner is None:
            logger.warning(
                f"NFT исчез из коллекции! TG:{tg_id} | NFT:{nft_address[:8]}..."
            )
            to_blacklist[tg_id] = {
                "nft_address": nft_address,
                "old_wallet": stored_wallet,
                "new_wallet": None,
                "reason": "nft_not_found",
                "detected_at": datetime.now().isoformat(),
            }
            continue

        if current_owner != stored_wallet:
            logger.warning(
                f"NFT перепродана! TG:{tg_id} | NFT:{nft_address[:8]}... | "
                f"Был:{stored_wallet[:8]}... | Стал:{current_owner[:8]}..."
            )
            to_blacklist[tg_id] = {
                "nft_address": nft_address,
                "old_wallet": stored_wallet,
                "new_wallet": current_owner,
                "reason": "owner_changed",
                "detected_at": datetime.now().isoformat(),
            }

    if to_blacklist:
        for tg_id in to_blacklist:
            blacklist[tg_id] = to_blacklist[tg_id]
            if tg_id in users:
                del users[tg_id]

        save_json(BLACKLIST_FILE, blacklist)
        save_json(USERS_FILE, users)

        msg = f"Заблокировано: {len(to_blacklist)} — {list(to_blacklist.keys())}"
        logger.warning(msg)
        print(f"🚫 NFT перепродажа! {msg}")
    else:
        logger.info("Все NFT на месте — нарушений нет")

    activated_count = sum(
        1 for u in users.values()
        if u.get("activated") and u.get("nft_address")
    )
    logger.info(f"Активных пользователей: {activated_count}")


if __name__ == "__main__":
    main()
