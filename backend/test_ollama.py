import json
import time
import requests

URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:0.5b"

messages = [
    {"role": "user", "content": "Reply with exactly: OK"}
]

payload = {
    "model": MODEL,
    "messages": messages,
    "stream": True,
    "options": {
        "temperature": 0.0,
        "num_predict": 5  # hard cap output tokens (speed)
    }
}

print("Sending request to Ollama...")
start = time.time()

with requests.post(URL, json=payload, stream=True, timeout=(10, None)) as r:
    r.raise_for_status()
    text = ""
    for line in r.iter_lines(decode_unicode=True):
        if not line:
            continue
        data = json.loads(line)
        # chat streaming chunks come in message.content
        msg = data.get("message", {})
        chunk = msg.get("content", "")
        if chunk:
            text += chunk
            print(chunk, end="", flush=True)
        if data.get("done"):
            break

print(f"\nDone in {time.time()-start:.2f}s")
print("Final:", repr(text.strip()))