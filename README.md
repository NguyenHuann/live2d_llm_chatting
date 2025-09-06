Here’s a polished **English version** of your `README.md` for the project:

---

````markdown
# Emu • AI Live2D Chat

An **AI VTuber** powered by **FastAPI + Live2D + g4f (LLM) + gTTS (TTS)**.  
Users can chat with a virtual character, rendered in Live2D on the web, with lip-sync and synthesized voice in Vietnamese.

---

## 🚀 Features

- **Backend**: FastAPI serving chat API and speech synthesis (gTTS).
- **Frontend**: HTML/CSS/JS + PixiJS + Live2D Cubism 4.
- **Lip-sync** support (mouth movement synchronized with audio).
- **LLM backend**: g4f (for research only).
- **Sample character**: Emu Otori (with a system prompt describing personality and backstory).

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/live2d_ai.git
cd live2d_ai
````

### 2. Create virtual environment & install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate     # Linux/macOS
# or .venv\Scripts\activate   # Windows PowerShell

pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Prepare static assets

* `static/index.html` → main UI
* `static/styles.css` → styles
* `static/main.js`, `static/live2d.js` → chat & Live2D logic
* `static/live2d/` → Live2D model directory (e.g. `14emu_sports02_t01/`)
* `static/vendor/` → pixi.js, pixi-live2d-display, live2dcubismcore.min.js
* `static/images/` → background image for avatar
* `static/audio/` → generated audio files will be stored here

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# LLM backend
LLM_BACKEND=g4f
G4F_MODEL=gpt-4o-mini
G4F_WEB_SEARCH=false

# gTTS (Text-to-Speech)
GTTS_LANG=vi
GTTS_SLOW=false
```

---

## ▶️ Run locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open [http://localhost:8000](http://localhost:8000) → interactive AI + Live2D chat.

---

## ☁️ Deployment

### Render (recommended for backend)

* **Build Command**:

  ```bash
  pip install -r requirements.txt
  ```
* **Start Command**:

  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

### Vercel (frontend only)

* Deploy the `static/` folder.
* Use `vercel.json` to proxy `/api/*` to your backend (Render/Oracle Cloud):

```json
{
  "version": 2,
  "builds": [{ "src": "static/**", "use": "@vercel/static" }],
  "routes": [
    { "src": "/static/(.*)", "dest": "/static/$1" },
    { "src": "/(.*)", "dest": "/static/index.html" }
  ],
  "rewrites": [
    { "source": "/api/:path*", "destination": "https://api.yourdomain.com/api/:path*" }
  ]
}
```

---

## 🗂 Project structure

```bash
live2d_ai/
│── main.py               # FastAPI app
│── llm.py                # LLM backend (g4f sync)
│── tts.py                # gTTS wrapper
│── utils.py              # .env + audio helpers
│── requirements.txt
│── .env
└── static/
    ├── index.html
    ├── styles.css
    ├── main.js
    ├── live2d.js
    ├── vendor/
    │    ├── pixi.min.js
    │    ├── index.min.js
    │    ├── cubism4.min.js
    │    └── live2dcubismcore.min.js
    ├── live2d/
    │    └── 14emu_sports02_t01/
    ├── images/
    │    └── bg_avatar.jpg
    └── audio/
```

---

## ⚠️ Notes

* **g4f** is intended for **research/educational purposes only**. It is unstable and may fail at times.
* For stable use, switch to **Gemini API** or **Ollama (local LLM)**.
* **gTTS** requires internet access and may have a few seconds of delay → the frontend shows `"🤔 Thinking..."` to improve UX.

---

## 📜 License

This project is for **educational / research purposes only**, not for commercial use.

```


