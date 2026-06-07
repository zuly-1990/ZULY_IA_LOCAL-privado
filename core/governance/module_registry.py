"""
core/governance/module_registry.py

Fase 18.5 — Control de Complejidad

Registro centralizado de módulos activos.
Permite saber qué está vivo en ZULY.
"""

from typing import Dict


class ModuleRegistry:
    """
    Registro centralizado de módulos activos.
    
    Permite rastrear qué módulos están cargados y activos.
    Evita crecimiento invisible del sistema.
    """
    
    def __init__(self):
        self.modules: Dict[str, str] = {}
    
    def register(self, name: str):
        """Registra un módulo como activo."""
        self.modules[name] = "active"
    
    def snapshot(self) -> Dict[str, str]:
        """Retorna snapshot de módulos activos."""
        return dict(self.modules)
    
    def count(self) -> int:
        """Cuenta módulos activos."""
        return len(self.modules)


# Instancia global
registry = ModuleRegistry()
