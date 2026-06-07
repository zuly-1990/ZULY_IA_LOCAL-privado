"""
test_assembly_core.py

Pruebas para AssemblyCore (Fase 19).
"""

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.assembly.assembly_core import AssemblyCore
from core.adapters.mock_adapter import MockAdapter


class TestAssemblyCore(unittest.TestCase):
    """Tests para creación de estructuras compuestas."""
    
    def setUp(self):
        """Inicializa AssemblyCore para cada test."""
        self.adapter = MockAdapter()
        self.assembly = AssemblyCore(adapter=self.adapter)
    
    def test_create_simple_structure(self):
        """Test crear estructura simple (base + columna)."""
        structure_def = {
            'name': 'simple_structure',
            'components': [
                {
                    'id': 'base',
                    'type': 'cube',
                    'location': [0, 0, 0],
                    'scale': 2.0
                },
                {
                    'id': 'column',
                    'type': 'cylinder',
                    'location': [0, 0, 1],
                    'scale': 0.5,
                    'parent': 'base'
                }
            ]
        }
        
        result = self.assembly.create_structure(structure_def)
        
        self.assertTrue(result.get('success'))
        self.assertEqual(len(result.get('created_objects')), 2)
        self.assertEqual(result['stats']['hierarchies'], 1)
    
    def test_create_structure_with_alignment(self):
        """Test estructura con alineación."""
        structure_def = {
            'name': 'aligned_structure',
            'components': [
                {
                    'id': 'base',
                    'type': 'cube',
                    'location': [0, 0, 0],
                    'scale': 2.0
                },
                {
                    'id': 'top_piece',
                    'type': 'cube',
                    'location': [5, 5, 5],  # Posición inicial irrelevante
                    'scale': 1.0,
                    'align_to': 'base',
                    'align_mode': 'top'
                }
            ]
        }
        
        result = self.assembly.create_structure(structure_def)
        
        self.assertTrue(result.get('success'))
        self.assertEqual(result['stats']['alignments'], 1)
    
    def test_complex_hierarchy(self):
        """Test jerarquía compleja (base → columnas → techo)."""
        structure_def = {
            'name': 'temple',
            'components': [
                {'id': 'base', 'type': 'cube', 'location': [0, 0, 0], 'scale': 3.0},
                {'id': 'col1', 'type': 'cylinder', 'location': [1, 1, 0.5], 'scale': 0.3, 'parent': 'base'},
                {'id': 'col2', 'type': 'cylinder', 'location': [-1, 1, 0.5], 'scale': 0.3, 'parent': 'base'},
                {'id': 'col3', 'type': 'cylinder', 'location': [1, -1, 0.5], 'scale': 0.3, 'parent': 'base'},
                {'id': 'col4', 'type': 'cylinder', 'location': [-1, -1, 0.5], 'scale': 0.3, 'parent': 'base'},
                {'id': 'roof', 'type': 'cube', 'location': [0, 0, 2], 'scale': 3.5, 'parent': 'base'}
            ]
        }
        
        result = self.assembly.create_structure(structure_def)
        
        self.assertTrue(result.get('success'))
        self.assertEqual(len(result.get('created_objects')), 6)
        self.assertEqual(result['stats']['hierarchies'], 5)
    
    def test_get_structure_hierarchy(self):
        """Test obtener jerarquía de estructura."""
        structure_def = {
            'name': 'test',
            'components': [
                {'id': 'root', 'type': 'cube', 'location': [0, 0, 0]},
                {'id': 'child1', 'type': 'cube', 'location': [1, 0, 0], 'parent': 'root'},
                {'id': 'child2', 'type': 'cube', 'location': [-1, 0, 0], 'parent': 'root'}
            ]
        }
        
        result = self.assembly.create_structure(structure_def)
        root_name = result['component_mapping']['root']
        
        hierarchy = self.assembly.get_structure_hierarchy(root_name)
        
        self.assertEqual(hierarchy['root'], root_name)
        self.assertIsNotNone(hierarchy['hierarchy'])
        self.assertEqual(len(hierarchy['hierarchy']['children']), 2)
    
    def test_empty_structure(self):
        """Test estructura vacía."""
        structure_def = {
            'name': 'empty',
            'components': []
        }
        
        result = self.assembly.create_structure(structure_def)
        
        self.assertFalse(result.get('success'))
        self.assertIn('error', result)


if __name__ == '__main__':
    unittest.main()
