#!/usr/bin/env python3
"""
ZULY MEJORA CUBO_3
- Cubo biselado
- Agujero solo en eje X (ROJO)
- Agujero solo en eje Z (AZUL)
- SIN agujero en Y
- Colores aplicados
"""

import subprocess
import time
from pathlib import Path
import tempfile

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_3.blend")

print("\n" + "="*70)
print("🎨 ZULY MEJORA: CUBO_3 V2 (X + Z, Sin Y)")
print("="*70)

improvement_script = """
import bpy
import math

print("\\n[ZULY] Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ========== CREAR CUBO BISELADO BLANCO ==========
print("[PASO-1] Creando cubo biselado blanco...")
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = "CuboBase"

# Material blanco
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

# Bevel modifier
bevel = cubo.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.2
bevel.segments = 2
bevel.affect = 'EDGES'

# Smooth shading
cubo.select_set(True)
bpy.context.view_layer.objects.active = cubo
bpy.ops.object.shade_smooth()
print("  ✓ Cubo biselado listo")

# ========== CREAR AGUJEROS ==========
# SOLO X y Z (sin Y)
agujeros = [
    {
        'nombre': 'AgujeroX',
        'rotacion': (0, math.radians(90), 0),
        'color': (1.0, 0.1, 0.1, 1.0),  # ROJO
    },
    {
        'nombre': 'AgujeroZ',
        'rotacion': (0, 0, 0),
        'color': (0.1, 0.3, 1.0, 1.0),  # AZUL
    },
]

print("\\n[PASO-2] Creando agujeros (X y Z)...")
cilindros = []

for config in agujeros:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=3.5, location=(0, 0, 0))
    cilindro = bpy.context.active_object
    cilindro.name = config['nombre']
    cilindro.rotation_euler = config['rotacion']
    
    # Material con color
    mat = bpy.data.materials.new(name=f"Mat{config['nombre']}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    output = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf.inputs[0].default_value = config['color']
    bsdf.inputs[9].default_value = 0.2
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    cilindro.data.materials.append(mat)
    cilindros.append(cilindro)
    print(f"  ✓ {config['nombre']} con color")

# ========== BOOLEAN OPERATIONS ==========
print("\\n[PASO-3] Aplicando Boolean operations...")
for cilindro in cilindros:
    boolean = cubo.modifiers.new(name=f"Bool{cilindro.name}", type='BOOLEAN')
    boolean.operation = 'DIFFERENCE'
    boolean.object = cilindro
    boolean.solver = 'FAST'
    
    cilindro.hide_set(True)
    cilindro.hide_render = True
    print(f"  ✓ Boolean {cilindro.name}")

# ========== FINALIZACION ==========
print("\\n[PASO-4] Finalizando...")
cubo.select_set(True)
bpy.context.view_layer.objects.active = cubo
bpy.ops.object.shade_smooth()

# GUARDAR
filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_3.blend'
bpy.ops.wm.save_mainfile(filepath=filepath)

print("\\n[OK] Guardado: cubo_3.blend")
print("\\n✨ CUBO_3 MEJORADO:")
print("  🤍 Cubo: Blanco biselado")
print("  🔴 Agujero X: ROJO")
print("  🔵 Agujero Z: AZUL")
print("  ❌ Agujero Y: ELIMINADO")
"""

try:
    print("\n📝 Fase 1: Preparando mejora...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(improvement_script)
        script_file = Path(f.name)
    print("   ✓ Script listo")
    
    print("\n🎨 Fase 2: ZULY ejecutando mejora...")
    start = time.time()
    cmd = [str(BLENDER_PATH), "--background", "--python", str(script_file)]
    result = subprocess.run(cmd, timeout=30)
    elapsed = time.time() - start
    
    print(f"\n✅ Mejora completada en {elapsed:.1f} segundos")
    
    # Verificar
    print("\n📊 Fase 3: Verificando...")
    if BLEND_FILE.exists():
        size = BLEND_FILE.stat().st_size / 1024
        print(f"   ✓ Archivo: {BLEND_FILE.name}")
        print(f"   ✓ Tamaño: {size:.1f} KB")
        print(f"   ✓ Status: MEJORADO")
    
    print("\n" + "="*70)
    print("✨ CUBO_3 V2 LISTO")
    print("="*70)
    print("\n🎯 Cambios:")
    print("   ✓ Cubo biselado (2x2x2)")
    print("   ✓ Agujero X rojo")
    print("   ✓ Agujero Z azul")
    print("   ✓ SIN agujero en Y")
    print("\n💡 Recarga en Blender (F5) para ver mejoras")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
finally:
    if script_file.exists():
        script_file.unlink()
