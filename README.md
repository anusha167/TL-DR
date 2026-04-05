# TL;DR ✦
### The whole story. Half the time.

> *For every article you starred and forgot.*

TL;DR is a Chrome extension + AI pipeline that automatically summarizes any article you save — and reads it back to you like a podcast. Save it once. Get the summary. Listen on the go.

Built at **DiamondHacks 2026**, powered by **Browser Use**.

---

## ✨ What it does

- **One click** — save any article from Chrome with the extension
- **AI browsing agent** — Browser Use navigates the live page like a human, extracting the full content
- **Gemini summarization** — clean, concise 3-5 sentence prose summary, no bullet points
- **Audio version** — full text-to-speech MP3, ready to listen like a podcast
- **Email notification** — get pinged the moment your summary is ready
- **Live dashboard** — your digest, stats, and audio player, all in one place

Works on articles, PDFs, research papers, news sites — anything.

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Chrome Extension | Manifest V3 |
| Backend | Python, Flask, SQLite |
| AI Browsing Agent | [Browser Use](https://github.com/browser-use/browser-use) + LangChain |
| Summarization | Gemini 2.0 Flash |
| Text-to-Speech | gTTS |
| Notifications | SMTP (Gmail) |
| Frontend | HTML, CSS, Vanilla JS |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Conda
- Google API Key (Gemini)
- OpenAI API Key
- Chrome browser

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/tldr.git
cd tldr
```

### 2. Set up the environment

```bash
conda create -n tldr_env python=3.11
conda activate tldr_env
pip install -r requirements.txt
```

### 3. Add your API keys

Create a `.env` file in the `backend/` folder:

```env
GOOGLE_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

> **Note:** Gmail requires an [App Password](https://support.google.com/accounts/answer/185833) — not your regular password.

### 4. Start the backend

```bash
cd backend
python app.py
```

Backend runs at `http://127.0.0.1:8080`

### 5. Load the Chrome extension

1. Open Chrome → `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked**
4. Select the `extension/` folder

### 6. Open the dashboard

Open `dashboard/index.html` in your browser.

---

## 📁 Project Structure

```
TL;DR/
├── backend/
│   ├── app.py          # Flask API
│   ├── agent.py        # Browser Use agent + PDF handler
│   ├── summarizer.py   # Gemini summarization
│   ├── tts.py          # gTTS audio generation
│   └── audio/          # Generated MP3s
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
└── dashboard/
    ├── index.html
    ├── styles.css
    └── app.js
```

---

## 🔄 How it works

```
User clicks extension
        ↓
Chrome sends URL → Flask API
        ↓
Browser Use opens page in real Chromium
(waits through Cloudflare, JS rendering, etc.)
        ↓
Gemini 2.0 Flash summarizes content
        ↓
gTTS converts summary → MP3
        ↓
Email notification sent to user
        ↓
Dashboard shows summary + audio player
```

---

## 🎧 Dashboard

- **Stats** — total saved, summarized, time saved, audio ready
- **Article cards** — summary, source, read time
- **Audio player** — play/pause, skip ±15s, scrub bar
- **Mode toggle** — Text, Audio, or Both
- **Email notifications** — register once, get pinged every time

---

## ⚠️ Known Limitations

- Some sites (e.g. Medium) require Cloudflare to auto-resolve — this adds a few seconds
- Gmail SMTP requires an App Password, not a regular password
- Gemini free tier has rate limits — use a billing-enabled project for heavy use

---

## 🏆 Built at DiamondHacks 2026

