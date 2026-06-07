import bpy
import math

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_hollow_v3(p_type, location):
    # 1. Crear Base
    if p_type == 'cube': bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    elif p_type == 'sphere': bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=location)
    elif p_type == 'monkey': bpy.ops.mesh.primitive_monkey_add(size=2, location=location)
    
    obj = bpy.context.active_object
    obj.name = f"ZULY_{p_type.upper()}"
    
    # IMPORTANTE: Forzar actualización de escena
    bpy.context.view_layer.update()
    
    # 2. Crear Taladros
    cutters = []
    # X
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=location, rotation=(0, math.pi/2, 0))
    cutters.append(bpy.context.active_object)
    # Y
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=location, rotation=(math.pi/2, 0, 0))
    cutters.append(bpy.context.active_object)
    # Z
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=location)
    cutters.append(bpy.context.active_object)
    
    # 3. Aplicar Booleanos con Garantía de Contexto
    for i, cut in enumerate(cutters):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        mod = obj.modifiers.new(name=f"Hole_{i}", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = cut
        mod.solver = 'EXACT'
        
        # Aplicar el modificador (esto es lo que suele fallar en background)
        # Usamos la técnica de conversión para "quemar" el modificador sin ops
        # O simplemente modifier_apply con el contexto forzado
        bpy.ops.object.modifier_apply(modifier=mod.name)
        
        # Borrar el taladro
        bpy.data.objects.remove(cut, do_unlink=True)
        
    return obj

clean_scene()
create_hollow_v3('cube', (0,0,0))
create_hollow_v3('sphere', (4,0,0))
create_hollow_v3('monkey', (8,0,0))

# Guardar y Validar
out_path = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_LAB\resultados_zuly\ZULY_ULTRA_FIX.blend"
bpy.ops.wm.save_as_mainfile(filepath=out_path)

# Verificación de vértices final
for o in bpy.data.objects:
    print(f"VERIFY: {o.name} | Verts: {len(o.data.vertices)}")
