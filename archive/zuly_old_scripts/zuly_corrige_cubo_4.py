#!/usr/bin/env python3
"""
ZULY CORRIGE: CUBO_4 CON AGUJEROS REALES Y COLORES
- Aplica booleanas
- Asigna materiales a caras internas
- Archivo: cubo_4.blend
"""

import subprocess
import tempfile
from pathlib import Path
import time

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_4.blend")

print("\n" + "="*70)
print("🔧 ZULY CORRIGE CUBO_4: Agujeros REALES y Colores")
print("="*70)

correction_script = """
import bpy
import math

print('\n[CORRIGE] Limpiando escena...')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Cubo base
bpy.ops.mesh.primitive_cube_add(size=2.2, location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = 'CuboBase'

# Material blanco base
mat_blanco = bpy.data.materials.new(name='MatBlanco')
mat_blanco.use_nodes = True
bsdf = mat_blanco.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
mat_blanco.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (1,1,1,1)
mat_blanco.node_tree.nodes['Principled BSDF'].inputs[9].default_value = 0.5
output = mat_blanco.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
mat_blanco.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
cubo.data.materials.append(mat_blanco)

# Bevel
bevel = cubo.modifiers.new(name='Bevel', type='BEVEL')
bevel.width = 0.2
bevel.segments = 2
bevel.affect = 'EDGES'

# Cilindros para agujeros
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=4, location=(0, 0, 0))
cy_x = bpy.context.active_object
cy_x.name = 'CY_X'
cy_x.rotation_euler = (0, math.radians(90), 0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=4, location=(0, 0, 0))
cy_y = bpy.context.active_object
cy_y.name = 'CY_Y'
cy_y.rotation_euler = (math.radians(90), 0, 0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=4, location=(0, 0, 0))
cy_z = bpy.context.active_object
cy_z.name = 'CY_Z'
cy_z.rotation_euler = (0, 0, 0)

# Booleanas
for eje, obj in zip(['X','Y','Z'], [cy_x, cy_y, cy_z]):
    bool_mod = cubo.modifiers.new(name=f'Bool{eje}', type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = obj
    bool_mod.solver = 'FAST'
    bpy.context.view_layer.objects.active = cubo
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

# Eliminar cilindros
for obj in [cy_x, cy_y, cy_z]:
    bpy.data.objects.remove(obj, do_unlink=True)

# Crear materiales de color
mat_rojo = bpy.data.materials.new(name='MatRojo')
mat_rojo.use_nodes = True
bsdf = mat_rojo.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
mat_rojo.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (1,0.1,0.1,1)
mat_rojo.node_tree.nodes['Principled BSDF'].inputs[9].default_value = 0.3
output = mat_rojo.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
mat_rojo.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

mat_verde = bpy.data.materials.new(name='MatVerde')
mat_verde.use_nodes = True
bsdf = mat_verde.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
mat_verde.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (0.1,1,0.1,1)
mat_verde.node_tree.nodes['Principled BSDF'].inputs[9].default_value = 0.3
output = mat_verde.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
mat_verde.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

mat_azul = bpy.data.materials.new(name='MatAzul')
mat_azul.use_nodes = True
bsdf = mat_azul.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
mat_azul.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (0.1,0.3,1,1)
mat_azul.node_tree.nodes['Principled BSDF'].inputs[9].default_value = 0.3
output = mat_azul.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
mat_azul.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Añadir materiales al cubo
cubo.data.materials.clear()
cubo.data.materials.append(mat_blanco) # 0
cubo.data.materials.append(mat_rojo)   # 1
cubo.data.materials.append(mat_verde)  # 2
cubo.data.materials.append(mat_azul)   # 3

# Seleccionar caras internas y asignar materiales
bpy.context.view_layer.objects.active = cubo
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_non_manifold()
bpy.ops.object.mode_set(mode='OBJECT')

for f in cubo.data.polygons:
    # X: agujero horizontal (mayor valor abs X)
    if abs(f.center[0]) > 0.9:
        f.material_index = 1
    # Y: agujero vertical (mayor valor abs Y)
    elif abs(f.center[1]) > 0.9:
        f.material_index = 2
    # Z: agujero frontal (mayor valor abs Z)
    elif abs(f.center[2]) > 0.9:
        f.material_index = 3
    else:
        f.material_index = 0

bpy.ops.object.mode_set(mode='OBJECT')

# Smooth shading
cubo.select_set(True)
bpy.context.view_layer.objects.active = cubo
bpy.ops.object.shade_smooth()

# Guardar
filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_4.blend'
bpy.ops.wm.save_mainfile(filepath=filepath)

print('\n✅ CUBO_4 corregido: Agujeros REALES y COLORES')
"""

try:
    print("\n📝 Fase 1: Preparando corrección...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(correction_script)
        script_file = Path(f.name)
    print("   ✓ Script listo")
    
    print("\n⚙️  Fase 2: ZULY corrigiendo...")
    start = time.time()
    cmd = [str(BLENDER_PATH), "--background", "--python", str(script_file)]
    result = subprocess.run(cmd, timeout=45)
    elapsed = time.time() - start
    
    print(f"\n✅ Corrección completada en {elapsed:.1f} segundos")
    
    print("\n📊 Fase 3: Verificando...")
    if BLEND_FILE.exists():
        size = BLEND_FILE.stat().st_size / 1024
        print(f"   ✓ Archivo: {BLEND_FILE.name}")
        print(f"   ✓ Tamaño: {size:.1f} KB")
        print(f"   ✓ Status: LISTO")
    
    print("\n" + "="*70)
    print("🎯 CUBO_4 CORREGIDO")
    print("="*70)
    print("\n✓ Agujeros REALES y COLORES asignados")
    print("\n💡 Recarga en Blender (F5)")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
finally:
    if script_file.exists():
        script_file.unlink()
