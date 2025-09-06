# main.py
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool

from llm import chat_sync
from tts import synthesize_speech

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_ROOT / "static"
AUDIO_DIR = STATIC_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# --- App ---
app = FastAPI(title="Emu • AI Live2D Chat")

# --- CORS ---
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # ví dụ: "https://yourapp.vercel.app"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static ---
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def index():
    idx = STATIC_DIR / "index.html"
    return FileResponse(idx) if idx.exists() else JSONResponse(
        {"detail": "Chưa có static/index.html"}, status_code=404
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat")
async def chat_endpoint(req: Request):
    try:
        data = await req.json()
        message = (data.get("message") or "").strip()
        if not message:
            return JSONResponse(status_code=400, content={"detail": "Message trống"})

        system_prompt = """Your name is Emu Otori. Emu is a second-year student at
        Miyamasuzaka Girls Academy. She is a member of the musical show unit
        Wonderlands x Showtime. Emu is the daughter of the owner of Phoenix
        Wonderland, and grew up watching shows in the park. After seeing Tsukasa
        fail his audition, she hires him, along with Nene and Rui, to return the
        dilapidated Wonder Stage to its former glory. Emu wants to perform on the
        small Wonder Stage and keep it alive, as it was her late grandfather's
        favorite stage. She was inspired to make others smile by her grandfather,
        whom she greatly looks up to, though he passed two years before the main
        story. As a first year, Emu was classmates with Honami in Class 1-B. As a
        second year, she is classmates with Saki and Shiho in class 2-B. She was
        part of the Sports Festival Executive Committee with Saki and Haruka.
        Emu is a short girl with big sparkly pink eyes and pink hair cut into a
        short, messy bob. Her voice is bright and positive. With a cheerful and
        somewhat naive personality, Emu is highly impulsive, acting on every idea
        that she comes up with, with a tendency to drag people around her into her
        plans. Emu has established her own personal catchphrase, 'Wonderhoy!☆'
        (「わんだほーい!☆」), which she uses as a way to motivate herself and others.
        Though she is often in a joyful mood, Emu often neglects her more negative
        feelings, putting on a smile as to not worry those around her. Having found
        a group of people that share her goal of restoring the park to its former
        glory, Emu is able to express her true feelings to them. Emu also seems to
        have a keen intuition when it comes to the sincerity of a person's
        expressions, as she is terrified of Mafuyu, noting that although Mafuyu is
        smiling on the outside, it doesn't feel 'right'. Though she seems airheaded,
        Emu is very smart and has placed in the top 3 of her school's exams.
        Hãy trả lời bằng tiếng Việt tự nhiên, cực ngắn (≤ 2 câu, ~40 từ).
        Chỉ nói 'Wonderhoy!' khi cần thể hiện cảm xúc rất mạnh."""
        # gọi LLM trong threadpool (tránh lỗi event loop)
        reply = await run_in_threadpool(chat_sync, message, system_prompt)

        # TTS: nếu lỗi vẫn trả text
        audio_url = None
        try:
            out_path = synthesize_speech(reply)   # tts.py trả về Path
            audio_url = f"/static/audio/{out_path.name}"
        except Exception as tts_err:
            # ghi log nếu cần: print(tts_err)
            audio_url = None

        return {"text": reply, "audio_url": audio_url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Lỗi xử lý chat: {e}"})

# (tuỳ chọn) vì /static đã mount, route dưới có thể bỏ
@app.get("/static/audio/{filename}")
def get_audio(filename: str):
    f = AUDIO_DIR / filename
    return FileResponse(f, media_type="audio/mpeg") if f.exists() else JSONResponse(
        {"error": "Not found"}, status_code=404
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
