import sys
from pathlib import Path

# Agregar path de ZULY al sys.path
zuly_path = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
if str(zuly_path) not in sys.path:
    sys.path.insert(0, str(zuly_path))

from core.agent import Agent
import bpy

print("\nVerificando el handler con guardado inmediato\n")

# Abrir el archivo corregido
bpy.ops.wm.open_mainfile(filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/pruebas/zuly_save_20260322_080838_fixed.blend")

print("Color antes de la actualización:")
if 'BlueDot' in bpy.data.materials:
    mat = bpy.data.materials['BlueDot']
    if mat.use_nodes:
        principled = mat.node_tree.nodes.get('Principled BSDF')
        if principled:
            color = list(principled.inputs['Base Color'].default_value)
            print(f"  {color}")

# Crear agente
agent = Agent()

# Cambiar el color a rojo
print("\nEjecutando handler set_material_color...")
result = agent.execute_via_router('blender.set_material_color', {
    'material_name': 'BlueDot',
    'color': [1.0, 0.0, 0.0, 1.0]  # Rojo
})

print(f"Resultado del handler: {result}")

print("\nColor inmediatamente después de la actualización:")
if 'BlueDot' in bpy.data.materials:
    mat = bpy.data.materials['BlueDot']
    if mat.use_nodes:
        principled = mat.node_tree.nodes.get('Principled BSDF')
        if principled:
            color = list(principled.inputs['Base Color'].default_value)
            print(f"  {color}")

# Guardar inmediatamente
print("\nGuardando archivo...")
bpy.ops.wm.save_as_mainfile(filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/pruebas/zuly_save_20260322_080838_test_red.blend")

# Recargar y verificar
print("\nRecargando archivo...")
bpy.ops.wm.open_mainfile(filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/pruebas/zuly_save_20260322_080838_test_red.blend")

print("\nColor después de recargar:")
if 'BlueDot' in bpy.data.materials:
    mat = bpy.data.materials['BlueDot']
    if mat.use_nodes:
        principled = mat.node_tree.nodes.get('Principled BSDF')
        if principled:
            color = list(principled.inputs['Base Color'].default_value)
            print(f"  {color}")

print("Verificación completada.")