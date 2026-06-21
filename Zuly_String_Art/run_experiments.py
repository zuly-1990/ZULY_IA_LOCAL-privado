import subprocess
import re

ORIGINAL_IMAGE = r"C:\Users\Admin\.gemini\antigravity\brain\c39cd392-d7db-4d2c-875e-6664c3cb2a95\portrait_for_string_art_1782063089154.png"

experiments = [
    {"id": "intento_1", "pins": 250, "lines": 1500},
    {"id": "intento_2", "pins": 300, "lines": 2500},
    {"id": "intento_3", "pins": 350, "lines": 3500}
]

best_score = -1
best_id = ""

for exp in experiments:
    print(f"--- Ejecutando {exp['id']} ({exp['pins']} clavos, {exp['lines']} líneas) ---")
    
    # 1. Run algorithm
    subprocess.run(["python", "string_art_algorithm.py", str(exp['pins']), str(exp['lines']), exp['id']])
    
    # 2. Run auditor
    generated_img = f"string_art_{exp['id']}.png"
    result = subprocess.run(["python", "string_art_auditor.py", ORIGINAL_IMAGE, generated_img], capture_output=True, text=True)
    print(result.stdout)
    
    # Extract score
    match = re.search(r"Auditor_Score:\s*([0-9.]+)%", result.stdout)
    if match:
        score = float(match.group(1))
        if score > best_score:
            best_score = score
            best_id = exp['id']

print(f"==================================================")
print(f"🏆 EL GANADOR ES: {best_id} con {best_score:.2f}% de precisión!")
print(f"==================================================")
print(f"El intento ganador es el que se enviará al servidor para generar el modelo BIM.")

# Escribir el ganador a un archivo para que el script maestro sepa cuál subir
with open("best_attempt.txt", "w") as f:
    f.write(best_id)
