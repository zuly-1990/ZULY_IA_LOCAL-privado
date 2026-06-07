# tests/test_structural_interpreter.py
import unittest
import sys
import os

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.structural_interpreter import StructuralInterpreter

class TestStructuralInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = StructuralInterpreter()

    def test_basic_structure(self):
        text = "Crea un cubo de tamaño 2 en 0,0,0"
        result = self.interpreter.interpret(text)
        
        self.assertEqual(len(result["elements"]), 1)
        el = result["elements"][0]
        self.assertEqual(el["type"], "cube")
        self.assertEqual(el["parameters"]["size"], 2.0)
        self.assertEqual(el["parameters"]["location"], [0.0, 0.0, 0.0])
        self.assertTrue(el["is_complete"])
        self.assertFalse(result["executable"])

    def test_missing_parameters(self):
        # Falta ubicación, debe ser executable: false
        text = "Crea un cubo de tamaño 5"
        result = self.interpreter.interpret(text)
        
        self.assertEqual(len(result["elements"]), 1)
        el = result["elements"][0]
        self.assertFalse(el["is_complete"])
        self.assertFalse(result["executable"])

    def test_roles(self):
        text = "Un plano para el suelo en 0,0,-1"
        result = self.interpreter.interpret(text)
        
        el = result["elements"][0]
        self.assertEqual(el["type"], "plane")
        self.assertEqual(el["role"], "base")
        self.assertEqual(el["parameters"]["location"], [0.0, 0.0, -1.0])

    def test_multiple_objects(self):
        text = "Cubo en 0,0,0 y una esfera en 5,5,5"
        result = self.interpreter.interpret(text)
        
        self.assertEqual(len(result["elements"]), 2)
        self.assertEqual(result["elements"][0]["type"], "cube")
        self.assertEqual(result["elements"][1]["type"], "sphere")
        self.assertFalse(result["executable"])

    def test_complex_tutorial_snippet(self):
        text = "Para la base usa un cilindro de radio 2 en 0,0,0. Para el soporte usa otro cilindro de radio 0.2 en 0,0,5"
        result = self.interpreter.interpret(text)
        
        self.assertEqual(len(result["elements"]), 2)
        self.assertEqual(result["elements"][0]["role"], "base")
        self.assertEqual(result["elements"][1]["role"], "support")

if __name__ == "__main__":
    unittest.main()
