"""
dice.py

Handler para crear un dado de parqués nivel maestro (V9) de manera nativa en ZULY.
"""
from typing import Dict, Any

def create_parques_dice_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Crea un dado de parqués de ultra-fidelidad (V9) usando el EngineAdapter.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
        
    if not adapter or not adapter.is_available():
        return {'success': False, 'message': 'EngineAdapter no disponible'}

    # 1. Crear materiales
    from core.utils.logging import log_info, log_success, log_error
    log_info("🎲 Iniciando creación de dado V9...")
    
    adapter.create_material('Die_White', [0.95, 0.95, 0.95, 1], 0.1, 1.0)
    adapter.create_material('Pip_Color', [1.0, 0.0, 0.0, 1], 0.8, 0.5)
    log_info("🎨 Materiales 'Die_White' y 'Pip_Color' creados.")

    # 2. Crear cubo base
    log_info("📦 Creando cubo base 'Parques_Die_Ultra_Color'...")
    res_cube = adapter.create_cube(location=[0, 0, 1], size=1.0, name='Parques_Die_Ultra_Color')
    if not res_cube.get('success'):
        log_error(f"❌ Error creando cubo: {res_cube.get('message') or res_cube.get('error')}")
        return res_cube
    
    # Pre-cargar slots de material y hacer loop cuts (se delega a scripting interno del adapter o run_script si es Blender)
    script_cube = """
import bpy
obj = bpy.data.objects.get('Parques_Die_Ultra_Color')
mat_white = bpy.data.materials.get('Die_White')
mat_color = bpy.data.materials.get('Pip_Color')
if obj and mat_white and mat_color:
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat_white)
    else:
        obj.data.materials[0] = mat_white
    obj.data.materials.append(mat_color)
    
    # Loop cuts
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=4)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599
"""
    adapter.run_python_script(script_cube)
    
    # 3. Añadir Bevel
    adapter.add_bevel_modifier('Parques_Die_Ultra_Color', width=0.25, segments=16)

    # 4. Los Puntos (Pips)
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
            pip_name = f"Pip_V9_{face}_{counter}"
            script_pip = f"""
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.18, location={loc})
obj = bpy.context.active_object
obj.name = '{pip_name}'
mat = bpy.data.materials.get('Pip_Color')
if mat:
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

# Boolean setup
main_obj = bpy.data.objects.get('Parques_Die_Ultra_Color')
if main_obj and obj:
    bpy.context.view_layer.objects.active = main_obj
    mod = main_obj.modifiers.new(name="Cut_V9_{counter}", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = obj
    mod.material_mode = 'TRANSFER'
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(obj, do_unlink=True)
"""
            adapter.run_python_script(script_pip)
            counter += 1

    # 5. Weighted Normals
    script_wn = """
import bpy
obj = bpy.data.objects.get('Parques_Die_Ultra_Color')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
    bpy.ops.object.modifier_apply(modifier="WN")
"""
    adapter.run_python_script(script_wn)

    return {
        'success': True,
        'message': 'Dado de parqués V9 creado nativamente',
        'result': {'name': 'Parques_Die_Ultra_Color', 'type': 'MESH'}
    }
