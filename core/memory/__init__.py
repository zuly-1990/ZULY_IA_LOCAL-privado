"""
core/memory/__init__.py

Módulo de memoria de ZULY.
Exports simplificados para evitar errores de dependencias circulares.
"""

# Clases principales - import directo cuando sea necesario
# from .memory_manager import MemoryManager
# from .trace_core import TraceCore
# etc.

# Por ahora, __init__.py mínimo para que el paquete sea importable
__all__ = [
    'archiver',
    'consequence_memory',
    'memory_manager',
    'retention_policy',
    'trace_core',
    'volatile_memory',
]
