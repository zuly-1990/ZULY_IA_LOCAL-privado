# tests/test_structural_interpreter_v1_1.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.structural_interpreter import StructuralInterpreter

class TestStructuralInterpreterV11(unittest.TestCase):
    def setUp(self):
        self.interpreter = StructuralInterpreter()

    def test_strict_roles(self):
        # Caso sin rol explícito
        text = "Crea un cubo"
        result = self.interpreter.interpret(text)
        self.assertEqual(result["elements"][0]["role"], "undefined")
        
        # Caso con rol explícito
        text = "Un cubo como base"
        result = self.interpreter.interpret(text)
        self.assertEqual(result["elements"][0]["role"], "base")

    def test_missing_parameters_listing(self):
        text = "Crea un cubo de tamaño 2"
        result = self.interpreter.interpret(text)
        el = result["elements"][0]
        self.assertIn("location", el["missing_parameters"])
        self.assertFalse(el["structurally_complete"])
        self.assertFalse(result["structurally_complete"])

    def test_spatial_relations(self):
        text = "Crea un cubo en 0,0,0 y una esfera encima del cubo"
        result = self.interpreter.interpret(text)
        
        self.assertEqual(len(result["elements"]), 2)
        self.assertEqual(len(result["relations"]), 1)
        rel = result["relations"][0]
        self.assertEqual(rel["type"], "encima_de")
        
        # Verificar que los IDs coincidan (sphere_1 suele ser el source en este texto)
        source_id = [el["id"] for el in result["elements"] if el["type"] == "sphere"][0]
        target_id = [el["id"] for el in result["elements"] if el["type"] == "cube"][0]
        self.assertEqual(rel["source"], source_id)
        self.assertEqual(rel["target"], target_id)

    def test_v1_1_schema(self):
        text = "Cubo en 0,0,0"
        result = self.interpreter.interpret(text)
        self.assertEqual(result["version"], "1.1.1")
        self.assertIn("structurally_complete", result)
        self.assertIn("relations", result)
        self.assertIn("missing_parameters", result) # Root level
        self.assertIn("missing_parameters", result["elements"][0]) # Element level
        self.assertFalse(result["executable"])

if __name__ == "__main__":
    unittest.main()
