# tests/test_structural_validation.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.structural_interpreter import StructuralInterpreter

class TestStructuralValidation(unittest.TestCase):
    def setUp(self):
        self.interpreter = StructuralInterpreter()

    def test_orphaned_relation_warning(self):
        # Texto que induce a error: menciona una relación con algo que no existe o no se detectó
        text = "Crea un cubo en 0,0,0. Pon algo encima de la esfera." 
        # (Aquí solo debería detectar el cubo, pero al buscar 'encima de' podría intentar vincular 
        # si hubiera una esfera. Forzamos la lógica manual de validación)
        
        result = self.interpreter.interpret(text)
        
        # Simulamos una relación huérfana inyectada (o provocada por un error de detección)
        result["relations"].append({"type": "encima_de", "source": "unknown_id", "target": "cube_1"})
        
        # Volvemos a validar para ver si detecta el 'unknown_id'
        from core.structural_interpreter import StructuralValidator
        warnings = StructuralValidator.validate(result)
        
        self.assertTrue(any("Relación huérfana" in w for w in warnings))

    def test_logical_inconsistency_warning(self):
        # Definir algo como soporte pero sin relaciones que lo usen
        text = "Un cilindro como soporte en 0,0,0"
        result = self.interpreter.interpret(text)
        
        self.assertTrue(any("incoherencia lógica" in w.lower() for w in result["warnings"]))
        self.assertTrue(any("support" in w.lower() for w in result["warnings"]))

if __name__ == "__main__":
    unittest.main()
