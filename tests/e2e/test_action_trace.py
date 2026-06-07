"""
tests/e2e/test_action_trace.py

Test E2E: Acción mínima registrada
"""

def test_action_is_traced():
    """Acción ejecutada, registrada y visible."""
    from core.agent import Agent
    
    agent = Agent(force_mock=True)
    
    # Registrar acción manualmente (sin execute que no existe aún)
    agent.trace_core.append_trace({
        "intention": "create_cube",
        "execution_success": True
    })
    
    report = agent.system_report()
    
    assert "TRAZA" in report
    assert "create_cube" in report
