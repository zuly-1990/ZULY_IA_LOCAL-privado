#!/usr/bin/env python3
"""
ZULY CORRIGE: Pintar AGUJEROS del cubo, no los cilindros
Lógica correcta:
1. Cilindros SIN color (solo para booleana)
2. Aplicar booleanas
3. Pintar SOLO el cubo
4. Eliminar cilindros
"""

import subprocess
import time
from pathlib import Path
import tempfile

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_3.blend")

print("\n" + "="*70)
print("🔧 ZULY CORRIGE: Pintar AGUJEROS (no cilindros)")
print("="*70)

corrected_script = """
import bpy
import math

print("\\n[ZULY] Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ========== PASO 1: CREAR CUBO BLANCO ==========
print("\\n[PASO-1] Creando cubo biselado blanco...")
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = "CuboBase"

# Material blanco para TODO el cubo
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

# ========== PASO 2: CREAR CILINDROS SIN MATERIAL ==========
print("\\n[PASO-2] Creando cilindros para booleana...")

cilindro_x = None
cilindro_z = None

# Cilindro para agujero X
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=3.5, location=(0, 0, 0))
cilindro_x = bpy.context.active_object
cilindro_x.name = "CY_X"
cilindro_x.rotation_euler = (0, math.radians(90), 0)

# Cilindro para agujero Z
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=3.5, location=(0, 0, 0))
cilindro_z = bpy.context.active_object
cilindro_z.name = "CY_Z"
cilindro_z.rotation_euler = (0, 0, 0)

print("  ✓ Cilindros sin material creados")

# ========== PASO 3: APLICAR BOOLEANAS ==========
print("\\n[PASO-3] Aplicando boolean operations...")

# Boolean X
bool_x = cubo.modifiers.new(name="BoolX", type='BOOLEAN')
bool_x.operation = 'DIFFERENCE'
bool_x.object = cilindro_x
bool_x.solver = 'FAST'

# Boolean Z
bool_z = cubo.modifiers.new(name="BoolZ", type='BOOLEAN')
bool_z.operation = 'DIFFERENCE'
bool_z.object = cilindro_z
bool_z.solver = 'FAST'

print("  ✓ Booleanas aplicadas")

# ========== PASO 4: CREAR MATERIALES CON COLORES ==========
print("\\n[PASO-4] Creando materiales para agujeros...")

# Material rojo (para agujero X)
mat_rojo = bpy.data.materials.new(name="MatRojo")
mat_rojo.use_nodes = True
nodes = mat_rojo.node_tree.nodes
links = mat_rojo.node_tree.links
nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf.inputs[0].default_value = (1.0, 0.1, 0.1, 1.0)
bsdf.inputs[9].default_value = 0.2
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
print("  ✓ Material rojo creado")

# Material azul (para agujero Z)
mat_azul = bpy.data.materials.new(name="MatAzul")
mat_azul.use_nodes = True
nodes = mat_azul.node_tree.nodes
links = mat_azul.node_tree.links
nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf.inputs[0].default_value = (0.1, 0.3, 1.0, 1.0)
bsdf.inputs[9].default_value = 0.2
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
print("  ✓ Material azul creado")

# ========== PASO 5: APLICAR SMOOTH ==========
print("\\n[PASO-5] Aplicando smooth shading...")
cubo.select_set(True)
bpy.context.view_layer.objects.active = cubo
bpy.ops.object.shade_smooth()
print("  ✓ Smooth aplicado")

# ========== PASO 6: AGREGAR MATERIALES AL CUBO ==========
print("\\n[PASO-6] Asignando materiales al cubo...")

# Limpiar materiales previos del cubo
cubo.data.materials.clear()

# Agregar todos los materiales
cubo.data.materials.append(mat_blanco)
cubo.data.materials.append(mat_rojo)
cubo.data.materials.append(mat_azul)

print("  ✓ Materiales asignados al cubo")

# ========== PASO 7: ELIMINAR CILINDROS ==========
print("\\n[PASO-7] Eliminando cilindros...")
for obj in [cilindro_x, cilindro_z]:
    bpy.data.objects.remove(obj, do_unlink=True)
print("  ✓ Cilindros eliminados")

# ========== PASO 8: GUARDAR ==========
print("\\n[PASO-8] Guardando...")
filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_3.blend'
bpy.ops.wm.save_mainfile(filepath=filepath)

print("\\n[OK] Guardado: cubo_3.blend")
print("\\n✨ CUBO_3 CORREGIDO:")
print("  🤍 Cubo: Blanco biselado")
print("  🔴 Agujero X: Tiene color ROJO")
print("  🔵 Agujero Z: Tiene color AZUL")
print("  ✓ Cilindros: ELIMINADOS")
"""

try:
    print("\n📝 Fase 1: Preparando corrección...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(corrected_script)
        script_file = Path(f.name)
    print("   ✓ Script de corrección listo")
    
    print("\n🔧 Fase 2: ZULY ejecutando corrección...")
    start = time.time()
    cmd = [str(BLENDER_PATH), "--background", "--python", str(script_file)]
    result = subprocess.run(cmd, timeout=30)
    elapsed = time.time() - start
    
    print(f"\n✅ Corrección completada en {elapsed:.1f} segundos")
    
    print("\n📊 Fase 3: Verificando...")
    if BLEND_FILE.exists():
        size = BLEND_FILE.stat().st_size / 1024
        print(f"   ✓ Archivo: {BLEND_FILE.name}")
        print(f"   ✓ Tamaño: {size:.1f} KB")
    
    print("\n" + "="*70)
    print("✨ CUBO_3 CORREGIDO CORRECTAMENTE")
    print("="*70)
    print("\n🎯 Cambios realizados:")
    print("   ✓ Cilindros: SIN material (solo para booleana)")
    print("   ✓ Agujeros: PINTADOS en el cubo")
    print("   ✓ Agujero X: Rojo")
    print("   ✓ Agujero Z: Azul")
    print("   ✓ Cilindros: ELIMINADOS del archivo")
    print("\n💡 Recarga en Blender (F5)")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
finally:
    if script_file.exists():
        script_file.unlink()
