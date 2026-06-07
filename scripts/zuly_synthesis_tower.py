import bpy
import sys
import os
import json

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "torre_zuly_v1.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_tower():
    log_info("=== INICIANDO SÍNTESIS URBANA VALIDADA: TORRE V1 ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. Base Cilíndrica (Estructura Principal)
    agent.execute_via_router('blender.create_cylinder', {
        'location': [0, 0, 10], 
        'radius': 2.0, 
        'depth': 20.0
    })
    agent.execute_via_router('blender.rename_object', {'old_name': 'Cylinder', 'new_name': 'Main_Tower'})
    
    # 3. Anillos de Observación (Torus-like but with Cylinders for simplicity/topology)
    for z in [5, 12, 18]:
        name = f"Observatory_{z}"
        agent.execute_via_router('blender.create_cylinder', {
            'location': [0, 0, z], 
            'radius': 3.5, 
            'depth': 0.8
        })
        agent.execute_via_router('blender.rename_object', {'old_name': 'Cylinder', 'new_name': name})

    # 4. Aguja (Cone)
    agent.execute_via_router('blender.create_cone', {
        'location': [0, 0, 22], 
        'radius1': 1.0, 
        'depth': 4.0
    })
    agent.execute_via_router('blender.rename_object', {'old_name': 'Cone', 'new_name': 'Spire'})

    # 5. VALIDACIÓN V3
    log_info("Auditando la estructura de la Torre...")
    validation = agent.execute_via_router('blender.validate_topology', {'object_name': 'Main_Tower'})
    
    # 6. Guardado Final
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== TORRE COMPLETADA: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error al guardar torre: {e}")

if __name__ == "__main__":
    create_tower()
