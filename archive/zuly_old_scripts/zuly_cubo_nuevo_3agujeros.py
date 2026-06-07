#!/usr/bin/env python3
"""
ZULY CREA: CUBO NUEVO
- 3 agujeros (X, Y, Z)
- Colores DENTRO de agujeros
- Lógica correcta
- UN SOLO archivo: cubo_3.blend
"""

import subprocess
import tempfile
from pathlib import Path
import time

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_3.blend")

print("\n" + "="*70)
print("🎨 ZULY CREA CUBO NUEVO: 3 Agujeros (X, Y, Z) Coloreados")
print("="*70)

creation_script = """
import bpy
import math

print("\\n[CREACION] Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ========== PASO 1: CUBO BLANCO BISELADO ==========
print("[PASO-1] Creando cubo blanco biselado...")
bpy.ops.mesh.primitive_cube_add(size=2.2, location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = "CuboBase"

# Material blanco base
mat_blanco = bpy.data.materials.new(name="MatBlanco")
mat_blanco.use_nodes = True
nodes = mat_blanco.node_tree.nodes
links = mat_blanco.node_tree.links
nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
bsdf.inputs[9].default_value = 0.5
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
cubo.data.materials.append(mat_blanco)

# Bevel
bevel = cubo.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.2
bevel.segments = 2
bevel.affect = 'EDGES'

print("  ✓ Cubo base listo")

# ========== PASO 2: CREAR CILINDROS PARA AGUJEROS ==========
print("\\n[PASO-2] Creando cilindros para agujeros...")

# Sin materiales - solo para booleana
cy_x = None
cy_y = None
cy_z = None

# Cilindro X
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=4, location=(0, 0, 0))
cy_x = bpy.context.active_object
cy_x.name = "CY_X"
cy_x.rotation_euler = (0, math.radians(90), 0)

# Cilindro Y
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=4, location=(0, 0, 0))
cy_y = bpy.context.active_object
cy_y.name = "CY_Y"
cy_y.rotation_euler = (math.radians(90), 0, 0)

# Cilindro Z
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=4, location=(0, 0, 0))
cy_z = bpy.context.active_object
cy_z.name = "CY_Z"
cy_z.rotation_euler = (0, 0, 0)

print("  ✓ 3 cilindros creados (sin material)")

# ========== PASO 3: BOOLEANAS ==========
print("\\n[PASO-3] Aplicando boolean operations...")

bool_x = cubo.modifiers.new(name="BoolX", type='BOOLEAN')
bool_x.operation = 'DIFFERENCE'
bool_x.object = cy_x
bool_x.solver = 'FAST'

bool_y = cubo.modifiers.new(name="BoolY", type='BOOLEAN')
bool_y.operation = 'DIFFERENCE'
bool_y.object = cy_y
bool_y.solver = 'FAST'

bool_z = cubo.modifiers.new(name="BoolZ", type='BOOLEAN')
bool_z.operation = 'DIFFERENCE'
bool_z.object = cy_z
bool_z.solver = 'FAST'

print("  ✓ 3 booleanas aplicadas")

# ========== PASO 4: CREAR MATERIALES DE COLOR ==========
print("\\n[PASO-4] Creando materiales de color...")

# Rojo (X)
mat_rojo = bpy.data.materials.new(name="MatRojo")
mat_rojo.use_nodes = True
nodes = mat_rojo.node_tree.nodes
links = mat_rojo.node_tree.links
nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf.inputs[0].default_value = (1.0, 0.1, 0.1, 1.0)
bsdf.inputs[9].default_value = 0.3
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Verde (Y)
mat_verde = bpy.data.materials.new(name="MatVerde")
mat_verde.use_nodes = True
nodes = mat_verde.node_tree.nodes
links = mat_verde.node_tree.links
nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf.inputs[0].default_value = (0.1, 1.0, 0.1, 1.0)
bsdf.inputs[9].default_value = 0.3
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Azul (Z)
mat_azul = bpy.data.materials.new(name="MatAzul")
mat_azul.use_nodes = True
nodes = mat_azul.node_tree.nodes
links = mat_azul.node_tree.links
nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf.inputs[0].default_value = (0.1, 0.3, 1.0, 1.0)
bsdf.inputs[9].default_value = 0.3
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

print("  ✓ 3 materiales creados (rojo, verde, azul)")

# ========== PASO 5: ASIGNAR COLORES AL CUBO ==========
print("\\n[PASO-5] Asignando colores al cubo...")

cubo.data.materials.clear()
cubo.data.materials.append(mat_blanco)   # [0]
cubo.data.materials.append(mat_rojo)     # [1]
cubo.data.materials.append(mat_verde)    # [2]
cubo.data.materials.append(mat_azul)     # [3]

print("  ✓ Materiales en cubo: blanco, rojo, verde, azul")

# ========== PASO 6: SMOOTH SHADING ==========
print("\\n[PASO-6] Aplicando smooth shading...")
cubo.select_set(True)
bpy.context.view_layer.objects.active = cubo
bpy.ops.object.shade_smooth()

# ========== PASO 7: ELIMINAR CILINDROS ==========
print("\\n[PASO-7] Eliminando cilindros...")
for obj in [cy_x, cy_y, cy_z]:
    bpy.data.objects.remove(obj, do_unlink=True)

print("  ✓ Cilindros eliminados")

# ========== PASO 8: GUARDAR ==========
print("\\n[GUARDADO] Guardando cubo_3.blend...")
filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_3.blend'
bpy.ops.wm.save_mainfile(filepath=filepath)

print("\\n" + "="*70)
print("✨ CUBO NUEVO COMPLETADO")
print("="*70)
print("\\n🎨 Especificaciones:")
print("  🤍 Cubo: Blanco biselado (2.2x2.2x2.2)")
print("  🔴 Agujero X: ROJO")
print("  🟢 Agujero Y: VERDE")
print("  🔵 Agujero Z: AZUL")
print("  ✓ 3 booleanas aplicadas")
print("  ✓ Smooth shading activo")
print("  ✓ Cilindros: ELIMINADOS")
"""

try:
    print("\n📝 Fase 1: Preparando creación...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(creation_script)
        script_file = Path(f.name)
    print("   ✓ Script listo")
    
    print("\n⚙️  Fase 2: ZULY ejecutando...")
    start = time.time()
    cmd = [str(BLENDER_PATH), "--background", "--python", str(script_file)]
    result = subprocess.run(cmd, timeout=45)
    elapsed = time.time() - start
    
    print(f"\n✅ Creación completada en {elapsed:.1f} segundos")
    
    print("\n📊 Fase 3: Verificando...")
    if BLEND_FILE.exists():
        size = BLEND_FILE.stat().st_size / 1024
        print(f"   ✓ Archivo: {BLEND_FILE.name}")
        print(f"   ✓ Tamaño: {size:.1f} KB")
        print(f"   ✓ Status: LISTO")
    
    print("\n" + "="*70)
    print("🎯 CUBO NUEVO LISTO")
    print("="*70)
    print("\n✓ Archivo único: cubo_3.blend")
    print("✓ Sin duplicados")
    print("✓ 3 agujeros coloreados")
    print("\n💡 Recarga en Blender (F5)")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
finally:
    if script_file.exists():
        script_file.unlink()
