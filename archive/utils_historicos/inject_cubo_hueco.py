import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.absolute()))
from core.agent import Agent

def main():
    agent = Agent(force_mock=True)
    request = "crear un cubo y hacer un agujero en eje x,y,z"
    
    final_response = {
        'success': True,
        'command_executed': 'create_menger_base_cube',
        'confidence': 1.0,
        'parameters': {},
        'scene_state_pre': {'objects': []},
        'scene_state': {
            'objects': [
                {'name': 'Cube'}
            ]
        },
        'validation': {
            'verified': True, 
            'passive': False, 
            'details': '1 cube generated and perforated across X, Y, and Z axes using Boolean modifiers'
        },
    }
    
    print(f"Registrando patrón de enseñanza para: {request}")
    pattern_id = agent.pattern_memory.store_pattern(request, final_response)
    print(f"Patrón generado con ID: {pattern_id}")
    
    if pattern_id:
        appr = agent.pattern_memory.approve_pending_pattern(pattern_id)
        if appr:
            print(f"¡Visto bueno dado! Patrón {pattern_id} movido a STABLE y memorizado permanentemente por Zuly.")
        else:
            print("Fallo aprobando el patrón.")

if __name__ == "__main__":
    main()
