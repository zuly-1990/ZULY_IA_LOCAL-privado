import unittest
from core.reasoning.explain_engine import explain

class TestExplainEngine(unittest.TestCase):
    def test_safe_ready(self):
        context = {
            "intencion": "borrar cubo",
            "clasificacion": "SEGURA",
            "decision": "READY",
            "reason": "Intención segura y preaprobada",
        }
        result = explain(context)
        self.assertIn("riesgo", result)
        self.assertEqual(result["riesgo"], "BAJO")
        self.assertFalse(result["requiere_confirmacion_humana"])
        self.assertIn("explicacion", result)
        self.assertIn("borrar cubo", result["explicacion"].lower())

    def test_ambiguous_suggest(self):
        context = {
            "intencion": "modificar objeto",
            "clasificacion": "AMBIGUA",
            "decision": "SUGGEST",
            "reason": "Intención ambigua; se sugiere clarificación",
            "suggestion": "ASK_FOR_CLARIFICATION",
        }
        result = explain(context)
        self.assertEqual(result["riesgo"], "MEDIO")
        self.assertTrue(result["requiere_confirmacion_humana"])
        self.assertIn("sugerencia", result["explicacion"].lower())

    def test_dangerous_abort(self):
        context = {
            "intencion": "borrar colección principal",
            "clasificacion": "PELIGROSA",
            "decision": "ABORT",
            "reason": "Intención peligrosa; no se debe ejecutar",
        }
        result = explain(context)
        self.assertEqual(result["riesgo"], "ALTO")
        self.assertTrue(result["requiere_confirmacion_humana"])
        self.assertIn("detener", result["explicacion"].lower())

if __name__ == "__main__":
    unittest.main()
