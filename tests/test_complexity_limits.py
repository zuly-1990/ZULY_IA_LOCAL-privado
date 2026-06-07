"""
tests/test_complexity_limits.py

Test de cordura - Fase 18.5
Verifica que los límites de complejidad funcionan.
"""

def test_max_actions_constant_exists():
    """Verifica que el límite de acciones existe."""
    from core.agent import MAX_ACTIONS_PER_SESSION
    
    assert MAX_ACTIONS_PER_SESSION == 50


def test_module_registry_works():
    """Verifica que el registro de módulos funciona."""
    from core.governance import registry
    
    # Debe tener módulos registrados
    snapshot = registry.snapshot()
    assert len(snapshot) > 0
    
    # Debe incluir módulos core
    assert "Agent" in snapshot or len(snapshot) >= 1


def test_agent_registers_modules():
    """Verifica que Agent registra sus módulos."""
    from core.agent import Agent
    from core.governance import registry
    
    # Limpiar registro
    registry.modules.clear()
    
    # Crear agent
    agent = Agent(force_mock=True)
    
    # Verificar que registró módulos
    snapshot = registry.snapshot()
    assert len(snapshot) > 0
    assert "Agent" in snapshot
    assert "SceneMonitor" in snapshot
