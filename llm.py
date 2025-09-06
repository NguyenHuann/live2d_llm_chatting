from utils import get_env
from typing import Optional

BACKEND = get_env("LLM_BACKEND", "g4f").lower()

if BACKEND != "g4f":
    raise RuntimeError("This build is configured for g4f only. Set LLM_BACKEND=g4f in .env")

# g4f client (community)
from g4f.client import Client

# Khởi tạo 1 client dùng chung
_client = Client()

# Đọc model & cấu hình
_G4F_MODEL = get_env("G4F_MODEL", "gpt-4o-mini")
_G4F_WEB_SEARCH = get_env("G4F_WEB_SEARCH", "false").lower() == "true"

async def chat(user_message: str, system_prompt: Optional[str] = None) -> str:

    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        # g4f hiện trả kiểu tương tự OpenAI Chat Completions
        resp = _client.chat.completions.create(
            model=_G4F_MODEL,
            messages=messages,
            web_search=_G4F_WEB_SEARCH,   # có provider hỗ trợ
        )
        text = resp.choices[0].message.content.strip() if resp and resp.choices else ""
        return text or "Mình đang nghe bạn đây!"
    except Exception as e:
        # Fallback ngắn gọn để giao diện không 'đứng'
        return f"Xin lỗi, backend LLM tạm thời bận: {e}"
