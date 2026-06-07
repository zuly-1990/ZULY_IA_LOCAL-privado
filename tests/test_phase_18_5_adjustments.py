"""
Test Fase 18.5 - Ajustes Post-Pruebas
Tests para los nuevos módulos de control, seguridad y trazabilidad.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.guards.environment_guard import EnvironmentGuard, get_environment_guard
from core.observability.action_logger import ActionLogger, get_action_logger
from core.execution.failsafe_executor import FailsafeExecutor, ExecutionState
from core.memory.volatile_memory import VolatileMemory, get_volatile_memory
from core.adapters.mock_adapter import MockAdapter


class TestEnvironmentGuard(unittest.TestCase):
    """Tests para el guardián de entorno."""
    
    def test_validate_with_mock_adapter(self):
        """Debe validar correctamente con MockAdapter."""
        adapter = MockAdapter()
        guard = EnvironmentGuard(adapter=adapter)
        
        context = guard.validate_environment()
        
        self.assertTrue(context.is_valid)
        self.assertEqual(context.scene_name, 'Scene')  # MockAdapter returns 'Scene'
        self.assertEqual(len(context.validation_errors), 0)
    
    def test_can_proceed(self):
        """can_proceed debe retornar True con adapter válido."""
        adapter = MockAdapter()
        guard = EnvironmentGuard(adapter=adapter)
        
        self.assertTrue(guard.can_proceed())
    
    def test_describe_current_state(self):
        """describe_current_state debe retornar info completa."""
        adapter = MockAdapter()
        guard = EnvironmentGuard(adapter=adapter)
        
        state = guard.describe_current_state()
        
        self.assertTrue(state['valid'])
        self.assertIn('scene', state)
        self.assertIn('object_count', state)


class TestActionLogger(unittest.TestCase):
    """Tests para el logger de acciones."""
    
    def setUp(self):
        self.logger = ActionLogger()
    
    def test_log_action(self):
        """Debe registrar acciones correctamente."""
        record = self.logger.log_action("create_cube", "Cube_001", True, "size=2m")
        
        self.assertEqual(record.action, "create_cube")
        self.assertEqual(record.target, "Cube_001")
        self.assertEqual(record.result, "OK")
    
    def test_log_ok_shortcut(self):
        """log_ok debe crear registro exitoso."""
        record = self.logger.log_ok("move_object", "Cube")
        self.assertEqual(record.result, "OK")
    
    def test_log_fail_shortcut(self):
        """log_fail debe crear registro fallido."""
        record = self.logger.log_fail("delete", "Sphere", "Not found")
        self.assertEqual(record.result, "FAIL")
    
    def test_rolling_window(self):
        """Debe respetar el límite de rolling window."""
        for i in range(600):
            self.logger.log_action(f"action_{i}", f"target_{i}", True)
        
        self.assertLessEqual(len(self.logger._records), ActionLogger.MAX_RECORDS)
    
    def test_session_summary(self):
        """get_session_summary debe retornar estadísticas correctas."""
        self.logger.log_ok("a1", "t1")
        self.logger.log_ok("a2", "t2")
        self.logger.log_fail("a3", "t3")
        
        summary = self.logger.get_session_summary()
        
        self.assertEqual(summary['total_actions'], 3)
        self.assertEqual(summary['ok_count'], 2)
        self.assertEqual(summary['fail_count'], 1)
    
    def test_export_to_markdown(self):
        """export_to_markdown debe generar formato válido."""
        self.logger.log_ok("create", "Cube")
        
        md = self.logger.export_to_markdown()
        
        self.assertIn("# Action Log", md)
        self.assertIn("create", md)
        self.assertIn("Cube", md)


class TestFailsafeExecutor(unittest.TestCase):
    """Tests para el ejecutor fail-safe."""
    
    def setUp(self):
        self.executor = FailsafeExecutor()
    
    def test_initial_state(self):
        """Debe iniciar en estado READY."""
        self.assertEqual(self.executor.state, ExecutionState.READY)
        self.assertFalse(self.executor.is_stopped)
    
    def test_execute_success(self):
        """Debe ejecutar handler exitoso correctamente."""
        def mock_handler(params):
            return {'success': True, 'message': 'Done'}
        
        result = self.executor.execute_single("test_action", mock_handler, {})
        
        self.assertTrue(result.success)
        self.assertFalse(result.stopped)
        self.assertEqual(self.executor.state, ExecutionState.READY)
    
    def test_execute_failure_stops(self):
        """Debe detenerse cuando un handler falla."""
        def failing_handler(params):
            return {'success': False, 'error': 'Something went wrong'}
        
        result = self.executor.execute_single("fail_action", failing_handler, {})
        
        self.assertFalse(result.success)
        self.assertTrue(result.stopped)
        self.assertEqual(self.executor.state, ExecutionState.STOPPED)
        self.assertEqual(self.executor.last_error, 'Something went wrong')
    
    def test_cannot_execute_when_stopped(self):
        """No debe ejecutar si está detenido."""
        # Primero, hacer que falle
        def failing_handler(params):
            return {'success': False, 'error': 'Error'}
        
        self.executor.execute_single("fail", failing_handler, {})
        
        # Intentar ejecutar otra acción
        def ok_handler(params):
            return {'success': True}
        
        result = self.executor.execute_single("next", ok_handler, {})
        
        self.assertFalse(result.success)
        self.assertIn("stopped", result.error.lower())
    
    def test_reset_allows_continue(self):
        """reset() debe permitir continuar después de fallo."""
        def failing_handler(params):
            return {'success': False, 'error': 'Error'}
        
        self.executor.execute_single("fail", failing_handler, {})
        self.assertTrue(self.executor.is_stopped)
        
        # Reset
        self.executor.reset()
        
        self.assertFalse(self.executor.is_stopped)
        self.assertEqual(self.executor.state, ExecutionState.READY)
    
    def test_sequence_stops_on_first_failure(self):
        """execute_sequence debe detenerse en el primer fallo."""
        def ok_handler(params):
            return {'success': True}
        
        def fail_handler(params):
            return {'success': False, 'error': 'Fail'}
        
        actions = [
            {'action_name': 'a1', 'handler': ok_handler, 'parameters': {}},
            {'action_name': 'a2', 'handler': fail_handler, 'parameters': {}},
            {'action_name': 'a3', 'handler': ok_handler, 'parameters': {}},  # No debe ejecutarse
        ]
        
        results = self.executor.execute_sequence(actions)
        
        self.assertEqual(len(results), 2)  # Solo 2 ejecutados
        self.assertTrue(results[0].success)
        self.assertFalse(results[1].success)


class TestVolatileMemory(unittest.TestCase):
    """Tests para la memoria volátil."""
    
    def setUp(self):
        self.memory = VolatileMemory()
    
    def test_register_object(self):
        """Debe registrar objetos correctamente."""
        self.memory.register_object("Cube", {"type": "MESH"})
        
        self.assertTrue(self.memory.object_exists("Cube"))
        self.assertEqual(self.memory.get_object_count(), 1)
    
    def test_unregister_object(self):
        """Debe eliminar objetos correctamente."""
        self.memory.register_object("Cube", {"type": "MESH"})
        
        result = self.memory.unregister_object("Cube")
        
        self.assertTrue(result)
        self.assertFalse(self.memory.object_exists("Cube"))
    
    def test_scene_change_clears_memory(self):
        """Cambiar escena debe limpiar toda la memoria."""
        self.memory.set_scene("Scene1")
        self.memory.register_object("Cube", {"type": "MESH"})
        self.memory.register_object("Sphere", {"type": "MESH"})
        
        # Cambiar escena
        self.memory.set_scene("Scene2")
        
        self.assertEqual(self.memory.get_object_count(), 0)
    
    def test_sync_removes_ghosts(self):
        """sync_with_scene debe eliminar referencias fantasma."""
        self.memory.register_object("Cube", {"type": "MESH"})
        self.memory.register_object("Sphere", {"type": "MESH"})
        self.memory.register_object("Ghost", {"type": "MESH"})
        
        # Solo Cube y Sphere existen en la escena real
        self.memory.sync_with_scene(["Cube", "Sphere"])
        
        self.assertTrue(self.memory.object_exists("Cube"))
        self.assertTrue(self.memory.object_exists("Sphere"))
        self.assertFalse(self.memory.object_exists("Ghost"))
    
    def test_active_object_cleared_on_sync(self):
        """Objeto activo debe limpiarse si ya no existe."""
        self.memory.register_object("Cube", {"type": "MESH"})
        self.memory.set_active_object("Cube")
        
        # Cube ya no existe en escena
        self.memory.sync_with_scene([])
        
        self.assertIsNone(self.memory.get_active_object())


if __name__ == '__main__':
    unittest.main()
