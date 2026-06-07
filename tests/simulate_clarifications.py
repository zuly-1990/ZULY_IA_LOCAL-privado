
import os
import json
from core.utils.transcription_evaluator import evaluate_transcription
from core.dialog.cognitive_risk_explainer import CognitiveRiskExplainer
from core.dialog.clarification_question_generator import ClarificationQuestionGenerator
from datetime import datetime

# Carpeta de transcripciones de prueba
TRANSCRIPTION_DIR = "tests/transcriptions"
REPORT_FILE = "transcription_clarification_simulation.json"
BITACORA_FILE = "bitacora/ACLARACIONES_AUTOMATICAS.md"
reporte = {}

# Inicializar generadores de aclaraciones
clarifier = ClarificationQuestionGenerator()
risk_explainer = CognitiveRiskExplainer()

# Preparar bitácora si no existe
if not os.path.exists(BITACORA_FILE):
    with open(BITACORA_FILE, "w", encoding="utf-8") as f:
        f.write("# BITÁCORA DE ACLARACIONES AUTOMÁTICAS\n\n")
        f.write("| Timestamp | Archivo | Paso Ambiguo | Pregunta Generada | Riesgo |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")

for filename in os.listdir(TRANSCRIPTION_DIR):
    if filename.endswith(".txt") or filename.endswith(".py"):
        path = os.path.join(TRANSCRIPTION_DIR, filename)
        print(f"Simulando aclaraciones para: {filename}")
        
        # Evaluar transcripción
        resultado = evaluate_transcription(path)
        
        # Generar preguntas de aclaración para pasos ambiguos
        aclaraciones = []
        ambiguous_steps = resultado.get("ambiguous_steps", [])
        
        for paso in ambiguous_steps:
            pregunta = clarifier.generate_question(paso)
            aclaraciones.append(pregunta)
            
            # Registrar en bitácora MD
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            paso_texto = paso.get("original_segment", "N/A").replace("|", "-")
            pregunta_clean = pregunta.replace("|", "-")
            riesgo = resultado.get("confidence_level", "URGENTE")
            
            with open(BITACORA_FILE, "a", encoding="utf-8") as f:
                f.write(f"| {timestamp} | {filename} | {paso_texto} | {pregunta_clean} | {riesgo} |\n")
        
        # Explicación de riesgos
        riesgos = risk_explainer.explain(resultado)
        
        # Guardar en reporte JSON
        reporte[filename] = {
            "confianza": resultado.get("confidence_level"),
            "aclaraciones": aclaraciones,
            "riesgos": riesgos
        }

# Guardar reporte final JSON
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    json.dump(reporte, f, indent=4, ensure_ascii=False)

print(f"\n✅ Simulación completada. Reporte guardado en: {REPORT_FILE}")
print(f"✅ Bitácora actualizada en: {BITACORA_FILE}")
