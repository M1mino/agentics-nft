# Agentics — AI Agent NFT Collection on TON

**Agentics** is a collection of **1,000 NFTs** featuring **30 unique AI agent characters** on the TON blockchain. Each NFT grants access to an interactive AI assistant with a distinct personality, powered by your choice of LLM (OpenAI, DeepSeek, Anthropic, Google).

⚠️ **Currently on testnet. Mainnet deployment in progress.**

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- A TON wallet (Tonkeeper)

### Contract Deployment

```bash
cd contracts
npm install
npx blueprint build
npx blueprint run scripts/deployNftCollection.ts
```

### Bot Setup

```bash
cd bot
pip install -r requirements.txt
# Edit .env with your bot token
python bot.py
```

### Mini App

```bash
cd miniapp
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8006
```

---

## 📁 Project Structure

```
agentics-nft/
├── contracts/          # Tact smart contracts (NFT Collection + NFT Item)
├── bot/                # Telegram bot (@AgenticsAIBot)
├── miniapp/            # Telegram Mini App (TON Connect + activation)
├── metadata/           # TEP-62 NFT metadata (collection.json + 1,000 NFTs)
├── images/             # Character artwork (30 PNGs)
├── scripts/            # Generation & utility scripts
├── deploy/             # Systemd services & Caddy config
├── AGENTS.md           # Full character descriptions (30 agents)
└── architecture.md     # System architecture
```

---

## 🧠 30 AI Agents

Each agent has a unique personality, backstory, and expertise:

### 🔥 Legendary (3)
| Agent | Type | Supply |
|-------|------|--------|
| Mentor-01 | Wise mentor, Socratic dialogue | 50 |
| Maverick-X7 | Bold rebel, provocateur | 50 |
| Seer-0mega | Mystic oracle, riddles | 50 |

### 💜 Epic (5)
| Agent | Type | Supply |
|-------|------|--------|
| Sage-Core | Knowledge library | 30 |
| Flux | Creative chaos | 30 |
| Echo | Mirror, active listening | 30 |
| Grit | Persistence, willpower | 30 |
| Shade | Stealth, hidden perspective | 30 |

### 💙 Rare (9) & 🤍 Common (13)
See [AGENTS.md](./AGENTS.md) for the full list of all 30 characters.

---

## 💎 How It Works

1. **Buy NFT** — User purchases from Getgems (free mint, gas only)
2. **Connect Wallet** — Mini App uses TON Connect to verify ownership
3. **Choose Agent** — Pick an agent from your NFTs
4. **Enter API Key** — Bring your own LLM API key (OpenAI, DeepSeek, etc.)
5. **Get Token** — Mini App generates an activation token
6. **Talk to Bot** — @AgenticsAIBot proxies messages to your chosen LLM with the character's system prompt

### Ownership Verification

A cron job checks NFT transfers every 2-3 minutes. If an NFT is resold, access is revoked and the bot notifies the previous owner.

---

## 🛠️ Smart Contract

- **Language:** Tact
- **Standard:** TEP-62 (NFT)
- **Features:**
  - Mint with fixed supply (1,000)
  - 5% royalty
  - Owner can set price and withdraw funds
  - Deployed on testnet: `EQC_UNVutKasGbtxaK57c2ENCytuKUvvEYy9BuOWLpsnRS_k`

---

## 🐳 Deploy

Systemd service files and Caddy config are in `deploy/`:

```bash
cp deploy/agentics-miniapp.service /etc/systemd/system/
cp deploy/agentics-bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now agentics-miniapp agentics-bot
```

---

## 🔗 Links

- **Bot:** [@AgenticsAIBot](https://t.me/AgenticsAIBot)
- **Collection (testnet):** [Getgems](https://testnet.getgems.io/collection/EQC_UNVutKasGbtxaK57c2ENCytuKUvvEYy9BuOWLpsnRS_k)
- **AgentPay:** [github.com/M1mino/agentpay](https://github.com/M1mino/agentpay) — Payment layer for AI agents

---

## 📄 License

MIT
