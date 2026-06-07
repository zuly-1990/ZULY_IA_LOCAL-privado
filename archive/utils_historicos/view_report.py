"""Script simple para ver el reporte del sistema"""
from core.agent import Agent

agent = Agent(force_mock=True)
print("\n=== REPORTE DEL SISTEMA ===\n")
print(agent.system_report())
