import sys
import time
import pprint

# Añadir el path al PYTHONPATH programáticamente si fuera necesario
sys.path.append('/opt/zuly')

from core.agent import Agent

def run_test(prompt):
    print(f"[*] Inicializando Agente Zuly Remoto (Modo Real)")
    # En producción real en el server asumimos force_mock=False
    agent = Agent(force_mock=False)
    
    print(f"\n[ZULY] Procesando petición: '{prompt}'")
    start_time = time.time()
    
    # Esto invocará la memoria a largo plazo que inyectamos antes
    result = agent.process_natural_request(prompt)
    elapsed = time.time() - start_time
    
    print("\n" + "="*50)
    if result.get('success'):
        print(f"✅ ÉXITO ({elapsed:.2f}s)")
        print(f"Feedback: {result.get('feedback')}")
        if 'scene_state' in result:
            print(f"Estado de la escena: {result['scene_state']}")
    else:
        print(f"❌ FALLÓ ({elapsed:.2f}s)")
        print(f"Motivo: {result.get('error', 'Desconocido')}")
        print(f"Feedback: {result.get('feedback')}")
    print("="*50)

if __name__ == "__main__":
    test_prompt = "crea un museo de arte abstracto con paredes curvas y luz cenital"
    if len(sys.argv) > 1:
        test_prompt = sys.argv[1]
    run_test(test_prompt)
