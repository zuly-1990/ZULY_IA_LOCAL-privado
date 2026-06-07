#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 PRUEBA REAL COMPLETA - ZULY + JUES + LYZU
Genera patrón real, valida, loguea, presenta resultados
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

print("="*70)
print("🧪 PRUEBA REAL - FLUJO COMPLETO ZULY + JUES + LYZU")
print("="*70)
print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

# PASO 1: ZULY genera patrón real en Blender
print("\n1️⃣  ZULY GENERANDO PATRÓN REAL...")

script_zuly = '''
import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')

print("="*60)
print("🤖 ZULY: Creando CUB-001 v2 (Prueba Real)")
print("="*60)

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear cubo con bisel profesional
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cubo = bpy.context.active_object
cubo.name = "CUB001_v2_PruebaReal"

# BEVEL profesional
bevel = cubo.modifiers.new(name="Bevel_Pro", type='BEVEL')
bevel.width = 0.08
bevel.segments = 4
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5236
bevel.miter_outer = 'MITER_ARC'

# Material azul profesional
mat = bpy.data.materials.new(name="Mat_Azul_Pro")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    # Azul corporativo
    principled.inputs['Base Color'].default_value = (0.1, 0.3, 0.8, 1.0)
    principled.inputs['Roughness'].default_value = 0.3
    principled.inputs['Specular'].default_value = 0.7
cubo.data.materials.append(mat)

# Iluminación profesional 3-point
# Key light
bpy.ops.object.light_add(type='AREA', location=(4, -4, 6))
key = bpy.context.active_object
key.name = "Key_Pro"
key.data.energy = 150
key.data.size = 3

# Fill light  
bpy.ops.object.light_add(type='AREA', location=(-4, 2, 4))
fill = bpy.context.active_object
fill.name = "Fill_Pro"
fill.data.energy = 80
fill.data.size = 2

# Rim light
bpy.ops.object.light_add(type='SPOT', location=(0, 4, 5))
rim = bpy.context.active_object
rim.name = "Rim_Pro"
rim.data.energy = 200

# Cámara profesional
bpy.ops.object.camera_add(location=(3.5, -3.5, 2.5))
cam = bpy.context.active_object
cam.name = "Camera_Pro"
direction = cubo.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# Render settings profesionales
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100

# Guardar
blend_path = './archivo_zuly/temp_arena/CUB001_v2_PruebaReal.blend'
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"✅ Guardado: {blend_path}")

# Info
print(f"   Vértices: {len(cubo.data.vertices)}")
print(f"   Caras: {len(cubo.data.polygons)}")
print(f"   Materiales: {len(cubo.data.materials)}")
print(f"   Modificadores: {len(cubo.modifiers)}")
'''

