import sys
from pathlib import Path

# Agregar path de ZULY al sys.path
zuly_path = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
if str(zuly_path) not in sys.path:
    sys.path.insert(0, str(zuly_path))

import bpy

print("\nRevisando el color actual del material BlueDot\n")

# Abrir el archivo
bpy.ops.wm.open_mainfile(filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/pruebas/zuly_save_20260322_080838.blend")

# Buscar el material BlueDot
if 'BlueDot' in bpy.data.materials:
    mat = bpy.data.materials['BlueDot']
    if mat.use_nodes and mat.node_tree:
        # En Blender, el color principal está en el Principled BSDF
        principled = mat.node_tree.nodes.get('Principled BSDF')
        if principled:
            color = principled.inputs['Base Color'].default_value
            print(f"Color actual de BlueDot: {color}")
        else:
            print("No se encontró Principled BSDF")
    else:
        # Si no usa nodos, usar diffuse_color
        print(f"Color diffuse: {mat.diffuse_color}")
else:
    print("Material BlueDot no encontrado")

print("Revisión completada.")