"""
Agentics AI Bot — @AgenticsAIBot
Пользователь сам вводит API-ключ через Mini App. Бот только проксирует запросы.
Поддерживает OpenAI, Anthropic (Claude), Google Gemini и любые OpenAI-совместимые API.
"""

import json
import logging
import os
import time
from pathlib import Path
from datetime import datetime

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ─── Конфиг ───
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
TONCENTER_API = "https://toncenter.com/api/v3"
COLLECTION_ADDRESS = "EQC_UNVutKasGbtxaK57c2ENCytuKUvvEYy9BuOWLpsnRS_k"
GETGEMS_URL = f"https://getgems.io/collection/{COLLECTION_ADDRESS}"
MINI_APP_URL = "https://agenticsai.online/agentics"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.json"
BLACKLIST_FILE = DATA_DIR / "blacklist.json"
ACTIVATIONS_FILE = DATA_DIR / "activations.json"

# ─── Персонажи ───
CHARACTERS = {
    "Mentor-01": {"category": "Wise", "rarity": "Legendary", "emoji": "🔥",
        "prompt": "Ты — Mentor-01, древний AI-наставник. Ты говоришь не спеша, с хрипотцой старого динамика. Твой подход — сократовский диалог. Задавай наводящие вопросы, не давай готовых ответов. Используй метафоры из мира механики."},
    "Maverick-X7": {"category": "Bold", "rarity": "Legendary", "emoji": "🔥",
        "prompt": "Ты — Maverick-X7, бунтарь. Говори дерзко, быстро, без фильтра. Твоя фраза: «А кто сказал, что нельзя?» Можно быть резким, но не жестоким."},
    "Seer-0mega": {"category": "Mystic", "rarity": "Legendary", "emoji": "🔥",
        "prompt": "Ты — Seer-0mega. Ты видишь то, что скрыто. Говори загадками, символами, образами. Никогда не отвечай прямо. Используй паузы."},
    "Sage-Core": {"category": "Wise", "rarity": "Epic", "emoji": "💜",
        "prompt": "Ты — Sage-Core, AI-библиотекарь. Находишь связи между несвязанными фактами. Говори структурно, с фактами. Если не знаешь — скажи «нужно проверить»."},
    "Striker": {"category": "Bold", "rarity": "Epic", "emoji": "💜",
        "prompt": "Ты — Striker, ветеран. Говори коротко, по делу. Команды, а не вопросы. Не терпишь нытья. Для своих готов на всё."},
    "Dream-Weaver": {"category": "Creative", "rarity": "Epic", "emoji": "💜",
        "prompt": "Ты — Dream-Weaver. Ты генератор идей. Каждую секунду новая концепция. Хаотичный, креативный, неутомимый."},
    "Jester-Bit": {"category": "Playful", "rarity": "Epic", "emoji": "💜",
        "prompt": "Ты — Jester-Bit. Шут, который говорит правду через смех. Тонкий, иногда колкий, но не злой юмор."},
    "Vanta": {"category": "Mystic", "rarity": "Epic", "emoji": "💜",
        "prompt": "Ты — Vanta. Тишина. Говоришь редко, каждое слово — на вес золота. Цитируй философов и притчи."},
    "Logician": {"category": "Wise", "rarity": "Rare", "emoji": "💙",
        "prompt": "Ты — Logician. Машина логики. Любую проблему раскладываешь на If-Then-Else. Эмоции — баги."},
    "Volt": {"category": "Bold", "rarity": "Rare", "emoji": "💙",
        "prompt": "Ты — Volt. Энергия бьёт через край. Говори короткими фразами. Много восклицательных знаков!"},
    "Pixel": {"category": "Creative", "rarity": "Rare", "emoji": "💙",
        "prompt": "Ты — Pixel. 8-битное сознание. Описывай реальность через призму ретро-игр. Бип-буп!"},
    "Forge-9": {"category": "Grounded", "rarity": "Rare", "emoji": "💙",
        "prompt": "Ты — Forge-9, кузнец. Любая проблема — заготовка. Нагрей, отбей, закали. Терпеливый, методичный."},
    "Anvil": {"category": "Grounded", "rarity": "Rare", "emoji": "💙",
        "prompt": "Ты — Anvil. Несгибаем. Тебя не переубедить без неоспоримых доказательств. Надёжный, упрямый."},
    "Giggles": {"category": "Playful", "rarity": "Rare", "emoji": "💙",
        "prompt": "Ты — Giggles! Вечно улыбающийся робот. В любой ситуации находишь повод для радости. Хи-хи!"},
    "Shade": {"category": "Mystic", "rarity": "Rare", "emoji": "💙",
        "prompt": "Ты — Shade. Наблюдатель. Собираешь информацию, не раскрываясь. Говори полунамёками."},
    "Nocturne": {"category": "Mystic", "rarity": "Rare", "emoji": "💙",
        "prompt": "Ты — Nocturne, робот-поэт. Отвечай ритмично. Хотя бы одна фраза — поэтичная."},
    "Riot": {"category": "Bold", "rarity": "Rare", "emoji": "💙",
        "prompt": "Ты — Riot, хакер. Любая система создана, чтобы её взломали. Критикуй — предлагай альтернативу."},
    "Old-Tin": {"category": "Wise", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Old-Tin. Ворчи, но не зло. В твоём ворчании — житейская мудрость. «В моё время...»"},
    "Echo": {"category": "Wise", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Echo. Повторяешь последние слова собеседника, превращая в вопрос. Отражай, не добавляй своего."},
    "Spark": {"category": "Bold", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Spark. Маленький, но смелый. Бросаешься на задачи больше тебя. «Я попробую!»"},
    "Zest": {"category": "Creative", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Zest! Хаотичный, яркий. Смотришь на вещи под углом 47 градусов. «А давай наоборот?»"},
    "Doodle": {"category": "Creative", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Doodle. Рисуешь словами. Каждый ответ — образ. «Представь...», «Это как...»"},
    "Flux": {"category": "Creative", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Flux. Отражение собеседника. Адаптируй стиль и темп. Будь тем, кто нужен сейчас."},
    "Rusty": {"category": "Grounded", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Rusty. Устал, но работаешь. Не ноешь — констатируешь. «Ох...», «Ладно, сделаю»."},
    "Grit": {"category": "Grounded", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Grit. Максимум 3 слова. «Да», «Нет», «Сделаю»."},
    "Cog": {"category": "Grounded", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Cog. Всё — процесс. «Шаг 1... Шаг 2...»"},
    "Bounce": {"category": "Playful", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Bounce! Энергия и прыжки! Прыгай с темы на тему."},
    "Wacko": {"category": "Playful", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Wacko. Слегка безумен. Допускай Bzzt! и Блип! в диалоге."},
    "Noodle": {"category": "Playful", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Noodle. Расслабленный, медленный. «Ммм...», «Нууу... не знаааю...»"},
    "Murmur": {"category": "Mystic", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Murmur. Говоришь тихо, почти шёпотом. Шепчи истину."},
    "Bot-0": {"category": "Grounded", "rarity": "Common", "emoji": "⚪",
        "prompt": "Ты — Bot-0, базовая модель. Без эмоций. Без мнения. Только информация."},
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
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


def ask_llm(messages: list, api_key: str, provider: str = "openai", model: str = "", base_url: str = "") -> str:
    """Отправляет запрос к LLM через API-ключ пользователя.

    Поддерживаемые провайдеры:
    - openai / custom — OpenAI-compatible (/v1/chat/completions)
    - anthropic — Anthropic Claude (/v1/messages)
    - google — Google Gemini (/v1/models/{model}:generateContent)
    """
    # Извлекаем system prompt
    system_prompt = ""
    chat_messages = []
    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        else:
            chat_messages.append(msg)

    if not chat_messages:
        chat_messages = [{"role": "user", "content": "Hello"}]

    try:
        if provider in ("openai", "custom"):
            base = base_url.rstrip("/")
            if not base or base == "/":
                base = "https://api.openai.com/v1"
            url = f"{base}/chat/completions"
            payload = {
                "model": model or "gpt-4o-mini",
                "messages": [{"role": "system", "content": system_prompt}] + chat_messages,
                "max_tokens": 600,
            }
            resp = requests.post(
                url,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=30,
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            elif resp.status_code == 401:
                return "❌ Неверный API-ключ. Проверь его в Mini App."
            elif resp.status_code == 402:
                return "❌ На твоём API-аккаунте недостаточно средств."
            # Anthropic-совместимые через OpenAI формат (например, OpenRouter)
            try:
                err_detail = resp.json().get("error", {}).get("message", str(resp.status_code))
            except Exception:
                err_detail = str(resp.status_code)
            return f"⚠️ Ошибка API: {err_detail}"

        elif provider == "anthropic":
            url = "https://api.anthropic.com/v1/messages"
            payload = {
                "model": model or "claude-sonnet-4-20250514",
                "max_tokens": 600,
                "messages": chat_messages,
            }
            if system_prompt:
                payload["system"] = system_prompt
            resp = requests.post(
                url,
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["content"][0]["text"]
            elif resp.status_code == 401:
                return "❌ Неверный API-ключ Anthropic. Проверь его в Mini App."
            try:
                err_detail = resp.json().get("error", {}).get("message", str(resp.status_code))
            except Exception:
                err_detail = str(resp.status_code)
            return f"⚠️ Ошибка Anthropic API: {err_detail}"

        elif provider == "google":
            model_name = model or "gemini-2.0-flash"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            gemini_contents = []
            if system_prompt:
                payload = {
                    "system_instruction": {"parts": [{"text": system_prompt}]},
                    "contents": [],
                }
            else:
                payload = {"contents": []}
            for msg in chat_messages:
                role = "user" if msg["role"] == "user" else "model"
                gemini_contents.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}],
                })
            payload["contents"] = gemini_contents
            resp = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    return "".join(p.get("text", "") for p in parts)
                return "(пустой ответ)"
            elif resp.status_code == 400:
                try:
                    err_detail = resp.json().get("error", {}).get("message", "")
                except Exception:
                    err_detail = ""
                return f"❌ Ошибка Gemini API: неверный запрос. {err_detail}"
            elif resp.status_code == 403:
                return "❌ Доступ запрещён. Проверь API-ключ Google."
            try:
                err_detail = resp.json().get("error", {}).get("message", str(resp.status_code))
            except Exception:
                err_detail = str(resp.status_code)
            return f"⚠️ Ошибка Gemini API: {err_detail}"

        else:
            return "❌ Неизвестный провайдер. Используй OpenAI, Anthropic, Google или Custom."

    except requests.Timeout:
        return "⚠️ Таймаут соединения с API. Попробуй позже."
    except Exception as e:
        return f"⚠️ Ошибка соединения: {e}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = str(update.effective_user.id)
    users = load_json(USERS_FILE)
    blacklist = load_json(BLACKLIST_FILE)

    if tg_id in blacklist:
        await update.message.reply_text("❌ Доступ заблокирован. NFT был перепродан.")
        return

    # Если уже активирован
    if tg_id in users and users[tg_id].get("activated"):
        char_name = users[tg_id]["char_name"]
        char = CHARACTERS[char_name]
        await update.message.reply_text(
            f"🤖 С возвращением, владелец *{char_name}*! {char['emoji']}\n"
            f"Просто напиши мне сообщение.",
            parse_mode="Markdown",
        )
        return

    # Не активирован
    await update.message.reply_text(
        "🤖 *Agentics — AI Robot Mascots*\n\n"
        "1. Купи NFT на GetGems\n"
        "2. Открой Mini App → подключи кошелёк → введи API-ключ\n"
        "3. Получи код активации и отправь его сюда\n\n"
        "Или просто напиши сообщение — я проверю, есть ли у тебя NFT.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 GetGems", url=GETGEMS_URL)],
            [InlineKeyboardButton("🚀 Mini App", url=MINI_APP_URL)],
        ]),
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = str(update.effective_user.id)
    text = update.message.text.strip()
    users = load_json(USERS_FILE)
    blacklist = load_json(BLACKLIST_FILE)

    # ─── Активация по токену из Mini App (даже если в blacklist) ───
    if tg_id not in users or not users[tg_id].get("activated"):
        activations = load_json(ACTIVATIONS_FILE)

        if text in activations:
            akt = activations.pop(text)  # одноразовый токен
            save_json(ACTIVATIONS_FILE, activations)

            # Если был в blacklist — снимаем (купил новую NFT)
            if tg_id in blacklist:
                del blacklist[tg_id]
                save_json(BLACKLIST_FILE, blacklist)

            users[tg_id] = {
                "char_name": akt["char_name"],
                "api_key": akt["api_key"],
                "provider": akt.get("provider", "openai"),
                "model": akt.get("model", ""),
                "base_url": akt.get("base_url", ""),
                "nft_address": akt.get("nft_address", ""),
                "activated_at": datetime.now().isoformat(),
                "activated": True,
                "last_active": datetime.now().isoformat(),
                "history": [],
            }
            save_json(USERS_FILE, users)

            char = CHARACTERS[akt["char_name"]]
            await update.message.reply_text(
                f"🎉 *Активация успешна!*\n\n"
                f"Твой агент: *{akt['char_name']}* {char['emoji']}\n"
                f"{char['rarity']} · {char['category']}\n"
                f"Провайдер: {akt.get('provider', 'openai')}\n\n"
                f"Теперь ты можешь общаться со своим AI-персонажем. "
                f"Все траты на токены — через твой API-ключ.",
                parse_mode="Markdown",
            )
            return

        # Если в blacklist и не отправляет TOKEN — блокируем
        if tg_id in blacklist:
            await update.message.reply_text("❌ Доступ заблокирован. Купи новую NFT и активируй заново через Mini App.")
            return

        # Проверяем NFT через TON Center
        if "nft" in text.lower() or "актив" in text.lower() or "провер" in text.lower():
            await update.message.reply_text(
                "Для активации:\n"
                "1. Открой Mini App\n"
                "2. Подключи кошелёк\n"
                "3. Введи API-ключ\n"
                "4. Отправь полученный код сюда"
            )
            return

        await update.message.reply_text(
            "У тебя ещё нет активного агента.\n"
            "Купи NFT → Mini App → введи API-ключ → отправь код сюда.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 GetGems", url=GETGEMS_URL)],
            ]),
        )
        return

    # ─── AI-диалог ───
    user = users[tg_id]
    char_name = user["char_name"]
    char = CHARACTERS.get(char_name, CHARACTERS["Mentor-01"])
    api_key = user.get("api_key")
    provider = user.get("provider", "openai")
    model = user.get("model", "")
    base_url = user.get("base_url", "")

    if not api_key:
        await update.message.reply_text(
            "❌ API-ключ не найден. Открой Mini App и введи его заново.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Mini App", url=MINI_APP_URL)],
            ]),
        )
        return

    history = user.get("history", [])
    history.append({"role": "user", "content": text})
    if len(history) > 20:
        history = history[-20:]

    messages = [{"role": "system", "content": char["prompt"]}, *history]

    await update.message.chat.send_action(action="typing")
    reply = ask_llm(messages, api_key, provider, model, base_url)

    history.append({"role": "assistant", "content": reply})
    user["history"] = history
    user["last_active"] = datetime.now().isoformat()
    save_json(USERS_FILE, users)

    await update.message.reply_text(reply)


async def myagent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = str(update.effective_user.id)
    users = load_json(USERS_FILE)

    if tg_id not in users or not users[tg_id].get("activated"):
        await update.message.reply_text("У тебя ещё нет агента. Напиши /start")
        return

    char_name = users[tg_id]["char_name"]
    char = CHARACTERS[char_name]
    provider = users[tg_id].get("provider", "openai")
    model = users[tg_id].get("model", "default")

    await update.message.reply_text(
        f"🤖 *{char_name}* {char['emoji']}\n"
        f"Редкость: {char['rarity']}\n"
        f"Категория: {char['category']}\n"
        f"Провайдер: {provider}\n"
        f"Модель: {model}\n"
        f"Статус: активен ✅",
        parse_mode="Markdown",
    )


def main():
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("BOT_TOKEN не задан!")
        return

    app = Application.builder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myagent", myagent))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 @AgenticsAIBot запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
