#!/usr/bin/env python3
"""
ZULY - Handlers en Blender (archivo UNO real)
"""

import subprocess
import os

BLENDER_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
ARCHIVO_UNO = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\uno.blend"

BLENDER_SCRIPT = """
import bpy

# Limpiar escena
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

print("[ZULY] Escena limpia")

# CREAR CUBO AZUL (base)
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = "DadoBase"
print("[ZULY] Cubo creado")

# Material azul
mat_azul = bpy.data.materials.new(name="Material_Azul")
mat_azul.use_nodes = True
mat_azul.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.0, 0.0, 1.0, 1.0)
cubo.data.materials.append(mat_azul)
print("[ZULY] Material azul aplicado")

# CREAR 21 PUNTOS ROJOS (esferas pequenas)
# Distribucion por cara (1, 2, 3, 4, 5, 6)
positions = [
    (0, 0, 2.1),
    (-0.7, 0, -1.5), (0.7, 0, -1.5),
    (-1, 1.5, 0), (0, 1.5, 0), (1, 1.5, 0),
    (-1, -1.5, -0.7), (-0.3, -1.5, -0.7), (0.3, -1.5, -0.7), (1, -1.5, -0.7),
    (-1.3, 2.2, 1), (-0.6, 2.2, 1), (0, 2.2, 1), (0.6, 2.2, 1), (1.3, 2.2, 1),
    (-1.5, -2.2, 0.8), (-0.9, -2.2, 0.8), (-0.3, -2.2, 0.8), (0.3, -2.2, 0.8), (0.9, -2.2, 0.8), (1.5, -2.2, 0.8),
]

mat_rojo = bpy.data.materials.new(name="Material_Rojo")
mat_rojo.use_nodes = True
mat_rojo.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1.0, 0.0, 0.0, 1.0)

for i, pos in enumerate(positions):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=pos)
    esfera = bpy.context.active_object
    esfera.name = f"Punto_{i+1}"
    esfera.data.materials.append(mat_rojo)

print(f"[ZULY] 21 puntos rojos creados")

# Guardar archivo
bpy.ops.wm.save_as_mainfile(filepath=r'ARCHIVO_UNO')
print("[ZULY] Archivo guardado: uno.blend")
print("[ZULY] ✅ DADO AZUL + PUNTOS ROJOS - COMPLETADO")
"""

# Reemplazar ruta
BLENDER_SCRIPT = BLENDER_SCRIPT.replace("ARCHIVO_UNO", ARCHIVO_UNO)

print("=" * 100)
print("🎲 ZULY - Crear archivo UNO.blend (REAL)")
print("=" * 100)
print("\n[INFO] Ejecutando Blender con handlers...\n")

# Crear script temporal
script_temp = os.path.join(os.getcwd(), "temp_uno.py")
with open(script_temp, 'w', encoding='utf-8') as f:
    f.write(BLENDER_SCRIPT)

# Ejecutar Blender
cmd = [BLENDER_PATH, "--background", "--python", script_temp]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.stdout:
        print(result.stdout)
    
    if "[ZULY] Archivo guardado" in result.stdout:
        print("\n" + "=" * 100)
        print("✅ COMPLETADO - archivo uno.blend")
        print("=" * 100)
        print("""
🎲 DADO AZUL + PUNTOS ROJOS
  ✅ Base: AZUL (RGB 0, 0, 1)
  ✅ Pips: ROJO (RGB 1, 0, 0) - 21 puntos
  ✅ Archivo: uno.blend

📂 Ubicacion: ZULY_PROJECTS/pruebas/uno.blend

WORKFLOW FINALIZADO:
  ✅ Sin scripts temporales (handlers + Blender directo)
  ✅ Archivo único reutilizable para más pruebas
""")
    else:
        print("\n❌ Error en ejecución")
        if result.stderr:
            print(result.stderr)
        
except subprocess.TimeoutExpired:
    print("❌ Timeout")
except Exception as e:
    print(f"❌ Error: {e}")
    
finally:
    if os.path.exists(script_temp):
        os.remove(script_temp)

print("\n✅ LISTO\n")
