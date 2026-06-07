import unittest
from core.reasoning.resolution_engine import resolve, DECISION_READY, DECISION_SUGGEST, DECISION_ABORT

class TestResolutionEngine(unittest.TestCase):
    def test_ready_decision(self):
        report = {"clasificacion": "SEGURA", "requiere_permiso_humano": False}
        result = resolve(report)
        self.assertEqual(result["decision"], DECISION_READY)
        self.assertIn("Intención segura", result["reason"])
        self.assertNotIn("suggestion", result)

    def test_suggest_decision(self):
        report = {"clasificacion": "AMBIGUA", "requiere_permiso_humano": True}
        result = resolve(report)
        self.assertEqual(result["decision"], DECISION_SUGGEST)
        self.assertIn("sugerencia", result["reason"].lower())
        self.assertEqual(result.get("suggestion"), "ASK_FOR_CLARIFICATION")

    def test_abort_decision(self):
        report = {"clasificacion": "PELIGROSA", "requiere_permiso_humano": True}
        result = resolve(report)
        self.assertEqual(result["decision"], DECISION_ABORT)
        self.assertIn("peligrosa", result["reason"].lower())
        self.assertNotIn("suggestion", result)

if __name__ == "__main__":
    unittest.main()
