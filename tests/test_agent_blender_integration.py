"""
Test de Integración: Agent + BlenderObserver
Verifica que el Agent capture snapshots y compare correctamente.
"""

import sys
import os
import unittest
from unittest.mock import MagicMock

# Mock de BPY
mock_bpy = MagicMock()
sys.modules['bpy'] = mock_bpy

# Importar Agente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.agent import Agent

class TestAgentBlenderIntegration(unittest.TestCase):
    
    def setUp(self):
        # Limpiar mocks de data.objects
        mock_bpy.data.objects = []
        self.agent = Agent()
        
    def test_snapshot_and_compare(self):
        """Test: Capturar dos snapshots y compararlos"""
        print("\n[TEST] Integración Agent Snapshot/Compare")
        
        # 1. Escena inicial vacía
        mock_bpy.data.objects = []
        snap1 = self.agent.get_blender_snapshot()
        
        # 2. Agregar un objeto ficticio
        obj1 = MagicMock()
        obj1.name = "Cube"
        obj1.type = 'MESH'
        obj1.users_collection = []
        mock_bpy.data.objects = [obj1]
        
        snap2 = self.agent.get_blender_snapshot()
        
        # 3. Comparar
        diff = self.agent.compare_blender_snapshots(snap1, snap2)
        
        self.assertEqual(diff["added_count"], 1)
        self.assertEqual(diff["added_names"], ["Cube"])
        self.assertEqual(diff["removed_count"], 0)
        
        print(f"  ✓ Cambio detectado: +{diff['added_names']}")

if __name__ == '__main__':
    print("="*70)
    print("TEST - AGENT BLENDER INTEGRATION (FASE 5.15)")
    print("="*70)
    unittest.main(verbosity=2)
