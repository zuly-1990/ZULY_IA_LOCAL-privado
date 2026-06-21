import os
import logging
import pprint
from core.agent import Agent

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

def test_c3():
    print("Iniciando Agente en modo force_mock...")
    agent = Agent(force_mock=True)
    
    print("\nEnviando solicitud C3 (Descomposición)...")
    res = agent.process_natural_request("descomponer: crea un templo con pilares")
    
    print("\nResultado General:")
    pprint.pprint(res)

if __name__ == "__main__":
    test_c3()
