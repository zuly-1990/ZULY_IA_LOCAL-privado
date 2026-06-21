import os
import sys
import time

try:
    from google import genai as google_genai
except ImportError:
    print("Error: google.genai not installed")
    sys.exit(1)

keys = [
    os.environ.get("GEMINI_KEY_1", ""), # Env key
    os.environ.get("GEMINI_KEY_2", ""), # Default 1
    os.environ.get("GEMINI_KEY_3", ""), # Default 2
    os.environ.get("GEMINI_KEY_4", "")  # Default 3
]

models = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

print("=== TESTING KEYS AND MODELS ===")
for i, key in enumerate(keys):
    print(f"\n--- Testing Key #{i+1} ({key[:15]}...) ---")
    try:
        client = google_genai.Client(api_key=key)
        for model in models:
            try:
                print(f"Trying model: {model} ...", end=" ", flush=True)
                response = client.models.generate_content(
                    model=model,
                    contents="Say OK"
                )
                print(f"SUCCESS! Response: {repr(response.text.strip())}")
            except Exception as e:
                err_msg = str(e).replace("\n", " ")
                if "quota" in err_msg.lower() or "limit" in err_msg.lower():
                    print(f"QUOTA ERROR: {err_msg[:120]}...")
                else:
                    print(f"FAILED: {err_msg[:120]}...")
    except Exception as e:
        print(f"Failed to initialize client: {e}")
