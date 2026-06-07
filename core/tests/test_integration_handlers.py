"""
test_integration_handlers.py

Tests de integración que validan handlers con LYZU Core.
"""

import unittest
from lyzu_core import LYZUCore
from core.commands.blender_handlers.primitives import (
    create_cube_handler,
    create_sphere_handler,
)
from core.commands.blender_handlers.transforms import (
    move_object_handler,
)


class TestHandlerIntegration(unittest.TestCase):
    """Tests de integración: handlers + LYZU Core"""
    
    def setUp(self):
        """Inicializa LYZU para cada test."""
        self.lyzu = LYZUCore(mode='reactive')
    
    def test_handlers_registered(self):
        """Verifica que los handlers están registrados."""
        handlers = self.lyzu.intent_router.get_handler_list()
        
        self.assertIn('blender.create_cube', handlers)
        self.assertIn('blender.create_sphere', handlers)
        self.assertIn('blender.move_object', handlers)
        self.assertGreaterEqual(len(handlers), 5)
    
    def test_create_cube_handler_direct(self):
        """Prueba directo del handler de crear cubo."""
        result = create_cube_handler({
            'location': [0, 0, 0],
            'scale': 1.0,
            'color': [1.0, 0.0, 0.0]
        })
        
        # Sin Blender, debe fallar gracefully
        self.assertIn('success', result)
        self.assertIn('error', result)
    
    def test_move_object_handler_direct(self):
        """Prueba directo del handler de mover."""
        result = move_object_handler({
            'location': [5, 10, 15]
        })
        
        self.assertIn('success', result)
        self.assertIn('error', result)
    
    def test_intent_to_handler_mapping(self):
        """Verifica que intenciones se mapean a handlers."""
        intents = self.lyzu.intent_manager.list_intents()
        
        # Verificar que crear_objeto está en el catálogo
        self.assertIn('crear_objeto', intents)
        self.assertIn('renderizar', intents)
        self.assertIn('mover_objeto', intents)
    
    def test_full_pipeline_with_memory_limit(self):
        """Prueba pipeline completo con límite de memoria."""
        inputs = [
            "Crea un cubo",
            "Crea una esfera",
            "Renderiza",
        ]
        
        for user_input in inputs:
            result = self.lyzu.process_user_input(user_input)
            self.assertIsNotNone(result)
        
        # Verificar que memoria tiene límite
        stats = self.lyzu.memory.get_memory_stats()
        self.assertLessEqual(stats['turns_in_memory'], stats['max_turns'])
    
    def test_memory_archiving(self):
        """Verifica que turnos se archivan cuando se excede límite."""
        # Crear sesión con límite bajo para testing
        self.lyzu.memory.max_turns = 3
        
        # Agregar turnos
        for i in range(5):
            from lyzu_core import ConversationTurn
            turn = ConversationTurn(
                timestamp="2025-12-08T12:00:00",
                user_input=f"Command {i}",
                intent="test",
                entities={},
                command_executed="test.command",
                result="{}",
                confidence=0.9
            )
            self.lyzu.memory.add_turn(turn)
        
        # Verificar que solo quedan 3 en memoria
        self.assertEqual(len(self.lyzu.memory.turns), 3)
        # Pero se archivaron los antiguos
        self.assertGreater(self.lyzu.memory.archived_turns_count, 0)


class TestHandlerResponses(unittest.TestCase):
    """Tests que validan estructura de respuestas de handlers."""
    
    def test_cube_handler_response_structure(self):
        """Valida estructura de respuesta del handler de cubo."""
        result = create_cube_handler({'location': [0, 0, 0]})
        
        # Debe tener 'success' y alguno de ['error', 'message', 'object_name']
        self.assertIn('success', result)
        self.assertIsInstance(result['success'], bool)
        
        if not result['success']:
            self.assertIn('error', result)
    
    def test_handler_parameter_validation(self):
        """Valida que handlers validan parámetros."""
        # Parámetros inválidos
        result = create_cube_handler({
            'location': [0, 0],  # Falta Z
            'scale': -1  # Escala negativa
        })
        
        # Debe fallar
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_sphere_handler_subdivisions(self):
        """Prueba que subdivisions se respeta."""
        result = create_sphere_handler({
            'location': [0, 0, 0],
            'subdivisions': 16
        })
        
        self.assertIn('success', result)


class TestMemoryStats(unittest.TestCase):
    """Tests para estadísticas de memoria."""
    
    def test_memory_stats_structure(self):
        """Valida estructura de stats de memoria."""
        lyzu = LYZUCore()
        stats = lyzu.memory.get_memory_stats()
        
        self.assertIn('turns_in_memory', stats)
        self.assertIn('max_turns', stats)
        self.assertIn('archived_turns', stats)
        self.assertIn('total_turns_processed', stats)
        self.assertIn('memory_usage_pct', stats)
    
    def test_memory_usage_percentage(self):
        """Verifica que porcentaje de memoria es correcto."""
        lyzu = LYZUCore()
        lyzu.memory.max_turns = 100
        
        # Agregar 50 turnos
        for i in range(50):
            from lyzu_core import ConversationTurn
            turn = ConversationTurn(
                timestamp="2025-12-08T12:00:00",
                user_input=f"Input {i}",
                intent="test",
                entities={},
                command_executed="test",
                result="{}",
                confidence=0.9
            )
            lyzu.memory.add_turn(turn)
        
        stats = lyzu.memory.get_memory_stats()
        self.assertEqual(stats['memory_usage_pct'], 50.0)


if __name__ == '__main__':
    unittest.main()
