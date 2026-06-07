"""
core/diagnostics/__init__.py

Sistema de Auto-Diagnóstico de ZULY.
FASE 22: Auto-Diagnóstico Controlado.

Filosofía:
- ZULY detecta problemas, NO los arregla
- Reportes estructurados y trazables
- Clasificación de severidad
- Compatible con Protocolo Negro
"""

from .system_health_checker import SystemHealthChecker, CheckResult, HealthReport
from .module_validator import ModuleValidator
from .diagnostic_reporter import DiagnosticReporter, IssueSeverity

__all__ = [
    'SystemHealthChecker',
    'CheckResult',
    'HealthReport',
    'ModuleValidator',
    'DiagnosticReporter',
    'IssueSeverity',
]
