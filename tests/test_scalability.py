"""
Test Scalability - Rolling Window
Tests para verificar que los límites de memoria funcionan correctamente.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import ExecutionContext


class TestExecutionContextScalability(unittest.TestCase):
    """Tests de escalabilidad del ExecutionContext."""
    
    def test_rolling_window_execution_history(self):
        """Execution history no debe exceder MAX_EXECUTION_HISTORY."""
        ctx = ExecutionContext()
        
        # Agregar más comandos que el límite
        for i in range(150):
            ctx.add_execution(f'command_{i}', success=True)
        
        # Verificar que se mantuvo el límite
        self.assertLessEqual(
            len(ctx.execution_history), 
            ExecutionContext.MAX_EXECUTION_HISTORY
        )
        
        # Verificar que los más recientes están presentes
        last_cmd = ctx.execution_history[-1]['command']
        self.assertEqual(last_cmd, 'command_149')
    
    def test_rolling_window_scene_states(self):
        """Scene states no debe exceder MAX_SCENE_STATES."""
        ctx = ExecutionContext()
        
        # Agregar más estados que el límite
        for i in range(50):
            ctx.add_scene_state({'state_id': i})
        
        # Verificar límite
        self.assertLessEqual(
            len(ctx.scene_states),
            ExecutionContext.MAX_SCENE_STATES
        )
        
        # Verificar que los más recientes están
        last_state = ctx.scene_states[-1]['state_id']
        self.assertEqual(last_state, 49)
    
    def test_rolling_window_errors(self):
        """Errors no debe exceder MAX_ERRORS."""
        ctx = ExecutionContext()
        
        # Agregar más errores que el límite
        for i in range(100):
            ctx.add_execution(f'cmd_{i}', success=False, error=f'error_{i}')
        
        # Verificar límite
        self.assertLessEqual(
            len(ctx.errors),
            ExecutionContext.MAX_ERRORS
        )
    
    def test_counts_preserved_after_rolling(self):
        """Los contadores totales deben preservarse aunque el historial se recorte."""
        ctx = ExecutionContext()
        
        # Agregar muchos comandos
        for i in range(200):
            ctx.add_execution(f'cmd_{i}', success=(i % 2 == 0))
        
        # El historial está recortado
        self.assertLessEqual(len(ctx.execution_history), 100)
        
        # Pero los contadores totales se mantienen
        summary = ctx.get_summary()
        self.assertEqual(summary['total_successes'], 100)  # 0,2,4...198 = 100 pares
        self.assertEqual(summary['total_failures'], 100)
    
    def test_memory_summary(self):
        """get_summary debe incluir información de memoria."""
        ctx = ExecutionContext()
        
        for i in range(10):
            ctx.add_execution(f'cmd_{i}', success=True)
        ctx.add_scene_state({'test': True})
        
        summary = ctx.get_summary()
        
        self.assertIn('memory', summary)
        self.assertEqual(summary['memory']['history_size'], 10)
        self.assertEqual(summary['memory']['scene_states'], 1)


if __name__ == '__main__':
    unittest.main()
