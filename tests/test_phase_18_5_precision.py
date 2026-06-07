"""
Tests para Fase 18.5 - Consolidación de Precisión
"""

import unittest
import os
import sys

# Añadir directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.reasoning.intention_classifier import classify_intention
from core.adapters.mock_adapter import MockAdapter
from core.utils.units import parse_dimension, to_meters

class TestPrecisionPhase(unittest.TestCase):
    
    def test_unit_parsing(self):
        """Verifica que el parser detecte unidades correctamente."""
        text = "crear un cilindro de 40mm de radio"
        val, unit = parse_dimension(text)
        self.assertEqual(val, 40.0)
        self.assertEqual(unit, "mm")
        self.assertEqual(to_meters(val, unit), 0.04)
        
        text2 = "un cubo de 5 cm"
        val2, unit2 = parse_dimension(text2)
        self.assertEqual(val2, 5.0)
        self.assertEqual(unit2, "cm")
        self.assertEqual(to_meters(val2, unit2), 0.05)

    def test_intention_classification_with_units(self):
        """Verifica que el classifier extraiga la intención dimensional."""
        text = "borrar cubo de 10cm"
        result = classify_intention(text)
        
        self.assertIn("dimension_intent", result)
        self.assertEqual(result["dimension_intent"]["value"], 10.0)
        self.assertEqual(result["dimension_intent"]["unit"], "cm")
        self.assertEqual(result["dimension_intent"]["meters"], 0.1)
        self.assertIn("precisión de 10.0cm", result["motivo"])

    def test_adapter_precision_apply(self):
        """Verifica que el adapter aplique la intención dimensional."""
        adapter = MockAdapter()
        
        # Simulación de lo que el Agent haría
        intent_text = "crear cilindro de 20mm"
        class_res = classify_intention(intent_text)
        
        res = adapter.create_primitive(
            primitive_type='cylinder',
            dimension_intent=class_res['dimension_intent']
        )
        
        self.assertTrue(res['success'])
        obj_name = res['object_name']
        
        # En MockAdapter para cilindro, scale = val_m
        state = adapter.get_scene_state()
        obj_info = next(o for o in state['objects'] if o['name'] == obj_name)
        
        # 20mm -> 0.02m
        self.assertEqual(obj_info['scale'], [0.02, 0.02, 0.02])
        self.assertEqual(obj_info['intended_dimension']['value'], 20.0)
        self.assertEqual(obj_info['intended_dimension']['unit'], 'mm')

if __name__ == '__main__':
    unittest.main()
