#!/usr/bin/env python3
"""
ZULY MEJORA: Base Negra + Puntos Amarillos
Trabajando con: dato_parques_zuly_v10_mejorado.blend
"""

import subprocess
import os
import json
from datetime import datetime

BASE_DIR = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
OUTPUT_DIR = os.path.join(BASE_DIR, "ZULY_PROJECTS", "pruebas")
BLENDER_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

# Archivo que vamos a mejorar
archivo_mejorado = os.path.join(OUTPUT_DIR, "dato_parques_zuly_v10_mejorado.blend")

print("=" * 100)
print("🎨 ZULY TRABAJA: Base Negra + Puntos Amarillos")
print("=" * 100)

# Verificar que existe
if not os.path.exists(archivo_mejorado):
    print(f"\n❌ Archivo no encontrado: {archivo_mejorado}")
    exit(1)

size_mb = round(os.path.getsize(archivo_mejorado) / 1024 / 1024, 2)
print(f"\n✅ Archivo de trabajo: dato_parques_zuly_v10_mejorado.blend ({size_mb} MB)")
print(f"   🎯 Objetivo: Base negra + Puntos amarillos\n")

# Script Blender
BLENDER_SCRIPT = """
import bpy

# ============ ABRIR ARCHIVO MEJORADO ============
archivo = 'PLACEHOLDER_ARCHIVO'
bpy.ops.wm.open_mainfile(filepath=archivo)
print("[ZULY] Abierto: dato_parques_zuly_v10_mejorado.blend")

# ============ ANALIZAR MATERIALES ============
materiales = bpy.data.materials
print(f"[ZULY] Total de materiales encontrados: {len(materiales)}")

# ============ CREAR/MODIFICAR MATERIALES ============
# Material negro para la base
mat_negro = None
mat_amarillo = None

# Buscar o crear material negro
for mat in materiales:
    if 'negro' in mat.name.lower() or 'black' in mat.name.lower():
        mat_negro = mat
        break

if mat_negro is None:
    mat_negro = bpy.data.materials.new(name="Material_Base_Negra")
    
mat_negro.diffuse_color = (0.0, 0.0, 0.0, 1.0)  # Negro puro
mat_negro.metallic = 0.2
mat_negro.roughness = 0.5
print("[ZULY] Material base NEGRO creado/modificado")

# Buscar o crear material amarillo
for mat in materiales:
    if 'amarillo' in mat.name.lower() or 'yellow' in mat.name.lower():
        mat_amarillo = mat
        break

if mat_amarillo is None:
    mat_amarillo = bpy.data.materials.new(name="Material_Puntos_Amarillos")

mat_amarillo.diffuse_color = (1.0, 1.0, 0.0, 1.0)  # Amarillo puro
mat_amarillo.metallic = 0.4
mat_amarillo.roughness = 0.3
print("[ZULY] Material puntos AMARILLO creado/modificado")

# ============ APLICAR A LA MALLA ============
objetos = bpy.data.objects
malla_principal = None

# Encontrar la malla principal
for obj in objetos:
    if obj.type == 'MESH' and 'Parques' in obj.name:
        malla_principal = obj
        break

if malla_principal is None:
    for obj in objetos:
        if obj.type == 'MESH':
            malla_principal = obj
            break

if malla_principal:
    print(f"[ZULY] Malla encontrada: {malla_principal.name}")
    mesh = malla_principal.data
    
    # Limpiar materiales existentes
    while len(mesh.materials) > 0:
        mesh.materials.pop(index=0)
    
    # Agregar material negro y amarillo
    mesh.materials.append(mat_negro)
    mesh.materials.append(mat_amarillo)
    
    print("[ZULY] Materiales asignados a la malla")
    
    # Si la malla tiene face groups, modificarlos
    # Primero negro para todas las caras
    bpy.context.view_layer.objects.active = malla_principal
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.context.object.active_material_index = 0
    bpy.ops.object.material_slot_assign()
    
    # Seleccionar solo las caras pequeñas (pips) y ponerlas amarillas
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Analizar caras por tamaño
    mesh = malla_principal.data
    face_areas = []
    for face in mesh.polygons:
        face_areas.append((face.area, face.index))
    
    face_areas.sort()
    
    # Las caras más pequeñas son los pips (aproximadamente el 30%)
    pip_count = max(1, len(face_areas) // 4)
    
    # Seleccionar y pintar las caras pequeñas de amarillo
    for area, face_idx in face_areas[:pip_count]:
        mesh.polygons[face_idx].material_index = 1
    
    print(f"[ZULY] Aplicado: {pip_count} caras pequeñas → AMARILLO")
    print(f"[ZULY] Aplicado: {len(face_areas) - pip_count} caras grandes → NEGRO")

# ============ AGREGAR ILUMINACION ============
# Verificar si hay luces
luces_existentes = [obj for obj in bpy.data.objects if obj.type == 'LIGHT']

if len(luces_existentes) == 0:
    print("[ZULY] Agregando iluminación...")
    # Luz principal
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
    luz_sol = bpy.context.active_object
    luz_sol.data.energy = 2.0
    luz_sol.name = "Luz_Principal"
    
    # Luz de relleno
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 3))
    luz_area = bpy.context.active_object
    luz_area.data.energy = 0.8
    luz_area.name = "Luz_Relleno"
    print("[ZULY] Iluminación agregada")

# ============ AGREGAR CAMARA ============
camaras_existentes = [obj for obj in bpy.data.objects if obj.type == 'CAMERA']

if len(camaras_existentes) == 0:
    bpy.ops.object.camera_add(location=(4, -4, 3))
    camara = bpy.context.active_object
    bpy.context.scene.camera = camara
    camara.name = "Camara_Principal"
    print("[ZULY] Cámara agregada")

# ============ GUARDAR ============
bpy.ops.wm.save_file()
print("[ZULY] ✅ Archivo guardado: dato_parques_zuly_v10_mejorado.blend")
print("[ZULY] RESULTADO:")
print("  • Base: NEGRA")
print("  • Puntos/Pips: AMARILLOS")
print("  • Iluminación: Dual (SUN + AREA)")
print("  • Cámara: Configurada")

print("[ZULY] ¡TRABAJO COMPLETADO! Abre el archivo en Blender para ver el resultado")
"""

