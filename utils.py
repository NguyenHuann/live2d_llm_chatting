import os, uuid
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_DIR   = PROJECT_ROOT / "static"
AUDIO_DIR    = STATIC_DIR / "audio"

# Load .env at import time so other modules reading env vars work immediately
load_dotenv(PROJECT_ROOT / ".env")

def init_env_and_dirs():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def get_env(key: str, default: str | None = None) -> str:
    val = os.getenv(key, default)
    if val is None:
        raise RuntimeError(f"Missing env var: {key}")
    return val

def new_audio_filename(ext: str = "mp3") -> str:
    return f"{uuid.uuid4().hex[:12]}.{ext}"

def is_valid_audio(path: Path) -> bool:
    try:
        return path.exists() and path.stat().st_size > 128  # >128B coi như hợp lệ
    except Exception:
        return False
