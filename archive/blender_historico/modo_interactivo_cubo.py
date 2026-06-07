"""
modo_interactivo_cubo.py
========================

Script interactivo para probar la primitiva de cubo con Zuly en consola.
Permite enviar comandos en lenguaje natural y ver la respuesta del agente.
"""

from core.agent import Agent

# Inicializar agente
agent = Agent(auto_monitor=True)

print("\n=== MODO INTERACTIVO: PRIMITIVA DE CUBO ===\n")
print("Escribe comandos en lenguaje natural para crear o modificar cubos.")
print("Ejemplo: 'Crea un cubo de oro en (2,0,0) con escala 3'\n")
print("Escribe 'salir' para terminar.\n")

while True:
    user_input = input("Tú > ")
    if user_input.strip().lower() in ("salir", "exit", "quit"): 
        print("Saliendo del modo interactivo.")
        break
    result = agent.process_natural_request(user_input)
    print("Zuly >", result.get('feedback', result))