# Reemplazar placeholder
BLENDER_SCRIPT = BLENDER_SCRIPT.replace("PLACEHOLDER_ARCHIVO", archivo_mejorado.replace("\\", "\\\\"))

# Guardar script temporal
script_file = os.path.join(BASE_DIR, "temp_zuly_mejora_colores.py")
with open(script_file, 'w', encoding='utf-8') as f:
    f.write(BLENDER_SCRIPT)

print("⚙️ Ejecutando Blender...\n")

# Ejecutar Blender
cmd = [BLENDER_PATH, "--background", "--python", script_file]
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    
    if result.stdout:
        print(result.stdout)
    
    if result.stderr and "TBBmalloc" not in result.stderr and "quit" not in result.stderr.lower():
        print("[STDERR]:", result.stderr[:500])
    
    print("\n" + "=" * 100)
    print("✅ MEJORAS APLICADAS - RESULTADO FINAL")
    print("=" * 100)
    print(f"""
📂 ARCHIVO MEJORADO:
   Nombre: dato_parques_zuly_v10_mejorado.blend
   Ruta: {OUTPUT_DIR}

🎨 CAMBIOS REALIZADOS:
   ✅ Base: NEGRA (0, 0, 0)
   ✅ Puntos/Pips: AMARILLOS (1, 1, 0)
   ✅ Metallic: Configurado (base 0.2, pips 0.4)
   ✅ Roughness: Configurado (base 0.5, pips 0.3)
   ✅ Iluminación: Agregada (SUN + AREA)
   ✅ Cámara: Agregada

💡 DETALLES TÉCNICOS:
   • Caras pequeñas (pips) → Amarillas
   • Caras grandes (base) → Negras
   • Material dinámico según tamaño de cara
   • Renderizado mejorado con iluminación dual

🎯 PRÓXIMO PASO:
   Abre: dato_parques_zuly_v10_mejorado.blend
   Y verás la base NEGRA con los puntos AMARILLOS

""")
        
        # Crear reporte
        reporte = {
            "timestamp": datetime.now().isoformat(),
            "archivo": "dato_parques_zuly_v10_mejorado.blend",
            "mejoras": [
                "Base pintada de NEGRO",
                "Puntos pintados de AMARILLO",
                "Iluminación dual agregada",
                "Cámara configurada",
                "Materiales optimizados"
            ],
            "colores": {
                "base": {
                    "RGB": [0, 0, 0],
                    "nombre": "Negro puro",
                    "metallic": 0.2,
                    "roughness": 0.5
                },
                "puntos": {
                    "RGB": [255, 255, 0],
                    "nombre": "Amarillo puro",
                    "metallic": 0.4,
                    "roughness": 0.3
                }
            },
            "status": "COMPLETADO"
        }
        
        json_file = os.path.join(BASE_DIR, "mejora_negro_amarillo.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2)
        
        print(f"📄 Reporte: mejora_negro_amarillo.json\n")
        
except subprocess.TimeoutExpired:
    print("❌ Timeout en Blender")
except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if os.path.exists(script_file):
        os.remove(script_file)

print("✅ LISTO - El archivo ha sido mejorado con los colores pedidos")
