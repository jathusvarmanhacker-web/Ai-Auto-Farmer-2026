# 🌿 AgroShield AI

**Smart Farming Assistant** for Sri Lankan farmers — available in English, தமிழ் (Tamil), and සිංහල (Sinhala).

Built with [Streamlit](https://streamlit.io) and powered by Claude AI (Anthropic).

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌍 **Multilingual** | English, Tamil, Sinhala — full UI translation |
| 🌦️ **Live Weather** | Real-time data via Open-Meteo for your farm location |
| 🌱 **Crop Manager** | Add, track, and remove crops with growth stage progress |
| 🔬 **Crop Scanner** | Upload a photo; AI simulates disease/pest detection |
| 📊 **Market Prices** | Live LKR/kg price table with estimated revenue per crop |
| 🤖 **AI Chat** | Claude-powered farming advisor that replies in your language |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/agroshield-ai.git
cd agroshield-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key

**Option A — environment variable (recommended):**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

**Option B — Streamlit secrets (for Streamlit Cloud):**

Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Then update `utils/ai_chat.py` line 5:
```python
api_key=st.secrets["ANTHROPIC_API_KEY"]
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo, branch `main`, and entry file `app.py`.
4. Under **Advanced settings → Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
5. Click **Deploy** — your app will be live in ~1 minute.

---

## 📁 Project Structure

```
agroshield-ai/
├── app.py                  # Main entry point (language select, login, routing)
├── requirements.txt
├── README.md
├── pages/
│   ├── dashboard.py        # Dashboard with weather + crop overview
│   ├── crops.py            # Add/remove crop tracking
│   ├── scanner.py          # Crop disease scanner (photo upload)
│   ├── market.py           # Market price table
│   └── chat.py             # AI farming assistant chat
└── utils/
    ├── translations.py     # All UI strings in EN / TA / SI
    ├── weather.py          # Open-Meteo weather API wrapper
    ├── market.py           # Static price table + revenue calculator
    └── ai_chat.py          # Anthropic Claude API wrapper
```

---

## 🔑 API Keys

| Service | Key needed | How to get |
|---|---|---|
| Claude AI | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| Weather | None | Free — [open-meteo.com](https://open-meteo.com) |

---

## 🛠️ Tech Stack

- **Streamlit** — UI framework
- **Anthropic Claude** — AI farming assistant
- **Open-Meteo** — Free weather API (no key required)
- **Pandas** — Market price table rendering

---

## 📄 License

MIT — free to use, modify, and deploy.
