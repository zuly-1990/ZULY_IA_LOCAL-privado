"""
Tests Mínimos para BlenderActionObserver - Fase 5.16
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.environment.blender_action_observer import BlenderActionObserver

class TestBlenderActionObserverMinimal(unittest.TestCase):
    
    def setUp(self):
        self.observer = BlenderActionObserver()
        
    def test_detect_creation(self):
        """Test: Detecta creación de objeto"""
        print("\n[TEST] Detectar Creación (CREATE)")
        
        snap_a = {"objects": []}
        snap_b = {"objects": [{"name": "Cube", "location": (0,0,0)}]}
        
        events = self.observer.detect_changes(snap_a, snap_b)
        
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["type"], "CREATE")
        self.assertEqual(events[0]["object"], "Cube")
        print("  ✓ Evento CREATE detectado")

    def test_detect_deletion(self):
        """Test: Detecta borrado de objeto"""
        print("\n[TEST] Detectar Borrado (DELETE)")
        
        snap_a = {"objects": [{"name": "Cube", "location": (0,0,0)}]}
        snap_b = {"objects": []}
        
        events = self.observer.detect_changes(snap_a, snap_b)
        
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["type"], "DELETE")
        self.assertEqual(events[0]["object"], "Cube")
        print("  ✓ Evento DELETE detectado")

    def test_detect_transform(self):
        """Test: Detecta movimiento (MODIFY)"""
        print("\n[TEST] Detectar Modificación (MODIFY)")
        
        snap_a = {"objects": [{"name": "Cube", "location": (0,0,0)}]}
        snap_b = {"objects": [{"name": "Cube", "location": (1,0,0)}]}
        
        events = self.observer.detect_changes(snap_a, snap_b)
        
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["type"], "MODIFY")
        self.assertEqual(events[0]["object"], "Cube")
        print("  ✓ Evento MODIFY detectado")

    def test_no_false_positives(self):
        """Test: Ignora cambios inexistentes"""
        print("\n[TEST] Sin Cambios")
        
        snap_a = {"objects": [{"name": "Cube", "location": (0,0,0)}]}
        snap_b = {"objects": [{"name": "Cube", "location": (0,0,0)}]}
        
        events = self.observer.detect_changes(snap_a, snap_b)
        
        self.assertEqual(len(events), 0)
        print("  ✓ Sin falsos positivos")

if __name__ == '__main__':
    print("="*70)
    print("TEST - BLENDER ACTION OBSERVER (FASE 5.16)")
    print("="*70)
    unittest.main(verbosity=2)
