"""
Tests Mínimos para Shield v1

Propósito:
- Validar que Shield v1 existe
- Validar que valida correctamente
- Validar que NO ejecuta
- Validar que NO importa core
- Tests estructurales + funcionales mínimos

Regla: Solo tests especificados.
"""

import sys
import os
import unittest

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from extensions.shields.shield_v1 import ShieldV1
from extensions.shields.rules import ShieldRules


class TestShieldV1Minimal(unittest.TestCase):
    """
    Tests mínimos para Shield v1.
    
    Tests estructurales + funcionales mínimos.
    """
    
    def test_1_shield_existe(self):
        """Test 1: El shield existe"""
        print("\n[TEST 1] Shield existe")
        
        # Validar que la clase existe
        self.assertTrue(hasattr(ShieldV1, 'validate_command'))
        
        print("  ✓ ShieldV1 existe con método validate_command")
    
    def test_2_permite_comando_valido(self):
        """Test 2: Permite comando válido"""
        print("\n[TEST 2] Permite comando válido")
        
        # Comando válido
        command = {
            'type': 'explicit_human',
            'callable': lambda: None
        }
        
        result = ShieldV1.validate_command(command)
        
        # Debe permitir
        self.assertTrue(result['allowed'])
        self.assertIn('validado', result['reason'].lower())
        
        print("  ✓ Shield permite comandos válidos")
    
    def test_3_bloquea_comando_invalido(self):
        """Test 3: Bloquea comando inválido"""
        print("\n[TEST 3] Bloquea comando inválido")
        
        # Comando con tipo bloqueado
        command = {
            'type': 'automatic',
            'callable': lambda: None
        }
        
        result = ShieldV1.validate_command(command)
        
        # Debe bloquear
        self.assertFalse(result['allowed'])
        self.assertIn('bloqueado', result['reason'].lower())
        
        print("  ✓ Shield bloquea comandos inválidos")
    
    def test_4_bloquea_campo_faltante(self):
        """Test 4: Bloquea si falta campo obligatorio"""
        print("\n[TEST 4] Bloquea campo faltante")
        
        # Comando sin 'callable'
        command = {
            'type': 'explicit_human'
        }
        
        result = ShieldV1.validate_command(command)
        
        # Debe bloquear
        self.assertFalse(result['allowed'])
        self.assertIn('faltante', result['reason'].lower())
        
        print("  ✓ Shield bloquea comandos con campos faltantes")
    
    def test_5_no_ejecuta(self):
        """Test 5: Shield NO ejecuta comandos"""
        print("\n[TEST 5] Shield NO ejecuta")
        
        # Variable para verificar ejecución
        executed = {'value': False}
        
        def test_callable():
            executed['value'] = True
        
        command = {
            'type': 'explicit_human',
            'callable': test_callable
        }
        
        # Validar comando
        result = ShieldV1.validate_command(command)
        
        # El callable NO debe haberse ejecutado
        self.assertFalse(executed['value'], "Shield ejecutó el comando (PROHIBIDO)")
        
        print("  ✓ Shield NO ejecuta comandos")
    
    def test_6_no_importa_core(self):
        """Test 6: Shield NO importa módulos del core"""
        print("\n[TEST 6] Shield NO importa core")
        
        # Validar que shield_v1 no importa core
        import extensions.shields.shield_v1 as shield_module
        
        shield_source = shield_module.__file__
        with open(shield_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que no hay imports del core (excepto interfaces públicas permitidas)
        self.assertNotIn('from core.agent', content)
        self.assertNotIn('from core.state', content)
        self.assertNotIn('from core.intention', content)
        self.assertNotIn('from core.learning', content)
        
        print("  ✓ Shield NO importa módulos del core")


if __name__ == '__main__':
    print("="*70)
    print("TESTS MÍNIMOS - SHIELD V1 (FASE 8.0)")
    print("="*70)
    print("\nTests cubiertos:")
    print("1. El shield existe")
    print("2. Permite comando válido")
    print("3. Bloquea comando inválido")
    print("4. Bloquea campo faltante")
    print("5. Shield NO ejecuta")
    print("6. Shield NO importa core")
    print("\nTests estructurales + funcionales mínimos.")
    print("="*70)
    unittest.main(verbosity=2)
