import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.absolute()))
from core.agent import Agent

def main():
    agent = Agent(force_mock=True)
    request = "crear un cubo luego crear una esfera luego crear un cilindro luego crear un plano luego crear un cono luego crear a suzanne"
    
    final_response = {
        'success': True,
        'command_executed': 'sequence_all_primitives',
        'confidence': 1.0,
        'parameters': {},
        'scene_state_pre': {'objects': []},
        'scene_state': {'objects': [{'name': 'Cube'}, {'name': 'Sphere'}, {'name': 'Cylinder'}, {'name': 'Plane'}, {'name': 'Cone'}, {'name': 'Suzanne'}]},
        'validation': {'verified': True, 'passive': False, 'details': '6 primitive models generated separated by 3.0 units'},
    }
    
    print(f"Registrando patrón para: {request}")
    pattern_id = agent.pattern_memory.store_pattern(request, final_response)
    print(f"Patrón generado de ID: {pattern_id}")
    
    if pattern_id:
        # Aquí era pattern_memory, no agent a secas
        appr = agent.pattern_memory.approve_pending_pattern(pattern_id)
        if appr:
            print(f"¡Visto bueno dado! Patrón {pattern_id} movido a STABLE y aprendido por Zuly.")
        else:
            print("Fallo aprobando el patrón.")

if __name__ == "__main__":
    main()
