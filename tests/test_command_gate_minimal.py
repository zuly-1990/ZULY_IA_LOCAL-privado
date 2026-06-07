"""
Tests Mínimos para CommandGate - Fase 5.17

Propósito:
- Validar que CommandGate existe
- Validar que define límites
- Validar que NO ejecuta lógica
- Tests estructurales, NO funcionales

Regla: Solo tests especificados.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.command.command_gate import CommandGate


class TestCommandGateMinimal(unittest.TestCase):
    """
    Tests mínimos para CommandGate.
    
    Tests estructurales, NO funcionales.
    """
    
    def test_1_gate_existe(self):
        """Test 1: El gate existe"""
        print("\n[TEST 1] Gate existe")
        
        # Validar que la clase existe
        self.assertTrue(hasattr(CommandGate, 'FORBIDDEN_COMMAND_TYPES'))
        self.assertTrue(hasattr(CommandGate, 'ALLOWED_COMMAND_TYPES'))
        
        print("  ✓ CommandGate existe con atributos requeridos")
    
    def test_2_define_comandos_prohibidos(self):
        """Test 2: Define comandos prohibidos"""
        print("\n[TEST 2] Define comandos prohibidos")
        
        # Validar que hay comandos prohibidos definidos
        self.assertIsInstance(CommandGate.FORBIDDEN_COMMAND_TYPES, list)
        self.assertGreater(len(CommandGate.FORBIDDEN_COMMAND_TYPES), 0)
        
        # Validar que incluye los tipos críticos
        self.assertIn('implicit', CommandGate.FORBIDDEN_COMMAND_TYPES)
        self.assertIn('automatic', CommandGate.FORBIDDEN_COMMAND_TYPES)
        self.assertIn('state_based', CommandGate.FORBIDDEN_COMMAND_TYPES)
        self.assertIn('self_generated', CommandGate.FORBIDDEN_COMMAND_TYPES)
        
        print(f"  ✓ {len(CommandGate.FORBIDDEN_COMMAND_TYPES)} tipos prohibidos definidos")
    
    def test_3_no_ejecuta_logica(self):
        """Test 3: NO ejecuta lógica"""
        print("\n[TEST 3] NO ejecuta lógica")
        
        # Validar que los métodos son solo consultas
        forbidden = CommandGate.get_forbidden_types()
        allowed = CommandGate.get_allowed_types()
        
        # Validar que retornan listas (no ejecutan lógica compleja)
        self.assertIsInstance(forbidden, list)
        self.assertIsInstance(allowed, list)
        
        # Validar que is_forbidden solo verifica (no ejecuta)
        result = CommandGate.is_forbidden('implicit')
        self.assertIsInstance(result, bool)
        
        print("  ✓ Gate solo define límites, no ejecuta lógica")
    
    def test_4_no_depende_agent(self):
        """Test 4: NO depende del Agent"""
        print("\n[TEST 4] NO depende del Agent")
        
        # Validar que CommandGate no importa Agent
        import core.command.command_gate as gate_module
        
        # Verificar que no hay referencia a Agent en el código
        gate_source = gate_module.__file__
        with open(gate_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertNotIn('from core.agent', content)
        self.assertNotIn('import agent', content.lower())
        
        print("  ✓ Gate NO depende del Agent")
    
    def test_5_no_importa_state_intention(self):
        """Test 5: NO importa StateAwareness o IntentionBoundary"""
        print("\n[TEST 5] NO importa StateAwareness o IntentionBoundary")
        
        # Validar que CommandGate no importa módulos cognitivos
        import core.command.command_gate as gate_module
        
        gate_source = gate_module.__file__
        with open(gate_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que no hay imports de módulos cognitivos
        self.assertNotIn('from core.state', content)
        self.assertNotIn('from core.intention', content)
        self.assertNotIn('from core.learning', content)
        
        print("  ✓ Gate NO importa módulos cognitivos")


if __name__ == '__main__':
    print("="*70)
    print("TESTS MÍNIMOS - COMMAND GATE (FASE 5.17)")
    print("="*70)
    print("\nTests cubiertos:")
    print("1. El gate existe")
    print("2. Define comandos prohibidos")
    print("3. NO ejecuta lógica")
    print("4. NO depende del Agent")
    print("5. NO importa StateAwareness o IntentionBoundary")
    print("\nTests estructurales, no funcionales.")
    print("="*70)
    unittest.main(verbosity=2)
