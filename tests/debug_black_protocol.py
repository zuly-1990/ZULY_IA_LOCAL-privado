import sys
import os
import traceback
from unittest.mock import MagicMock, patch

# Añadir el path raíz para importar core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.agent import Agent
from core.utils.nlu import CommandIntent

def debug_block():
    print("--- INICIO DEPURACIÓN PROTOCOLO NEGRO ---")
    try:
        with patch('core.agent.is_author_verified', return_value=True), \
             patch('core.agent.CommandLoader'), \
             patch('core.agent.NaturalLanguageProcessor'), \
             patch('core.agent.SceneMonitor'), \
             patch('core.agent.V0Validator'), \
             patch('core.agent.PatternMemory'), \
             patch('core.agent.StateAwareness'), \
             patch('core.agent.BlenderObserver'), \
             patch('core.agent.BlenderSemanticObserver'), \
             patch('core.agent.IntentionSimulator'), \
             patch('core.agent.TraceCore'):
            
            agent = Agent()
            agent.authorized = False # Simulamos acceso no verificado
            
            # Mocks necesarios para process_natural_request
            agent.nlu.process = MagicMock(return_value=[CommandIntent("CREATE", 0.95)])
            agent.analyze_scene = MagicMock(return_value={"context": {}})
            
            print("Procesando petición...")
            result = agent.process_natural_request("crea algo")
            print(f"Resultado: {result}")
            
    except Exception:
        print("ERROR DETECTADO:")
        traceback.print_exc()

if __name__ == '__main__':
    debug_block()
