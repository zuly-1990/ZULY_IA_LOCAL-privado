import bpy
import sys
import os

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_parques_zuly_v8.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_parques_dice_v8():
    log_info("=== INICIANDO SÍNTESIS DE DADO DE PARQUÉS ULTRA-FINO (V8 - ALTA DENSIDAD) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. Materiales de Contraste
    agent.execute_via_router('blender.create_material', {'name': 'Die_White', 'color': [0.95, 0.95, 0.95, 1], 'roughness': 0.1, 'specular': 1.0})
    agent.execute_via_router('blender.create_material', {'name': 'Pip_Black', 'color': [0.0, 0.0, 0.0, 1], 'roughness': 0.9, 'specular': 0.0})
    
    # 3. El Dado (Cuerpo Principal con ALTA DENSIDAD)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0, 'name': 'Parques_Die_Ultra'})
    agent.execute_via_router('blender.apply_material', {'object_name': 'Parques_Die_Ultra', 'material_name': 'Die_White'})
    
    # INCREMENTO DE DENSIDAD BASE (Loop Cuts)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
import bmesh

obj = bpy.data.objects.get('Parques_Die_Ultra')
if obj:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Subdividir para densidad limpia (Simple)
    bpy.ops.mesh.subdivide(number_cuts=4)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599
"""
    })

    # 4. Biselado Premium (0.25m / 16 segs)
    agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Parques_Die_Ultra',
        'width': 0.25,
        'segments': 16
    })
    
    # 5. Los Puntos (Pips) - ALTA RESOLUCIÓN Y CIRUGÍA DEFINITIVA
    pips_map = {
        'F1': [[0, 0, 1.95]],
        'F2': [[0.5, -0.95, 1.5], [-0.5, -0.95, 0.5]],
        'F3': [[0.95, 0.5, 1.5], [0.95, 0, 1], [0.95, -0.5, 0.5]],
        'F4': [[-0.95, 0.5, 1.5], [-0.95, 0.5, 0.5], [-0.95, -0.5, 1.5], [-0.95, -0.5, 0.5]],
        'F5': [[0.5, 0.95, 1.5], [-0.5, 0.95, 0.5], [0.5, 0.95, 0.5], [-0.5, 0.95, 1.5], [0, 0.95, 1]],
        'F6': [[0.5, 0.5, 0.05], [0.5, -0.5, 0.05], [-0.5, 0.5, 0.05], [-0.5, -0.5, 0.05], [0.5, 0, 0.05], [-0.5, 0, 0.05]]
    }
    
    counter = 0
    for face, locs in pips_map.items():
        for loc in locs:
            pip_name = f"Pip_HQ_{face}_{counter}"
            # Crear esfera DE ALTA RESOLUCIÓN
            agent.execute_via_router('blender.run_python_script', {
                'script_content': f"""
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.18, location={loc})
obj = bpy.context.active_object
obj.name = '{pip_name}'
"""
            })
            
            # ASIGNAR MATERIAL NEGRO
            agent.execute_via_router('blender.apply_material', {
                'object_name': pip_name,
                'material_name': 'Pip_Black'
            })
            
            # CIRUGÍA TÉCNICA DEFINITIVA
            agent.execute_via_router('blender.run_python_script', {
                'script_content': f"""
import bpy
obj = bpy.data.objects.get('Parques_Die_Ultra')
cutter = bpy.data.objects.get('{pip_name}')
if obj and cutter:
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Cut_HQ_{counter}", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
"""
            })
            counter += 1

    # 6. Weighted Normals (Estabilización final)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die_Ultra')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
    bpy.ops.object.modifier_apply(modifier="WN")
"""
    })

    # 7. Guardado Final
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADO DE PARQUÉS ULTRA-FINO V8 COMPLETADO: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error guardando dado V8: {e}")

if __name__ == "__main__":
    create_parques_dice_v8()
