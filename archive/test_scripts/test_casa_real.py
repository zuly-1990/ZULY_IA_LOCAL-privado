#!/usr/bin/env python3
"""
🏠 CASA 2 PLANTAS - Prueba Real en Blender
Genera modelo y guarda como .blend
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime

# Ruta de Blender
script_dir = Path(__file__).parent
blender_exe = script_dir / "blender/v3/blender-3.6.0-zuly/blender.exe"

# Script Python para Blender
blender_script = """
import bpy
import math
from datetime import datetime

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# PLANTA BAJA

# Piso
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
piso1 = bpy.context.active_object
piso1.scale = (8, 10, 0.2)

# Paredes
paredes_pb = [
    ((0, 5, 1.25), (8, 0.3, 2.5)),    # Frente
    ((0, -5, 1.25), (8, 0.3, 2.5)),   # Atrás
    ((-4, 0, 1.25), (0.3, 10, 2.5)),  # Izq
    ((4, 0, 1.25), (0.3, 10, 2.5)),   # Der
]

for pos, scale in paredes_pb:
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    pared = bpy.context.active_object
    pared.scale = scale

# Puertas
puertas = [
    ((0, 5.15, 0.9), (0.9, 0.1, 1.8)),
    ((-2, 0.15, 0.9), (0.9, 0.1, 1.8)),
]

for pos, scale in puertas:
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    puerta = bpy.context.active_object
    puerta.scale = scale

# Ventanas
ventanas = [
    ((-2, 5.15, 1.5), (0.8, 0.1, 0.8)),
    ((2, 5.15, 1.5), (0.8, 0.1, 0.8)),
    ((-2, -5.15, 1.5), (0.8, 0.1, 0.8)),
    ((2, -5.15, 1.5), (0.8, 0.1, 0.8)),
    ((-4.15, -3, 1.5), (0.1, 0.8, 0.8)),
    ((-4.15, 3, 1.5), (0.1, 0.8, 0.8)),
    ((4.15, -3, 1.5), (0.1, 0.8, 0.8)),
    ((4.15, 3, 1.5), (0.1, 0.8, 0.8)),
]

for pos, scale in ventanas:
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    ventana = bpy.context.active_object
    ventana.scale = scale

# PLANTA ALTA

# Piso 2
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.7))
piso2 = bpy.context.active_object
piso2.scale = (8, 10, 0.2)

# Paredes planta alta
for pos, scale in paredes_pb:
    pos_nueva = (pos[0], pos[1], pos[2] + 2.7)
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos_nueva)
    pared = bpy.context.active_object
    pared.scale = scale

# Ventanas planta alta
ventanas_pa = [
    ((-2, 5.15, 3.5), (0.8, 0.1, 0.8)),
    ((2, 5.15, 3.5), (0.8, 0.1, 0.8)),
]

for pos, scale in ventanas_pa:
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    ventana = bpy.context.active_object
    ventana.scale = scale

# TECHOS Y ACABADOS

# Techo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 5.2))
techo = bpy.context.active_object
techo.scale = (8, 10, 0.2)

# Tejado triangular
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 5.7))
tejado1 = bpy.context.active_object
tejado1.scale = (8, 0.5, 0.8)
tejado1.rotation_euler = (math.radians(30), 0, 0)

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 5.7))
tejado2 = bpy.context.active_object
tejado2.scale = (8, 0.5, 0.8)
tejado2.rotation_euler = (math.radians(-30), 0, 0)

# ESCALERAS
for i in range(5):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -1.5 - i*0.3, 0.5 + i*0.3))
    escalon = bpy.context.active_object
    escalon.scale = (0.3, 0.8, 0.2)

# PILARES
for x in [-3.5, 3.5]:
    for y in [-3.5, 3.5]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=5, location=(x, y, 2.5))

# JARDIN (plantas y terraza)
for x in [-7, -5, 5, 7]:
    for y in [-7, 7]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(x, y, 0.3))

# Camino
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 8, 0.05))
camino = bpy.context.active_object
camino.scale = (2, 2, 0.1)

# Terraza
bpy.ops.mesh.primitive_cube_add(size=1, location=(-6, 5, 0.1))
terraza = bpy.context.active_object
terraza.scale = (2, 2, 0.1)

# GUARDAR BLENDER
fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
archivo = f"Casa_Completa_2Plantas_{fecha}.blend"
ruta = f"ZULY_LAB/{archivo}"

bpy.ops.wm.save_as_mainfile(filepath=ruta)

print("\\n✅ CASA COMPLETADA")
print(f"📄 Guardada en: {ruta}")
print(f"📊 Total objetos: {len(bpy.context.scene.objects)}")
print(f"🏠 Estructura: Paredes, puertas, ventanas, techo, escaleras, pilares, jardín")
"""

# Guardar script temporal
temp_script = script_dir / "temp_house.py"
with open(temp_script, "w", encoding="utf-8") as f:
    f.write(blender_script)

print("\n" + "="*70)
print("  🏠 CREANDO CASA COMPLETA 2 PLANTAS")
print("="*70 + "\n")

# Ejecutar Blender
cmd = [str(blender_exe), "--background", "--python", str(temp_script)]

print(f"⚙️  Ejecutando Blender...\n")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

# Verificar archivo
zuly_lab = script_dir / "ZULY_LAB"
blend_files = sorted(zuly_lab.glob("Casa_Completa_2Plantas_*.blend"))[-1:]

if blend_files:
    archivo = blend_files[0]
    tamaño = archivo.stat().st_size / (1024*1024)
    print(f"\n✅ ARCHIVO CREADO:")
    print(f"   📄 {archivo.name}")
    print(f"   📦 Tamaño: {tamaño:.2f} MB")
    print(f"   📍 {archivo}\n")

# Limpiar
temp_script.unlink()
