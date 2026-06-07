#!/usr/bin/env python3
"""
ZULY CREA: Cubo 3
- Cubo biselado
- Agujero en eje X (ROJO)
- Agujero en eje Y (VERDE)
- Agujero en eje Z (AZUL)
"""

import subprocess
import time
from pathlib import Path
import tempfile

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_OUTPUT = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_3.blend")

print("\n" + "="*70)
print("🎨 ZULY CREA: CUBO_3 (Biselado + 3 Agujeros Coloreados)")
print("="*70)

creation_script = """
import bpy
import math

print("\\n[CREACION] Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# CREAR CUBO BLANCO COMO BASE
print("[CREACION] Creando cubo biselado (2x2x2)...")
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = "CuboBase3"

# MATERIAL BLANCO PARA CUBO
mat_blanco = bpy.data.materials.new(name="MatBlanco")
mat_blanco.use_nodes = True
bsdf = mat_blanco.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
bsdf.inputs[9].default_value = 0.5
cubo.data.materials.append(mat_blanco)

# BEVEL MODIFIER
bevel = cubo.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.2
bevel.segments = 2
bevel.affect = 'EDGES'

# SMOOTH SHADING
cubo.select_set(True)
bpy.context.view_layer.objects.active = cubo
bpy.ops.object.shade_smooth()

print("[CREACION] Cubo base con bevel listo")

# CREAR 3 CILINDROS PARA LOS AGUJEROS
agujeros_config = [
    {
        'nombre': 'AjujeroX',
        'rotacion': (0, math.radians(90), 0),
        'color_name': 'MatRojo',
        'color_rgb': (1.0, 0.0, 0.0, 1.0),
    },
    {
        'nombre': 'AjujeroY',
        'rotacion': (math.radians(90), 0, 0),
        'color_name': 'MatVerde',
        'color_rgb': (0.0, 1.0, 0.0, 1.0),
    },
    {
        'nombre': 'AjujeroZ',
        'rotacion': (0, 0, 0),
        'color_name': 'MatAzul',
        'color_rgb': (0.0, 0.5, 1.0, 1.0),
    },
]

cilindros = []

for config in agujeros_config:
    print(f"[CREACION] Creando {config['nombre']}...")
    
    # Crear cilindro
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=3.5, location=(0, 0, 0))
    cilindro = bpy.context.active_object
    cilindro.name = config['nombre']
    
    # Aplicar rotacion
    cilindro.rotation_euler = config['rotacion']
    
    # Crear material con color
    mat_color = bpy.data.materials.new(name=config['color_name'])
    mat_color.use_nodes = True
    bsdf = mat_color.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = config['color_rgb']
    bsdf.inputs[9].default_value = 0.2
    
    cilindro.data.materials.append(mat_color)
    cilindros.append(cilindro)
    
    print(f"  ✓ {config['nombre']} creado con color")

print("\\n[OPERACION] Aplicando Boolean operations...")

# APLICAR BOOLEAN OPERATIONS
for cilindro in cilindros:
    boolean_mod = cubo.modifiers.new(name=f"Boolean_{cilindro.name}", type='BOOLEAN')
    boolean_mod.operation = 'DIFFERENCE'
    boolean_mod.object = cilindro
    boolean_mod.solver = 'FAST'
    
    # Ocultar cilindro
    cilindro.hide_set(True)
    cilindro.hide_render = True
    
    print(f"  ✓ Boolean para {cilindro.name} aplicado")

print("\\n[FINALIZACION] Optimizando...")

# Aplicar modifiers del cubo
cubo.select_set(True)
bpy.context.view_layer.objects.active = cubo

# Smooth final
bpy.ops.object.shade_smooth()

print("[FINALIZACION] Guardando cubo_3.blend...")

# GUARDAR
filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_3.blend'
bpy.ops.wm.save_as_mainfile(filepath=filepath)

print(f"[OK] Archivo guardado: cubo_3.blend")
print("[OK] Cubo biselado con 3 agujeros coloreados creado")
print("\\nESTADO FINAL:")
print("  - CuboBase3: Material blanco")
print("  - AjujeroX: Material ROJO")
print("  - AjujeroY: Material VERDE")
print("  - AjujeroZ: Material AZUL")
"""

try:
    print("\n📝 Fase 1: Preparando script...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(creation_script)
        script_file = Path(f.name)
    print("   ✓ Script preparado")
    
    print("\n⚙️  Fase 2: ZULY ejecutando creación...")
    start = time.time()
    cmd = [str(BLENDER_PATH), "--background", "--python", str(script_file)]
    result = subprocess.run(cmd, timeout=45)
    elapsed = time.time() - start
    
    print(f"\n✅ Creación completada en {elapsed:.1f} segundos")
    
    # Verificar
    print("\n📊 Fase 3: Verificando archivo...")
    if BLEND_OUTPUT.exists():
        size = BLEND_OUTPUT.stat().st_size / 1024
        print(f"   ✓ Archivo: {BLEND_OUTPUT.name}")
        print(f"   ✓ Tamaño: {size:.1f} KB")
        print(f"   ✓ Ubicación: {BLEND_OUTPUT.parent.name}/")
    else:
        print("   ✗ ERROR: Archivo no creado")
    
    print("\n" + "="*70)
    print("✨ CUBO_3 LISTO")
    print("="*70)
    print("\n🎨 Componentes:")
    print("   🤍 Cubo base: Blanco biselado")
    print("   🔴 Agujero X: ROJO")
    print("   🟢 Agujero Y: VERDE")
    print("   🔵 Agujero Z: AZUL")
    print("\n💡 Próximo: Abre cubo_3.blend en Blender")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
finally:
    if script_file.exists():
        script_file.unlink()
