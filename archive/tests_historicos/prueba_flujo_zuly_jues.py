#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FLUJO COMPLETO ZULY + JUES-BOT - PRUEBA UNIFICADA
Actúa como usuario solicitando un patrón simple
"""

import subprocess
import json
import shutil
from pathlib import Path
from datetime import datetime

# ============================================================================
# PASO 1: USUARIO SOLICITA PATRÓN
# ============================================================================
print("="*70)
print("👤 USUARIO: 'Necesito un cubo rojo con bordes suaves'")
print("="*70)

pedido = {
    "id": "PED-001",
    "descripcion": "Cubo rojo con bordes suaves",
    "color": "#FF0000",
    "timestamp": datetime.now().isoformat()
}

print(f"\n📋 Pedido registrado:")
print(f"   ID: {pedido['id']}")
print(f"   Descripción: {pedido['descripcion']}")
print(f"   Color requerido: {pedido['color']}")

# ============================================================================
# PASO 2: ZULY GENERA EL PATRÓN
# ============================================================================
print("\n" + "="*70)
print("🤖 ZULY: Generando patrón CUB-001_v1...")
print("="*70)

# Script Python para Blender
script_generacion = '''
import bpy
import sys

print("="*60)
print("ZULY GENERANDO: CUB-001_v1 - Cubo Rojo con Bisel")
print("="*60)

# RESET
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)

# Crear cubo
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cubo = bpy.context.active_object
cubo.name = "CUB001_v1_RojoSuave"

# Aplicar escala
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# BEVEL
bevel = cubo.modifiers.new(name="Bevel_Suave", type='BEVEL')
bevel.width = 0.05
bevel.segments = 3
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5236

# AUTO SMOOTH
cubo.data.use_auto_smooth = True
cubo.data.auto_smooth_angle = 0.5236

# MATERIAL ROJO EXACTO (#FF0000)
mat = bpy.data.materials.new(name="Mat_Rojo_Puro")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    principled.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)  # ROJO PURO
    principled.inputs['Roughness'].default_value = 0.5
    principled.inputs['Specular'].default_value = 0.5
cubo.data.materials.append(mat)

# ILUMINACIÓN
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
key = bpy.context.active_object
key.name = "Key_Light"
key.data.energy = 5.0

bpy.ops.object.light_add(type='AREA', location=(-5, 2, 5))
fill = bpy.context.active_object
fill.name = "Fill_Light"
fill.data.energy = 2.0

# CÁMARA
bpy.ops.object.camera_add(location=(3, -3, 2.5))
cam = bpy.context.active_object
cam.name = "Camera"
direction = cubo.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# RENDER
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# GUARDAR
blend_path = './archivo_zuly/temp_arena/CUB001_v1.blend'
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

print("✅ Patrón generado y guardado en: " + blend_path)
'''

# Guardar y ejecutar script de generación
script_gen_path = Path('temp_generar_cubo.py')
with open(script_gen_path, 'w', encoding='utf-8') as f:
    f.write(script_generacion)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
result_gen = subprocess.run(
    [blender_exe, '--background', '--python', str(script_gen_path)],
    capture_output=True,
    text=True,
    cwd=r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
)

print(result_gen.stdout[-1500:] if len(result_gen.stdout) > 1500 else result_gen.stdout)
script_gen_path.unlink()

# ============================================================================
# PASO 3: JUES-BOT VALIDA EL PATRÓN
# ============================================================================
print("\n" + "="*70)
print("🤖 JUES-BOT: Iniciando inspección técnica...")
print("="*70)

script_validacion = '''
import bpy
import bmesh
import hashlib
from pathlib import Path

print("\\n" + "="*60)
print("JUES-BOT VALIDANDO: CUB-001_v1")
print("="*60)

blend_path = './archivo_zuly/temp_arena/CUB001_v1.blend'
target_color = '#FF0000'

bpy.ops.wm.open_mainfile(filepath=blend_path)

# Encontrar objeto
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break

# A. VISIÓN DE RAYOS X (Manifold)
dg = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(dg)
mesh_eval = obj_eval.data

bm = bmesh.new()
bm.from_mesh(mesh_eval)
wire_edges = sum(1 for e in bm.edges if len(e.link_faces) == 0)
non_manifold = sum(1 for e in bm.edges if len(e.link_faces) > 2)
bm.free()

malla_status = "LIMPIA" if wire_edges == 0 and non_manifold == 0 else "CORRUPTA"
print("   [A] Vision Rayos X: " + malla_status)

# B. INSTINTO DE OPTIMIZACIÓN (Peso)
path = Path(blend_path)
size_kb = round(path.stat().st_size / 1024, 2)
LIMITE = 2000
peso_status = "OPTIMO" if size_kb <= LIMITE else "GRASA"
print("   [B] Instinto Optimizacion: " + peso_status + " (" + str(size_kb) + " KB)")

# C. SINCRONÍA CROMÁTICA (Color)
mat = obj.data.materials[0]
principled = None
for node in mat.node_tree.nodes:
    if node.type == 'BSDF_PRINCIPLED':
        principled = node
        break

color = principled.inputs['Base Color'].default_value
r, g, b = int(color[0]*255), int(color[1]*255), int(color[2]*255)
hex_found = '#{:02X}{:02X}{:02X}'.format(r, g, b)
color_status = "MATCH" if hex_found == target_color else "NO_MATCH"
print("   [C] Sincronia Cromatica: " + color_status + " (" + hex_found + " vs " + target_color + ")")

# D. SELLO DE INMUTABILIDAD (Hash)
coords_str = ""
for v in mesh_eval.vertices:
    coords_str += "{:.3f},{:.3f},{:.3f};".format(v.co.x, v.co.y, v.co.z)
for poly in mesh_eval.polygons:
    verts = ",".join(str(v) for v in poly.vertices)
    coords_str += "[{}]".format(verts)

hash_md5 = hashlib.md5(coords_str.encode()).hexdigest()
print("   [D] Sello Inmutabilidad: " + hash_md5[:16] + "...")
print("       Vertices: " + str(len(mesh_eval.vertices)))

# CALCULAR PUNTUACIÓN
puntos = 0
if malla_status == "LIMPIA": puntos += 25
if peso_status == "OPTIMO": puntos += 25
if color_status == "MATCH": puntos += 25
puntos += 25  # Hash siempre cuenta

errores = 0
if malla_status == "CORRUPTA": errores += 1
if color_status == "NO_MATCH": errores += 1

dictamen = "APTO_PARA_SELLO" if errores == 0 else "NO_APTO"

# DASHBOARD
print("\\n" + "="*60)
print("DASHBOARD JUES-BOT - CUB-001_v1")
print("="*60)
print("   ESTADO DE MALLA:          [" + malla_status + "]")
print("   CONCORDANCIA DE COLOR:    [" + color_status + "]")
print("      └─ Color detectado: " + hex_found)
print("   PESO DE PATRÓN:           [" + str(size_kb) + " KB]")
print("   HASH DE INMUTABILIDAD:    [" + hash_md5[:16] + "...]")
print("      └─ Vértices: " + str(len(mesh_eval.vertices)))
print("="*60)
print("\\nDICTAMEN FINAL: " + dictamen)
print("Puntuacion: " + str(puntos) + "/100")
print("Errores: " + str(errores))
print("="*60)

# Guardar resultado
resultado = {
    "candidato_id": "CUB-001_v1",
    "puntuacion": puntos,
    "dictamen": dictamen,
    "errores": errores,
    "superpoderes": {
        "malla": {"status": malla_status, "wire": wire_edges, "non_manifold": non_manifold},
        "peso": {"status": peso_status, "kb": size_kb},
        "color": {"status": color_status, "encontrado": hex_found, "esperado": target_color},
        "hash": {"md5": hash_md5, "vertices": len(mesh_eval.vertices)}
    }
}

import json
with open('./archivo_zuly/temp_arena/JUES_RESULT_CUB001_v1.json', 'w') as f:
    json.dump(resultado, f, indent=2)

print("\\n✅ Validacion completa. Esperando decision del Soberano...")
'''

script_val_path = Path('temp_validar_cubo.py')
with open(script_val_path, 'w', encoding='utf-8') as f:
    f.write(script_validacion)

result_val = subprocess.run(
    [blender_exe, '--background', '--python', str(script_val_path)],
    capture_output=True,
    text=True,
    cwd=r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
)

print(result_val.stdout[-2000:] if len(result_val.stdout) > 2000 else result_val.stdout)
script_val_path.unlink()

# ============================================================================
# PASO 4: PRESENTAR AL SOBERANO
# ============================================================================
print("\n" + "="*70)
print("👑 SOBERANO: VISTO BUENO REQUERIDO")
print("="*70)

# Leer resultado
result_path = Path('archivo_zuly/temp_arena/JUES_RESULT_CUB001_v1.json')
if result_path.exists():
    with open(result_path, 'r') as f:
        resultado = json.load(f)
    
    print("\n📊 RESUMEN PARA DECISIÓN:")
    print("-"*70)
    print(f"   Patrón: {resultado['candidato_id']}")
    print(f"   Puntuación JUES: {resultado['puntuacion']}/100")
    print(f"   Dictamen: {resultado['dictamen']}")
    print(f"   Errores: {resultado['errores']}")
    print("-"*70)
    
    sp = resultado['superpoderes']
    print(f"\n   ✓ Malla: {sp['malla']['status']}")
    print(f"   ✓ Peso: {sp['peso']['status']} ({sp['peso']['kb']} KB)")
    print(f"   ✓ Color: {sp['color']['status']} ({sp['color']['encontrado']})")
    print(f"   ✓ Hash: {sp['hash']['md5'][:16]}...")
    
    print("\n" + "="*70)
    print("📝 ACCIONES DISPONIBLES:")
    print("="*70)
    print("   [S] SELLO     → Aprobar y archivar en mastered/")
    print("   [R] RECHAZO   → Descartar y bitacorar")
    print("   [C] CORREGIR  → Devolver para ajustes")
    print("="*70)
    print("\n💬 Tu decisión, Soberano? (S/R/C): ")
else:
    print("❌ Error: No se encontró resultado de validación")

print("\n🏁 FLUJO COMPLETO DEMONSTRADO")
print("   1. Usuario solicitó → 2. ZULY generó → 3. JUES validó → 4. Esperando sello")
