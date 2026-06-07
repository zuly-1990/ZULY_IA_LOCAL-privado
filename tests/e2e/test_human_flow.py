"""
tests/e2e/test_human_flow.py

Test E2E: Flujo completo humano
Este test vale oro. Si pasa, el sistema tiene coherencia.
"""

def test_full_human_flow():
    """Flujo completo: múltiples acciones, todas visibles."""
    from core.agent import Agent
    
    agent = Agent(force_mock=True)
    
    # Contar eventos iniciales
    initial_count = len(agent.trace_core.traces)
    
    # Simular acciones
    agent.trace_core.append_trace({
        "intention": "create_cube",
        "execution_success": True
    })
    
    agent.trace_core.append_trace({
        "intention": "move_object",
        "execution_success": True
    })
    
    report = agent.system_report()
    
    # Verificar coherencia del sistema
    assert "TRAZA" in report, "Debe incluir sección TRAZA"
    assert "move_object" in report, "Debe mostrar último evento"
    assert "Eventos registrados:" in report, "Debe contar eventos"
    
    # Verificar que el conteo aumentó
    final_count = len(agent.trace_core.traces)
    assert final_count == initial_count + 2, f"Debe tener {initial_count + 2} eventos, tiene {final_count}"
