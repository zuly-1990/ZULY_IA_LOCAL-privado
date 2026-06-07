"""
Tests Mínimos para ExecutionShell - Fase 5.18

Propósito:
- Validar que ExecutionShell existe
- Validar que ejecuta callables
- Validar que NO decide
- Tests estructurales + mecánicos, NO cognitivos

Regla: Solo tests especificados.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.execution.execution_shell import ExecutionShell


class TestExecutionShellMinimal(unittest.TestCase):
    """
    Tests mínimos para ExecutionShell.
    
    Tests estructurales + mecánicos, NO cognitivos.
    """
    
    def test_1_shell_existe(self):
        """Test 1: El shell existe"""
        print("\n[TEST 1] Shell existe")
        
        # Validar que la clase existe
        self.assertTrue(hasattr(ExecutionShell, 'execute'))
        
        # Validar que execute es estático
        self.assertTrue(callable(ExecutionShell.execute))
        
        print("  ✓ ExecutionShell existe con método execute")
    
    def test_2_ejecuta_callable(self):
        """Test 2: Ejecuta callable simple"""
        print("\n[TEST 2] Ejecuta callable")
        
        # Función simple de prueba
        def suma(a, b):
            return a + b
        
        # Ejecutar a través del shell
        result = ExecutionShell.execute(suma, 2, 3)
        
        # Validar resultado
        self.assertEqual(result, 5)
        
        print("  ✓ Shell ejecuta callables correctamente")
    
    def test_3_no_decide(self):
        """Test 3: NO contiene lógica de decisión"""
        print("\n[TEST 3] NO decide")
        
        # Validar que execute no tiene lógica de decisión
        import inspect
        source = inspect.getsource(ExecutionShell.execute)
        
        # Verificar que no hay keywords de decisión/lógica de negocio
        # (permitimos solo el return y la llamada al callable)
        decision_keywords = ['if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except:', 'match ']
        
        # Buscar keywords de decisión (excluyendo los que están en docstrings)
        lines = source.split('\n')
        code_lines = []
        in_docstring = False
        
        for line in lines:
            stripped = line.strip()
            if '"""' in stripped or "'''" in stripped:
                in_docstring = not in_docstring
                continue
            if not in_docstring and stripped and not stripped.startswith('#'):
                code_lines.append(stripped)
        
        # Verificar que no hay keywords de decisión en código real
        code = ' '.join(code_lines)
        for keyword in decision_keywords:
            self.assertNotIn(keyword, code, f"ExecutionShell.execute contiene '{keyword}' (lógica de decisión)")
        
        print("  ✓ Shell NO contiene lógica de decisión")
    
    def test_4_no_importa_core(self):
        """Test 4: NO importa módulos del núcleo cognitivo"""
        print("\n[TEST 4] NO importa núcleo cognitivo")
        
        # Validar que ExecutionShell no importa módulos cognitivos
        import core.execution.execution_shell as shell_module
        
        shell_source = shell_module.__file__
        with open(shell_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que no hay imports del núcleo
        self.assertNotIn('from core.agent', content)
        self.assertNotIn('from core.state', content)
        self.assertNotIn('from core.intention', content)
        self.assertNotIn('from core.command', content)
        self.assertNotIn('from core.learning', content)
        
        print("  ✓ Shell NO importa núcleo cognitivo")
    
    def test_5_no_estado_no_intencion(self):
        """Test 5: NO lee estado ni genera intención"""
        print("\n[TEST 5] NO estado, NO intención")
        
        # Validar que el código no contiene referencias a estado o intención
        import core.execution.execution_shell as shell_module
        
        shell_source = shell_module.__file__
        with open(shell_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que no hay referencias
        self.assertNotIn('StateAwareness', content)
        self.assertNotIn('IntentionBoundary', content)
        self.assertNotIn('CommandGate', content)
        self.assertNotIn('PatternMemory', content)
        
        print("  ✓ Shell NO lee estado ni genera intención")


if __name__ == '__main__':
    print("="*70)
    print("TESTS MÍNIMOS - EXECUTION SHELL (FASE 5.18)")
    print("="*70)
    print("\nTests cubiertos:")
    print("1. El shell existe")
    print("2. Ejecuta callable simple")
    print("3. NO contiene lógica de decisión")
    print("4. NO importa núcleo cognitivo")
    print("5. NO lee estado ni genera intención")
    print("\nTests estructurales + mecánicos, NO cognitivos.")
    print("="*70)
    unittest.main(verbosity=2)
