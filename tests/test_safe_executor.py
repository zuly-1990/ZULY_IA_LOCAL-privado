import unittest
import os
from core.execution.safe_executor import execute, LOG_FILE

class TestSafeExecutor(unittest.TestCase):
    def setUp(self):
        # Clear log file before tests if it exists
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)

    def test_unauthorized_action(self):
        request = {
            "accion_autorizada": False,
            "accion": "seleccionar_objeto",
            "parametros": {"nombre": "Cubo"},
            "origen_confirmacion": "humano"
        }
        result = execute(request)
        self.assertEqual(result["estado"], "BLOQUEADO")
        self.assertIn("no autorizada", result["motivo"].lower())
        self.assertTrue(os.path.exists(LOG_FILE))

    def test_not_in_whitelist(self):
        request = {
            "accion_autorizada": True,
            "accion": "borrar_cubo",
            "parametros": {"nombre": "Cubo"},
            "origen_confirmacion": "humano"
        }
        result = execute(request)
        self.assertEqual(result["estado"], "BLOQUEADO")
        self.assertIn("lista blanca", result["motivo"].lower())

    def test_invalid_origin(self):
        request = {
            "accion_autorizada": True,
            "accion": "seleccionar_objeto",
            "parametros": {"nombre": "Cubo"},
            "origen_confirmacion": "sistema"
        }
        result = execute(request)
        self.assertEqual(result["estado"], "BLOQUEADO")
        self.assertIn("origen humano", result["motivo"].lower())

    def test_valid_action(self):
        request = {
            "accion_autorizada": True,
            "accion": "seleccionar_objeto",
            "parametros": {"nombre": "Cubo"},
            "origen_confirmacion": "humano"
        }
        result = execute(request)
        self.assertEqual(result["estado"], "ACCION_EJECUTADA")
        self.assertEqual(result["resultado"], "OK")
        self.assertTrue(result["reversible"])
        self.assertIn("registro_id", result)
        
        # Verify log entry
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log_content = f.read()
            self.assertIn("ACCION: seleccionar_objeto", log_content)
            self.assertIn("RESULTADO: OK", log_content)

if __name__ == "__main__":
    unittest.main()
