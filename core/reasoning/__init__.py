"""
core/reasoning/__init__.py

Módulo de razonamiento de ZULY.
Exports simplificados para evitar errores de dependencias circulares.
"""

# Funciones principales - import directo cuando sea necesario
# from .decision_chain_simulator import simulate_decision_chain
# from .explain_engine import ExplainEngine
# etc.

# Por ahora, __init__.py mínimo para que el paquete sea importable
__all__ = [
    'decision_chain_simulator',
    'explain_engine',
    'inference_engine',
    'intention_classifier',
    'intention_simulator',
    'permission_gate',
    'resolution_engine',
]
