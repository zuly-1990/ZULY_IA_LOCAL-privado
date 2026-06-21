import requests
import os

api_key = os.environ.get("OPENROUTER_API_KEY", "")

headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "https://github.com/ZULY",
    "Content-Type": "application/json"
}
data = {
    "model": "google/gemma-2-9b-it:free",
    "messages": [{"role": "user", "content": "Hola"}]
}
response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
print(response.status_code)
print(response.text)
