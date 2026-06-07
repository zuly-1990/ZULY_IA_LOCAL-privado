"""
Tests Mínimos para StateAwareness - Fase 5.14

Propósito:
- Validar que snapshot funciona
- Validar que NO modifica estado
- Solo tests mínimos (no cobertura total)

Regla: NO más tests que los especificados.
"""

import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.state.state_awareness import StateAwareness


class TestStateAwarenessMinimal(unittest.TestCase):
    """
    Tests mínimos para StateAwareness.
    
    Solo valida funcionalidad básica.
    NO busca cobertura total.
    """
    
    def setUp(self):
        """Setup con mock de agent"""
        self.mock_agent = MagicMock()
        self.mock_agent.operational_state = "Observación"
        self.mock_agent.authorized = True
        self.mock_agent.context = MagicMock()
        self.mock_agent.context.execution_history = []
        self.mock_agent.pattern_memory = None
        
        self.awareness = StateAwareness(self.mock_agent)
    
    def test_1_snapshot_devuelve_dict_valido(self):
        """Test 1: Snapshot devuelve diccionario válido"""
        print("\n[TEST 1] Snapshot devuelve dict válido")
        
        snapshot = self.awareness.snapshot()
        
        # Validar estructura
        self.assertIsInstance(snapshot, dict)
        self.assertIn('timestamp', snapshot)
        self.assertIn('operational_state', snapshot)
        self.assertIn('security', snapshot)
        self.assertIn('validation', snapshot)
        self.assertIn('learning', snapshot)
        self.assertIn('execution', snapshot)
        
        print(f"  ✓ Snapshot válido: {list(snapshot.keys())}")
    
    def test_2_estado_operativo_correcto(self):
        """Test 2: Estado operativo se lee correctamente"""
        print("\n[TEST 2] Estado operativo correcto")
        
        # Test con Observación
        self.mock_agent.operational_state = "Observación"
        snapshot = self.awareness.snapshot()
        self.assertEqual(snapshot['operational_state'], 'OBSERVACIÓN')
        
        # Test con Aprendizaje
        self.mock_agent.operational_state = "Ejecución con Aprendizaje"
        snapshot = self.awareness.snapshot()
        self.assertEqual(snapshot['operational_state'], 'EJECUCIÓN_CON_APRENDIZAJE')
        
        # Test con Bloqueo
        self.mock_agent.operational_state = "Bloqueo Ético"
        snapshot = self.awareness.snapshot()
        self.assertEqual(snapshot['operational_state'], 'BLOQUEO_ÉTICO')
        
        print("  ✓ Estados operativos correctos")
    
    def test_3_estado_seguridad_correcto(self):
        """Test 3: Estado de seguridad se lee correctamente"""
        print("\n[TEST 3] Estado seguridad correcto")
        
        # Test con autor verificado
        self.mock_agent.authorized = True
        snapshot = self.awareness.snapshot()
        self.assertTrue(snapshot['security']['author_verified'])
        
        # Test sin autor verificado
        self.mock_agent.authorized = False
        snapshot = self.awareness.snapshot()
        self.assertFalse(snapshot['security']['author_verified'])
        
        print("  ✓ Estado de seguridad correcto")
    
    def test_4_estado_aprendizaje_correcto(self):
        """Test 4: Estado de aprendizaje se lee correctamente"""
        print("\n[TEST 4] Estado aprendizaje correcto")
        
        # Test sin pattern_memory
        self.mock_agent.pattern_memory = None
        snapshot = self.awareness.snapshot()
        self.assertFalse(snapshot['learning']['enabled'])
        self.assertEqual(snapshot['learning']['patterns_total'], 0)
        
        # Test con pattern_memory
        mock_memory = MagicMock()
        mock_memory.get_stats.return_value = {'total_patterns': 5}
        mock_memory.patterns = [{'pattern_id': 'test-123'}]
        self.mock_agent.pattern_memory = mock_memory
        
        snapshot = self.awareness.snapshot()
        self.assertEqual(snapshot['learning']['patterns_total'], 5)
        self.assertEqual(snapshot['learning']['last_pattern_id'], 'test-123')
        
        print("  ✓ Estado de aprendizaje correcto")
    
    def test_5_snapshot_no_modifica_estado(self):
        """Test 5: Snapshot NO modifica estado del agent"""
        print("\n[TEST 5] Snapshot NO modifica estado")
        
        # Capturar estado inicial
        initial_state = self.mock_agent.operational_state
        initial_authorized = self.mock_agent.authorized
        
        # Ejecutar snapshot
        snapshot = self.awareness.snapshot()
        
        # Validar que NO cambió
        self.assertEqual(self.mock_agent.operational_state, initial_state)
        self.assertEqual(self.mock_agent.authorized, initial_authorized)
        
        print("  ✓ Estado NO modificado por snapshot")


if __name__ == '__main__':
    print("="*70)
    print("TESTS MÍNIMOS - STATE AWARENESS (FASE 5.14)")
    print("="*70)
    print("\nTests cubiertos:")
    print("1. Snapshot devuelve dict válido")
    print("2. Estado operativo correcto")
    print("3. Estado seguridad correcto")
    print("4. Estado aprendizaje correcto")
    print("5. Snapshot NO modifica estado")
    print("\nRegla: NO más tests.")
    print("="*70)
    unittest.main(verbosity=2)
