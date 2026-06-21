import requests
import json

api_key = "sk-142d07e242ec48fe9a9195cc04dc447b"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}

try:
    print("Consultando saldo de DeepSeek...")
    response = requests.get("https://api.deepseek.com/user/balance", headers=headers, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        if "balance_infos" in data:
            print("✅ LLAVE VÁLIDA. Información de saldo:")
            for info in data["balance_infos"]:
                print(f"Moneda: {info.get('currency')} | Saldo Total: {info.get('total_balance')} | Saldo Concedido: {info.get('granted_balance')}")
        else:
            print("✅ LLAVE VÁLIDA. (Estructura de saldo diferente)")
            print(json.dumps(data, indent=2))
            
        # Prueba rápida de chat por si acaso el endpoint de balance cambió
        print("\nRealizando prueba rápida de generación...")
        chat_data = {
            "model": "deepseek-coder",
            "messages": [{"role": "user", "content": "hola"}],
            "max_tokens": 5
        }
        chat_resp = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=chat_data, timeout=15)
        if chat_resp.status_code == 200:
            print("✅ PRUEBA DE GENERACIÓN EXITOSA.")
        else:
            print(f"❌ ERROR EN GENERACIÓN: {chat_resp.status_code} - {chat_resp.text}")
            
    else:
        print(f"❌ ERROR AL CONSULTAR SALDO: {response.status_code}")
        print(response.text)
except Exception as e:
    print("Error de conexión:", e)
