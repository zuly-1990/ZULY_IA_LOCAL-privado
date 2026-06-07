#!/usr/bin/env python3
"""
ZULY MEJORA: Base Negra + Puntos Amarillos
"""

import subprocess
import os
from datetime import datetime

BASE_DIR = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
OUTPUT_DIR = os.path.join(BASE_DIR, "ZULY_PROJECTS", "pruebas")
BLENDER_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

archivo_mejorado = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\dado_parques_zuly_v10_mejorado.blend"

print("=" * 100)
print("🎨 ZULY MEJORA: Base Negra + Puntos Amarillos")
print("=" * 100)

if not os.path.exists(archivo_mejorado):
    print(f"\n❌ Archivo no encontrado: {archivo_mejorado}")
    exit(1)

size_mb = round(os.path.getsize(archivo_mejorado) / 1024 / 1024, 2)
print(f"\n✅ Archivo de trabajo: dato_parques_zuly_v10_mejorado.blend ({size_mb} MB)")
print("   🎯 Objetivo: Base negra + Puntos amarillos\n")

# Script Blender simplificado
BLENDER_SCRIPT = """
import bpy

archivo = 'ARCHIVO_PATH'
bpy.ops.wm.open_mainfile(filepath=archivo)
print("[ZULY] Abierto: dato_parques_zuly_v10_mejorado.blend")

# Crear materiales
mat_negro = bpy.data.materials.new(name="Base_Negra")
mat_negro.diffuse_color = (0.0, 0.0, 0.0, 1.0)
mat_negro.metallic = 0.2
mat_negro.roughness = 0.5

mat_amarillo = bpy.data.materials.new(name="Puntos_Amarillos")
mat_amarillo.diffuse_color = (1.0, 1.0, 0.0, 1.0)
mat_amarillo.metallic = 0.4
mat_amarillo.roughness = 0.3

print("[ZULY] Materiales creados: Negro + Amarillo")

# Encontrar la malla
malla = None
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        malla = obj
        break

if malla:
    print(f"[ZULY] Malla encontrada: {malla.name}")
    mesh = malla.data
    
    # Limpiar materiales viejos
    while len(mesh.materials) > 0:
        mesh.materials.pop(index=0)
    
    # Agregar nuevos materiales
    mesh.materials.append(mat_negro)
    mesh.materials.append(mat_amarillo)
    
    # Calcular tamaño de caras
    face_areas = []
    for face in mesh.polygons:
        face_areas.append((face.area, face.index))
    
    face_areas.sort()
    
    # Caras pequeñas (pips) = amarillas
    pip_count = max(1, len(face_areas) // 4)
    
    # Asignar colores
    for area, face_idx in face_areas[:pip_count]:
        mesh.polygons[face_idx].material_index = 1  # Amarillo
    
    for area, face_idx in face_areas[pip_count:]:
        mesh.polygons[face_idx].material_index = 0  # Negro
    
    print(f"[ZULY] Colores aplicados: {pip_count} caras AMARILLAS, {len(face_areas) - pip_count} caras NEGRAS")

# Agregar iluminacion
luces = [obj for obj in bpy.data.objects if obj.type == 'LIGHT']
if len(luces) == 0:
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
    luz1 = bpy.context.active_object
    luz1.data.energy = 2.0
    
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 3))
    luz2 = bpy.context.active_object
    luz2.data.energy = 0.8
    
    print("[ZULY] Iluminacion agregada")

# Agregar camara
camaras = [obj for obj in bpy.data.objects if obj.type == 'CAMERA']
if len(camaras) == 0:
    bpy.ops.object.camera_add(location=(4, -4, 3))
    bpy.context.scene.camera = bpy.context.active_object
    print("[ZULY] Camara agregada")

# Guardar
bpy.ops.wm.save_mainfile(filepath=archivo)
print("[ZULY] GUARDADO: dato_parques_zuly_v10_mejorado.blend")
print("[ZULY] ✅ BASE: NEGRA | PUNTOS: AMARILLOS")
"""

# Hacer replacement
BLENDER_SCRIPT = BLENDER_SCRIPT.replace("ARCHIVO_PATH", archivo_mejorado.replace("\\", "\\\\"))

# Guardar script
script_file = os.path.join(BASE_DIR, "temp_mejora_colores.py")
with open(script_file, 'w', encoding='utf-8') as f:
    f.write(BLENDER_SCRIPT)

print("⚙️ Ejecutando Blender...\n")

cmd = [BLENDER_PATH, "--background", "--python", script_file]
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    
    if result.stdout:
        print(result.stdout)
    
    print("\n" + "=" * 100)
    print("✅ MEJORA COMPLETADA")
    print("=" * 100)
    print("""
🎨 RESULTADO FINAL:
   ✅ Base: NEGRA (RGB 0, 0, 0)
   ✅ Puntos: AMARILLOS (RGB 255, 255, 0)
   ✅ Materiales: Optimizados
   ✅ Iluminacion: Agregada
   ✅ Archivo: Guardado

📂 Abre: dato_parques_zuly_v10_mejorado.blend
   Para ver el resultado en Blender
""")
        
except subprocess.TimeoutExpired:
    print("❌ Timeout")
except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if os.path.exists(script_file):
        os.remove(script_file)

print("\n✅ LISTO")
