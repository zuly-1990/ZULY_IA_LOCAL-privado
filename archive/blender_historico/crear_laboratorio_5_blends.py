#!/usr/bin/env python3
"""
LABORATORIO: Crear 5 archivos .blend
====================================

4 basados en lo aprendido + 1 a criterio propio
Todos etiquetados como laboratorio
Ubicación: ZULY_PROJECTS/pruebas/laboratorio_*.blend
"""

import subprocess
import sys
import os
from datetime import datetime
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.cognition.c2_pattern_storage import PatternStorageV2

print("=" * 80)
print("LABORATORIO: Crear 5 archivos .blend")
print("=" * 80)

BLENDER_EXE = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
OUTPUT_DIR = r"ZULY_PROJECTS\pruebas"
STORAGE = PatternStorageV2()

# ============================================================================
# LABORATORIO 1: Dado Parques V10 (Interactive System - Esfera simple)
# ============================================================================

print("\n[LAB 1/5] laboratorio_dado_parques_v10.blend")
print("-" * 80)

lab1_script = """import bpy
import os
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Crear esferas simples en rejilla
for x in range(3):
    for y in range(3):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(x*2.5, y*2.5, 1))
        obj = bpy.context.active_object
        obj.name = f"Dado_Lab1_{x}_{y}"

# Agregar material
mat = bpy.data.materials.new("Lab1Material")
mat.diffuse_color = (0.2, 0.6, 1.0, 1.0)

for obj in bpy.data.objects:
    if 'Dado_Lab1' in obj.name and obj.type == 'MESH':
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

# Luz y camara
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
bpy.context.active_object.data.energy = 1.5
bpy.ops.object.camera_add(location=(5, 5, 5))
bpy.context.scene.camera = bpy.context.active_object

# Guardar archivo
output_path = os.path.expanduser("~/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/pruebas/laboratorio_dado_parques_v10.blend")
bpy.ops.wm.save_as_mainfile(filepath=output_path)
print(f"Saved: {output_path}")
"""

# ============================================================================
# LABORATORIO 2: Dado Parques V9 (Interactive System - Cubos)
# ============================================================================

print("[LAB 2/5] laboratorio_dado_parques_v9.blend")
print("-" * 80)

lab2_script = """import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Crear cubos en piramide
for x in range(-2, 3):
    for y in range(-2, 3):
        z = abs(x) + abs(y)
        size = 0.7
        bpy.ops.mesh.primitive_cube_add(size=size, location=(x*1.5, y*1.5, z))
        obj = bpy.context.active_object
        obj.name = f"Cubo_Lab2_{x}_{y}"

# Agregar material rojo
mat = bpy.data.materials.new("Lab2Material")
mat.diffuse_color = (1.0, 0.3, 0.3, 1.0)

for obj in bpy.data.objects:
    if 'Cubo_Lab2' in obj.name and obj.type == 'MESH':
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

# Luz y camara
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
bpy.context.active_object.data.energy = 1.5
bpy.ops.object.camera_add(location=(8, 8, 5))
bpy.context.scene.camera = bpy.context.active_object
"""

# ============================================================================
# LABORATORIO 3: Dado Crazy Cut (Procedural System - Meshes complejos)
# ============================================================================

print("[LAB 3/5] laboratorio_dado_crazy_cut.blend")
print("-" * 80)

lab3_script = """import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Crear objetos UV sphere con modificadores
for i in range(5):
    for j in range(2):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.6,
            location=(i*2, j*3, 0)
        )
        obj = bpy.context.active_object
        obj.name = f"CrazyCut_{i}_{j}"
        
        # Agregar subdivision surface
        subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
        subsurf.levels = 2

# Agregar material metalico
mat = bpy.data.materials.new("Lab3Material")
mat.diffuse_color = (1.0, 0.85, 0.0, 1.0)

for obj in bpy.data.objects:
    if 'CrazyCut' in obj.name and obj.type == 'MESH':
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

# Luz y camara
bpy.ops.object.light_add(type='SUN', location=(5, 5, 6))
bpy.context.active_object.data.energy = 2.0
bpy.ops.object.camera_add(location=(10, 10, 8))
bpy.context.scene.camera = bpy.context.active_object
"""

