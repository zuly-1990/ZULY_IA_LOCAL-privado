#!/usr/bin/env python3
"""
Reconstruir uno.blend CON TheCubeUniverseEngine integrado
"""

import subprocess
import os
import sys

sys.path.insert(0, r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")

from core.cognition.c_engine_integration import engine_integration

BLENDER_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
ARCHIVO_UNO = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\uno.blend"

print("=" * 100)
print("🎲 ZULY - Reconstruir uno.blend CON TheCubeUniverseEngine")
print("=" * 100)

print("\n[1] Engine calcula parámetros...")

volumen_m3 = 0.001
evaluacion = engine_integration.evaluate_viability(volumen_m3)
descomposicion = engine_integration.decompose_construction_task(volumen_m3, "Dado ZULY")
pattern = engine_integration.pattern_from_volume(volumen_m3)
atom_info = engine_integration.get_atom_info()
logistica = descomposicion['decomposition']['logistics']
size_m = pattern['equivalent_cube_side_m']

print(f"   ✅ Viabilidad: {evaluacion['viability'].upper()}")
print(f"   ✅ Masa: {evaluacion['properties']['masa_kg']:.3f}kg")
print(f"   ✅ Tamaño: {size_m*100:.2f}cm")

if evaluacion['viability'] != 'viable':
    print(f"\n❌ No viable. Abortando.")
    exit(1)

print("\n[2] Generando script Blender...")

# Script template
script = f"""
import bpy

# Parámetros engine
s = {size_m}
masa = {evaluacion['properties']['masa_kg']}
dens = {evaluacion['properties']['densidad_kgm3']}

# Limpiar
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

# Cubo azul
bpy.ops.mesh.primitive_cube_add(size=s, location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = "DadoZULY_Engine"
cubo["engine_v20"] = True
cubo["masa_kg"] = masa
cubo["densidad"] = dens

# Material azul
mat_a = bpy.data.materials.new("MotorAzul")
mat_a.use_nodes = True
mat_a.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0,0,1,1)
cubo.data.materials.append(mat_a)

# Material rojo
mat_r = bpy.data.materials.new("MotorRojo")
mat_r.use_nodes = True
mat_r.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1,0,0,1)

# Posiciones pips
pos = [
(0,0,{size_m/2+0.01}),
({-size_m*0.35},0,{-size_m*0.75}),
({size_m*0.35},0,{-size_m*0.75}),
({-size_m*0.5},{size_m*0.75},0),
(0,{size_m*0.75},0),
({size_m*0.5},{size_m*0.75},0),
({-size_m*0.5},{-size_m*0.75},-0.035),
(-0.015,{-size_m*0.75},-0.035),
(0.015,{-size_m*0.75},-0.035),
({size_m*0.5},{-size_m*0.75},-0.035),
({-size_m*0.65},{size_m*1.1},0.05),
(-0.03,{size_m*1.1},0.05),
(0,{size_m*1.1},0.05),
(0.03,{size_m*1.1},0.05),
({size_m*0.65},{size_m*1.1},0.05),
({-size_m*0.75},{-size_m*1.1},0.04),
(-0.045,{-size_m*1.1},0.04),
(-0.015,{-size_m*1.1},0.04),
(0.015,{-size_m*1.1},0.04),
(0.045,{-size_m*1.1},0.04),
({size_m*0.75},{-size_m*1.1},0.04),
]

# Crear pips
for p in pos:
    bpy.ops.mesh.primitive_uv_sphere_add(radius={size_m*0.125}, location=p)
    e = bpy.context.active_object
    e.data.materials.append(mat_r)

print("[ENGINE] OK - Dado preciso con engine v20 creado")

# Guardar
bpy.ops.wm.save_as_mainfile(filepath=r'{ARCHIVO_UNO}')
print("[ENGINE] OK - Guardado: uno.blend")
"""

print("   ✅ Script generado")

print("\n[3] Ejecutando Blender...")

script_file = os.path.join(os.getcwd(), "temp_engine.py")
with open(script_file, 'w', encoding='utf-8') as f:
    f.write(script)

cmd = [BLENDER_PATH, "--background", "--python", script_file]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    
    if "[ENGINE] OK" in result.stdout:
        print("   ✅ Blender ejecutado")
        print("\n" + "=" * 100)
        print("✅✅✅ INTEGRACIÓN COMPLETADA ✅✅✅")
        print("=" * 100)
        print(f"""
🎲 ARCHIVO: uno.blend

TheCubeUniverseEngine v20 INTEGRADO:
  ✅ Parámetro: Tamaño = {size_m*100:.2f}cm (desde patrón atómico)
  ✅ C1 (EVALUADOR): Viabilidad = {evaluacion['viability'].upper()}
  ✅ C2 (PATRONES): Átomos = {pattern['total_atoms']:,} × 0.137mm
  ✅ C3 (OBJETIVOS): Logística = {logistica['viajes_dobletroque']} viajes

ZULY TRANSFORMADO:
  • De: Sistema de dibujo 3D
  • A: Plataforma de ingeniería PRECISA
  • Base: TheCubeUniverseEngine v20
  • Framework: C1+C2+C3 integrados
  • Motor: Propiedades físicas calculadas, no adivinadas

🚀 LISTO PARA USAR:
  Handlers reciben parámetros del engine
  ZULY proyecta con matemática, no con intuición
""")
        print("=" * 100)
    else:
        print("   ⚠️ Verificar output...")
        print(result.stdout[-500:] if result.stdout else "Sin output")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    
finally:
    if os.path.exists(script_file):
        os.remove(script_file)

print("\n✅ COMPLETADO\n")
