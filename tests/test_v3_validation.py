"""
test_v3_validation.py

Pruebas para V3Validator (Fase 19).
"""

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.validation.v3_validator import V3Validator
from core.adapters.mock_adapter import MockAdapter
from core.assembly.assembly_core import AssemblyCore


class TestV3Validation(unittest.TestCase):
    """Tests para validación estructural V3."""
    
    def setUp(self):
        """Inicializa validator para cada test."""
        self.adapter = MockAdapter()
        self.validator = V3Validator(adapter=self.adapter)
        self.assembly = AssemblyCore(adapter=self.adapter)
    
    def test_valid_simple_structure(self):
        """Test estructura simple válida."""
        structure_def = {
            'name': 'valid',
            'components': [
                {'id': 'base', 'type': 'cube', 'location': [0, 0, 0]},
                {'id': 'top', 'type': 'cube', 'location': [0, 0, 1], 'parent': 'base'}
            ]
        }
        
        result = self.assembly.create_structure(structure_def)
        mapping = result['component_mapping']
        
        validation = self.validator.validate_structure(mapping)
        
        self.assertTrue(validation['valid'])
        self.assertEqual(len(validation['errors']), 0)
    
    def test_detect_cycle(self):
        """Test detección de ciclos en jerarquía."""
        # Crear objetos manualmente para forzar ciclo
        self.adapter.create_primitive('cube')
        self.adapter.create_primitive('cube')
        
        obj1 = 'Cube_001'
        obj2 = 'Cube_002'
        
        # A → B → A (ciclo)
        self.adapter.set_parent(obj2, obj1)
        # Intentar establecer ciclo directamente en _hierarchy (mock)
        self.adapter._hierarchy[obj1] = obj2  # Forzar ciclo
        
        validation = self.validator.validate_hierarchy([obj1, obj2])
        
        self.assertFalse(validation['valid'])
        self.assertGreater(len(validation['errors']), 0)
    
    def test_floating_object_warning(self):
        """Test advertencia de objeto flotante."""
        # Crear objeto sin parent en Z alto
        result = self.adapter.create_primitive('cube', location=[0, 0, 5])
        obj_name = result['object_name']
        
        validation = self.validator.validate_floating_objects([obj_name], ground_threshold=0.01)
        
        self.assertGreater(len(validation['warnings']), 0)
        self.assertIn('flota', validation['warnings'][0].lower())
    
    def test_dimensional_coherence_warning(self):
        """Test advertencia de hijo más grande que padre."""
        # Crear padre pequeño e hijo grande
        self.adapter.create_primitive('cube', location=[0, 0, 0], scale=0.5)
        self.adapter.create_primitive('cube', location=[0, 0, 1], scale=2.0)
        
        parent = 'Cube_001'
        child = 'Cube_002'
        
        # Establecer relación
        self.adapter.set_parent(child, parent)
        
        validation = self.validator.validate_dimensional_coherence([parent, child])
        
        # Debe generar WARNING, no error
        self.assertGreater(len(validation['warnings']), 0)
    
    def test_validate_pattern_valid(self):
        """Test validación de patrón válido."""
        pattern = {
            'name': 'test_pattern',
            'components': [
                {'id': 'base', 'type': 'cube', 'location': [0, 0, 0]},
                {'id': 'top', 'type': 'cube', 'location': [0, 0, 1], 'parent': 'base'}
            ]
        }
        
        validation = self.validator.validate_pattern(pattern)
        
        self.assertTrue(validation['valid'])
        self.assertEqual(len(validation['errors']), 0)
    
    def test_validate_pattern_invalid(self):
        """Test validación de patrón inválido."""
        pattern = {
            'name': 'bad_pattern',
            'components': [
                {'id': 'obj1', 'type': 'cube', 'parent': 'does_not_exist'}
            ]
        }
        
        validation = self.validator.validate_pattern(pattern)
        
        self.assertFalse(validation['valid'])
        self.assertGreater(len(validation['errors']), 0)


if __name__ == '__main__':
    unittest.main()