# ============================================================================
# LABORATORIO 4: Dado Redondo (Geometric Object - Toroide)
# ============================================================================

print("[LAB 4/5] laboratorio_dado_redondo.blend")
print("-" * 80)

lab4_script = """import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Crear toroides
for i in range(3):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=2.0,
        minor_radius=0.5,
        location=(i*6, 0, 0)
    )
    obj = bpy.context.active_object
    obj.name = f"Toroide_{i}"

# Agregar material verde
mat = bpy.data.materials.new("Lab4Material")
mat.diffuse_color = (0.2, 0.8, 0.2, 1.0)

for obj in bpy.data.objects:
    if 'Toroide' in obj.name and obj.type == 'MESH':
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

# Luz y camara
bpy.ops.object.light_add(type='SUN', location=(5, 5, 4))
bpy.context.active_object.data.energy = 1.8
bpy.ops.object.camera_add(location=(6, 6, 6))
bpy.context.scene.camera = bpy.context.active_object
"""

# ============================================================================
# LABORATORIO 5: Sistema Hibrido (Criterio propio - Playground creativo)
# ============================================================================

print("[LAB 5/5] laboratorio_playground_hibrido.blend")
print("-" * 80)

lab5_script = """import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Creando Playground Hibrido (Mi Criterio)")

# PISO: Plano grande
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -2))
piso = bpy.context.active_object
piso.name = "Piso"

# CENTRO: Esfera grande (centro de atencion)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, location=(0, 0, 0))
centro = bpy.context.active_object
centro.name = "Centro_Energia"

# ORBITA 1: Cubos orbitando
import math
for i in range(8):
    angle = (i / 8) * 2 * math.pi
    x = 4 * math.cos(angle)
    y = 4 * math.sin(angle)
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(x, y, 0.5))
    cubo = bpy.context.active_object
    cubo.name = f"Orbita1_Cubo_{i}"

# ORBITA 2: Esferas en orbita
for i in range(6):
    angle = (i / 6) * 2 * math.pi
    x = 6.5 * math.cos(angle)
    y = 6.5 * math.sin(angle)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(x, y, 1))
    esfera = bpy.context.active_object
    esfera.name = f"Orbita2_Esfera_{i}"

# TORRES: Cilindros en las esquinas
for xi in [-7, 7]:
    for yi in [-7, 7]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.3, depth=3, location=(xi, yi, 1.5)
        )
        cilindro = bpy.context.active_object
        cilindro.name = f"Torre_{xi}_{yi}"

# MATERIALES Y COLORES
materiales = {
    "Centro_Energia": (0.8, 0.0, 0.8, 1.0),  # Magenta
    "Piso": (0.5, 0.5, 0.5, 1.0),            # Gris
}

mat_orbita1 = bpy.data.materials.new("Orbita1")
mat_orbita1.diffuse_color = (0.0, 1.0, 1.0, 1.0)  # Cian

mat_orbita2 = bpy.data.materials.new("Orbita2")
mat_orbita2.diffuse_color = (1.0, 1.0, 0.0, 1.0)  # Amarillo

mat_torres = bpy.data.materials.new("Torres")
mat_torres.diffuse_color = (1.0, 0.5, 0.0, 1.0)   # Naranja

# Aplicar materiales
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        mat = None
        if obj.name == "Centro_Energia":
            mat_base = bpy.data.materials.new("Centro")
            mat_base.diffuse_color = materiales["Centro_Energia"]
            mat = mat_base
        elif obj.name == "Piso":
            mat_base = bpy.data.materials.new("Piso")
            mat_base.diffuse_color = materiales["Piso"]
            mat = mat_base
        elif "Orbita1" in obj.name:
            mat = mat_orbita1
        elif "Orbita2" in obj.name:
            mat = mat_orbita2
        elif "Torre" in obj.name:
            mat = mat_torres
        
        if mat:
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)

# ILUMINACION
bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
luz_principal = bpy.context.active_object
luz_principal.data.energy = 2.0

bpy.ops.object.light_add(type='POINT', location=(-5, -5, 3))
luz_secundaria = bpy.context.active_object
luz_secundaria.data.energy = 1.0
luz_secundaria.data.color = (0.5, 1.0, 1.0)

# CAMARA
bpy.ops.object.camera_add(location=(12, -12, 8))
camara = bpy.context.active_object
bpy.context.scene.camera = camara
camara.rotation_euler = (1.1, 0, 0.785)
camara.name = "CamaraPlayground"

print("Playground Hibrido completado")
"""

