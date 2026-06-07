import bpy
import sys
import os

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_parques_zuly_v6.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_parques_dice_v6():
    log_info("=== INICIANDO SÍNTESIS DE DADO DE PARQUÉS PRO (V6 - CONTRASTE NEGRO) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. Materiales de Contraste
    agent.execute_via_router('blender.create_material', {'name': 'Die_White', 'color': [0.95, 0.95, 0.95, 1], 'roughness': 0.1, 'specular': 1.0})
    agent.execute_via_router('blender.create_material', {'name': 'Pip_Black', 'color': [0.02, 0.02, 0.02, 1], 'roughness': 0.8, 'specular': 0.0})
    
    # 3. El Dado (Cuerpo Principal)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0, 'name': 'Parques_Die_Pro'})
    agent.execute_via_router('blender.apply_material', {'object_name': 'Parques_Die_Pro', 'material_name': 'Die_White'})
    
    # SUAVIZADO INDUSTRIAL V6
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die_Pro')
if obj:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599
"""
    })

    # 4. Biselado Premium (0.25m / 16 segs)
    agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Parques_Die_Pro',
        'width': 0.25,
        'segments': 16
    })
    
    # 5. Los Puntos (Pips) - Mapa de 21 puntos con herencia de material negro
    pips_map = {
        'F1': [[0, 0, 2.0]],
        'F2': [[0.5, -1, 1.5], [-0.5, -1, 0.5]],
        'F3': [[1, 0.5, 1.5], [1, 0, 1], [1, -0.5, 0.5]],
        'F4': [[-1, 0.5, 1.5], [-1, 0.5, 0.5], [-1, -0.5, 1.5], [-1, -0.5, 0.5]],
        'F5': [[0.5, 1, 1.5], [-0.5, 1, 0.5], [0.5, 1, 0.5], [-0.5, 1, 1.5], [0, 1, 1]],
        'F6': [[0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, 0.5, 0], [-0.5, -0.5, 0], [0.5, 0, 0], [-0.5, 0, 0]]
    }
    
    counter = 0
    for face, locs in pips_map.items():
        for loc in locs:
            pip_name = f"Pip_{face}_{counter}"
            # Crear esfera operando
            agent.execute_via_router('blender.create_sphere', {
                'location': loc,
                'radius': 0.18,
                'name': pip_name
            })
            
            # ASIGNAR MATERIAL NEGRO ANTES DEL BOOLEANO (Herencia)
            agent.execute_via_router('blender.apply_material', {
                'object_name': pip_name,
                'material_name': 'Pip_Black'
            })
            
            # BOOLEAN CORREGIDO
            agent.execute_via_router('blender.add_boolean', {
                'object_name': 'Parques_Die_Pro',
                'operand_object': pip_name,
                'operation': 'DIFFERENCE',
                'hide_operand': True
            })
            counter += 1

    # 6. Weighted Normals (Cierre técnico)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die_Pro')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
"""
    })

    # 7. Guardado Final
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADO DE PARQUÉS PRO V6 COMPLETADO: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error guardando dado V6: {e}")

if __name__ == "__main__":
    create_parques_dice_v6()
