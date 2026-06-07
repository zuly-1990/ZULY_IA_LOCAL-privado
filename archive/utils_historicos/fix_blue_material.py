import sys
from pathlib import Path

# Agregar path de ZULY al sys.path
zuly_path = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
if str(zuly_path) not in sys.path:
    sys.path.insert(0, str(zuly_path))

import bpy

print("\nCorrigiendo el material BlueDot\n")

# Abrir el archivo
bpy.ops.wm.open_mainfile(filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/pruebas/zuly_save_20260322_080838.blend")

# Buscar el material BlueDot
if 'BlueDot' in bpy.data.materials:
    mat = bpy.data.materials['BlueDot']
    print(f"Material encontrado. use_nodes: {mat.use_nodes}")

    # Activar nodos si no están activados
    if not mat.use_nodes:
        mat.use_nodes = True
        print("Nodos activados")

    # Buscar o crear Principled BSDF
    principled = mat.node_tree.nodes.get('Principled BSDF')
    if not principled:
        principled = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        print("Principled BSDF creado")

    # Establecer el color azul
    blue_color = [0.0, 0.3, 1.0, 1.0]
    principled.inputs['Base Color'].default_value = tuple(blue_color)
    print(f"Color establecido a: {blue_color}")

    # Verificar el color
    current_color = list(principled.inputs['Base Color'].default_value)
    print(f"Color actual verificado: {current_color}")

    # Guardar el archivo
    bpy.ops.wm.save_as_mainfile(filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/pruebas/zuly_save_20260322_080838_fixed.blend")
    print("Archivo guardado como zuly_save_20260322_080838_fixed.blend")

else:
    print("Material BlueDot no encontrado")

print("Corrección completada.")