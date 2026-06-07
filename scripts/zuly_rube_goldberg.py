import bpy
import sys
import os
from mathutils import Vector
import math

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "rube_goldberg_zuly.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_rube_goldberg():
    log_info("=== INICIANDO SÍNTESIS DE RUBE GOLDBERG (RIGID BODY) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    agent.execute_via_router('blender.clear_scene', {})
    
    # Activar entorno de físicas global
    agent.execute_via_router('blender.run_python_script', {'script_content': """
import bpy
bpy.ops.scene.rigidbody_world_add()
"""})

    # ==========================
    # 1. MATERIALES
    # ==========================
    agent.execute_via_router('blender.create_material', {'name': 'Die_White', 'color': [0.95, 0.95, 0.95, 1], 'roughness': 0.1, 'specular': 1.0})
    agent.execute_via_router('blender.create_material', {'name': 'Ramp_Mat', 'color': [0.1, 0.1, 0.1, 1], 'roughness': 0.8, 'specular': 0.2})
    
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

    # ==========================
    # 2. FUNCION CREADORA DE DADO REDONDO (Físico)
    # ==========================
    pips_map = {
        'F1': [[0, 0, 1.95]],
        'F2': [[0.5, -0.95, 1.5], [-0.5, -0.95, 0.5]],
        'F3': [[0.95, 0.5, 1.5], [0.95, 0, 1], [0.95, -0.5, 0.5]],
        'F4': [[-0.95, 0.5, 1.5], [-0.95, 0.5, 0.5], [-0.95, -0.5, 1.5], [-0.95, -0.5, 0.5]],
        'F5': [[0.5, 0.95, 1.5], [-0.5, 0.95, 0.5], [0.5, 0.95, 0.5], [-0.5, 0.95, 1.5], [0, 0.95, 1]],
        'F6': [[0.5, 0.5, 0.05], [0.5, -0.5, 0.05], [-0.5, 0.5, 0.05], [-0.5, -0.5, 0.05], [0.5, 0, 0.05], [-0.5, 0, 0.05]]
    }

    def build_physical_round_die(name, location):
        script_sphere = f"""
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0, location=(0,0,1))
obj = bpy.context.active_object
obj.name = '{name}'

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

        # Pips
        center = Vector((0.0, 0.0, 1.0))
        cut_depth_radius = 0.95 
        counter = 0
        for face, locs in pips_map.items():
            face_material_name = colors_map[face][0]
            for p_loc in locs:
                orig_vec = Vector(p_loc)
                direction = (orig_vec - center).normalized()
                spherized_pos = center + (direction * cut_depth_radius)
                new_loc = [spherized_pos.x, spherized_pos.y, spherized_pos.z]
                
                pip_name = f"Pip_{name}_{counter}"
                script_create_pip = f"""
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.18, location={new_loc})
cutter = bpy.context.active_object
cutter.name = '{pip_name}'
mat = bpy.data.materials.get('{face_material_name}')
if mat:
    cutter.data.materials.append(mat)
"""
                agent.execute_via_router('blender.run_python_script', {'script_content': script_create_pip})
                
                script_boolean = f"""
import bpy
obj = bpy.data.objects.get('{name}')
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

        script_wn_phys = f"""
import bpy
obj = bpy.data.objects.get('{name}')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
    bpy.ops.object.modifier_apply(modifier="WN")
    
    # Mover a locación final
    obj.location = {location}
    
    # ASIGNAR FÍSICA A DADO (ACTIVO)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = 'ACTIVE'
    obj.rigid_body.collision_shape = 'SPHERE'
    obj.rigid_body.mass = 1.0
    obj.rigid_body.restitution = 0.6  # Bounciness
    obj.rigid_body.friction = 0.4
"""
        agent.execute_via_router('blender.run_python_script', {'script_content': script_wn_phys})

    # ==========================
    # 3. CREAR DADOS SUSPENDIDOS
    # ==========================
    # Dado 1: Altura 5
    build_physical_round_die('RoundDie_1', [0, 8, 5])
    # Dado 2: Altura 8, ligeramente desplazado para chocar
    build_physical_round_die('RoundDie_2', [0, 9, 8])
    # Dado 3: Altura 12
    build_physical_round_die('RoundDie_3', [0, 10, 11])

    # ==========================
    # 4. ESCENARIO PASIVO (Rampa y Suelo)
    # ==========================
    script_scenario = """
import bpy
import math

# RAMPA
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), scale=(5, 10, 0.5))
ramp = bpy.context.active_object
ramp.name = 'Ramp'
ramp.rotation_euler = (math.radians(25), 0, 0)
ramp.location = (0, 5, 2)

# PLATAFORMA RECEPTORA O CAJÓN (Unidad Sólida de una pieza)
# 1. Cubo Exterior (La Base)
bpy.ops.mesh.primitive_cube_add(location=(0, -8, -1), scale=(9, 9, 2))
cajon = bpy.context.active_object
cajon.name = 'SinglePiece_Box'

# 2. Cubo Cortador (El Ahuecado)
bpy.ops.mesh.primitive_cube_add(location=(0, -8, 0.5), scale=(8.5, 8.5, 2))
cutter_box = bpy.context.active_object
cutter_box.name = 'Hollow_Cutter'

# 3. Aplicar Booleano para ahuecar y dejar el cajón limpio
bpy.context.view_layer.objects.active = cajon
mod = cajon.modifiers.new(name="Carve_Inside", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = cutter_box
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(cutter_box, do_unlink=True)

# Físicas Pasivas
env_objs = [ramp, cajon]
mat_ramp = bpy.data.materials.get('Ramp_Mat')

for o in env_objs:
    if mat_ramp:
        o.data.materials.append(mat_ramp)
    bpy.context.view_layer.objects.active = o
    
    # Fundamental para físicas: Aplicar Escala
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    bpy.ops.rigidbody.object_add()
    o.rigid_body.type = 'PASSIVE'
    o.rigid_body.collision_shape = 'MESH' # Precisión física máxima
    o.rigid_body.restitution = 0.5
    o.rigid_body.friction = 0.5
"""
    agent.execute_via_router('blender.run_python_script', {'script_content': script_scenario})

    # 5. Luces y Guardado
    agent.execute_via_router('blender.run_python_script', {'script_content': """
import bpy
bpy.ops.object.light_add(type='AREA', location=(0, 0, 15), rotation=(0, 0, 0))
bpy.context.active_object.data.energy = 2000
bpy.context.active_object.data.size = 20
"""})

    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== MÁQUINA DE RUBE GOLDBERG COMPLETADA: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error guardando scene: {e}")

if __name__ == "__main__":
    create_rube_goldberg()
