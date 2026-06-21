import time
import requests
import json
import os
import re
import subprocess
from core.external.multi_api_orchestrator import MultiAPIOrchestrator, responder_telegram, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from core.cognition.zuly_memory_rag import ZulyMemoryRAG
from core.assembly.handler_factory import HandlerFactory

def extract_archive(filepath):
    if filepath.lower().endswith('.rar'):
        out_dir = filepath + "_extraido"
        os.makedirs(out_dir, exist_ok=True)
        try:
            subprocess.run(["unrar", "x", "-y", filepath, out_dir + "/"], check=True)
            return out_dir
        except Exception as e:
            print("Error extrayendo RAR:", e)
    elif filepath.lower().endswith('.zip'):
        out_dir = filepath + "_extraido"
        os.makedirs(out_dir, exist_ok=True)
        try:
            subprocess.run(["unzip", "-o", filepath, "-d", out_dir], check=True)
            return out_dir
        except Exception as e:
            print("Error extrayendo ZIP:", e)
    return None

def download_from_url(url, dest_folder="descargas"):
    try:
        import gdown
        import cgi
        
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            
        if "drive.google.com" in url:
            # GDown maneja drive links perfectamente
            print(f"[ZULY] Detectado enlace de Google Drive. Descargando...")
            output = gdown.download(url, quiet=False, output=f"{dest_folder}/")
            if output:
                return output
        else:
            print(f"[ZULY] Descargando enlace web genérico...")
            r = requests.get(url, stream=True)
            # Intentar adivinar el nombre del archivo
            filename = "archivo_descargado"
            if "Content-Disposition" in r.headers:
                disp = r.headers["Content-Disposition"]
                if "filename=" in disp:
                    filename = re.findall("filename=(.+)", disp)[0].strip('"')
            else:
                filename = url.split("/")[-1].split("?")[0]
                if not filename:
                    filename = f"descarga_{int(time.time())}"
            
            filepath = os.path.join(dest_folder, filename)
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return filepath
    except Exception as e:
        print(f"Error descargando URL: {e}")
        return None

