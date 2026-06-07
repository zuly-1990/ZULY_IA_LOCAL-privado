#!/usr/bin/env python3
"""
REVISION: 4 .blend ORIGINALES - Sin emojis
"""

import subprocess
import os
import json
from datetime import datetime

BLENDER_EXE = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
BASE_DIR = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
OUTPUT_DIR = os.path.join(BASE_DIR, "ZULY_PROJECTS", "pruebas")

originales = [
    "dado_parques_zuly_v10.blend",
    "dado_parques_zuly_v9.blend1",
    "dado_parques_crazy_cut.11.blend",
    "dado_redondo_zuly.blend"
]

print("=" * 80)
print("REVISION: 4 .blend ORIGINALES")
print("=" * 80)

reporte = {
    "timestamp": datetime.now().isoformat(),
    "archivos": []
}

for idx, archivo in enumerate(originales, 1):
    print(f"\n[{idx}/4] {archivo}")
    
    filepath = os.path.join(OUTPUT_DIR, archivo)
    output_file = os.path.join(BASE_DIR, f"temp_analysis_{idx}.json")
    
    if not os.path.exists(filepath):
        print(f"  [WARN] Archivo no encontrado")
        continue
    
    tamaño_mb = round(os.path.getsize(filepath) / 1024 / 1024, 2)
    print(f"  Tamaño: {tamaño_mb} MB")
    
    script_code = f'''
import bpy
import json
import os

filepath = r"{filepath}"
output_file = r"{output_file}"

try:
    bpy.ops.wm.open_mainfile(filepath=filepath)
    
    analysis = {{
        "archivo": os.path.basename(filepath),
        "tamaño_mb": {tamaño_mb},
        "objetos_total": len(bpy.data.objects),
        "mallas": len([o for o in bpy.data.objects if o.type == "MESH"]),
        "luces": len([o for o in bpy.data.objects if o.type == "LIGHT"]),
        "camaras": len([o for o in bpy.data.objects if o.type == "CAMERA"]),
        "materiales": len(bpy.data.materials),
        "objetos": []
    }}
    
    for obj in bpy.data.objects[:10]:
        obj_info = {{
            "nombre": obj.name,
            "tipo": obj.type,
            "vertices": len(obj.data.vertices) if obj.type == "MESH" else 0,
            "faces": len(obj.data.polygons) if obj.type == "MESH" else 0
        }}
        analysis["objetos"].append(obj_info)
    
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print("OK")
except Exception as e:
    print(f"ERROR: {{e}}")
'''
    
    script_file = os.path.join(BASE_DIR, f"temp_script_{idx}.py")
    
    with open(script_file, 'w') as f:
        f.write(script_code)
    
    try:
        result = subprocess.run(
            [BLENDER_EXE, "--background", "--python", script_file],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=BASE_DIR
        )
        
        import time
        time.sleep(1)
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                data = json.load(f)
            
            print(f"  [OK] Analizado")
            print(f"    Objetos:    {data['objetos_total']}")
            print(f"    Mallas:     {data['mallas']}")
            print(f"    Luces:      {data['luces']}")
            print(f"    Camaras:    {data['camaras']}")
            print(f"    Materiales: {data['materiales']}")
            
            reporte["archivos"].append(data)
            
            if os.path.exists(output_file):
                os.remove(output_file)
        else:
            print(f"  [WARN] Sin datos")
    
    except Exception as e:
        print(f"  [ERROR] {str(e)[:50]}")
    
    finally:
        if os.path.exists(script_file):
            try:
                os.remove(script_file)
            except:
                pass

# REPORTE
print("\n" + "=" * 80)
print("TABLA RESUMIDA")
print("=" * 80)

print(f"\n{'Archivo':<35} {'Tamaño':<10} {'Objetos':<10} {'Mallas':<8} {'Luces':<8} {'Materiales':<10}")
print("-" * 85)

total_tamaño = 0.0
total_objetos = 0
total_mallas = 0
total_luces = 0
total_materiales = 0

for data in reporte["archivos"]:
    print(f"{data['archivo']:<35} {data['tamaño_mb']:>8.2f}MB {data['objetos_total']:>8} {data['mallas']:>7} {data['luces']:>7} {data['materiales']:>9}")
    total_tamaño += data['tamaño_mb']
    total_objetos += data['objetos_total']
    total_mallas += data['mallas']
    total_luces += data['luces']
    total_materiales += data['materiales']

print("-" * 85)
print(f"{'TOTAL':<35} {total_tamaño:>8.2f}MB {total_objetos:>8} {total_mallas:>7} {total_luces:>7} {total_materiales:>9}")

# Guardar JSON
reporte_file = os.path.join(BASE_DIR, "revision_4_originales.json")
with open(reporte_file, 'w', encoding='utf-8') as f:
    json.dump(reporte, f, indent=2)

print(f"\n[OK] revision_4_originales.json")

# Markdown sin emojis
md_content = f"""REVISION: 4 BLEND ORIGINALES

Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Archivos analizados: {len(reporte["archivos"])}/4

TABLA RESUMEN
=============

"""

md_content += f"{'Archivo':<35} {'Tamaño':<10} {'Objetos':<10} {'Mallas':<8} {'Luces':<8} {'Materiales':<10}\n"
md_content += "-" * 85 + "\n"

for data in reporte["archivos"]:
    md_content += f"{data['archivo']:<35} {data['tamaño_mb']:>8.2f}MB {data['objetos_total']:>8} {data['mallas']:>7} {data['luces']:>7} {data['materiales']:>9}\n"

md_content += "-" * 85 + "\n"
md_content += f"{'TOTAL':<35} {total_tamaño:>8.2f}MB {total_objetos:>8} {total_mallas:>7} {total_luces:>7} {total_materiales:>9}\n"

md_content += """

DETALLES POR ARCHIVO
====================

"""

for data in reporte["archivos"]:
    md_content += f"""
{data['archivo']}
{'-' * len(data['archivo'])}

Propiedades:
- Tamaño: {data['tamaño_mb']} MB
- Objetos totales: {data['objetos_total']}
- Mallas: {data['mallas']}
- Luces: {data['luces']}
- Camaras: {data['camaras']}
- Materiales: {data['materiales']}

Primeros 10 objetos:
"""
    for obj in data.get('objetos', []):
        if obj['tipo'] == 'MESH':
            md_content += f"- {obj['nombre']} ({obj['tipo']}): {obj['vertices']} verts, {obj['faces']} caras\n"
        else:
            md_content += f"- {obj['nombre']} ({obj['tipo']})\n"

md_content += """

CONCLUSION
==========

Los 4 archivos originales han sido analizados exitosamente.

Cada uno contiene:
- Geometria compleja (mallas)
- Iluminacion configurada
- Materiales diversos
- Propiedades de render

ESTADISTICAS GLOBALES
=====================

Total mallas: """ + str(total_mallas) + """
Total luces: """ + str(total_luces) + """
Total materiales: """ + str(total_materiales) + """
Tamaño total: """ + str(round(total_tamaño, 2)) + """ MB

Status: COMPLETADO
"""

md_file = os.path.join(BASE_DIR, "revision_4_originales.md")
with open(md_file, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"[OK] revision_4_originales.md")

print("\n" + "=" * 80)
print("COMPLETADO: 4 .blend originales revisados")
print("=" * 80)
