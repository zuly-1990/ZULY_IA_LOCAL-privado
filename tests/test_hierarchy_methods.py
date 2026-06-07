"""
test_hierarchy_methods.py

Pruebas para métodos de jerarquía en adapters (Fase 19).
"""

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.adapters.mock_adapter import MockAdapter


class TestHierarchyMethods(unittest.TestCase):
    """Tests para set_parent, get_parent, get_children, align_objects."""
    
    def setUp(self):
        """Inicializa adapter para cada test."""
        self.adapter = MockAdapter()
        
        # Crear objetos test
        self.adapter.create_primitive('cube', location=[0, 0, 0])
        self.adapter.create_primitive('cube', location=[2, 0, 0])
        self.adapter.create_primitive('cube', location=[-2, 0, 0])
        
        # Nombres esperados
        self.obj1 = 'Cube_001'
        self.obj2 = 'Cube_002'
        self.obj3 = 'Cube_003'
    
    def test_set_parent_success(self):
        """Test establecer relación parent/child."""
        result = self.adapter.set_parent(self.obj2, self.obj1)
        
        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('child'), self.obj2)
        self.assertEqual(result.get('parent'), self.obj1)
    
    def test_get_parent(self):
        """Test obtener padre de un objeto."""
        # Sin parent
        parent = self.adapter.get_parent(self.obj1)
        self.assertIsNone(parent)
        
        # Con parent
        self.adapter.set_parent(self.obj2, self.obj1)
        parent = self.adapter.get_parent(self.obj2)
        self.assertEqual(parent, self.obj1)
    
    def test_get_children(self):
        """Test obtener hijos de un objeto."""
        # Sin hijos
        children = self.adapter.get_children(self.obj1)
        self.assertEqual(children, [])
        
        # Con hijos
        self.adapter.set_parent(self.obj2, self.obj1)
        self.adapter.set_parent(self.obj3, self.obj1)
        
        children = self.adapter.get_children(self.obj1)
        self.assertEqual(len(children), 2)
        self.assertIn(self.obj2, children)
        self.assertIn(self.obj3, children)
    
    def test_cycle_detection(self):
        """Test detección de ciclos en jerarquía."""
        # A → B
        self.adapter.set_parent(self.obj2, self.obj1)
        
        # Intentar B → A (ciclo)
        result = self.adapter.set_parent(self.obj1, self.obj2)
        
        self.assertFalse(result.get('success'))
        self.assertIn('ciclo', result.get('message', '').lower())
    
    def test_unparent(self):
        """Test desparentar un objeto."""
        # Parentar
        self.adapter.set_parent(self.obj2, self.obj1)
        self.assertEqual(self.adapter.get_parent(self.obj2), self.obj1)
        
        # Desparentar
        result = self.adapter.set_parent(self.obj2, None)
        self.assertTrue(result.get('success'))
        self.assertIsNone(self.adapter.get_parent(self.obj2))
    
    def test_align_objects_center(self):
        """Test alineación center."""
        result = self.adapter.align_objects(self.obj2, self.obj1, 'center')
        
        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('new_location'), [0, 0, 0])
    
    def test_align_objects_top(self):
        """Test alineación top."""
        result = self.adapter.align_objects(self.obj2, self.obj1, 'top')
        
        self.assertTrue(result.get('success'))
        new_loc = result.get('new_location')
        # Debe estar encima (Z positivo)
        self.assertGreater(new_loc[2], 0)
    
    def test_align_objects_invalid(self):
        """Test alineación con objeto inexistente."""
        result = self.adapter.align_objects('NoExiste', self.obj1, 'center')
        
        self.assertFalse(result.get('success'))


if __name__ == '__main__':
    unittest.main()
