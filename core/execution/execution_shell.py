"""
Execution Shell - Cápsula de Ejecución Neutra (Fase 5.18)

Responsabilidad:
- Ejecutar comandos explícitos ya autorizados
- NO validar
- NO decidir
- NO interpretar
- SOLO ejecutar

Principio Rector:
"Ejecutar no implica comprender ni elegir."

La ejecución es un acto mecánico, no cognitivo.
"""

from typing import Any, Callable


class ExecutionShell:
    """
    Capa de ejecución neutra.
    
    Ejecuta comandos explícitos ya autorizados.
    No valida, no decide, no interpreta.
    
    Separación definitiva:
    - Núcleo: Control / Límites / Filosofía
    - Shell: Ejecución pura
    """
    
    @staticmethod
    def execute(callable_fn: Callable, *args: Any, **kwargs: Any) -> Any:
        """
        Ejecuta una función ya validada externamente.
        
        Esta función NO:
        - Decide si algo debe ejecutarse
        - Analiza texto
        - Lee estado
        - Consulta intención
        - Genera comandos
        - Encadena acciones
        - Reintenta automáticamente
        - Registra aprendizaje
        - Modifica el núcleo
        
        Solo ejecuta.
        
        Args:
            callable_fn: Función a ejecutar (ya validada)
            *args: Argumentos posicionales
            **kwargs: Argumentos con nombre
            
        Returns:
            Resultado de la ejecución
            
        Raises:
            Exception: Cualquier excepción técnica de la ejecución
        """
        return callable_fn(*args, **kwargs)


# Constantes de validación
EXECUTION_IS_MECHANICAL = True
EXECUTION_IS_COGNITIVE = False

# Mensaje de advertencia
WARNING_MESSAGE = (
    "Ejecutar no implica comprender ni elegir. "
    "La ejecución es un acto mecánico, no cognitivo."
)
