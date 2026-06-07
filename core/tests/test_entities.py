"""
core/tests/test_entities.py
==========================

Pruebas unitarias para la extracción de entidades.
"""

import unittest
from core.intents import EntityExtractor


class TestEntityExtractorAdvanced(unittest.TestCase):
    """Pruebas avanzadas para EntityExtractor."""
    
    def setUp(self):
        self.extractor = EntityExtractor()
    
    def test_multiple_colors(self):
        """Prueba detección de múltiples colores."""
        command = "Crea un cubo azul y una esfera roja"
        entities = self.extractor.extract(command)
        # Debería detectar al menos color
        self.assertIn('color', entities)
    
    def test_size_units(self):
        """Prueba detección de tamaño con unidades."""
        commands = [
            "Tamaño 5 metros",
            "Size: 10m",
            "Escala 2.5 cm"
        ]
        for cmd in commands:
            entities = self.extractor.extract(cmd)
            # Debería detectar tamaño
            self.assertTrue(any(k in ['tamaño', 'escala'] for k in entities.keys()))
    
    def test_rotation_extraction(self):
        """Prueba extracción de rotación."""
        command = "Rotación 45, 90, 180"
        entities = self.extractor.extract(command)
        if 'rotacion' in entities:
            self.assertIsNotNone(entities['rotacion'].value)
    
    def test_quantity_extraction(self):
        """Prueba extracción de cantidad."""
        commands = [
            "Crear 5 cubos",
            "Duplicar 3 esferas",
            "Hacer 10 objetos"
        ]
        for cmd in commands:
            entities = self.extractor.extract(cmd)
            if 'cantidad' in entities:
                self.assertGreater(entities['cantidad'].value, 0)
    
    def test_confidence_scores(self):
        """Prueba que las confianzas sean coherentes."""
        command = "Crea un cubo rojo en posición 1,2,3"
        entities = self.extractor.extract(command)
        
        for name, entity in entities.items():
            self.assertGreaterEqual(entity.confidence, 0.0)
            self.assertLessEqual(entity.confidence, 1.0)
    
    def test_entity_validation(self):
        """Prueba validación de entidades."""
        # Crear entidades válidas
        valid_entities = {
            'tamaño': type('E', (), {'value': 5, 'confidence': 0.9})(),
        }
        is_valid, errors = self.extractor.validate_entities(valid_entities)
        self.assertTrue(is_valid)
        
        # Crear entidades inválidas
        invalid_entities = {
            'tamaño': type('E', (), {'value': -5, 'confidence': 0.9})(),
        }
        is_valid, errors = self.extractor.validate_entities(invalid_entities)
        self.assertFalse(is_valid)
    
    def test_empty_command(self):
        """Prueba con comando vacío."""
        entities = self.extractor.extract("")
        self.assertIsInstance(entities, dict)
    
    def test_unknown_command(self):
        """Prueba con comando desconocido."""
        entities = self.extractor.extract("Haz algo completamente aleatorio")
        # Debería retornar dict vacío o sin entidades relevantes
        self.assertIsInstance(entities, dict)


if __name__ == '__main__':
    unittest.main()
