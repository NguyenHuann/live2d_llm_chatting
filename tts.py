from pathlib import Path
from gtts import gTTS
from utils import get_env, new_audio_filename, AUDIO_DIR, is_valid_audio

def synthesize_speech(text: str) -> Path:
    lang = get_env("GTTS_LANG", "vi")
    slow = get_env("GTTS_SLOW", "false").lower() == "true"

    final = AUDIO_DIR / new_audio_filename("mp3")
    tmp   = final.with_suffix(".tmp")

    # tạo MP3 tạm
    tts = gTTS(text=text, lang=lang, slow=slow)
    tts.save(str(tmp))

    # xác thực & đổi tên atomically
    if not is_valid_audio(tmp):
        tmp.unlink(missing_ok=True)
        raise RuntimeError("gTTS tạo file âm thanh rỗng hoặc lỗi.")

    tmp.replace(final)
    return final
