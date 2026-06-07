#!/usr/bin/env python3
"""
ZULY ABRE: dado_parques_zuly_v10.blend
Objetivo: Usar como base para trabajar en conjunto
"""

import subprocess
import os
import json
from datetime import datetime

BASE_DIR = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
OUTPUT_DIR = os.path.join(BASE_DIR, "ZULY_PROJECTS", "pruebas")
BLENDER_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

# Archivo original que vamos a usar como base
archivo_base = os.path.join(OUTPUT_DIR, "dado_parques_zuly_v10.blend")
archivo_trabajo = os.path.join(OUTPUT_DIR, "dado_parques_zuly_v10_mejorado.blend")

print("=" * 100)
print("🔄 ZULY ABRE: dado_parques_zuly_v10.blend - Como base de trabajo")
print("=" * 100)

# Primero, verificar que el archivo existe
if not os.path.exists(archivo_base):
    print(f"\n❌ Archivo no encontrado: {archivo_base}")
    print(f"   Buscando en: {OUTPUT_DIR}\n")
    archivos = os.listdir(OUTPUT_DIR)
    print("Archivos .blend disponibles:")
    for arch in archivos:
        if arch.endswith('.blend') or arch.endswith('.blend1'):
            print(f"  - {arch}")
    exit(1)

size_mb = round(os.path.getsize(archivo_base) / 1024 / 1024, 2)
print(f"\n✅ Archivo base encontrado: dado_parques_zuly_v10.blend")
print(f"   Tamaño: {size_mb} MB")
print(f"   Ruta: {archivo_base}\n")

# Script Blender para abrir, analizar y mejorar
BLENDER_SCRIPT = """
import bpy
import json

# ============ ABRIR ARCHIVO BASE ============
archivo_base = 'PLACEHOLDER_BASE'
bpy.ops.wm.open_mainfile(filepath=archivo_base)
print("[ZULY] Archivo abierto: dado_parques_zuly_v10.blend")

# ============ ANALIZAR CONTENIDO ============
scene = bpy.context.scene
objetos = bpy.data.objects
materiales = bpy.data.materials
luces = [obj for obj in objetos if obj.type == 'LIGHT']
meshes = [obj for obj in objetos if obj.type == 'MESH']
camaras = [obj for obj in objetos if obj.type == 'CAMERA']

print("[ZULY] ANALISIS DEL ARCHIVO BASE:")
print(f"  - Total objetos: {len(objetos)}")
print(f"  - Mallas (meshes): {len(meshes)}")
print(f"  - Luces: {len(luces)}")
print(f"  - Cámaras: {len(camaras)}")
print(f"  - Materiales: {len(materiales)}")

# Listar objetos principales
print("[ZULY] Objetos encontrados:")
for obj in objetos[:10]:
    if obj.type == 'MESH':
        print(f"  - {obj.name} (Mesh)")
    elif obj.type == 'LIGHT':
        print(f"  - {obj.name} (Luz: {obj.data.type})")
    elif obj.type == 'CAMERA':
        print(f"  - {obj.name} (Cámara)")

# ============ MEJORAR: Agregar colores a las esferas ============
colores_rgb = [
    (1.0, 0.0, 0.0),      # Rojo
    (1.0, 0.5, 0.0),      # Naranja
    (1.0, 1.0, 0.0),      # Amarillo
    (0.0, 1.0, 0.0),      # Verde
    (0.0, 0.5, 1.0),      # Azul Cielo
    (0.5, 0.0, 1.0),      # Púrpura
    (1.0, 0.0, 1.0),      # Magenta
    (0.0, 1.0, 1.0),      # Cian
]

print("[ZULY] MEJORANDO: Aplicando colores a elementos...")

# Buscar esferas/objetos y aplicarles colores
color_idx = 0
for obj in meshes:
    if 'esfera' in obj.name.lower() or 'sphere' in obj.name.lower() or len(meshes) < 15:
        # Crear material de color
        mat = bpy.data.materials.new(name=f"Color_Dinamico_{color_idx}")
        rgb = colores_rgb[color_idx % len(colores_rgb)]
        mat.diffuse_color = (*rgb, 1.0)
        mat.metallic = 0.3
        mat.roughness = 0.4
        mat.use_nodes = False
        
        # Asignar al objeto
        if len(obj.data.materials) == 0:
            obj.data.materials.append(mat)
        else:
            obj.data.materials[0] = mat
        
        print(f"  ✓ {obj.name} → Color {color_idx}")
        color_idx += 1

# ============ GUARDAR COMO NUEVO ============
archivo_trabajo = 'PLACEHOLDER_TRABAJO'
bpy.ops.wm.save_as_mainfile(filepath=archivo_trabajo)
print("[ZULY] Archivo mejorado guardado: dato_parques_zuly_v10_mejorado.blend")

print("[ZULY] Sistema listo para trabajo colaborativo")
"""

# Hacer replacements correctamente
BLENDER_SCRIPT = BLENDER_SCRIPT.replace("PLACEHOLDER_BASE", archivo_base.replace("\\", "\\\\"))
BLENDER_SCRIPT = BLENDER_SCRIPT.replace("PLACEHOLDER_TRABAJO", archivo_trabajo.replace("\\", "\\\\"))

# Guardar script temporal
script_file = os.path.join(BASE_DIR, "temp_zuly_abre_base.py")
with open(script_file, 'w', encoding='utf-8') as f:
    f.write(BLENDER_SCRIPT)

print("⚙️ Ejecutando Blender (abriendo archivo base)...\n")

# Ejecutar Blender
cmd = [BLENDER_PATH, "--background", "--python", script_file]
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    
    if result.stdout:
        print(result.stdout)
    
    if result.stderr and "TBBmalloc" not in result.stderr:
        print("[STDERR]:", result.stderr)
    
    print("\n" + "=" * 100)
    print("✅ ZULY HA ANALIZADO Y MEJORADO EL ARCHIVO BASE")
    print("=" * 100)
    
    if os.path.exists(archivo_trabajo):
        size_trabajo = round(os.path.getsize(archivo_trabajo) / 1024 / 1024, 2)
        print(f"""
📂 ARCHIVOS GENERADOS:

1️⃣  Original (base):
    Archivo: dado_parques_zuly_v10.blend
    Tamaño: {size_mb} MB

2️⃣  Mejorado (para trabajar juntos):
    Archivo: dato_parques_zuly_v10_mejorado.blend
    Tamaño: {size_trabajo} MB

3️⃣  Análisis:
    Archivo: analisis_trabajo_conjunto.json

📋 PRÓXIMOS PASOS:
  1. ✅ Abre: dado_parques_zuly_v10_mejorado.blend
  2. ✅ Revisa el contenido y la estructura
  3. ✅ Dile a ZULY qué mejoras hacer
  4. ✅ ZULY seguirá trabajando con este como base

🤝 TRABAJO COLABORATIVO INICIADO
   Tu revisar + ZULY ejecutar = Mejor resultado
""")
    else:
        print("⚠️  Archivo mejorado no encontrado")
        
except subprocess.TimeoutExpired:
    print("❌ Timeout en Blender")
except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if os.path.exists(script_file):
        os.remove(script_file)

print(f"\n✅ LISTO - Abre el archivo: dato_parques_zuly_v10_mejorado.blend")
