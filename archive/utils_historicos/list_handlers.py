"""Listar todos los handlers registrados"""
from core.agent import Agent

agent = Agent(force_mock=True)
handlers = sorted(agent.intent_router.command_handlers.keys())

print(f"\nTotal de handlers registrados: {len(handlers)}\n")
print("Lista completa:")
for i, h in enumerate(handlers, 1):
    print(f"{i:2}. {h}")
