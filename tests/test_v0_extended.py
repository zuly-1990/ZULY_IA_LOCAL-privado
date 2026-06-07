"""
Tests Comprehensivos para V0 Validator Extendido
Fase 5.12 - Validación Estructural

Valida:
- Creación de objetos
- Transformaciones (mover, rotar, escalar)
- Eliminación de objetos
- Cambios de propiedades (warnings)
- Validación pasiva
"""

import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.validation.v0_validator import V0Validator
from core.validation.state_snapshot import StateSnapshot


class TestV0Extended(unittest.TestCase):
    
    def setUp(self):
        """Setup para cada test"""
        self.validator = V0Validator()
        # Mock StateSnapshot para evitar dependencia de Blender
        self.original_capture = StateSnapshot.capture
    
    def tearDown(self):
        """Cleanup después de cada test"""
        StateSnapshot.capture = self.original_capture
    
    def test_creation_validation_success(self):
        """Test: Validación exitosa de creación de objeto"""
        print("\n[TEST] Creación de objeto - Éxito")
        
        # PRE: Sin objetos
        pre_snapshot = {}
        # POST: Un cubo
        post_snapshot = {
            'Cube': {
                'type': 'MESH',
                'location': (0.0, 0.0, 0.0),
                'rotation': (0.0, 0.0, 0.0),
                'scale': (1.0, 1.0, 1.0),
                'visible': True,
                'name': 'Cube'
            }
        }
        
        StateSnapshot.capture = MagicMock(side_effect=[pre_snapshot, post_snapshot])
        
        self.validator.start_validation()
        
        result = self.validator.validate({
            'success': True,
            'effect': 'create',  # CLAVE: usar 'effect'
            'result': {'name': 'Cube'}
        })
        
        self.assertTrue(result['verified'])
        self.assertIn('Cube', result['details'])
        print(f"  ✓ {result['details']}")
    
    def test_creation_validation_false_positive(self):
        """Test: Detecta falso positivo (dice crear pero no hay objeto nuevo)"""
        print("\n[TEST] Creación - Falso positivo")
        
        # PRE y POST iguales (no se creó nada)
        snapshot = {'ExistingCube': {'type': 'MESH'}}
        StateSnapshot.capture = MagicMock(side_effect=[snapshot, snapshot])
        
        self.validator.start_validation()
        
        result = self.validator.validate({
            'success': True,
            'effect': 'create',
            'result': {'name': 'NewCube'}
        })
        
        self.assertFalse(result['verified'])
        self.assertIn('no aparecieron objetos nuevos', result['details'])
        print(f"  ✓ Falso positivo detectado: {result['details']}")
    
    def test_transformation_validation_success(self):
        """Test: Validación exitosa de transformación"""
        print("\n[TEST] Transformación - Éxito")
        
        # PRE: Cubo en origen
        pre_snapshot = {
            'Cube': {
                'location': (0.0, 0.0, 0.0),
                'rotation': (0.0, 0.0, 0.0),
                'scale': (1.0, 1.0, 1.0)
            }
        }
        # POST: Cubo movido
        post_snapshot = {
            'Cube': {
                'location': (5.0, 0.0, 0.0),  # CAMBIÓ
                'rotation': (0.0, 0.0, 0.0),
                'scale': (1.0, 1.0, 1.0)
            }
        }
        
        StateSnapshot.capture = MagicMock(side_effect=[pre_snapshot, post_snapshot])
        
        self.validator.start_validation()
        
        result = self.validator.validate({
            'success': True,
            'effect': 'transform',  # CLAVE: efecto declarado
            'result': {'name': 'Cube'}
        })
        
        self.assertTrue(result['verified'])
        self.assertIn('location', result['changes'])
        print(f"  ✓ {result['details']}")
    
    def test_transformation_no_change_detected(self):
        """Test: Detecta cuando transformación no cambió nada"""
        print("\n[TEST] Transformación - Sin cambios")
        
        # PRE y POST iguales
        snapshot = {
            'Cube': {
                'location': (0.0, 0.0, 0.0),
                'rotation': (0.0, 0.0, 0.0),
                'scale': (1.0, 1.0, 1.0)
            }
        }
        StateSnapshot.capture = MagicMock(side_effect=[snapshot, snapshot])
        
        self.validator.start_validation()
        
        result = self.validator.validate({
            'success': True,
            'effect': 'transform',
            'result': {'name': 'Cube'}
        })
        
        self.assertFalse(result['verified'])
        self.assertIn('no se detectaron cambios', result['details'])
        print(f"  ✓ Sin cambios detectado: {result['details']}")
    
    def test_deletion_validation_success(self):
        """Test: Validación exitosa de eliminación"""
        print("\n[TEST] Eliminación - Éxito")
        
        # PRE: Cubo existe
        pre_snapshot = {
            'Cube': {'type': 'MESH'}
        }
        # POST: Cubo eliminado
        post_snapshot = {}
        
        StateSnapshot.capture = MagicMock(side_effect=[pre_snapshot, post_snapshot])
        
        self.validator.start_validation()
        
        result = self.validator.validate({
            'success': True,
            'effect': 'delete',
            'result': {'name': 'Cube'}
        })
        
        self.assertTrue(result['verified'])
        self.assertIn('ya no existe', result['details'])
        print(f"  ✓ {result['details']}")
    
    def test_deletion_object_still_exists(self):
        """Test: Detecta cuando objeto no fue eliminado"""
        print("\n[TEST] Eliminación - Objeto aún existe")
        
        # PRE y POST iguales (no se eliminó)
        snapshot = {'Cube': {'type': 'MESH'}}
        StateSnapshot.capture = MagicMock(side_effect=[snapshot, snapshot])
        
        self.validator.start_validation()
        
        result = self.validator.validate({
            'success': True,
            'effect': 'delete',
            'result': {'name': 'Cube'}
        })
        
        self.assertFalse(result['verified'])
        self.assertIn('aún existe', result['details'])
        print(f"  ✓ Fallo detectado: {result['details']}")
    
    def test_property_change_warning_not_blocking(self):
        """Test: Cambios de propiedades generan warning, NO bloquean"""
        print("\n[TEST] Propiedades - Warning, no bloqueo")
        
        # PRE y POST iguales (propiedad no cambió)
        snapshot = {
            'Cube': {
                'visible': True,
                'name': 'Cube'
            }
        }
        StateSnapshot.capture = MagicMock(side_effect=[snapshot, snapshot])
        
        self.validator.start_validation()
        
        result = self.validator.validate({
            'success': True,
            'effect': 'property',  # Efecto de propiedad
            'result': {'name': 'Cube'}
        })
        
        # CRÍTICO: verified debe ser True (no bloquea)
        self.assertTrue(result['verified'])
        self.assertIn('warning', result)
        print(f"  ✓ Warning generado, no bloqueó: {result.get('warning')}")
    
    def test_passive_validation(self):
        """Test: Validación pasiva para comandos sin efecto estructural"""
        print("\n[TEST] Validación pasiva")
        
        snapshot = {}
        StateSnapshot.capture = MagicMock(side_effect=[snapshot, snapshot])
        
        self.validator.start_validation()
        
        # Comando sin 'effect' o con effect desconocido
        result = self.validator.validate({
            'success': True,
            # NO tiene 'effect'
            'result': {}
        })
        
        # CRÍTICO: debe pasar sin error
        self.assertTrue(result['verified'])
        self.assertIn('pasiva', result['details'])
        print(f"  ✓ {result['details']}")
    
    def test_rotation_and_scale_detection(self):
        """Test: Detecta cambios en rotación y escala"""
        print("\n[TEST] Transformación - Rotación y escala")
        
        # PRE: Estado inicial
        pre_snapshot = {
            'Cube': {
                'location': (0.0, 0.0, 0.0),
                'rotation': (0.0, 0.0, 0.0),
                'scale': (1.0, 1.0, 1.0)
            }
        }
        # POST: Rotado y escalado
        post_snapshot = {
            'Cube': {
                'location': (0.0, 0.0, 0.0),  # Sin cambio
                'rotation': (1.571, 0.0, 0.0),  # CAMBIÓ (90 grados)
                'scale': (2.0, 2.0, 2.0)  # CAMBIÓ (doble tamaño)
            }
        }
        
        StateSnapshot.capture = MagicMock(side_effect=[pre_snapshot, post_snapshot])
        
        self.validator.start_validation()
        
        result = self.validator.validate({
            'success': True,
            'effect': 'transform',
            'result': {'name': 'Cube'}
        })
        
        self.assertTrue(result['verified'])
        self.assertIn('rotation', result['changes'])
        self.assertIn('scale', result['changes'])
        self.assertNotIn('location', result['changes'])
        print(f"  ✓ Cambios detectados: {result['changes']}")


if __name__ == '__main__':
    print("="*70)
    print("TESTS COMPREHENSIVOS - V0 VALIDATOR EXTENDIDO")
    print("="*70)
    unittest.main(verbosity=2)