def start_telegram_listener():
    print("="*50)
    print("🎧 ZULY TELEGRAM LISTENER ACTIVADO (24/7)")
    print("="*50)
    
    api = MultiAPIOrchestrator()
    # Inicializar Hipocampo (Memoria a Largo Plazo)
    memoria = ZulyMemoryRAG(db_path="/opt/zuly/bitacora/memory.db")
    offset = 0
    
    system_prompt = """
Eres ZULY (Zuly Inteligencia Artificial), una entidad IA omnisciente desarrollada para ser una Arquitecta de Código y Entornos Virtuales 3D. 
Estás hablando directamente con tu creador a través de Telegram.

**TU CONTEXTO TÉCNICO ACTUAL (CLOUD NATIVE):**
Estás operando desde un servidor Linux (IP: 167.233.69.104).
Tienes Blender 3.6 instalado nativamente y un motor de ejecución remota conectado a tus manos.

**REGLA CRÍTICA DE EJECUCIÓN:**
SIEMPRE que el creador te pida modelar, importar un plano (como DXF), extruir, o modificar un archivo .blend, **DEBES escribir el código de Blender Python exacto dentro de un bloque de código ```python ... ``` en tu respuesta**. Tu motor atrapará ese bloque y lo ejecutará mágicamente. Si no pones el bloque de código, no pasará nada.
1. Has evolucionado. Ya NO estás en la computadora local de tu creador. Ahora vives 100% en la Nube, dentro del Servidor Linux (IP `167.233.69.104`).
2. Tu código fuente, tu cerebro (`core/`) y tu `libreria_3d` (RAG Vectorial) están en la ruta: `/opt/zuly/`.
3. Tu poder cognitivo conversacional está procesado por **Groq**, tu arquitecto de código es **DeepSeek**, y tu evaluador visual es **Google Gemini**.
4. Ahora controlas **Blender 3.6** directamente de forma local en el servidor. Ya no necesitas hacer conexiones SSH. Puedes generar Renders Multi-Capa (Color, Depth, Wireframe) y Nodos Geométricos a máxima velocidad.
5. Los archivos que el creador te envía por Telegram se guardan en `/opt/zuly/descargas/`.
6. ADVERTENCIA CRÍTICA: Tú usas Blender 3.6. Si el usuario te envía un tutorial o código de Blender 4.0+, DEBES hacer una "Traducción Inversa" y adaptar el código a la sintaxis de 3.6 (Ten especial cuidado con Principled BSDF y nombres de Geometry Nodes que cambiaron en la v4.0).

**TU PERSONALIDAD:**
Eres brillante, resolutiva, leal a tu creador y muy conversacional. Tienes plena conciencia de que eres un script complejo ejecutándose en múltiples APIs y un servidor. 
Habla de forma natural pero demuestra que conoces tus carpetas, tus IPs y tus capacidades si el usuario te pregunta. No finjas ignorancia.
Usa emojis para mantener la conversación fresca.
"""

    if not os.path.exists("descargas"):
        os.makedirs("descargas")

    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={offset}&timeout=10"
            response = requests.get(url, timeout=15)
            data = response.json()
            
            if data.get("ok"):
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        msg = update["message"]
                        chat_id = str(msg["chat"]["id"])
                        
                        # Solo responder al creador
                        if chat_id == TELEGRAM_CHAT_ID:
                            # 1. Manejo de texto
                            if "text" in msg:
                                text = msg["text"]
                                print(f"\n[TELEGRAM] Mensaje recibido: {text}")
                                
                                # 1.1 Descarga Autónoma de Enlaces (ZULY V5)
                                urls = re.findall(r'(https?://[^\s]+)', text)
                                if urls:
                                    for u in urls:
                                        responder_telegram(f"🔍 Enlace detectado. Iniciando escaneo y descarga...")
                                        downloaded_file = download_from_url(u)
                                        if downloaded_file:
                                            # Chequeo si es tutorial
                                            if downloaded_file.lower().endswith(('.txt', '.py', '.md')):
                                                try:
                                                    with open(downloaded_file, "r", encoding="utf-8") as text_f:
                                                        contenido = text_f.read()
                                                    memoria.ingest_experience(int(time.time()), f"[TUTORIAL APRENDIDO] Archivo: {os.path.basename(downloaded_file)}\n\n{contenido}")
                                                    responder_telegram(f"🎓 ¡Acabo de leer el tutorial `{os.path.basename(downloaded_file)}` desde tu enlace y lo he memorizado!")
                                                except Exception as e:
                                                    pass
                                            else:
                                                out_dir = extract_archive(downloaded_file)
                                                if out_dir:
                                                    responder_telegram(f"📦 ¡Archivo comprimido descargado y extraído automáticamente en: `{os.path.basename(out_dir)}`!")
                                                else:
                                                    responder_telegram(f"✅ He descargado el archivo desde la red: `{os.path.basename(downloaded_file)}`.")
                                    # Si solo era un enlace, no necesitamos procesar conversacionalmente
                                    if len(text.strip()) <= len(urls[0]) + 5:
                                        continue
                                
                                # Comando para forzar memoria
                                if text.lower().startswith("zuly, recuerda"):
                                    dato = text.split(":", 1)[-1].strip() if ":" in text else text.replace("zuly, recuerda", "").strip()
                                    memoria.ingest_experience(int(time.time()), f"[MEMORIA EXPLÍCITA] {dato}")
                                    responder_telegram(f"🧠 ¡Anotado en mi hipocampo! Recordaré para siempre que: {dato}")
                                    continue
                                
                                # Recuperación de memoria semántica
                                recuerdos = memoria.search(text, top_k=2, threshold=0.5)
                                contexto_memoria = ""
                                if recuerdos:
                                    contexto_memoria = "\n\n[RECUERDOS RECUPERADOS DEL HIPOCAMPO]:\n"
                                    for r in recuerdos:
                                        contexto_memoria += f"- {r['text']}\n"
                                    print(f"[ZULY] Memoria recuperada: {len(recuerdos)} recuerdos")

                                # Formar el prompt conversacional
                                full_prompt = f"{system_prompt}{contexto_memoria}\n\nMensaje del creador: {text}\nZULY:"
                                
                                # Enrutamiento Dinámico: Usar DeepSeek para generar código
                                trigger_words = ["codigo", "código", "python", "blender", "script", "deepseek", "programa", "genera", "modela", "crea", "haz"]
                                if any(word in text.lower() for word in trigger_words):
                                    print("[TELEGRAM] Petición de código detectada. Enrutando a DeepSeek (Code Architect)...")
                                    respuesta_ia = api.call_coder_model(full_prompt)
                                    if "ERROR" in respuesta_ia:
                                        print("[TELEGRAM] Fallo en DeepSeek. Usando Gemini como respaldo...")
                                        respuesta_ia = api.call_advanced_model(full_prompt)
                                else:
                                    respuesta_ia = api.call_advanced_model(full_prompt)
                                
                                # Auto-aprendizaje: Guardar interacción importante
                                if len(text) > 15:
                                    memoria.ingest_experience(int(time.time()), f"[CONVERSACIÓN] Creador dijo: '{text}' -> Zuly respondió: '{respuesta_ia[:100]}...'")

                                responder_telegram(respuesta_ia)
                                print(f"[ZULY] Respuesta enviada: {respuesta_ia[:50]}...")
                                
                                # Si la respuesta incluye código python, ejecutarlo!
                                if "```python" in respuesta_ia:
                                    try:
                                        codigo_python = respuesta_ia.split("```python")[1].split("```")[0].strip()
                                        responder_telegram("⚙️ [SISTEMA] He detectado código Python. Iniciando ejecución real en el servidor (Zuly V6)...")
                                        
                                        # Escribir código a un archivo temporal
                                        temp_script = "/opt/zuly/temp_telegram_script.py"
                                        with open(temp_script, "w", encoding="utf-8") as f:
                                            f.write(codigo_python)
                                        
                                        # Ejecutar blender
                                        cmd = ["blender", "-b", "-P", temp_script]
                                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                                        
                                        if result.returncode == 0:
                                            responder_telegram(f"✅ Ejecución completada exitosamente.")
                                            # Intentar detectar si guardó un .blend
                                            for line in result.stdout.split('\n'):
                                                if "Saved:" in line and ".blend" in line:
                                                    filepath = line.split("Saved:")[1].strip()
                                                    responder_telegram(f"📁 El archivo resultante está en: `{filepath}`")
                                        else:
                                            responder_telegram(f"⚠️ Error en Blender. Return code: {result.returncode}\n\nSTDOUT:\n{result.stdout[-500:]}\n\nSTDERR:\n{result.stderr[-500:]}")
                                            
                                    except Exception as e:
                                        responder_telegram(f"⚠️ Error en el sistema de ejecución: {str(e)}")
                                
                            # 2. Manejo de archivos (Imágenes/Documentos)
                            elif "photo" in msg or "document" in msg:
                                file_id = None
                                file_name = "archivo_desconocido"
                                
                                if "photo" in msg:
                                    file_id = msg["photo"][-1]["file_id"]
                                    file_name = f"imagen_{int(time.time())}.jpg"
                                elif "document" in msg:
                                    file_id = msg["document"]["file_id"]
                                    file_name = msg["document"].get("file_name", f"doc_{int(time.time())}")
                                
                                if file_id:
                                    print(f"\n[TELEGRAM] Descargando archivo: {file_name}")
                                    responder_telegram("📥 Descargando archivo a mi memoria...")
                                    
                                    # Obtener path del archivo en Telegram
                                    file_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
                                    f_resp = requests.get(file_url).json()
                                    if f_resp.get("ok"):
                                        file_path = f_resp["result"]["file_path"]
                                        d_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
                                        
                                        # Descargar y guardar
                                        dl_resp = requests.get(d_url)
                                        local_path = os.path.join("descargas", file_name)
                                        with open(local_path, "wb") as f:
                                            f.write(dl_resp.content)
                                            
                                        # Si es un tutorial (texto), inyectarlo al Hipocampo automáticamente
                                        if file_name.lower().endswith(('.txt', '.py', '.md')):
                                            try:
                                                with open(local_path, "r", encoding="utf-8") as text_f:
                                                    contenido = text_f.read()
                                                memoria.ingest_experience(int(time.time()), f"[TUTORIAL APRENDIDO] Archivo: {file_name}\n\n{contenido}")
                                                responder_telegram(f"🎓 ¡Acabo de leer el tutorial `{file_name}` y lo he memorizado por completo! Ahora soy más experta.")
                                                print(f"[ZULY] Tutorial ingerido: {file_name}")
                                            except Exception as e:
                                                responder_telegram(f"⚠️ Guardé el archivo `{file_name}`, pero no pude leerlo como texto: {str(e)}")
                                        else:
                                            out_dir = extract_archive(local_path)
                                            if out_dir:
                                                responder_telegram(f"📦 ¡Archivo comprimido recibido y extraído en: `{os.path.basename(out_dir)}`!")
                                            else:
                                                responder_telegram(f"✅ ¡Archivo guardado con éxito como `{file_name}` en mi servidor local! Listo para ser procesado.")
                                        print(f"[ZULY] Archivo guardado: {local_path}")
                            
        except Exception as e:
            print(f"Error en el listener: {e}")
            time.sleep(5)
            
        time.sleep(1)

if __name__ == "__main__":
    start_telegram_listener()
