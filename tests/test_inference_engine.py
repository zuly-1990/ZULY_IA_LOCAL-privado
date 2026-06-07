import unittest
from core.reasoning.inference_engine import infer_risk

class TestInferenceEngine(unittest.TestCase):
    def test_low_risk(self):
        memory_summary = {
            "resumen": {
                "COHERENTE": 5,
                "FALLO_DE_CONTEXTO": 0,
                "INCONSISTENTE": 0
            }
        }
        result = infer_risk("seleccionar_objeto", memory_summary)
        self.assertEqual(result["juicio"], "BAJO_RIESGO")
        self.assertIn("mayoritariamente coherente", result["explicacion"])
        self.assertFalse(result["accion_ejecutada"])

    def test_moderate_risk(self):
        memory_summary = {
            "resumen": {
                "COHERENTE": 5,
                "FALLO_DE_CONTEXTO": 0,
                "INCONSISTENTE": 1
            }
        }
        result = infer_risk("seleccionar_objeto", memory_summary)
        self.assertEqual(result["juicio"], "RIESGO_MODERADO")
        self.assertIn("inconsistencias", result["explicacion"])
        self.assertIn("confirmación humana", result["recomendacion"])

    def test_high_risk(self):
        memory_summary = {
            "resumen": {
                "COHERENTE": 1,
                "FALLO_DE_CONTEXTO": 2,
                "INCONSISTENTE": 0
            }
        }
        result = infer_risk("seleccionar_objeto", memory_summary)
        self.assertEqual(result["juicio"], "ALTO_RIESGO")
        self.assertIn("previos superan", result["explicacion"])
        self.assertIn("Abortar", result["recomendacion"])

if __name__ == "__main__":
    unittest.main()
