import unittest
import os
from core.feedback.result_observer import observe_result, LOG_FILE

class TestResultObserver(unittest.TestCase):
    def test_coherent_observation(self):
        execution_report = {
            "accion": "seleccionar_objeto",
            "resultado_esperado": {"objeto_seleccionado": "Cubo"}
        }
        current_context = {
            "active_object": "Cubo",
            "existing_objects": ["Cubo", "Luz", "Camara"]
        }
        result = observe_result(execution_report, current_context)
        self.assertEqual(result["estado"], "COHERENTE")
        self.assertTrue(result["verificacion"])
        self.assertFalse(result["requiere_intervencion_humana"])

    def test_context_failure(self):
        execution_report = {
            "accion": "seleccionar_objeto",
            "resultado_esperado": {"objeto_seleccionado": "Esfera"}
        }
        current_context = {
            "active_object": None,
            "existing_objects": ["Cubo"]
        }
        result = observe_result(execution_report, current_context)
        self.assertEqual(result["estado"], "FALLO_DE_CONTEXTO")
        self.assertFalse(result["verificacion"])
        self.assertTrue(result["requiere_intervencion_humana"])

    def test_inconsistent_observation(self):
        execution_report = {
            "accion": "seleccionar_objeto",
            "resultado_esperado": {"objeto_seleccionado": "Cubo"}
        }
        current_context = {
            "active_object": "Luz",
            "existing_objects": ["Cubo", "Luz"]
        }
        result = observe_result(execution_report, current_context)
        self.assertEqual(result["estado"], "INCONSISTENTE")
        self.assertFalse(result["verificacion"])
        self.assertTrue(result["requiere_intervencion_humana"])

if __name__ == "__main__":
    unittest.main()
