#!/usr/bin/env python3
"""
Agujero atravesado con color interior
"""

import subprocess
import tempfile
from pathlib import Path

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_INPUT = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_biselado.blend")

code = """
import bpy

# CARGAR EL BLEND
bpy.ops.wm.open_mainfile(filepath=r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_biselado.blend')

# OBTENER CUBO
cubo = None
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        cubo = obj
        break

if cubo:
    print("[OK] Cubo encontrado: " + cubo.name)
    
    # CREAR CILINDRO (va a hacer el agujero)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=3.5, location=(0, 0, 0))
    cilindro = bpy.context.active_object
    cilindro.name = "Agujero"
    print("[OK] Cilindro agujero creado")
    
    # MATERIAL COLOR PARA EL AGUJERO
    mat_color = bpy.data.materials.new(name="ColorAgujero")
    mat_color.use_nodes = True
    mat_color.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.8, 1.0, 1.0)  # Azul celeste
    mat_color.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.3  # Roughness
    cilindro.data.materials.append(mat_color)
    print("[OK] Material azul aplicado")
    
    # BOOLEAN MODIFIER (restar cilindro del cubo)
    boolean_mod = cubo.modifiers.new(name="BooleanAgujero", type='BOOLEAN')
    boolean_mod.operation = 'DIFFERENCE'
    boolean_mod.object = cilindro
    boolean_mod.solver = 'FAST'
    print("[OK] Boolean modifier aplicado")
    
    # OCULTAR CILINDRO (solo queremos el agujero)
    cilindro.hide_set(True)
    cilindro.hide_render = True
    print("[OK] Cilindro convertido a agujero (oculto)")
    
    # APLICAR SHADING SMOOTH
    cubo.select_set(True)
    bpy.context.view_layer.objects.active = cubo
    bpy.ops.object.shade_smooth()
    print("[OK] Smooth shading aplicado")

# GUARDAR
bpy.ops.wm.save_mainfile()
print("[OK] Guardado: cubo_biselado.blend actualizado")
print("[LISTO] Podes ver el agujero de color en Blender")
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(code)
    temp_path = Path(f.name)

try:
    print("Haciendo agujero atravesado con color...")
    cmd = [str(BLENDER_PATH), "--background", "--python", str(temp_path)]
    result = subprocess.run(cmd, timeout=30)
    print("✅ Agujero completado - actualiza Blender (File > Reload) para ver cambios")
    
except Exception as e:
    print(f"[ERROR] {e}")
finally:
    if temp_path.exists():
        temp_path.unlink()
