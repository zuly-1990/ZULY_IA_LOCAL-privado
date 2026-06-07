#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostracion JUES-BOT V1.0 - 3 Candidatos Arena
"""

import subprocess
import json
from pathlib import Path

script_blender = '''
import bpy
import bmesh
import hashlib
from pathlib import Path

def check_manifold(obj):
    if not obj or obj.type != 'MESH':
        return {"status": "CORRUPTA", "detalle": "No mesh"}
    
    # Aplicar modificadores temporales para validar geometría real
    dg = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(dg)
    mesh_eval = obj_eval.data
    
    # Contar vértices duplicados (indicador de no-manifold)
    bm = bmesh.new()
    bm.from_mesh(mesh_eval)
    bm.verts.ensure_lookup_table()
    
    # Verificar si hay bordes sin cara (wire edges)
    wire_edges = sum(1 for e in bm.edges if len(e.link_faces) == 0)
    
    # Verificar caras no-manifold (bordes con >2 caras)
    non_manifold = 0
    for e in bm.edges:
        if len(e.link_faces) > 2:
            non_manifold += 1
    
    bm.free()
    
    if wire_edges == 0 and non_manifold == 0:
        return {"status": "LIMPIA", "detalle": "Geometria manifold OK ({} verts, {} wire, {} non-manifold)".format(len(mesh_eval.vertices), wire_edges, non_manifold)}
    else:
        return {"status": "CORRUPTA", "detalle": "{} wire edges, {} non-manifold edges".format(wire_edges, non_manifold)}

def check_efficiency(path_str):
    path = Path(path_str)
    if not path.exists():
        return {"status": "ERROR", "peso_kb": 0}
    
    size_kb = round(path.stat().st_size / 1024, 2)
    # Umbral aumentado para archivos con escena completa (luces, cámaras, materiales)
    LIMITE_KB = 2000
    if size_kb > LIMITE_KB:
        return {"status": "GRASA", "peso_kb": size_kb, "alerta": "{}KB > {}KB".format(size_kb, LIMITE_KB)}
    else:
        return {"status": "OPTIMO", "peso_kb": size_kb}

def validate_color(obj, target_hex):
    if not obj or not obj.data.materials:
        return {"status": "NO_MATCH", "color_encontrado": None}
    
    mat = obj.data.materials[0]
    if not mat.use_nodes:
        return {"status": "NO_MATCH"}
    
    principled = None
    for node in mat.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled = node
            break
    
    if not principled:
        return {"status": "NO_MATCH"}
    
    color = principled.inputs['Base Color'].default_value
    r, g, b = int(color[0]*255), int(color[1]*255), int(color[2]*255)
    hex_found = '#{:02X}{:02X}{:02X}'.format(r, g, b)
    
    if hex_found.upper() == target_hex.upper():
        return {"status": "MATCH", "color_encontrado": hex_found}
    else:
        return {"status": "NO_MATCH", "color_encontrado": hex_found, "color_esperado": target_hex}

def generate_hash(obj):
    if not obj or obj.type != 'MESH':
        return {"hash": "ERROR", "vertices_count": 0}
    
    coords_str = ""
    for v in obj.data.vertices:
        coords_str += "{:.3f},{:.3f},{:.3f};".format(v.co.x, v.co.y, v.co.z)
    
    for poly in obj.data.polygons:
        verts = ",".join(str(v) for v in poly.vertices)
        coords_str += "[{}]".format(verts)
    
    hash_md5 = hashlib.md5(coords_str.encode()).hexdigest()
    return {"hash": hash_md5, "vertices_count": len(obj.data.vertices), "faces_count": len(obj.data.polygons)}

resultados = []

for blend_path, candidato_id, target_color in [
    ('./archivo_zuly/temp_arena/Candidato_A.blend', 'Candidato_A', '#F2F2F2'),
    ('./archivo_zuly/temp_arena/Candidato_B.blend', 'Candidato_B', '#999999'),
    ('./archivo_zuly/temp_arena/Candidato_C.blend', 'Candidato_C', '#CCD9E6')
]:
    print("\\n" + "="*60)
    print("JUES-BOT: " + candidato_id)
    print("="*60)
    
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    obj = None
    for o in bpy.context.scene.objects:
        if o.type == 'MESH':
            obj = o
            break
    
    manifold = check_manifold(obj)
    efficiency = check_efficiency(blend_path)
    color = validate_color(obj, target_color)
    hash_data = generate_hash(obj)
    
    print("   Malla: {}".format(manifold['status']))
    print("   Peso: {} KB".format(efficiency['peso_kb']))
    print("   Color: {} (esperado: {})".format(color.get('color_encontrado', 'N/A'), target_color))
    print("   Hash: {}...".format(hash_data['hash'][:16]))
    print("   Vertices: {}".format(hash_data['vertices_count']))
    
    puntos = 0
    if manifold['status'] == 'LIMPIA': puntos += 25
    if efficiency['status'] == 'OPTIMO': puntos += 25
    if color['status'] == 'MATCH': puntos += 25
    if hash_data['hash'] != 'ERROR': puntos += 25
    
    errores = 0
    if manifold['status'] == 'CORRUPTA': errores += 1
    if color['status'] == 'NO_MATCH': errores += 1
    
    dictamen = "APTO" if errores == 0 else "NO_APTO"
    
    print("\\n   Puntuacion: {}/100".format(puntos))
    print("   Dictamen: {}".format(dictamen))
    
    resultados.append({
        'candidato_id': candidato_id,
        'puntuacion': puntos,
        'dictamen': dictamen,
        'manifold': manifold,
        'efficiency': efficiency,
        'color': color,
        'hash': hash_data
    })

print("\\n" + "="*60)
print("RANKING FASE DE ARENA")
print("="*60)

ranking = sorted(resultados, key=lambda x: x['puntuacion'], reverse=True)
for i, r in enumerate(ranking, 1):
    medalla = "#1" if i == 1 else "#2" if i == 2 else "#3"
    print("   [{}] {}: {}/100 - {}".format(medalla, r['candidato_id'], r['puntuacion'], r['dictamen']))

print("\\nGanador recomendado: {}".format(ranking[0]['candidato_id']))
print("="*60)

import json
with open('./archivo_zuly/temp_arena/RESULTADO_ARENA.json', 'w') as f:
    json.dump({'ranking': ranking, 'ganador': ranking[0]}, f, indent=2)

print("\\nResultado guardado en: archivo_zuly/temp_arena/RESULTADO_ARENA.json")
'''

# Guardar y ejecutar
script_path = Path('temp_jues_demo.py')
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_blender)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
result = subprocess.run(
    [blender_exe, '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    cwd=r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
)

print("="*70)
print("JUES-BOT V1.0 - DEMOSTRACION FASE DE ARENA")
print("="*70)
print(result.stdout[-3500:] if len(result.stdout) > 3500 else result.stdout)
if result.stderr:
    print("\nErrores:", result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)

script_path.unlink()
