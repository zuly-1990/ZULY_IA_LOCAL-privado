import bpy
import sys
import os
import json

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "monumento_zuly_v1.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error, log_warning

def create_pavilion():
    log_info("=== INICIANDO SÍNTESIS URBANA VALIDADA: PABELLÓN V1 ===")
    
    # Asegurar directorio
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    
    # Inicializar Agente
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. Piso (Slab)
    agent.execute_via_router('blender.create_plane', {'location': [0, 0, 0], 'scale': 10.0})
    agent.execute_via_router('blender.rename_object', {'old_name': 'Plane', 'new_name': 'Base_Platform'})
    
    # 3. Pilares (Uso de un loop para control total)
    pillares_coords = [[-4, -4, 0], [4, -4, 0], [4, 4, 0], [-4, 4, 0]]
    for i, coord in enumerate(pillares_coords):
        name = f"Pillar_{i+1}"
        agent.execute_via_router('blender.create_cube', {'location': [coord[0], coord[1], 2.5]})
        agent.execute_via_router('blender.scale_object', {'object_name': 'Cube', 'scale': [0.5, 0.5, 2.5]})
        agent.execute_via_router('blender.rename_object', {'old_name': 'Cube', 'new_name': name})
        
    # 4. Techo (Roof)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 5.2]})
    agent.execute_via_router('blender.scale_object', {'object_name': 'Cube', 'scale': [5.0, 5.0, 0.1]})
    agent.execute_via_router('blender.rename_object', {'old_name': 'Cube', 'new_name': 'Roof'})
    
    # 5. Núcleo de Oro (The Soul)
    agent.execute_via_router('blender.create_sphere', {'location': [0, 0, 2.5], 'radius': 1.0})
    agent.execute_via_router('blender.rename_object', {'old_name': 'Sphere', 'new_name': 'Cognitive_Core'})
    
    # 6. Iluminación y Cámara
    agent.execute_via_router('blender.create_light', {'light_type': 'SUN', 'location': [5, -5, 10]})
    agent.execute_via_router('blender.create_camera', {'location': [15, -15, 10]})
    
    # 7. VALIDACIÓN V3 (Antes de guardar)
    log_info("Ejecutando Auditoría V3 en el Núcleo Cognitivo...")
    validation = agent.execute_via_router('blender.validate_topology', {'object_name': 'Cognitive_Core'})
    
    if validation.get('success'):
        log_success("✓ Validación V3 exitosa para el Núcleo.")
    else:
        log_warning("! Advertencia: El núcleo tiene inconsistencias topológicas.")

    # 8. Guardado Final en ruta establecida
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== SÍNTESIS COMPLETADA EXPENDIENTE: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error al guardar .blend: {e}")

if __name__ == "__main__":
    create_pavilion()
