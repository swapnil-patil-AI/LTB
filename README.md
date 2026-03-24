# LTB Analytics Platform — Demo App

## Look-to-Book Intelligence Platform
**Management Demo Application** — Air Canada NDC

---

## Features

| Tab | Description |
|-----|-------------|
| 🏠 Dashboard | Executive overview with KPI cards, seller summaries, worst routes |
| 📊 LTB Analytics | Detailed table with Daily / 7-Day / 14-Day / 30-Day LTB per seller per route |
| 📈 Charts & Trends | 30-day trend lines, heatmaps, search vs booking volumes |
| ⚖️ Rule Engine | ATPCO-style priority rules, live routing simulator, add/disable rules |
| 🤖 AI Insights | Claude-powered analysis, quick questions, rule suggestions |

---

## Quick Deploy to Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path**: `streamlit_app.py`
5. In **Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
6. Click Deploy

---

## Local Run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## Demo Data

The app generates 30 days of realistic dummy data for 5 sellers across 15 routes:

**Sellers:**
- Sabre (ac.gndc.sabre) — Low LTB, high converting
- Amadeus (ac.gndc.amadeus) — Excellent conversion
- Travelport (ac.gndc.travelport) — Medium-high LTB
- FareNexus (ac.gndc.farenexus) — High LTB
- NDCConnect (ac.gndc.ndcconnect) — Very high LTB (demo worst case)

**Routes:** YUL→LHR, YYZ→CDG, YVR→NRT, YYC→LAX, YUL→DXB + 10 more

---

## AI Assistant

The AI assistant uses **Claude Sonnet** via Anthropic API. Provide your `ANTHROPIC_API_KEY` via:
- Streamlit Secrets (recommended for deployment)
- Sidebar input (for local testing)

The assistant has full context of the current LTB data and active rules in every message.

---

*Built for Air Canada NDC · Look-to-Book Analytics Platform · v1.0*
