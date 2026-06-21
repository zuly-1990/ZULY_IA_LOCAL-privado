import os
import requests

def test_openrouter():
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/ZULY", # Requerido por OpenRouter
        "X-Title": "ZULY AI", # Opcional
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek/deepseek-coder",
        "messages": [
            {"role": "user", "content": "Escribe una línea de código en Python que imprima 'API Conectada'"}
        ]
    }
    
    try:
        print("Probando conexión a OpenRouter...")
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=15)
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        print("✅ CONEXIÓN EXITOSA!")
        print("Respuesta del modelo:", content)
    except Exception as e:
        print("❌ ERROR DE CONEXIÓN:")
        print(e)
        if hasattr(e, 'response') and e.response is not None:
            print("Detalles del error:", e.response.text)

if __name__ == "__main__":
    test_openrouter()
