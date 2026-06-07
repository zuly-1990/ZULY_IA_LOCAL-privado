"""
Tests Mínimos para IntentionBoundary - Fase 5.16

Propósito:
- Validar que IntentionBoundary existe
- Validar que define límites
- Validar que NO ejecuta lógica
- Tests estructurales, NO funcionales

Regla: Solo tests especificados.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.intention.intention_boundary import IntentionBoundary


class TestIntentionBoundaryMinimal(unittest.TestCase):
    """
    Tests mínimos para IntentionBoundary.
    
    Tests estructurales, NO funcionales.
    """
    
    def test_1_boundary_existe(self):
        """Test 1: El boundary existe"""
        print("\n[TEST 1] Boundary existe")
        
        # Validar que la clase existe
        self.assertTrue(hasattr(IntentionBoundary, 'FORBIDDEN_INTENT_SOURCES'))
        self.assertTrue(hasattr(IntentionBoundary, 'ALLOWED_INTENT_SOURCES'))
        
        print("  ✓ IntentionBoundary existe con atributos requeridos")
    
    def test_2_define_intenciones_prohibidas(self):
        """Test 2: Define intenciones prohibidas"""
        print("\n[TEST 2] Define intenciones prohibidas")
        
        # Validar que hay intenciones prohibidas definidas
        self.assertIsInstance(IntentionBoundary.FORBIDDEN_INTENT_SOURCES, list)
        self.assertGreater(len(IntentionBoundary.FORBIDDEN_INTENT_SOURCES), 0)
        
        # Validar que incluye las fuentes críticas
        self.assertIn('state_snapshot', IntentionBoundary.FORBIDDEN_INTENT_SOURCES)
        self.assertIn('pattern_memory', IntentionBoundary.FORBIDDEN_INTENT_SOURCES)
        self.assertIn('self_reflection', IntentionBoundary.FORBIDDEN_INTENT_SOURCES)
        
        print(f"  ✓ {len(IntentionBoundary.FORBIDDEN_INTENT_SOURCES)} fuentes prohibidas definidas")
    
    def test_3_no_ejecuta_logica(self):
        """Test 3: NO ejecuta lógica"""
        print("\n[TEST 3] NO ejecuta lógica")
        
        # Validar que los métodos son solo consultas
        forbidden = IntentionBoundary.get_forbidden_sources()
        allowed = IntentionBoundary.get_allowed_sources()
        
        # Validar que retornan listas (no ejecutan lógica compleja)
        self.assertIsInstance(forbidden, list)
        self.assertIsInstance(allowed, list)
        
        # Validar que is_forbidden solo verifica (no ejecuta)
        result = IntentionBoundary.is_forbidden('state_snapshot')
        self.assertIsInstance(result, bool)
        
        print("  ✓ Boundary solo define límites, no ejecuta lógica")
    
    def test_4_no_depende_agent(self):
        """Test 4: NO depende del Agent"""
        print("\n[TEST 4] NO depende del Agent")
        
        # Validar que IntentionBoundary no importa Agent
        import core.intention.intention_boundary as boundary_module
        
        # Verificar que no hay referencia a Agent en el código
        boundary_source = boundary_module.__file__
        with open(boundary_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertNotIn('from core.agent', content)
        self.assertNotIn('import agent', content.lower())
        
        print("  ✓ Boundary NO depende del Agent")
    
    def test_5_no_importa_state_o_pattern(self):
        """Test 5: NO importa StateAwareness o PatternMemory"""
        print("\n[TEST 5] NO importa StateAwareness o PatternMemory")
        
        # Validar que IntentionBoundary no importa StateAwareness o PatternMemory
        import core.intention.intention_boundary as boundary_module
        
        boundary_source = boundary_module.__file__
        with open(boundary_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que no hay imports (no solo palabras en comentarios)
        self.assertNotIn('from core.state', content)
        self.assertNotIn('from core.learning', content)
        self.assertNotIn('import StateAwareness', content)
        self.assertNotIn('import PatternMemory', content)
        
        print("  ✓ Boundary NO importa StateAwareness o PatternMemory")


if __name__ == '__main__':
    print("="*70)
    print("TESTS MÍNIMOS - INTENTION BOUNDARY (FASE 5.16)")
    print("="*70)
    print("\nTests cubiertos:")
    print("1. El boundary existe")
    print("2. Define intenciones prohibidas")
    print("3. NO ejecuta lógica")
    print("4. NO depende del Agent")
    print("5. NO importa StateAwareness o PatternMemory")
    print("\nTests estructurales, no funcionales.")
    print("="*70)
    unittest.main(verbosity=2)
