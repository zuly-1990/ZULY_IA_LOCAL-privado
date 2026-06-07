"""
core.cognition
===============

Módulo de Cognición Base (Plan C)

Componentes:
- C1: Evaluador de Resultados
- C2: Memoria de Experiencias (próximo)
- C3: Objetivos Abstractos (próximo)
- C4: Autoajuste Procedural (próximo)
"""

from .c1_result_evaluator import (
    C1ResultEvaluator,
    SceneAnalyzer,
    MetricsCalculator,
    DiagnosticGenerator,
    EvaluationResult,
    Diagnostic,
    MetricResult,
    EvaluationStatus,
    MetricType
)

__all__ = [
    "C1ResultEvaluator",
    "SceneAnalyzer",
    "MetricsCalculator",
    "DiagnosticGenerator",
    "EvaluationResult",
    "Diagnostic",
    "MetricResult",
    "EvaluationStatus",
    "MetricType"
]

__version__ = "1.0.0"
