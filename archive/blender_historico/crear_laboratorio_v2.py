#!/usr/bin/env python3
"""
Crear 5 archivos .blend en laboratorio
Guardar en: ZULY_PROJECTS/pruebas/laboratorio_*.blend
"""

import subprocess
import sys
import os
from datetime import datetime
import json

BLENDER_EXE = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
BASE_DIR = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
OUTPUT_DIR = os.path.join(BASE_DIR, "ZULY_PROJECTS", "pruebas")

print("=" * 80)
print("LABORATORIO: 5 archivos .blend")
print("=" * 80)
print(f"Ubicacion: {OUTPUT_DIR}\n")

# ============================================================================
# Definir los 5 laboratorios
# ============================================================================

laboratorios = {
    "laboratorio_dado_parques_v10": """
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for x in range(3):
    for y in range(3):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(x*2.5, y*2.5, 1))
        bpy.context.active_object.name = f"Dado_{x}_{y}"
mat = bpy.data.materials.new("Mat1")
mat.diffuse_color = (0.2, 0.6, 1.0, 1.0)
for obj in bpy.data.objects:
    if obj.type == 'MESH' and 'Dado_' in obj.name:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
bpy.context.active_object.data.energy = 1.5
""",

    "laboratorio_dado_parques_v9": """
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for x in range(-2, 3):
    for y in range(-2, 3):
        z = abs(x) + abs(y)
        bpy.ops.mesh.primitive_cube_add(size=0.7, location=(x*1.5, y*1.5, z))
        bpy.context.active_object.name = f"Cubo_{x}_{y}"
mat = bpy.data.materials.new("Mat2")
mat.diffuse_color = (1.0, 0.3, 0.3, 1.0)
for obj in bpy.data.objects:
    if obj.type == 'MESH' and 'Cubo_' in obj.name:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
bpy.context.active_object.data.energy = 1.5
""",

    "laboratorio_dado_crazy_cut": """
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for i in range(5):
    for j in range(2):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=(i*2, j*3, 0))
        obj = bpy.context.active_object
        obj.name = f"Cut_{i}_{j}"
        subsurf = obj.modifiers.new(name="Sub", type='SUBSURF')
        subsurf.levels = 2
mat = bpy.data.materials.new("Mat3")
mat.diffuse_color = (1.0, 0.85, 0.0, 1.0)
for obj in bpy.data.objects:
    if obj.type == 'MESH' and 'Cut_' in obj.name:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
bpy.ops.object.light_add(type='SUN', location=(5, 5, 6))
bpy.context.active_object.data.energy = 2.0
""",

    "laboratorio_dado_redondo": """
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for i in range(3):
    bpy.ops.mesh.primitive_torus_add(major_radius=2.0, minor_radius=0.5, location=(i*6, 0, 0))
    bpy.context.active_object.name = f"Toro_{i}"
mat = bpy.data.materials.new("Mat4")
mat.diffuse_color = (0.2, 0.8, 0.2, 1.0)
for obj in bpy.data.objects:
    if obj.type == 'MESH' and 'Toro_' in obj.name:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
bpy.ops.object.light_add(type='SUN', location=(5, 5, 4))
bpy.context.active_object.data.energy = 1.8
""",

    "laboratorio_playground_hibrido": """
import bpy
import math
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Piso
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -2))
bpy.context.active_object.name = "Piso"

# Centro
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, location=(0, 0, 0))
bpy.context.active_object.name = "Centro"

# Orbita 1
for i in range(8):
    angle = (i / 8) * 2 * math.pi
    x = 4 * math.cos(angle)
    y = 4 * math.sin(angle)
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(x, y, 0.5))
    bpy.context.active_object.name = f"Orb1_{i}"

# Orbita 2
for i in range(6):
    angle = (i / 6) * 2 * math.pi
    x = 6.5 * math.cos(angle)
    y = 6.5 * math.sin(angle)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(x, y, 1))
    bpy.context.active_object.name = f"Orb2_{i}"

# Torres
for xi in [-7, 7]:
    for yi in [-7, 7]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=3, location=(xi, yi, 1.5))
        bpy.context.active_object.name = f"Torre_{xi}_{yi}"

# Materiales
mat_centro = bpy.data.materials.new("Centro")
mat_centro.diffuse_color = (0.8, 0.0, 0.8, 1.0)

mat_piso = bpy.data.materials.new("Piso")
mat_piso.diffuse_color = (0.5, 0.5, 0.5, 1.0)

mat_orb1 = bpy.data.materials.new("Orb1")
mat_orb1.diffuse_color = (0.0, 1.0, 1.0, 1.0)

mat_orb2 = bpy.data.materials.new("Orb2")
mat_orb2.diffuse_color = (1.0, 1.0, 0.0, 1.0)

mat_torre = bpy.data.materials.new("Torre")
mat_torre.diffuse_color = (1.0, 0.5, 0.0, 1.0)

# Aplicar
for obj in bpy.data.objects:
    if not obj.type == 'MESH': continue
    obj.data.materials.clear()
    if "Centro" in obj.name:
        obj.data.materials.append(mat_centro)
    elif "Piso" in obj.name:
        obj.data.materials.append(mat_piso)
    elif "Orb1_" in obj.name:
        obj.data.materials.append(mat_orb1)
    elif "Orb2_" in obj.name:
        obj.data.materials.append(mat_orb2)
    elif "Torre_" in obj.name:
        obj.data.materials.append(mat_torre)

# Luces
bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
bpy.context.active_object.data.energy = 2.0

bpy.ops.object.light_add(type='POINT', location=(-5, -5, 3))
bpy.context.active_object.data.energy = 1.0
bpy.context.active_object.data.color = (0.5, 1.0, 1.0)

# Camara
bpy.ops.object.camera_add(location=(12, -12, 8))
bpy.context.scene.camera = bpy.context.active_object
"""
}

