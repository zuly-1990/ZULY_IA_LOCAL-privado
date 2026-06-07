# tests/test_transcription_processor.py
import unittest
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.utils.transcription_processor import TranscriptionProcessor

class TestTranscriptionProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = TranscriptionProcessor()

    def test_cleaning(self):
        text = "Eh bueno, mira, crea un cubo ok"
        cleaned = self.processor.clean_text(text)
        self.assertNotIn("eh", cleaned)
        self.assertNotIn("bueno", cleaned)
        self.assertNotIn("mira", cleaned)
        self.assertNotIn("ok", cleaned)
        self.assertIn("crea un cubo", cleaned)

    def test_segmentation(self):
        text = "Primero haz un cubo. Luego una esfera. Paso 2: escala todo."
        steps = self.processor.segment_didactic_steps(text)
        self.assertGreaterEqual(len(steps), 3)
        self.assertIn("haz un cubo", steps[0])
        self.assertIn("una esfera", steps[1])

    def test_full_report_generation(self):
        text = "Primero crea un cilindro como soporte en 0,0,0. Luego pon un plano debajo del cilindro."
        report = self.processor.process_transcription(text)
        
        self.assertEqual(report["steps_count"], 2)
        self.assertEqual(report["steps"][0]["structural_map"]["elements"][0]["type"], "cylinder")
        self.assertEqual(report["steps"][0]["structural_map"]["elements"][0]["role"], "support")
        
        # Verificar relaciones espaciales en el flujo
        rel_found = False
        for step in report["steps"]:
            if len(step["structural_map"]["relations"]) > 0:
                rel_found = True
                break
        self.assertTrue(rel_found)

    def test_structural_warnings_in_transcript(self):
        # Un soporte sin nada que soportar (en el mismo segmento)
        text = "Crea un cilindro como soporte"
        report = self.processor.process_transcription(text)
        self.assertTrue(len(report["global_warnings"]) > 0)
        self.assertIn("incoherencia lógica", report["global_warnings"][0].lower())

if __name__ == "__main__":
    unittest.main()
