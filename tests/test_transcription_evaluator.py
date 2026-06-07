# tests/test_transcription_evaluator.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.utils.transcription_evaluator import TranscriptionEvaluator
from core.utils.transcription_processor import TranscriptionProcessor

class TestTranscriptionEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = TranscriptionEvaluator()
        self.processor = TranscriptionProcessor()

    def test_clarity_scoring(self):
        # Texto claro
        self.assertEqual(self.evaluator.evaluate_step_clarity("Crea un cubo en 0,0,0"), 1.0)
        # Texto ambiguo
        ambiguous = "Crea un cubo un poco más o menos por ahí"
        score = self.evaluator.evaluate_step_clarity(ambiguous)
        self.assertLess(score, 1.0)
        self.assertGreaterEqual(score, 0.0)

    def test_technical_gap_detection(self):
        # Objeto sin ubicación ni relación
        report = self.processor.process_transcription("Crea un cilindro")
        gaps = self.evaluator.detect_technical_gaps(report["steps"][0])
        self.assertTrue(any("no tiene ubicación" in g.lower() for g in gaps))

    def test_confidence_levels(self):
        # Tutorial de Alta Confianza
        high_text = "Primero crea un cubo en 0,0,0. Luego escala el cubo a 2."
        high_report = self.processor.process_transcription(high_text)
        self.assertEqual(high_report["confidence_level"], "ALTO")

        # Tutorial de Baja Confianza
        low_text = "Crea un cubo un poco por ahí quizás."
        low_report = self.processor.process_transcription(low_text)
        self.assertEqual(low_report["confidence_level"], "BAJO")

if __name__ == "__main__":
    unittest.main()
