#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 ZULY MAESTRO - Combinar los 27 patrones en un solo .blend
Grid organizado 5x6 con todos los patrones sellados
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_maestro = '''
import bpy
import sys
from pathlib import Path
import mathutils

print("="*70)
print("🏆 ZULY MAESTRO - Creando escena con 27 patrones")
print("="*70)

# Limpiar todo
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Eliminar luces y cámaras existentes
for obj in bpy.data.objects:
    if obj.type in ['LIGHT', 'CAMERA']:
        bpy.data.objects.remove(obj, do_unlink=True)

# Lista de patrones y sus posiciones en grid (x, y)
# Grid de 5 columnas x 6 filas, espaciado 5m
patrones = [
    # Fila 1: CUB avanzados
    ("CUB-001_Modelado_BiselRealista", 0, 0),
    ("CUB-002_Transform_PivoteSuelo", 5, 0),
    ("CUB-003_Modelado_MuroPro", 10, 0),
    ("CUB-004-HIBRIDO_Prueba", 15, 0),
    ("CUB-005_BooleanExacto", 20, 0),
    
    # Fila 2: P-001 cubos básicos
    ("P-001A_CuboBasico_1m", 0, -5),
    ("P-001B_CuboBasico_2m", 5, -5),
    ("P-001C_CuboBasico_05m", 10, -5),
    ("P-001D_CuboBasico_3m", 15, -5),
    
    # Fila 3: P-002 esferas (5 esferas)
    ("P-002A_EsferaUV_1m", 0, -10),
    ("P-002B_EsferaUV_2m", 5, -10),
    ("P-002C_EsferaICO_1m", 10, -10),
    ("P-002D_EsferaICO_05m", 15, -10),
    ("P-002E_EsferaUV_05m", 20, -10),
    
    # Fila 4: P-003 spheres + P-004 cilindros
    ("P-003A_SphereAltaRes", 0, -15),
    ("P-003B_SphereBajaRes", 5, -15),
    ("P-003C_SphereMini", 10, -15),
    ("P-004A_CilindroAlto", 15, -15),
    ("P-004B_CilindroAncho", 20, -15),
    
    # Fila 5: P-005 conos + P-006 plano + MAT materiales
    ("P-005A_ConoAlto", 0, -20),
    ("P-005B_ConoChato", 5, -20),
    ("P-006A_PlanoBase", 10, -20),
    ("MAT-001_Material_Metal", 15, -20),
    ("MAT-002_Material_Vidrio", 20, -20),
    
    # Fila 6: MAT-003 + LUZ iluminaciones
    ("MAT-003_Material_Emisivo", 0, -25),
    ("LUZ-001_Iluminacion_3Point", 10, -25),
    ("LUZ-002_Iluminacion_HDRI", 20, -25),
]

mastered_path = Path("c:/Users/Admin/Desktop/ZULY_IA_LOCAL/archivo_zuly/por_estado_aprendizaje/mastered")

importados = 0
fallidos = 0

for nombre, x, y in patrones:
    blend_file = mastered_path / nombre / "blend" / f"{nombre}.blend"
    
    if not blend_file.exists():
        print(f"❌ No encontrado: {nombre}")
        fallidos += 1
        continue
    
    print(f"\\n📦 Importando {nombre}...")
    
    # Importar objeto del blend
    with bpy.data.libraries.load(str(blend_file)) as (data_from, data_to):
        data_to.objects = data_from.objects
    
    # Agregar objetos a la escena
    for obj in data_to.objects:
        if obj is not None and obj.type == 'MESH':
            bpy.context.collection.objects.link(obj)
            
            # Posicionar en grid
            obj.location = (x, y, 1)
            
            # Resetear rotación
            obj.rotation_euler = (0, 0, 0)
            
            # Escalar uniforme si es necesario
            # obj.scale = (1, 1, 1)
            
            print(f"   ✅ {obj.name} en ({x}, {y})")
            importados += 1

print(f"\\n📊 IMPORTACIÓN COMPLETADA:")
print(f"   ✅ Importados: {importados} objetos")
print(f"   ❌ Fallidos: {fallidos}")

# Añadir iluminación global
print("\\n💡 Añadiendo iluminación global...")

# Sol
bpy.ops.object.light_add(type='SUN', location=(10, -10, 20))
sol = bpy.context.active_object
sol.name = "ZULY_MAESTRO_Sol"
sol.data.energy = 3

# Cámara aérea
print("📷 Posicionando cámara aérea...")
bpy.ops.object.camera_add(location=(12, -15, 30))
cam = bpy.context.active_object
cam.name = "ZULY_MAESTRO_Camara"
cam.rotation_euler = (math.radians(60), 0, math.radians(45))
bpy.context.scene.camera = cam

# Configurar render
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 3840  # 4K
bpy.context.scene.render.resolution_y = 2160
bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.bloom_intensity = 0.1

# Guardar
output = './ZULY_MAESTRO.blend'
print(f"\\n💾 Guardando {output}...")
bpy.ops.wm.save_as_mainfile(filepath=output)

# Estadísticas
print("\\n" + "="*70)
print("📊 ESTADÍSTICAS ZULY MAESTRO")
print("="*70)
print(f"📦 Objetos importados: {importados}")
print(f"🏆 Total patrones: 27")
print(f"📐 Dimensiones grid: 25m x 30m")
print(f"📁 Archivo: {output}")
print(f"🎨 Sistema: ZULY v1.0 - Nivel 4 Experto")
print("="*70)
'''

script_path = zuly_path / 'temp_zuly_maestro.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_maestro)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🏆 Generando ZULY_MAESTRO.blend con 27 patrones...")
print("⏱️  Esto puede tomar 2-3 minutos...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-3000:] if len(result.stdout) > 3000 else result.stdout)

script_path.unlink()

print("\n✅ ZULY_MAESTRO.blend creado")
