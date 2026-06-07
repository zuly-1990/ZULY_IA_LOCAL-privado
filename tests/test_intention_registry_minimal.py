"""
Tests Mínimos para IntentionRegistry - Fase 5.18 (Oficial)
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.intention.intention_registry import IntentionRegistry

class TestIntentionRegistryMinimal(unittest.TestCase):
    
    def setUp(self):
        self.registry = IntentionRegistry()
    
    def test_registry_structure(self):
        """Test: Estructura de salida correcta"""
        print("\n[TEST] Estructura de Registro")
        result = self.registry.register("proyecto.blend", "Intención válida")
        
        self.assertEqual(result["project"], "proyecto.blend")
        self.assertEqual(result["intention"], "Intención válida")
        self.assertEqual(result["source"], "HUMAN_DECLARATION")
        self.assertIn("timestamp", result)
        print("  ✓ Estructura validada")

    def test_validation_empty(self):
        """Test: Validación de texto vacío"""
        print("\n[TEST] Validación Vacía")
        with self.assertRaises(ValueError):
            self.registry.register("p.blend", "   ")
        print("  ✓ Rechaza texto vacío")

    def test_validation_length(self):
        """Test: Validación de longitud"""
        print("\n[TEST] Validación Longitud")
        long_text = "a" * 501
        with self.assertRaises(ValueError):
            self.registry.register("p.blend", long_text)
        print("  ✓ Rechaza texto excesivo")

if __name__ == '__main__':
    print("="*70)
    print("TEST - INTENTION REGISTRY (FASE 5.18)")
    print("="*70)
    unittest.main(verbosity=2)
