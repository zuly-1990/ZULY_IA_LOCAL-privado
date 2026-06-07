import sys
import os
import traceback

sys.path.append('.')

try:
    from core.utils.transcription_processor import TranscriptionProcessor
    from core.utils.transcription_evaluator import TranscriptionEvaluator
    
    p = TranscriptionProcessor()
    text = "Primero crea un cubo en 0,0,0. Luego escala el cubo a 2."
    report = p.process_transcription(text)
    print("SUCCESS")
except Exception:
    traceback.print_exc()
