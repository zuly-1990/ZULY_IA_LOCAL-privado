import bpy
import sys
import os
import json

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_parques_zuly.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error, log_warning

def create_parques_dice():
    log_info("=== INICIANDO SÍNTESIS DE DADO DE PARQUÉS (V4) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. El Dado (Cuerpo Principal)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0})
    agent.execute_via_router('blender.rename_object', {'old_name': 'Cube', 'new_name': 'Parques_Die'})
    
    # SUAVIZADO INDUSTRIAL (Auto-Smooth + Shade Smooth)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die')
if obj:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599
"""
    })

    # 3. Biselado más profundo para estética Parqués (0.25m)
    agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Parques_Die',
        'width': 0.25,
        'segments': 16
    })
    
    # 4. Los Puntos (Pips) - Mapa de 21 puntos (1-6)
    pips_map = {
        '1': [[0, 0, 2.0]],
        '2': [[0.5, -1, 1.5], [-0.5, -1, 0.5]],
        '3': [[1, 0.5, 1.5], [1, 0, 1], [1, -0.5, 0.5]],
        '4': [[-1, 0.5, 1.5], [-1, 0.5, 0.5], [-1, -0.5, 1.5], [-1, -0.5, 0.5]],
        '5': [[0.5, 1, 1.5], [-0.5, 1, 0.5], [0.5, 1, 0.5], [-0.5, 1, 1.5], [0, 1, 1]],
        '6': [[0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, 0.5, 0], [-0.5, -0.5, 0], [0.5, 0, 0], [-0.5, 0, 0]]
    }
    
    # Material para el Dado
    agent.execute_via_router('blender.create_material', {
        'name': 'Die_White',
        'color': [1, 1, 1, 1],
        'roughness': 0.1
    })
    agent.execute_via_router('blender.apply_material', {'object_name': 'Parques_Die', 'material_name': 'Die_White'})

    # Procesar Pips (Boolean Difference)
    for face, locs in pips_map.items():
        for i, loc in enumerate(locs):
            name = f"pip_{face}_{i}"
            agent.execute_via_router('blender.create_sphere', {
                'location': loc,
                'radius': 0.18
            })
            agent.execute_via_router('blender.add_boolean', {
                'object_name': 'Parques_Die',
                'target_name': 'Sphere',
                'operation': 'DIFFERENCE'
            })
            agent.execute_via_router('blender.delete_object', {'object_name': 'Sphere'})

    # 5. Weighted Normals para limpiar sombras
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
"""
    })

    # 6. Iluminación y Cámara
    agent.execute_via_router('blender.create_light', {'light_type': 'SUN', 'energy': 5.0})
    agent.execute_via_router('blender.create_camera', {'location': [4, -4, 4]})

    # 7. Guardado
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADO DE PARQUÉS V4 COMPLETADO: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error al guardar dado V4: {e}")

if __name__ == "__main__":
    create_parques_dice()