# ============================================================================
# EJECUTAR TODOS LOS LABORATORIOS
# ============================================================================

labs = [
    ("laboratorio_dado_parques_v10", lab1_script),
    ("laboratorio_dado_parques_v9", lab2_script),
    ("laboratorio_dado_crazy_cut", lab3_script),
    ("laboratorio_dado_redondo", lab4_script),
    ("laboratorio_playground_hibrido", lab5_script),
]

results = []

for lab_name, script_content in labs:
    output_file = os.path.join(OUTPUT_DIR, f"{lab_name}.blend")
    
    # Guardar script temporal
    temp_script = f"temp_{lab_name}.py"
    with open(temp_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Ejecutar Blender
    try:
        result = subprocess.run(
            [BLENDER_EXE, "--background", "--python", temp_script],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Verificar resultado
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"[OK] {lab_name}.blend ({size/1024:.1f} KB)")
            results.append({
                "name": lab_name,
                "status": "OK",
                "file": output_file,
                "size": size
            })
        else:
            print(f"[WARN] No se genero {lab_name}.blend")
            results.append({
                "name": lab_name,
                "status": "WARN - No generado",
                "file": output_file,
                "size": 0
            })
    except Exception as e:
        print(f"[ERROR] {lab_name}: {str(e)[:50]}")
        results.append({
            "name": lab_name,
            "status": f"ERROR: {str(e)[:30]}",
            "file": output_file,
            "size": 0
        })
    
    # Limpiar
    if os.path.exists(temp_script):
        os.remove(temp_script)

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 80)
print("RESUMEN: LABORATORIO 5 ARCHIVOS .BLEND")
print("=" * 80)

print("\nARCHIVOS GENERADOS:")
for r in results:
    status_icon = "[OK]" if r['status'] == "OK" else "[WARN]" if "WARN" in r['status'] else "[ERROR]"
    print(f"  {status_icon} {r['name']}.blend")
    if r['size'] > 0:
        print(f"        Ubicacion: {r['file']}")
        print(f"        Tamaño: {r['size']/1024:.1f} KB")

print(f"\nUBICACION: {OUTPUT_DIR}/laboratorio_*.blend")

print(f"""
DESCRIPCION:

1. laboratorio_dado_parques_v10.blend
   - 9 esferas en rejilla 3x3
   - Material azul
   - Patron aprendido: dado_parques_v10
   - Concepto: Sistema simple de objetos interactivos

2. laboratorio_dado_parques_v9.blend
   - 25 cubos en piramide hexagonal
   - Material rojo
   - Patron aprendido: dado_parques_v9
   - Concepto: Construccion geometrica

3. laboratorio_dado_crazy_cut.blend
   - 10 esferas con subdivision surface
   - Material dorado
   - Patron aprendido: dado_crazy_cut
   - Concepto: Geometria procesal avanzada

4. laboratorio_dado_redondo.blend
   - 3 toroides en fila
   - Material verde
   - Patron aprendido: dado_redondo
   - Concepto: Objetos geometricos redondos

5. laboratorio_playground_hibrido.blend (MI CRITERIO)
   - Playground creativo que combina TODO
   - Centro energetico + 2 orbitas + torres
   - Multiples materiales y luces
   - Concepto: Composicion artistica que integra aprendizaje completo
   
TODOS ETIQUETADOS COMO: laboratorio_*

Proximos pasos:
  1. Abrir en Blender UI: blender laboratorio_*.blend
  2. Editar y mejorar manualmente
  3. Usar como templates para futuras creaciones
  4. Entrenar C2 con estos archivos
""")

# Guardar metadata
metadata = {
    "timestamp": datetime.now().isoformat(),
    "laboratory": "Laboratorio 5 Blends",
    "location": OUTPUT_DIR,
    "files": results,
    "description": "5 archivos blend etiquetados como laboratorio - 4 de patrones aprendidos + 1 criterio propio"
}

with open("laboratorio_metadata.json", 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2)

print("\nMetadata guardada: laboratorio_metadata.json")