results = []

for lab_name, script_content in laboratorios.items():
    print(f"[{len(results)+1}/5] {lab_name}.blend")
    print("-" * 80)
    
    # Crear script temporal
    temp_script = os.path.join(BASE_DIR, f"temp_{lab_name}.py")
    output_file = os.path.join(OUTPUT_DIR, f"{lab_name}.blend")
    
    # Escribir script con ruta absoluta de salida
    full_script = f"""
import bpy
{script_content}

# Guardar archivo
output_path = r"{output_file}"
bpy.ops.wm.save_as_mainfile(filepath=output_path)
print(f"GUARDADO: {{output_path}}")
"""
    
    with open(temp_script, 'w', encoding='utf-8') as f:
        f.write(full_script)
    
    # Ejecutar Blender
    try:
        result = subprocess.run(
            [BLENDER_EXE, "--background", "--python", temp_script],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=BASE_DIR
        )
        
        # Verificar si se creo el archivo
        import time
        time.sleep(1)  # Esperar a que Blender termine
        
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"[OK] Archivo creado: {size/1024:.1f} KB")
            results.append({"name": lab_name, "status": "OK", "size": size})
        else:
            print(f"[WARN] Archivo no encontrado: {output_file}")
            results.append({"name": lab_name, "status": "WARN", "size": 0})
            
            # Debug: mostrar output de Blender
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
    
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Timeout")
        results.append({"name": lab_name, "status": "TIMEOUT", "size": 0})
    except Exception as e:
        print(f"[ERROR] {str(e)[:50]}")
        results.append({"name": lab_name, "status": f"ERROR", "size": 0})
    
    # Limpiar script temporal
    if os.path.exists(temp_script):
        try:
            os.remove(temp_script)
        except:
            pass

# ============================================================================
# RESUMEN
# ============================================================================

print("\n" + "=" * 80)
print("RESUMEN FINAL")
print("=" * 80)

ok_count = sum(1 for r in results if r['status'] == 'OK')
print(f"\nArchivos creados: {ok_count}/{len(results)}")

for r in results:
    icon = "[OK]" if r['status'] == "OK" else "[FAIL]"
    print(f"  {icon} {r['name']}.blend")
    if r['size'] > 0:
        print(f"        Tamaño: {r['size']/1024:.1f} KB")

print(f"\nUbicacion: {OUTPUT_DIR}/laboratorio_*.blend")

# Guardar metadata
metadata = {
    "timestamp": datetime.now().isoformat(),
    "laboratory": "Laboratorio 5 Blends",
    "location": OUTPUT_DIR,
    "results": results,
    "description": "5 archivos blend -4 de patrones aprendidos + 1 criterio propio"
}

metadata_file = os.path.join(BASE_DIR, "laboratorio_metadata.json")
with open(metadata_file, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2)

print(f"\nMetadata: {metadata_file}")
