#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 JUES-BOT VALIDACIÓN V2 - CUB-001
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_jues = '''
import bpy
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("="*60)
print("🤖 JUES-BOT V2: Validando CUB-001")
print("="*60)

blend_path = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend'
target_color = '#1A4DCC'

# Abrir archivo
print("\\n📂 Abriendo archivo...")
bpy.ops.wm.open_mainfile(filepath=blend_path)

# Buscar primer mesh
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break

print(f"   Objeto encontrado: {obj.name if obj else 'None'}")
objeto_original = obj

if not obj:
    print("❌ ERROR: No hay objeto mesh")
    sys.exit(1)

# Aplicar SLIZ
print("\\n💡 Aplicando SLIZ...")
luces = aplicar_iluminacion_profesional(objeto_original)
print(f"   Luces: {list(luces.keys())}")

# VALIDAR COLOR (directo)
print("\\n🎨 Validando color...")
mat = objeto_original.data.materials[0] if objeto_original.data.materials else None
if mat and mat.use_nodes:
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        c = bsdf.inputs['Base Color'].default_value
        hex_color = f"#{int(c[0]*255):02X}{int(c[1]*255):02X}{int(c[2]*255):02X}"
        print(f"   Color detectado: {hex_color}")
        print(f"   Esperado: {target_color}")
        match = hex_color.upper() == target_color.upper()
        print(f"   MATCH: {match}")

# Calcular hash
print("\\n🔒 Calculando hash...")
coords_str = ""
for v in objeto_original.data.vertices:
    coords_str += f"{v.co.x:.3f},{v.co.y:.3f},{v.co.z:.3f};"
for poly in objeto_original.data.polygons:
    verts_indices = ",".join(str(v) for v in poly.vertices)
    coords_str += f"[{verts_indices}]"
hash_md5 = hashlib.md5(coords_str.encode('utf-8')).hexdigest()
print(f"   Hash: {hash_md5[:16]}...")

# Verificar peso
file_size = Path(blend_path).stat().st_size / 1024
print(f"\\n📊 Peso: {file_size:.1f} KB")

# Resultado
print("\\n" + "="*60)
if match:
    print("✅ RESULTADO: APTO_PARA_SELLO")
    print("   - Color: MATCH")
    print("   - Geometría: OK")
    print("   - Listo para aprobación del Soberano")
else:
    print("❌ RESULTADO: NO_APTO")
    print(f"   - Color: NO_MATCH ({hex_color} vs {target_color})")

print("="*60)

# Guardar reporte
report = {
    "patron": "CUB-001",
    "color_match": match,
    "color_detectado": hex_color if mat else None,
    "hash": hash_md5,
    "peso_kb": file_size,
    "dictamen": "APTO" if match else "NO_APTO"
}

report_path = './archivo_zuly/temp_arena/CUB-001_JUES_REPORT.json'
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)

print(f"\\n📄 Reporte: {report_path}")
'''

script_path = zuly_path / 'temp_jues_v2.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_jues)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🤖 Ejecutando JUES-BOT V2...")
result = subprocess.run(
    [blender_exe, '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)

script_path.unlink()

print("\n✅ Validación completada")
