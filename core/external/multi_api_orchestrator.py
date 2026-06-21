import os
import requests
import json
import time
from typing import Dict, Any, Optional
from core.utils.logging import log_info, log_error

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

def enviar_alerta_telegram(mensaje: str):
    """Envía un mensaje de alerta al celular del usuario vía Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": f"🚨 *ZULY ALERT*\n\n{mensaje}", "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def responder_telegram(mensaje: str):
    """Envía una respuesta conversacional normal al usuario vía Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def enviar_imagen_telegram(ruta_imagen: str, caption: str = "Render completado"):
    """Envía un render (imagen) al celular del usuario vía Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    try:
        with open(ruta_imagen, "rb") as f:
            requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption}, files={"photo": f}, timeout=15)
    except:
        pass

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

# Nuevo SDK google.genai (reemplaza al deprecado google.generativeai)
try:
    from google import genai as google_genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

class MultiAPIOrchestrator:
    """
    Gestiona múltiples proveedores de IA para optimizar costos y velocidad.
    Permite escalar desde modelos rápidos (Groq/Llama) hasta modelos complejos (Gemini/Claude).
    """
    def __init__(self):
        # Configuración Groq
        groq_key = os.environ.get("GROQ_API_KEY", "")
        self.groq_client = Groq(api_key=groq_key) if HAS_GROQ else None
        
        # Configuracion Gemini con nuevo SDK google.genai
        self.gemini_ready = False
        default_gemini_keys_list = [
            os.environ.get("GEMINI_KEY_1", ""),
            os.environ.get("GEMINI_KEY_2", ""),
            os.environ.get("GEMINI_KEY_3", "")
        ]
        env_key = os.environ.get("GEMINI_API_KEY")
        keys_set = []
        if env_key:
            for k in env_key.split(","):
                if k.strip() and k.strip() not in keys_set:
                    keys_set.append(k.strip())
        for k in default_gemini_keys_list:
            if k not in keys_set:
                keys_set.append(k)
        
        self.gemini_keys = keys_set
        self.current_gemini_key_index = 0
        self.gemini_model_name = "gemini-2.5-flash"

        if HAS_GEMINI and self.gemini_keys:
            try:
                self.gemini_client = google_genai.Client(api_key=self.gemini_keys[0])
                self.gemini_ready = True
                log_info(f"[NUEVO SDK] google.genai conectado con {len(self.gemini_keys)} llave(s). Modelo: {self.gemini_model_name}")
            except Exception as e:
                log_error(f"Error configurando nuevo SDK Gemini: {e}")
                
        # Configuración OpenRouter (Arquitecto de Código)
        self.deepseek_ready = False
        self.deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if self.deepseek_key:
            self.deepseek_ready = True
            log_info("DeepSeek API conectada como Arquitecto de Código.")

    def call_coder_model(self, prompt: str) -> str:
        """Llama a DeepSeek Coder para generar código avanzado de Blender"""
        log_info("Usando DeepSeek (Code Architect)...")
        if not self.deepseek_ready:
            return "ERROR: DeepSeek no configurado."
            
        try:
            import requests
            headers = {
                "Authorization": f"Bearer {self.deepseek_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-coder",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4000
            }
            response = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            log_error(f"Error en DeepSeek API: {e}")
            enviar_alerta_telegram(f"🚨 La API de *DeepSeek* falló.\nError: `{e}`")
            return "ERROR_DEEPSEEK_API"

    def call_fast_model(self, prompt: str) -> str:
        """Llama a un modelo ultrarrápido y gratuito (Ej. Groq + Llama 3)"""
        # Intentamos primero con Groq (Llama 3 8B)
        if HAS_GROQ and self.groq_client:
            try:
                log_info("[LYZU] Usando Groq (Fast Logic)...")
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant",
                    temperature=0.0
                )
                return response.choices[0].message.content
            except Exception as e:
                log_error(f"Error en Groq API: {e}")
                enviar_alerta_telegram(f"Groq fallo. Error: {e}")
                # Fallback a Gemini si Groq falla
                log_info("[LYZU] Groq fallo, usando Gemini como fallback...")
                return self.call_advanced_model(prompt)
        
        # Si no hay Groq disponible, usamos Gemini directamente
        log_info("[LYZU] Groq no disponible, usando Gemini para Fast Logic...")
        return self.call_advanced_model(prompt)

    def call_advanced_model(self, prompt: str, attempt=1) -> str:
        """Llama a Gemini 2.0 Flash con el nuevo SDK google.genai (1500 req/dia free tier)"""
        import time
        log_info(f"[NUEVO SDK] gemini-2.0-flash | Intento {attempt} | Llave #{self.current_gemini_key_index + 1}/{len(self.gemini_keys)}")
        if not self.gemini_ready:
            log_error("Gemini no configurado.")
            return "ERROR_ADVANCED_API: GEMINI_NOT_CONFIGURED"

        try:
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            log_error(f"[DIAGNOSTICO GEMINI] Fallo llamado a API. Error: {e}")
            error_str = str(e).lower()
            # Rotar llave en cualquier error de quota, rate limit o 429
            if ("quota" in error_str or "rate" in error_str or "429" in error_str or "resource_exhausted" in error_str):
                if attempt <= len(self.gemini_keys):
                    self.current_gemini_key_index = (self.current_gemini_key_index + 1) % len(self.gemini_keys)
                    new_key = self.gemini_keys[self.current_gemini_key_index]
                    log_info(f"Cuota agotada. Rotando a llave #{self.current_gemini_key_index + 1}: {new_key[:20]}...")
                    try:
                        self.gemini_client = google_genai.Client(api_key=new_key)
                        time.sleep(3)
                        return self.call_advanced_model(prompt, attempt + 1)
                    except Exception as ex:
                        log_error(f"Error rotando llave Gemini: {ex}")
                else:
                    # Si ya rotamos todas las llaves, intentamos usar gemini-1.5-flash como fallback
                    if self.gemini_model_name == "gemini-2.5-flash":
                        log_info("Rotando a modelo gemini-1.5-flash como fallback...")
                        self.gemini_model_name = "gemini-1.5-flash"
                        self.current_gemini_key_index = 0
                        self.gemini_client = google_genai.Client(api_key=self.gemini_keys[0])
                        return self.call_advanced_model(prompt, 1)
                    elif self.gemini_model_name == "gemini-1.5-flash" and self.deepseek_ready:
                        # Fallback de emergencia a DeepSeek Coder
                        log_info("Gemini agotado, usando DeepSeek Coder como fallback de emergencia...")
                        res = self.call_coder_model(prompt)
                        if res and not res.startswith("ERROR"):
                            return res
                            
                    log_error("Todas las llaves y modelos agotaron cuota. Esperando 15s y reintentando...")
                    time.sleep(15)
                    self.gemini_model_name = "gemini-2.5-flash"
                    self.current_gemini_key_index = 0
                    self.gemini_client = google_genai.Client(api_key=self.gemini_keys[0])
                    return self.call_advanced_model(prompt, 1)

            log_error(f"Error Gemini API (no tratado como quota): {e}")
            return f"ERROR_ADVANCED_API: {e}"

    def analyze_image_with_vision(self, prompt: str, image_path: str) -> str:
        """Llama a Gemini Vision para evaluar un render"""
        if not self.gemini_ready:
            return "ERROR: Gemini Vision no configurado."
        try:
            import PIL.Image
            img = PIL.Image.open(image_path)
            # Con el nuevo SDK, vision se llama igual pero con lista de contenidos
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model_name,
                contents=[prompt, img]
            )
            return response.text
        except Exception as e:
            log_error(f"Error en Gemini Vision analizando {image_path}: {e}")
            return f"ERROR_VISION: {e}"

    def process_with_best_api(self, prompt: str, route: str) -> str:
        """Elige la API basandose en la ruta sugerida por el ConfidenceRouter"""
        if route == 'reinforce':
            return self.call_fast_model(prompt)
        else:
            return self.call_advanced_model(prompt)

