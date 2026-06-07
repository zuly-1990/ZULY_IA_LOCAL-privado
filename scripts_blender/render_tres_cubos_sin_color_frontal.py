import bpy
import mathutils
import os

# Limpiar la escena
def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

limpiar_escena()

# Fondo gris medio
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.6, 0.6, 0.6, 1)

# Crear tres cubos sin material (color por defecto)
positions = [(-1.5, 0, 0), (0, 0, 0), (1.5, 0, 0)]
cubos = []
for i, pos in enumerate(positions):
    bpy.ops.mesh.primitive_cube_add(location=pos)
    cube = bpy.context.active_object
    cube.name = f'Cube_SinColor_{i+1}'
    cubos.append(cube)

# Luz principal frontal
bpy.ops.object.light_add(type='AREA', location=(0, 8, 8))
light1 = bpy.context.active_object
light1.data.energy = 1200
light1.data.color = (1, 1, 1)

# Luz lateral para volumen
bpy.ops.object.light_add(type='POINT', location=(6, 0, 6))
light2 = bpy.context.active_object
light2.data.energy = 1000
light2.data.color = (1, 1, 1)

# Calcular centroide de los cubos
centroide = mathutils.Vector((0, 0, 0))
for cube in cubos:
    centroide += cube.location
centroide /= len(cubos)

# Crear la cámara y aplicar buenas prácticas
bpy.ops.object.camera_add(location=(0, 4, 2))
cam = bpy.context.active_object
cam.data.lens = 50
cam.data.show_limits = True
cam.data.show_name = True
# Apuntar la cámara al centroide

# Orientar la cámara
import math

direction = centroide - cam.location
rot_quat = direction.to_track_quat('-Z', 'Y')
cam.rotation_euler = rot_quat.to_euler()
bpy.context.scene.camera = cam

# Configurar render
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 1
bpy.context.scene.render.image_settings.file_format = 'PNG'
output_dir = r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/frames_animacion_tres_cubos_sin_color/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
frame_path = os.path.join(output_dir, "tres_cubos_sin_color_frontal.png")
bpy.context.scene.render.filepath = frame_path
bpy.ops.render.render(write_still=True)

# Guardar archivo .blend para revisión manual
bpy.ops.wm.save_as_mainfile(filepath=r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/tres_cubos_sin_color_frontal.blend")

print("Imagen de tres cubos sin color renderizada y guardada en export/pruebas_cubo/frames_animacion_tres_cubos_sin_color. Archivo .blend guardado para revisión manual.")