# Guardar y ejecutar script ZULY
script_path = zuly_path / 'temp_zuly_test.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_zuly)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
result_zuly = subprocess.run(
    [blender_exe, '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    cwd=str(zuly_path)
)

print(result_zuly.stdout[-1500:] if len(result_zuly.stdout) > 1500 else result_zuly.stdout)
if result_zuly.stderr and "Error" in result_zuly.stderr:
    print(f"⚠️  Errores: {result_zuly.stderr[-500:]}")

script_path.unlink()

# PASO 2: LYZU registra evento
print("\n2️⃣  LYZU REGISTRANDO EVENTO...")

lyzu_script = f'''
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from cerebro_lyzu import recordar_evento

hash_id = recordar_evento(
    entidad="ZULY",
    tipo="generacion",
    datos={{
        "pattern_id": "CUB001_v2_PruebaReal",
        "ubicacion": "./archivo_zuly/temp_arena/",
        "timestamp": "{datetime.now().isoformat()}",
        "caracteristicas": {{
            "tipo": "cubo_biselado",
            "color": "azul_profesional",
            "iluminacion": "3_point_profesional"
        }}
    }}
)
print(f"🧠 LYZU: Evento registrado - Hash {{hash_id}}")
'''

lyzu_path = zuly_path / 'temp_lyzu_log.py'
with open(lyzu_path, 'w', encoding='utf-8') as f:
    f.write(lyzu_script)

result_lyzu = subprocess.run(
    [sys.executable, str(lyzu_path)],
    capture_output=True,
    text=True,
    cwd=str(zuly_path)
)
print(result_lyzu.stdout)
lyzu_path.unlink()

# PASO 3: JUES-BOT valida
print("\n3️⃣  JUES-BOT VALIDANDO TÉCNICAMENTE...")

jues_script = '''
import bpy
import bmesh
import hashlib
import json
from pathlib import Path

print("="*60)
print("🤖 JUES-BOT: INSPECCIÓN TÉCNICA")
print("="*60)

blend_path = './archivo_zuly/temp_arena/CUB001_v2_PruebaReal.blend'
target_color = '#1A4DCC'  # Azul esperado

bpy.ops.wm.open_mainfile(filepath=blend_path)

# Encontrar objeto
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break

# A. Visión de Rayos X (Manifold)
dg = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(dg)
mesh_eval = obj_eval.data

bm = bmesh.new()
bm.from_mesh(mesh_eval)
wire_edges = sum(1 for e in bm.edges if len(e.link_faces) == 0)
non_manifold = sum(1 for e in bm.edges if len(e.link_faces) > 2)
bm.free()

malla_status = "LIMPIA" if wire_edges == 0 and non_manifold == 0 else "CORRUPTA"
print(f"   [A] Visión Rayos X: {malla_status}")

# B. Instinto Optimización
path = Path(blend_path)
size_kb = round(path.stat().st_size / 1024, 2)
LIMITE = 2000
peso_status = "OPTIMO" if size_kb <= LIMITE else "GRASA"
print(f"   [B] Instinto Optimización: {peso_status} ({size_kb} KB)")

# C. Sincronía Cromática
mat = obj.data.materials[0]
principled = None
for node in mat.node_tree.nodes:
    if node.type == 'BSDF_PRINCIPLED':
        principled = node
        break

color = principled.inputs['Base Color'].default_value
r, g, b = int(color[0]*255), int(color[1]*255), int(color[2]*255)
hex_found = '#{:02X}{:02X}{:02X}'.format(r, g, b)
color_status = "MATCH" if hex_found.upper() == target_color.upper() else f"NO_MATCH ({hex_found})"
print(f"   [C] Sincronía Cromática: {color_status}")

# D. Sello Inmutabilidad
coords_str = ""
for v in mesh_eval.vertices:
    coords_str += "{:.3f},{:.3f},{:.3f};".format(v.co.x, v.co.y, v.co.z)
for poly in mesh_eval.polygons:
    verts = ",".join(str(v) for v in poly.vertices)
    coords_str += "[{}]".format(verts)

hash_md5 = hashlib.md5(coords_str.encode()).hexdigest()
print(f"   [D] Sello Inmutabilidad: {hash_md5[:16]}...")
print(f"       Vértices: {len(mesh_eval.vertices)}")

# Puntuación
puntos = 0
if malla_status == "LIMPIA": puntos += 25
if peso_status == "OPTIMO": puntos += 25
if "MATCH" in color_status: puntos += 25
puntos += 25

errores = 0
if malla_status == "CORRUPTA": errores += 1
if "NO_MATCH" in color_status: errores += 1

dictamen = "APTO_PARA_SELLO" if errores == 0 else "NO_APTO"

print("="*60)
print(f"DASHBOARD JUES-BOT:")
print(f"   Malla: {malla_status}")
print(f"   Peso: {size_kb} KB [{peso_status}]")
print(f"   Color: {hex_found} [{color_status}]")
print(f"   Hash: {hash_md5[:16]}...")
print(f"   Vértices: {len(mesh_eval.vertices)}")
print("="*60)
print(f"Puntuación: {puntos}/100")
print(f"Dictamen: {dictamen}")
print(f"Errores: {errores}")
print("="*60)

# Guardar resultado
resultado = {
    "candidato_id": "CUB001_v2_PruebaReal",
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

with open('./archivo_zuly/temp_arena/JUES_RESULT_CUB001_v2.json', 'w') as f:
    json.dump(resultado, f, indent=2)

print("✅ Validación completa. Resultado guardado.")
'''

jues_path = zuly_path / 'temp_jues_val.py'
with open(jues_path, 'w', encoding='utf-8') as f:
    f.write(jues_script)

result_jues = subprocess.run(
    [blender_exe, '--background', '--python', str(jues_path)],
    capture_output=True,
    text=True,
    cwd=str(zuly_path)
)

print(result_jues.stdout[-2000:] if len(result_jues.stdout) > 2000 else result_jues.stdout)
jues_path.unlink()

# PASO 4: LYZU registra validación
print("\n4️⃣  LYZU REGISTRANDO VALIDACIÓN JUES...")

lyzu_script2 = f'''
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from cerebro_lyzu import recordar_evento

hash_id = recordar_evento(
    entidad="JUES-BOT",
    tipo="validacion",
    datos={{
        "pattern_id": "CUB001_v2_PruebaReal",
        "dictamen": "ver_resultado_json",
        "timestamp": "{datetime.now().isoformat()}"
    }}
)
print(f"🧠 LYZU: Validación registrada - Hash {{hash_id}}")
'''

lyzu_path2 = zuly_path / 'temp_lyzu_log2.py'
with open(lyzu_path2, 'w', encoding='utf-8') as f:
    f.write(lyzu_script2)

result_lyzu2 = subprocess.run(
    [sys.executable, str(lyzu_path2)],
    capture_output=True,
    text=True,
    cwd=str(zuly_path)
)
print(result_lyzu2.stdout)
lyzu_path2.unlink()

# PASO 5: Presentar resumen al usuario
print("\n" + "="*70)
print("📊 RESUMEN PARA REVISIÓN DEL SOBERANO")
print("="*70)

result_file = zuly_path / 'archivo_zuly/temp_arena/JUES_RESULT_CUB001_v2.json'
if result_file.exists():
    with open(result_file, 'r') as f:
        resultado = json.load(f)
    
    print(f"\n🎯 Patrón: CUB001_v2_PruebaReal")
    print(f"📍 Ubicación: archivo_zuly/temp_arena/CUB001_v2_PruebaReal.blend")
    print(f"\n🔍 Resultado JUES-BOT:")
    print(f"   Puntuación: {resultado['puntuacion']}/100")
    print(f"   Dictamen: {resultado['dictamen']}")
    print(f"   Errores: {resultado['errores']}")
    
    sp = resultado['superpoderes']
    print(f"\n   ✓ Malla: {sp['malla']['status']}")
    print(f"   ✓ Peso: {sp['peso']['kb']} KB [{sp['peso']['status']}]")
    print(f"   ✓ Color: {sp['color']['encontrado']} [{sp['color']['status']}]")
    print(f"   ✓ Hash: {sp['hash']['md5'][:16]}...")
    
    print("\n" + "="*70)
    print("📝 ACCIONES DISPONIBLES:")
    print("="*70)
    print("   [S] SELLO → Aprobar y mover a mastered/")
    print("   [R] RECHAZO → Descartar y bitacorar")
    print("   [C] CORREGIR → Devolver a ZULY")
    print("="*70)
    print("\n💬 Tu decisión, Soberano? (S/R/C)")
    print("   (Abre el .blend en Blender para revisar visualmente)")
    print("="*70)

print(f"\nFin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
