
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.agent import Agent

print("--- TEST COGNICION ---")
agent = Agent(force_mock=True)

print("\n1. Ejecutando comando que debería disparar cognición (render)...")
res = agent.execute_via_router('blender.render_scene', {
    'output_path': 'test_cognition.png'
})

print(f"\nÉxito: {res.get('success')}")
if 'cognition_diagnosis' in res:
    diag = res['cognition_diagnosis']
    print(f"Diagnosis Cognitiva encontrada!")
    print(f"Status: {diag['status']}")
    print(f"Score: {diag['score']}")
    print(f"Findings: {diag['findings']}")
else:
    print("ERROR: No se encontró diagnosis cognitiva en el resultado.")

print("\n--- FIN TEST ---")
