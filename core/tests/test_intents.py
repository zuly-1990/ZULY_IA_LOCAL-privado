"""
core/tests/test_intents.py
=========================

Pruebas unitarias para el módulo de intenciones.
"""

import unittest
from core.intents import EntityExtractor, IntentManager, IntentRouter


class TestEntityExtractor(unittest.TestCase):
    """Pruebas para la extracción de entidades."""
    
    def setUp(self):
        self.extractor = EntityExtractor()
    
    def test_extract_object(self):
        """Prueba extracción de objeto."""
        command = "Crea un cubo"
        entities = self.extractor.extract(command)
        self.assertIn('objeto', entities)
        self.assertEqual(entities['objeto'].value, 'Cube')
    
    def test_extract_color(self):
        """Prueba extracción de color."""
        command = "Crea un cubo rojo"
        entities = self.extractor.extract(command)
        self.assertIn('color', entities)
        self.assertEqual(entities['color'].value, (1.0, 0.0, 0.0))
    
    def test_extract_position(self):
        """Prueba extracción de posición."""
        command = "Posiciona en 5,10,15"
        entities = self.extractor.extract(command)
        self.assertIn('posicion', entities)
        x, y, z = entities['posicion'].value
        self.assertEqual((x, y, z), (5.0, 10.0, 15.0))
    
    def test_validate_entities(self):
        """Prueba validación de entidades."""
        entities = {
            'tamaño': type('Entity', (), {'value': 5.0})(),
            'posicion': type('Entity', (), {'value': (0, 0, 0), 'confidence': 0.9})(),
        }
        # Estas pruebas necesitan ajustarse al Dataclass Entity
        pass
    
    def test_extract_all(self):
        """Prueba extracción múltiple."""
        command = "Crea un cubo rojo en posición 2,3,4 con tamaño 5"
        entities = self.extractor.extract(command)
        self.assertGreater(len(entities), 0)


class TestIntentManager(unittest.TestCase):
    """Pruebas para el gestor de intenciones."""
    
    def setUp(self):
        self.manager = IntentManager()
    
    def test_classify_crear_objeto(self):
        """Prueba clasificación de intención crear."""
        intent = self.manager.classify("Crea un cubo")
        self.assertEqual(intent.name, 'crear_objeto')
        self.assertGreater(intent.confidence, 0.6)
    
    def test_classify_renderizar(self):
        """Prueba clasificación de intención renderizar."""
        intent = self.manager.classify("Renderiza la escena")
        self.assertEqual(intent.name, 'renderizar')
    
    def test_classify_mover(self):
        """Prueba clasificación de intención mover."""
        intent = self.manager.classify("Mueve el cubo a otra posición")
        self.assertEqual(intent.name, 'mover_objeto')
    
    def test_list_intents(self):
        """Prueba listado de intenciones."""
        intents = self.manager.list_intents()
        self.assertGreater(len(intents), 5)
        self.assertIn('crear_objeto', intents)


class TestIntentRouter(unittest.TestCase):
    """Pruebas para el router de intenciones."""
    
    def setUp(self):
        self.router = IntentRouter()
        # Registrar handler de prueba
        self.router.register_handler('test.command', lambda entities: 'success')
    
    def test_register_handler(self):
        """Prueba registro de handler."""
        self.assertIn('test.command', self.router.command_handlers)
    
    def test_route_and_execute(self):
        """Prueba enrutamiento y ejecución."""
        intent = {'command': 'test.command', 'name': 'test'}
        result = self.router.route_and_execute(intent, {})
        self.assertEqual(result.output, 'success')
    
    def test_missing_handler(self):
        """Prueba comportamiento con handler faltante."""
        intent = {'command': 'nonexistent.command', 'name': 'test'}
        result = self.router.route_and_execute(intent, {})
        self.assertIn('failed', result.status.value.lower())
    
    def test_execution_history(self):
        """Prueba historial de ejecuciones."""
        intent = {'command': 'test.command', 'name': 'test'}
        self.router.route_and_execute(intent, {})
        history = self.router.get_history()
        self.assertEqual(len(history), 1)


if __name__ == '__main__':
    unittest.main()
