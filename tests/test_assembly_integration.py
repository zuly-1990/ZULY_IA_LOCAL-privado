"""
test_assembly_integration.py

Test end-to-end para Fase 20: Assembly + Handlers + Agent
"""

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.adapters.mock_adapter import MockAdapter
from core.commands.blender_handlers.assembly import (
    build_structure_handler,
    save_pattern_handler,
    load_pattern_handler,
    list_patterns_handler
)


class TestAssemblyIntegration(unittest.TestCase):
    """Tests de integración end-to-end para assembly system."""
    
    def setUp(self):
        """Inicializa adapter para cada test."""
        self.adapter = MockAdapter()
    
    def test_build_structure_handler(self):
        """Test handler de construcción de estructura."""
        structure_def = {
            'name': 'simple_house',
            'components': [
                {'id': 'base', 'type': 'cube', 'location': [0, 0, 0], 'scale': 3.0},
                {'id': 'wall1', 'type': 'cube', 'location': [1, 1, 1], 'scale': [0.2, 2, 2], 'parent': 'base'},
                {'id': 'roof', 'type': 'cone', 'location': [0, 0, 2], 'scale': 3.5, 'parent': 'base'}
            ]
        }
        
        result = build_structure_handler(
            {'structure_def': structure_def, 'validate': True},
            self.adapter
        )
        
        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('effect'), 'create')
        self.assertEqual(len(result['result']['created_objects']), 3)
        
        # Verificar validación V3
        validation = result.get('validation')
        self.assertIsNotNone(validation)
        self.assertTrue(validation.get('valid'))
    
    def test_save_and_load_pattern(self):
        """Test guardar y cargar patrón."""
        # Definir patrón
        pattern_components = [
            {'id': 'base', 'type': 'cube', 'location': [0, 0, 0]},
            {'id': 'top', 'type': 'sphere', 'location': [0, 0, 1], 'parent': 'base'}
        ]
        
        # Guardar patrón
        save_result = save_pattern_handler(
            {
                'name': 'test_pattern',
                'description': 'Patrón de prueba',
                'components': pattern_components
            },
            self.adapter
        )
        
        self.assertTrue(save_result.get('success'))
        self.assertEqual(save_result.get('effect'), 'property')
        
        # Listar patrones
        list_result = list_patterns_handler({}, self.adapter)
        
        self.assertTrue(list_result.get('success'))
        patterns = list_result['result']['patterns']
        self.assertGreater(len(patterns), 0)
        
        # Verificar que nuestro patrón está en la lista
        pattern_names = [p['name'] for p in patterns]
        self.assertIn('test_pattern', pattern_names)
        
        # Cargar y construir patrón
        load_result = load_pattern_handler(
            {'name': 'test_pattern', 'location': [5, 0, 0], 'validate': True},
            self.adapter
        )
        
        self.assertTrue(load_result.get('success'))
        self.assertEqual(len(load_result['result']['created_objects']), 2)
    
    def test_build_with_validation_warnings(self):
        """Test que warnings de V3 no bloqueen creación."""
        # Crear estructura con objeto flotante (sin parent, Z alto)
        structure_def = {
            'name': 'floating_test',
            'components': [
                {'id': 'obj1', 'type': 'cube', 'location': [0, 0, 5], 'scale': 1.0}  # Flotante
            ]
        }
        
        result = build_structure_handler(
            {'structure_def': structure_def, 'validate': True},
            self.adapter
        )
        
        self.assertTrue(result.get('success'))
        
        # Debe tener warnings
        validation = result.get('validation')
        self.assertIsNotNone(validation)
        self.assertTrue(validation.get('valid'))  # Válido, pero con warnings
        self.assertGreater(len(validation.get('warnings', [])), 0)
    
    def test_invalid_pattern_rejected(self):
        """Test que patrón inválido sea rechazado."""
        # Patrón con parent que no existe
        invalid_components = [
            {'id': 'obj1', 'type': 'cube', 'parent': 'does_not_exist'}
        ]
        
        result = save_pattern_handler(
            {
                'name': 'invalid_pattern',
                'description': 'Patrón inválido',
                'components': invalid_components
            },
            self.adapter
        )
        
        self.assertFalse(result.get('success'))
        self.assertIn('validation_errors', result)
    
    def test_build_without_validation(self):
        """Test construcción sin validación V3."""
        structure_def = {
            'name': 'no_validation_test',
            'components': [
                {'id': 'base', 'type': 'cube', 'location': [0, 0, 0]}
            ]
        }
        
        result = build_structure_handler(
            {'structure_def': structure_def, 'validate': False},
            self.adapter
        )
        
        self.assertTrue(result.get('success'))
        self.assertIsNone(result.get('validation'))
    
    def test_list_patterns_empty(self):
        """Test listado de patrones (puede estar vacío o no)."""
        result = list_patterns_handler({}, self.adapter)
        
        self.assertTrue(result.get('success'))
        self.assertIn('patterns', result['result'])
        self.assertIsInstance(result['result']['patterns'], list)


if __name__ == '__main__':
    unittest.main()
