"""
Tests Mínimos para StateGuard - Fase 5.15

Propósito:
- Validar que StateGuard existe
- Validar que define límites
- Validar que NO ejecuta lógica
- Tests estructurales, NO funcionales

Regla: Solo tests especificados.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.state.state_guard import StateGuard


class TestStateGuardMinimal(unittest.TestCase):
    """
    Tests mínimos para StateGuard.
    
    Tests estructurales, NO funcionales.
    """
    
    def test_1_guard_existe(self):
        """Test 1: El guard existe"""
        print("\n[TEST 1] Guard existe")
        
        # Validar que la clase existe
        self.assertTrue(hasattr(StateGuard, 'FORBIDDEN_USES'))
        self.assertTrue(hasattr(StateGuard, 'ALLOWED_USES'))
        
        print("  ✓ StateGuard existe con atributos requeridos")
    
    def test_2_guard_define_usos_prohibidos(self):
        """Test 2: El guard define usos prohibidos"""
        print("\n[TEST 2] Guard define usos prohibidos")
        
        # Validar que hay usos prohibidos definidos
        self.assertIsInstance(StateGuard.FORBIDDEN_USES, list)
        self.assertGreater(len(StateGuard.FORBIDDEN_USES), 0)
        
        # Validar que incluye los usos críticos
        self.assertIn('decision_making', StateGuard.FORBIDDEN_USES)
        self.assertIn('flow_control', StateGuard.FORBIDDEN_USES)
        self.assertIn('learning_trigger', StateGuard.FORBIDDEN_USES)
        
        print(f"  ✓ {len(StateGuard.FORBIDDEN_USES)} usos prohibidos definidos")
    
    def test_3_guard_no_ejecuta_logica(self):
        """Test 3: El guard NO ejecuta lógica"""
        print("\n[TEST 3] Guard NO ejecuta lógica")
        
        # Validar que los métodos son solo consultas
        forbidden = StateGuard.get_forbidden_uses()
        allowed = StateGuard.get_allowed_uses()
        
        # Validar que retornan listas (no ejecutan lógica compleja)
        self.assertIsInstance(forbidden, list)
        self.assertIsInstance(allowed, list)
        
        # Validar que is_forbidden solo verifica (no ejecuta)
        result = StateGuard.is_forbidden('decision_making')
        self.assertIsInstance(result, bool)
        
        print("  ✓ Guard solo define límites, no ejecuta lógica")
    
    def test_4_guard_no_depende_agent(self):
        """Test 4: El guard NO depende del Agent"""
        print("\n[TEST 4] Guard NO depende del Agent")
        
        # Validar que StateGuard no importa Agent
        import core.state.state_guard as guard_module
        
        # Verificar que no hay referencia a Agent en el código
        guard_source = guard_module.__file__
        with open(guard_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertNotIn('from core.agent', content)
        self.assertNotIn('import agent', content.lower())
        
        print("  ✓ Guard NO depende del Agent")
    
    def test_5_guard_no_importa_state_awareness(self):
        """Test 5: El guard NO importa StateAwareness"""
        print("\n[TEST 5] Guard NO importa StateAwareness")
        
        # Validar que StateGuard no importa StateAwareness
        import core.state.state_guard as guard_module
        
        guard_source = guard_module.__file__
        with open(guard_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertNotIn('StateAwareness', content)
        self.assertNotIn('state_awareness', content)
        
        print("  ✓ Guard NO importa StateAwareness")


if __name__ == '__main__':
    print("="*70)
    print("TESTS MÍNIMOS - STATE GUARD (FASE 5.15)")
    print("="*70)
    print("\nTests cubiertos:")
    print("1. El guard existe")
    print("2. El guard define usos prohibidos")
    print("3. El guard NO ejecuta lógica")
    print("4. El guard NO depende del Agent")
    print("5. El guard NO importa StateAwareness")
    print("\nTests estructurales, no funcionales.")
    print("="*70)
    unittest.main(verbosity=2)
