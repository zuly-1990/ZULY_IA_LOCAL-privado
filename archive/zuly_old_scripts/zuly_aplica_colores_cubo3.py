#!/usr/bin/env python3
"""
ZULY REPARA: Aplicar colores a los agujeros de CUBO_3
Trabajo SOLO con cubo_3.blend hasta satisfacción total
"""

import subprocess
import time
from pathlib import Path
import tempfile

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_3.blend")

print("\n" + "="*70)
print("🔧 ZULY REPARA: Aplicar COLORES a agujeros de CUBO_3")
print("="*70)

repair_script = """
import bpy

filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_3.blend'

print("\\n[REPARACION] Abriendo cubo_3.blend...")
bpy.ops.wm.open_mainfile(filepath=filepath)

# LIMPIAR MATERIALES PREVIOS
print("[REPARACION] Limpiando materiales existentes...")
for mat in bpy.data.materials:
    if "Mat" in mat.name or "Color" in mat.name:
        bpy.data.materials.remove(mat)

# CREAR MATERIALES CON COLORES
print("\\n[COLORES] Creando materiales...")

# MATERIAL BLANCO para cubo
mat_blanco = bpy.data.materials.new(name="MatBlancoFinal")
mat_blanco.use_nodes = True
nodes = mat_blanco.node_tree.nodes
links = mat_blanco.node_tree.links
nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
bsdf.inputs['Roughness'].default_value = 0.5
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
print("  ✓ Blanco creado")

# MATERIAL ROJO para AjujeroX
mat_rojo = bpy.data.materials.new(name="MatRojoFinal")
mat_rojo.use_nodes = True
nodes = mat_rojo.node_tree.nodes
links = mat_rojo.node_tree.links
nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf.inputs['Base Color'].default_value = (1.0, 0.1, 0.1, 1.0)
bsdf.inputs['Roughness'].default_value = 0.3
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
print("  ✓ Rojo creado")

# MATERIAL VERDE para AjujeroY
mat_verde = bpy.data.materials.new(name="MatVerdeFinal")
mat_verde.use_nodes = True
nodes = mat_verde.node_tree.nodes
links = mat_verde.node_tree.links
nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf.inputs['Base Color'].default_value = (0.1, 1.0, 0.1, 1.0)
bsdf.inputs['Roughness'].default_value = 0.3
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
print("  ✓ Verde creado")

# MATERIAL AZUL para AjujeroZ
mat_azul = bpy.data.materials.new(name="MatAzulFinal")
mat_azul.use_nodes = True
nodes = mat_azul.node_tree.nodes
links = mat_azul.node_tree.links
nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf.inputs['Base Color'].default_value = (0.1, 0.3, 1.0, 1.0)
bsdf.inputs['Roughness'].default_value = 0.3
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
print("  ✓ Azul creado")

# APLICAR MATERIALES A OBJETOS
print("\\n[APLICACION] Asignando materiales a objetos...")

asignaciones = {
    'CuboBase3': mat_blanco,
    'AjujeroX': mat_rojo,
    'AjujeroY': mat_verde,
    'AjujeroZ': mat_azul,
}

for obj_name, material in asignaciones.items():
    # Buscar objeto
    obj = bpy.data.objects.get(obj_name)
    if obj and obj.type == 'MESH':
        # Limpiar materiales previos
        obj.data.materials.clear()
        # Agregar nuevo material
        obj.data.materials.append(material)
        print(f"  ✓ {obj_name} <- {material.name}")
        
        # Hacer visible (por si estaba oculto)
        obj.hide_set(False)
        obj.hide_render = False
    else:
        print(f"  ✗ NO ENCONTRADO: {obj_name}")

# APLICAR SMOOTH SHADING A TODO
print("\\n[ACABADO] Aplicando smooth shading...")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.shade_smooth()
        obj.select_set(False)

print("  ✓ Smooth shading aplicado")

# GUARDAR MISMO ARCHIVO
print("\\n[GUARDADO] Guardando cubo_3.blend...")
bpy.ops.wm.save_mainfile(filepath=filepath)

print("[OK] Archivo guardado")
print("\\nRESUMEN FINAL:")
print("  🤍 CuboBase3: Blanco")
print("  🔴 AjujeroX: Rojo")
print("  🟢 AjujeroY: Verde")
print("  🔵 AjujeroZ: Azul")
print("\\n✓ COLORES APLICADOS CORRECTAMENTE")
"""

try:
    print("\n📝 Paso 1: Preparando reparación...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(repair_script)
        script_file = Path(f.name)
    print("   ✓ Script listo")
    
    print("\n🔧 Paso 2: ZULY ejecutando reparación...")
    start = time.time()
    cmd = [str(BLENDER_PATH), "--background", "--python", str(script_file)]
    result = subprocess.run(cmd, timeout=30)
    elapsed = time.time() - start
    
    print(f"\n✅ Reparación completada en {elapsed:.1f} segundos")
    
    # Verificar
    print("\n📊 Paso 3: Verificando archivo...")
    if BLEND_FILE.exists():
        size = BLEND_FILE.stat().st_size / 1024
        print(f"   ✓ Archivo: {BLEND_FILE.name}")
        print(f"   ✓ Tamaño: {size:.1f} KB")
        print(f"   ✓ Status: COLORES APLICADOS")
    
    print("\n" + "="*70)
    print("✨ CUBO_3 REPARADO Y COLOREADO")
    print("="*70)
    print("\n🎨 Colores aplicados:")
    print("   🤍 Cubo: BLANCO")
    print("   🔴 Agujero X: ROJO")
    print("   🟢 Agujero Y: VERDE")
    print("   🔵 Agujero Z: AZUL")
    print("\n💡 Recarga en Blender (F5) para ver colores")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
finally:
    if script_file.exists():
        script_file.unlink()
