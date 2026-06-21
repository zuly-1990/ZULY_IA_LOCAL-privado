import google.generativeai as genai
import sys

import os
api_key = os.environ.get("GEMINI_API_KEY", "")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Hola, di 'API OK' si recibes este mensaje.")
    print("Respuesta de Gemini:", response.text)
except Exception as e:
    print("Error conectando con Gemini:", e)
    sys.exit(1)
