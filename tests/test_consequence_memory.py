import unittest
import os
import json
from core.memory.consequence_memory import store_consequence, query_consequences, MEMORY_FILE

class TestConsequenceMemory(unittest.TestCase):
    def setUp(self):
        # Clear memory file before tests
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)

    def test_store_and_query_coherent(self):
        report = {
            "accion": "seleccionar_objeto",
            "estado": "COHERENTE",
            "parametros": {"nombre": "Cubo"}
        }
        store_consequence(report)
        
        result = query_consequences("seleccionar_objeto")
        self.assertEqual(result["resumen"]["COHERENTE"], 1)
        self.assertEqual(result["total_experiencias"], 1)

    def test_multiple_consequences(self):
        actions = [
            {"accion": "seleccionar_objeto", "estado": "COHERENTE"},
            {"accion": "seleccionar_objeto", "estado": "COHERENTE"},
            {"accion": "seleccionar_objeto", "estado": "FALLO_DE_CONTEXTO"},
            {"accion": "enfocar_objeto", "estado": "INCONSISTENTE"}
        ]
        
        for a in actions:
            store_consequence(a)
            
        # Check seleccionar_objeto
        stats_sel = query_consequences("seleccionar_objeto")
        self.assertEqual(stats_sel["resumen"]["COHERENTE"], 2)
        self.assertEqual(stats_sel["resumen"]["FALLO_DE_CONTEXTO"], 1)
        self.assertEqual(stats_sel["total_experiencias"], 3)
        
        # Check enfocar_objeto
        stats_enf = query_consequences("enfocar_objeto")
        self.assertEqual(stats_enf["resumen"]["INCONSISTENTE"], 1)
        self.assertEqual(stats_enf["total_experiencias"], 1)

    def test_empty_query(self):
        result = query_consequences("accion_inexistente")
        self.assertEqual(result["total_experiencias"], 0)
        self.assertEqual(result["resumen"]["COHERENTE"], 0)

if __name__ == "__main__":
    unittest.main()
