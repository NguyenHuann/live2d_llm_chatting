from typing import Optional
from g4f.client import Client
from utils import get_env
import time

# Cấu hình từ .env (có giá trị mặc định an toàn cho nghiên cứu)
G4F_MODEL = get_env("G4F_MODEL", "gpt-4o-mini")
G4F_WEB_SEARCH = (get_env("G4F_WEB_SEARCH", "false").lower() == "true")

_client = Client()

def chat_sync(user_message: str, system_prompt: Optional[str] = None, retries: int = 1) -> str:
    """
    Gọi g4f đồng bộ. Dùng cho FastAPI thông qua run_in_threadpool.
    Trả về chuỗi văn bản (đã strip).
    """
    if not user_message:
        return "Bạn muốn hỏi gì nè?"

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    last_err = None
    for attempt in range(retries + 1):
        try:
            resp = _client.chat.completions.create(
                model=G4F_MODEL,
                messages=messages,
                web_search=G4F_WEB_SEARCH,
            )
            text = resp.choices[0].message.content.strip()
            # Hậu kỳ nhẹ: giới hạn tối đa khoảng 2 câu/ ~40-60 từ cho nhanh
            if len(text) > 600:
                text = text[:600].rsplit(" ", 1)[0] + "…"
            return text or "Mình đang nghe bạn đây!"
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(0.2)  # backoff ngắn
    return f"Xin lỗi, backend LLM tạm thời bận: {last_err}"
