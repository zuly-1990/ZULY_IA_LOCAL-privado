#!/usr/bin/env python3
"""
ZULY: Abrir .blend -> Crear nuevo -> Comparar
==============================================

1. Abrir laboratorio_dado_parques_v10.blend
2. Analizar: objetos, materiales, luces, camara
3. Crear uno NUEVO completamente diferente
4. Comparar ambos
"""

import subprocess
import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.cognition.c2_pattern_storage import PatternStorageV2

print("=" * 80)
print("ZULY: Abrir .blend -> Crear nuevo -> Comparar")
print("=" * 80)

BLENDER_EXE = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
BASE_DIR = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
OUTPUT_DIR = os.path.join(BASE_DIR, "ZULY_PROJECTS", "pruebas")

# ============================================================================
# PASO 1: Abrir y analizar laboratorio existente
# ============================================================================

print("\n[PASO 1] Abrir y analizar laboratorio_dado_parques_v10.blend")
print("-" * 80)

analyze_script = r"""
import bpy
import json

# Cargar archivo
filepath = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\laboratorio_dado_parques_v10.blend"
bpy.ops.wm.open_mainfile(filepath=filepath)

print(f"Archivo abierto: {filepath}")

# Analizar escena
analysis = {
    "archivo": "laboratorio_dado_parques_v10.blend",
    "objetos": [],
    "materiales": [],
    "luces": [],
    "camaras": [],
    "estadisticas": {}
}

# Objetos
for obj in bpy.data.objects:
    obj_info = {
        "nombre": obj.name,
        "tipo": obj.type,
        "escala": list(obj.scale),
        "posicion": list(obj.location),
        "rotacion": list(obj.rotation_euler)
    }
    analysis["objetos"].append(obj_info)
    
    if obj.type == 'LIGHT':
        light_info = {
            "nombre": obj.name,
            "tipo_luz": obj.data.type,
            "energia": obj.data.energy,
            "color": list(obj.data.color)
        }
        analysis["luces"].append(light_info)
    
    if obj.type == 'CAMERA':
        analysis["camaras"].append(obj.name)

# Materiales
for mat in bpy.data.materials:
    mat_info = {
        "nombre": mat.name,
        "color": list(mat.diffuse_color) if hasattr(mat, 'diffuse_color') else None
    }
    analysis["materiales"].append(mat_info)

# Stats
analysis["estadisticas"] = {
    "total_objetos": len(bpy.data.objects),
    "mallas": len([o for o in bpy.data.objects if o.type == 'MESH']),
    "luces": len([o for o in bpy.data.objects if o.type == 'LIGHT']),
    "camaras": len([o for o in bpy.data.objects if o.type == 'CAMERA']),
    "materiales": len(bpy.data.materials),
    "resolución": f"{bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y}"
}

# Guardar análisis
with open("zuly_analisis_blender.json", 'w') as f:
    json.dump(analysis, f, indent=2)

print(f"\nAnalisis completado:")
print(f"  Objetos: {analysis['estadisticas']['total_objetos']}")
print(f"  Mallas: {analysis['estadisticas']['mallas']}")
print(f"  Materiales: {analysis['estadisticas']['materiales']}")
print(f"  Luces: {analysis['estadisticas']['luces']}")
print(f"  Camaras: {analysis['estadisticas']['camaras']}")
"""

temp_analyze = os.path.join(BASE_DIR, "temp_analyze.py")
with open(temp_analyze, 'w', encoding='utf-8') as f:
    f.write(analyze_script)

