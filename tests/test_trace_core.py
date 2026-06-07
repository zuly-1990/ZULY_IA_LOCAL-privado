import sys
import os
import unittest
import json
import shutil

# Añadir el path raíz para importar core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.memory.trace_core import TraceCore

class TestTraceCore(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/temp_memory"
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file = os.path.join(self.test_dir, "traces.json")
        self.trace_core = TraceCore(storage_path=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_append_and_query_trace(self):
        """Prueba que se pueden registrar y consultar trazas."""
        trace_data = {
            "intention": "CREATE",
            "execution_success": True,
            "explanation": "Cubo creado exitosamente."
        }
        self.trace_core.append_trace(trace_data)
        
        # Recargar para asegurar persistencia
        new_tc = TraceCore(storage_path=self.test_file)
        self.assertEqual(len(new_tc.traces), 1)
        self.assertEqual(new_tc.traces[0]["data"]["intention"], "CREATE")

    def test_query_failures(self):
        """Prueba la consulta de fallos acumulados."""
        self.trace_core.append_trace({"intention": "RENDER", "execution_success": False})
        self.trace_core.append_trace({"intention": "RENDER", "execution_success": False})
        self.trace_core.append_trace({"intention": "RENDER", "execution_success": True})
        
        self.assertEqual(self.trace_core.query_failures("RENDER"), 2)

    def test_needs_human_authorization(self):
        """Prueba si detecta que una acción requiere humano."""
        self.trace_core.append_trace({"intention": "DELETE", "auth_required": True})
        self.assertTrue(self.trace_core.needs_human_authorization("DELETE"))
        self.assertFalse(self.trace_core.needs_human_authorization("CREATE"))

if __name__ == '__main__':
    unittest.main()
