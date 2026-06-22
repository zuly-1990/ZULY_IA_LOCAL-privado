import os
import glob
import json
import requests
from datetime import datetime

# Rutas
LIBRERIA_DIR = "/opt/zuly/libreria_3d/arquitectura"
LOG_FILE = "/opt/zuly/scraper.log"

def get_env_var(filepath, var_name):
    try:
        with open(filepath, "r") as f:
            for line in f:
                if line.startswith(var_name):
                    return line.strip().split("=")[1].strip('"').strip("'")
    except Exception:
        pass
    return None

def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error enviando telegram: {e}")

def main():
    # Cargar secretos
    token = get_env_var("/opt/zuly/.env", "TELEGRAM_TOKEN")
    chat_id = get_env_var("/opt/zuly/.env", "TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("No se encontraron credenciales de Telegram.")
        return

    # Contar modelos aprobados
    blend_files = glob.glob(os.path.join(LIBRERIA_DIR, "*.blend"))
    total_aprobados = len(blend_files)
    
    # Extraer estadisticas del log (rechazos, pesos)
    rechazados = 0
    saltados = 0
    hoy = datetime.now().strftime("%Y-%m-%d")
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
            lineas = f.readlines()
            # Como es un reporte simple, contaremos las palabras clave historicas o del ultimo dia
            for linea in lineas:
                if "RECHAZADO por DeepSeek" in linea:
                    rechazados += 1
                elif "Saltando" in linea and "pesa demasiado" in linea:
                    saltados += 1

    # Construir informe
    informe = f"""🏛 <b>Reporte Diario de Aprendizaje: Zuly V6</b> 🏛

¡Hola Arquitecta! Aquí está mi informe de estudio automático:

✅ <b>Modelos Aprendidos y Aprobados:</b> {total_aprobados}
❌ <b>Modelos Rechazados por DeepSeek:</b> {rechazados} (Basura geométrica)
⚠️ <b>Modelos Saltados por Peso (>30MB):</b> {saltados}

<i>Sigo ejecutando mi ciclo de estudio en el servidor Linux 24/7. ¡Nos vemos mañana!</i> 🚀"""

    send_telegram_message(token, chat_id, informe)
    print("Informe diario enviado con éxito.")

if __name__ == "__main__":
    main()
