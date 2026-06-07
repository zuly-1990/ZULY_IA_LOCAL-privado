import bpy
import sys
import os
import math
from mathutils import Vector

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_redondo_zuly.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_round_dice():
    log_info("=== INICIANDO SÍNTESIS DE DADO REDONDO MULTI-COLOR ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    agent.execute_via_router('blender.clear_scene', {})
    
    # 1. Materiales Base
    agent.execute_via_router('blender.create_material', {'name': 'Die_White', 'color': [0.95, 0.95, 0.95, 1], 'roughness': 0.1, 'specular': 1.0})
    
    colors_map = {
        'F1': ('Pip_Red', [1.0, 0.0, 0.0, 1]),
        'F2': ('Pip_Blue', [0.0, 0.0, 1.0, 1]),
        'F3': ('Pip_Green', [0.0, 1.0, 0.0, 1]),
        'F4': ('Pip_Yellow', [1.0, 0.8, 0.0, 1]),
        'F5': ('Pip_Orange', [1.0, 0.4, 0.0, 1]),
        'F6': ('Pip_Purple', [0.6, 0.0, 0.8, 1])
    }
    for mat_name, rgba in colors_map.values():
        agent.execute_via_router('blender.create_material', {'name': mat_name, 'color': rgba, 'roughness': 0.8, 'specular': 0.5})

    # 2. CUERPO BASE: UV SPHERE PERFECTA
    script_sphere = """
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0, location=(0,0,1))
obj = bpy.context.active_object
obj.name = 'Round_Die_MultiColor'

mat_white = bpy.data.materials.get('Die_White')
if mat_white:
    obj.data.materials.append(mat_white)
    
mats_to_add = ['Pip_Red', 'Pip_Blue', 'Pip_Green', 'Pip_Yellow', 'Pip_Orange', 'Pip_Purple']
for m in mats_to_add:
    c_mat = bpy.data.materials.get(m)
    if c_mat:
        obj.data.materials.append(c_mat)

bpy.ops.object.shade_smooth()
obj.data.use_auto_smooth = True
obj.data.auto_smooth_angle = 0.523599
"""
    agent.execute_via_router('blender.run_python_script', {'script_content': script_sphere})

    # 3. LOS PUNTOS (Pips) - PROYECCIÓN ESFÉRICA
    pips_map = {
        'F1': [[0, 0, 1.95]],
        'F2': [[0.5, -0.95, 1.5], [-0.5, -0.95, 0.5]],
        'F3': [[0.95, 0.5, 1.5], [0.95, 0, 1], [0.95, -0.5, 0.5]],
        'F4': [[-0.95, 0.5, 1.5], [-0.95, 0.5, 0.5], [-0.95, -0.5, 1.5], [-0.95, -0.5, 0.5]],
        'F5': [[0.5, 0.95, 1.5], [-0.5, 0.95, 0.5], [0.5, 0.95, 0.5], [-0.5, 0.95, 1.5], [0, 0.95, 1]],
        'F6': [[0.5, 0.5, 0.05], [0.5, -0.5, 0.05], [-0.5, 0.5, 0.05], [-0.5, -0.5, 0.05], [0.5, 0, 0.05], [-0.5, 0, 0.05]]
    }
    
    center = Vector((0.0, 0.0, 1.0))
    # En el dado cubico (v10), la distancia del pip center al centro del cubo variaba dependiendo 
    # si estaba en una esquina o centro de cara.
    # Ahora forzamos a que TODOS los pip centers esten exactamente a una profundidad fija de 0.95 de la esfera pura
    cut_depth_radius = 0.95 

    counter = 0
    for face, locs in pips_map.items():
        face_material_name = colors_map[face][0]
        
        for p_loc in locs:
            orig_vec = Vector(p_loc)
            # 3.1 Proyección Radial Matemática
            direction = (orig_vec - center).normalized()
            # 3.2 Reposicionar en el radio deseado de la esfera
            spherized_pos = center + (direction * cut_depth_radius)
            new_loc = [spherized_pos.x, spherized_pos.y, spherized_pos.z]
            
            pip_name = f"Pip_Round_{face}_{counter}"
            
            script_create_pip = f"""
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.18, location={new_loc})
obj = bpy.context.active_object
obj.name = '{pip_name}'
mat = bpy.data.materials.get('{face_material_name}')
if mat:
    obj.data.materials.append(mat)
"""
            agent.execute_via_router('blender.run_python_script', {'script_content': script_create_pip})
            
            # CIRUGÍA TÉCNICA
            script_boolean = f"""
import bpy
obj = bpy.data.objects.get('Round_Die_MultiColor')
cutter = bpy.data.objects.get('{pip_name}')
if obj and cutter:
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Cut_{counter}", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    mod.material_mode = 'TRANSFER'
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
"""
            agent.execute_via_router('blender.run_python_script', {'script_content': script_boolean})
            counter += 1

    # 4. Weighted Normals (Suavizado óptimo de recortes curvos)
    script_wn = """
import bpy
obj = bpy.data.objects.get('Round_Die_MultiColor')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
    bpy.ops.object.modifier_apply(modifier="WN")
"""
    agent.execute_via_router('blender.run_python_script', {'script_content': script_wn})

    # Guardar
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADO REDONDO COMPLETADO: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error guardando dado redondo: {e}")

if __name__ == "__main__":
    create_round_dice()
