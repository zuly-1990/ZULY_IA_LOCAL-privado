#!/usr/bin/env python3
"""
Script generado por Zuly: 
Jugar solo con cubos, editar archivo base, crear 4 cubos y hacer agujeros XYZ
"""

import subprocess
import tempfile
from pathlib import Path
import os

BLENDER_PATH = Path(r"blender\v3\blender-3.6.0-zuly\blender.exe").absolute()
BLEND_DIR = Path("ZULY_LAB/resultados_zuly").absolute()
BLEND_IN = BLEND_DIR / "zuly_cli_resultado_primitivas.blend"
BLEND_OUT = BLEND_DIR / "cubos_perforados.blend"

# Reconstruimos el string uniendo partes para no pelar con format y brackets
code_p1 = "import bpy\nimport math\n"
code_p2 = "bpy.ops.wm.open_mainfile(filepath=r'" + BLEND_IN.as_posix() + "')\n"
code_p3 = """
print("[ZULY] Limpiando escena para dejar solo cubos...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("[ZULY] Creando 1 cubo central...")
positions = [
    (0, 0, 0)
]
cubes = []
for pos in positions:
    bpy.ops.mesh.primitive_cube_add(size=2, location=pos)
    cubes.append(bpy.context.active_object)

print("[ZULY] Creando perforaciones XYZ a traves de los cubos...")
bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=10, location=(0, 0, 0))
cyl_x = bpy.context.active_object
cyl_x.rotation_euler = (0, math.pi/2, 0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=10, location=(0, 0, 0))
cyl_y = bpy.context.active_object
cyl_y.rotation_euler = (math.pi/2, 0, 0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=10, location=(0, 0, 0))
cyl_z = bpy.context.active_object

for cube in cubes:
    for i, cyl in enumerate([cyl_x, cyl_y, cyl_z]):
        name_s = ["X", "Y", "Z"][i]
        bool_mod = cube.modifiers.new(type='BOOLEAN', name="Agujero_" + name_s)
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = cyl
        bool_mod.solver = 'FAST'
        
        bpy.context.view_layer.objects.active = cube
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)

bpy.data.objects.remove(cyl_x)
bpy.data.objects.remove(cyl_y)
bpy.data.objects.remove(cyl_z)

"""
code_p4 = "out_path = r'" + BLEND_OUT.as_posix() + "'\n"
code_p5 = "bpy.ops.wm.save_as_mainfile(filepath=out_path)\n"
code_p6 = "print('[ZULY] Cambios guardados en ' + out_path)\n"

code = code_p1 + code_p2 + code_p3 + code_p4 + code_p5 + code_p6

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(code)
    temp_path = Path(f.name)

try:
    print(f"[ZULY EJECUTANDO] Editando archivo: {BLEND_IN.name}")
    print("[ZULY EJECUTANDO] Operacion: 4 cubos perforados en X, Y, Z...")
    cmd = [str(BLENDER_PATH), "--background", "--python", str(temp_path)]
    result = subprocess.run(cmd, timeout=45, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ ZULY Script completado con éxito.")
    else:
        print("❌ Error en Blender:")
        print(result.stdout)
        print(result.stderr)
        
except Exception as e:
    print(f"[ERROR EXCEPCION] {e}")
finally:
    if temp_path.exists():
        temp_path.unlink()