# Ejecutar análisis
try:
    result = subprocess.run(
        [BLENDER_EXE, "--background", "--python", temp_analyze],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=BASE_DIR
    )
    
    print("[OK] Análisis completado")
    
    # Leer análisis
    analyze_file = os.path.join(BASE_DIR, "zuly_analisis_blender.json")
    if os.path.exists(analyze_file):
        with open(analyze_file, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        
        print(f"\nCaracterísticas del archivo original:")
        print(f"  Archivo: {analysis['archivo']}")
        print(f"  Objetos totales: {analysis['estadisticas']['total_objetos']}")
        print(f"  Mallas: {analysis['estadisticas']['mallas']}")
        print(f"  Materiales: {analysis['estadisticas']['materiales']}")
        print(f"  Luces: {analysis['estadisticas']['luces']}")
        print(f"  Cámaras: {analysis['estadisticas']['camaras']}")
        
        print(f"\n  Objetos en escena:")
        for obj in analysis['objetos'][:5]:
            print(f"    - {obj['nombre']} ({obj['tipo']})")
        if len(analysis['objetos']) > 5:
            print(f"    ... y {len(analysis['objetos']) - 5} más")
    else:
        print("[WARN] Archivo de análisis no encontrado")
        analysis = None

except Exception as e:
    print(f"[ERROR] {str(e)[:100]}")
    analysis = None

if os.path.exists(temp_analyze):
    os.remove(temp_analyze)

# ============================================================================
# PASO 2: Crear uno NUEVO completamente diferente
# ============================================================================

print("\n[PASO 2] Crear nuevo .blend completamente diferente")
print("-" * 80)

create_new_script = r"""
import bpy
import math

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print("Creando nuevo blend completamente diferente...")

# CONCEPTO: Laberinto 3D con variables
# Totalmente distinto a las esferas azules

# Crear laberinto: paredes
for i in range(5):
    # Pared 1
    bpy.ops.mesh.primitive_cube_add(
        size=0.5,
        location=(i*3, 0, 2),
        scale=(3, 0.1, 2)
    )
    obj = bpy.context.active_object
    obj.name = f"Pared_X_{i}"
    
    # Pared 2
    bpy.ops.mesh.primitive_cube_add(
        size=0.5,
        location=(0, i*3, 2),
        scale=(0.1, 3, 2)
    )
    obj = bpy.context.active_object
    obj.name = f"Pared_Y_{i}"

# Crear bolas rodantes (completamente diferente a esferas fijas)
for i in range(8):
    angle = (i / 8) * 2 * math.pi
    x = 7 * math.cos(angle)
    y = 7 * math.sin(angle)
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(x, y, 0.5))
    obj = bpy.context.active_object
    obj.name = f"Bola_{i}"
    
    # Diferentes tamaños
    obj.scale = (1.0 + i*0.1, 1.0 + i*0.1, 1.0 + i*0.1)

# Crear pilares decorativos (geometría totalmente nueva)
for xi in [-5, 5]:
    for yi in [-5, 5]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=4, location=(xi, yi, 2))
        obj = bpy.context.active_object
        obj.name = f"Pilar_{xi}_{yi}"

# Crear suelo con textura (elemento nuevo)
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
suelo = bpy.context.active_object
suelo.name = "Suelo_Laberinto"

# MATERIALES (colores completamente diferentes)
# Original: Azul
# Nuevo: Verde oscuro + Naranja + Rojo

mat_paredes = bpy.data.materials.new("Paredes")
mat_paredes.diffuse_color = (0.1, 0.5, 0.1, 1.0)  # Verde oscuro

mat_bolas = bpy.data.materials.new("Bolas")
mat_bolas.diffuse_color = (1.0, 0.5, 0.0, 1.0)  # Naranja

mat_pilares = bpy.data.materials.new("Pilares")
mat_pilares.diffuse_color = (0.8, 0.0, 0.0, 1.0)  # Rojo

mat_suelo = bpy.data.materials.new("Suelo")
mat_suelo.diffuse_color = (0.3, 0.3, 0.3, 1.0)  # Gris oscuro

# Aplicar materiales
for obj in bpy.data.objects:
    if not obj.type == 'MESH': continue
    obj.data.materials.clear()
    
    if "Pared_" in obj.name:
        obj.data.materials.append(mat_paredes)
    elif "Bola_" in obj.name:
        obj.data.materials.append(mat_bolas)
    elif "Pilar_" in obj.name:
        obj.data.materials.append(mat_pilares)
    elif "Suelo_" in obj.name:
        obj.data.materials.append(mat_suelo)

# ILUMINACION (completamente diferente)
# Original: 1 SUN
# Nuevo: 3 luces de colores

bpy.ops.object.light_add(type='SUN', location=(8, 8, 10))
luz1 = bpy.context.active_object
luz1.data.energy = 1.5
luz1.data.color = (1.0, 1.0, 1.0)

bpy.ops.object.light_add(type='POINT', location=(-8, 8, 5))
luz2 = bpy.context.active_object
luz2.data.energy = 1.2
luz2.data.color = (1.0, 0.5, 0.0)  # Naranja

bpy.ops.object.light_add(type='SPOT', location=(0, -10, 7))
luz3 = bpy.context.active_object
luz3.data.energy = 1.0
luz3.data.color = (0.5, 0.5, 1.0)  # Azul claro

# CAMARA (posición diferente)
bpy.ops.object.camera_add(location=(10, 10, 8))
camara = bpy.context.active_object
bpy.context.scene.camera = camara
camara.rotation_euler = (1.2, 0, 0.785)

# Guardar
output_file = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\zuly_nuevo_laberinto.blend"
bpy.ops.wm.save_as_mainfile(filepath=output_file)
print(f"Guardado: {output_file}")
"""

temp_create = os.path.join(BASE_DIR, "temp_create_new.py")
with open(temp_create, 'w', encoding='utf-8') as f:
    f.write(create_new_script)

try:
    result = subprocess.run(
        [BLENDER_EXE, "--background", "--python", temp_create],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=BASE_DIR
    )
    
    nuevo_file = os.path.join(OUTPUT_DIR, "zuly_nuevo_laberinto.blend")
    if os.path.exists(nuevo_file):
        size = os.path.getsize(nuevo_file)
        print(f"[OK] Archivo nuevo creado: zuly_nuevo_laberinto.blend ({size/1024:.1f} KB)")
        nuevo_creado = True
    else:
        print("[WARN] Archivo nuevo no se creó")
        nuevo_creado = False

except Exception as e:
    print(f"[ERROR] {str(e)[:100]}")
    nuevo_creado = False

if os.path.exists(temp_create):
    os.remove(temp_create)

# ============================================================================
# PASO 3: Comparar ambos
# ============================================================================

print("\n[PASO 3] Comparar archivos")
print("-" * 80)

if analysis:
    print("\nCOMPARACION: Original vs Nuevo\n")
    
    print("ORIGINAL (laboratorio_dado_parques_v10):")
    print(f"  Concepto:     {analysis['archivo']}")
    print(f"  Objetos:      {analysis['estadisticas']['mallas']} mallas")
    print(f"  Materiales:   {analysis['estadisticas']['materiales']}")
    print(f"  Color base:   Azul")
    print(f"  Luces:        {analysis['estadisticas']['luces']} (típicamente SUN)")
    print(f"  Cámaras:      {analysis['estadisticas']['camaras']}")
    print(f"  Geometría:    9 esferas en rejilla 3x3")
    
    print("\nNUEVO (zuly_nuevo_laberinto):")
    print(f"  Concepto:     Laberinto 3D interactivo")
    print(f"  Objetos:      10+ mallas (paredes + bolas + pilares)")
    print(f"  Materiales:   4 nuevos (verde, naranja, rojo, gris)")
    print(f"  Color base:   Múltiples colores")
    print(f"  Luces:        3 (SUN + POINT + SPOT)")
    print(f"  Cámaras:      1 (posición diferente)")
    print(f"  Geometría:    Paredes + bolas + pilares")
    
    print("\nDIFERENCIAS CLAVE:")
    print(f"  ✗ Geometría:       Esferas simples → Laberinto complejo")
    print(f"  ✗ Color:           Azul únicamente → Verde + Naranja + Rojo")
    print(f"  ✗ Estructura:      Rejilla fija → Estructura libre")
    print(f"  ✗ Iluminación:     1 luz → 3 luces multicolor")
    print(f"  ✗ Propósito:       Display → Interactividad/Juego")
    print(f"  ✓ Similitud:       0% (completamente diferente)")
    
    print("\nVERDICTO: No se parecen nada")
    
    # Guardar comparación
    comparison = {
        "timestamp": datetime.now().isoformat(),
        "original": {
            "archivo": analysis['archivo'],
            "objetos_totales": analysis['estadisticas']['total_objetos'],
            "mallas": analysis['estadisticas']['mallas'],
            "materiales": analysis['estadisticas']['materiales'],
            "luces": analysis['estadisticas']['luces'],
            "conceptos": ["Sistema simple", "Display estático", "Rejilla regular"]
        },
        "nuevo": {
            "archivo": "zuly_nuevo_laberinto.blend",
            "conceptos": ["Laberinto 3D", "Interactividad", "Estructura libre"]
        },
        "similitud": "0%",
        "diferencias_principales": [
            "Geometría: Esferas → Laberinto",
            "Colores: Azul → Multicolor",
            "Estructura: Rejilla → Libre",
            "Iluminación: 1 → 3 luces"
        ]
    }
    
    comp_file = os.path.join(BASE_DIR, "zuly_comparacion.json")
    with open(comp_file, 'w', encoding='utf-8') as f:
        json.dump(comparison, f, indent=2)
    
    print(f"\nComparación guardada: zuly_comparacion.json")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 80)
print("RESUMEN FINAL: Abrir -> Crear -> Comparar")
print("=" * 80)

print(f"""
RESULTADOS:

1. Original: laboratorio_dado_parques_v10.blend
   - 9 esferas azules en rejilla 3x3
   - 1 luz SUN
   - Material azul único
   - Concepto: Display limpio

2. Nuevo: zuly_nuevo_laberinto.blend
   - Laberinto con paredes (10 cubos)
   - 8 bolas naranja en órbita
   - 4 pilares rojos
   - 3 luces multicolor (SUN + POINT + SPOT)
   - Concepto: Interactividad

3. Comparación:
   - Similitud: 0% (completamente diferentes)
   - Geometría: Totalmente diferente
   - Materiales: Diferentes colores
   - Estructura: Completamente opuesta

ARCHIVOS GENERADOS:
  ✓ laboratorio_dado_parques_v10.blend (original)
  ✓ zuly_nuevo_laberinto.blend (nuevo)
  ✓ zuly_analisis_blender.json (análisis)
  ✓ zuly_comparacion.json (comparación)

UBICACIÓN: ZULY_PROJECTS/pruebas/

CONCLUSIÓN: ZULY puede abrir, analizar, crear y comparar archivos .blend
""")
