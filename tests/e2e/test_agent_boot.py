"""
tests/e2e/test_agent_boot.py

Test E2E: Arranque limpio de ZULY
"""

def test_agent_boots_cleanly():
    """ZULY despierta y puede verse a sí misma."""
    from core.agent import Agent
    
    agent = Agent(force_mock=True)
    
    report = agent.system_report()
    
    assert "ESTADO DEL SISTEMA" in report
    assert "Adapter" in report or "ADAPTER" in report
