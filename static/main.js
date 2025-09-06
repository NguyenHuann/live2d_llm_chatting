const messages = document.getElementById("messages");
const msgInput = document.getElementById("msg");
const sendBtn = document.getElementById("send");
const voice = document.getElementById("voice");

function addMessage(sender, text, isPending = false) {
  const div = document.createElement("div");
  div.className = `msg ${sender}`;
  div.textContent = text;
  if (isPending) div.dataset.pending = "true"; // đánh dấu để thay thế sau
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return div;
}

async function sendMessage() {
  const text = msgInput.value.trim();
  if (!text) return;

  // user message
  addMessage("user", text);
  msgInput.value = "";

  // bot placeholder
  const placeholder = addMessage("bot", "🤔 Thinking...", true);

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    const data = await res.json();

    // update placeholder
    placeholder.textContent = data.text || "❌ Lỗi AI không phản hồi";
    delete placeholder.dataset.pending;

    // play audio nếu có
    if (data.audio_url) {
      voice.src = data.audio_url;
      voice.play().catch(err => console.warn("Audio play error:", err));
    }
  } catch (err) {
    placeholder.textContent = "❌ Lỗi server!";
    delete placeholder.dataset.pending;
  }
}

sendBtn.addEventListener("click", sendMessage);
msgInput.addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});
