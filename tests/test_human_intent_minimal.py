"""
Tests Mínimos para Intención Humana (Fase 5.18)
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extensions.knowledge_intake.human_intent import register_intent

class TestHumanIntentMinimal(unittest.TestCase):
    
    def test_register_intent(self):
        """Test: Registro básico de intención devuelve estructura correcta"""
        print("\n[TEST] Registro de Intención Humana")
        
        project = "escena_prueba.blend"
        intent_type = "PRACTICA"
        
        data = register_intent(project, intent_type)
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data["project"], project)
        self.assertEqual(data["intent"], intent_type)
        self.assertEqual(data["source"], "HUMAN_DECLARATION")
        self.assertIn("timestamp", data)
        
        print(f"  ✓ Registro validado: {data}")

if __name__ == '__main__':
    print("="*70)
    print("TEST - HUMAN INTENT (FASE 5.18)")
    print("="*70)
    unittest.main(verbosity=2)
