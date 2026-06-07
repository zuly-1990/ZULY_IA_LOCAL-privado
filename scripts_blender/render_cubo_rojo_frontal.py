import bpy
import math
import os

# Limpiar la escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Fondo gris medio
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.6, 0.6, 0.6, 1)

# Crear cubo
bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.0))
cube = bpy.context.active_object
cube.name = 'Cube_Rojo'

# Crear material rojo
mat_name = 'Rojo'
if mat_name not in bpy.data.materials:
    mat = bpy.data.materials.new(name=mat_name)
    mat.diffuse_color = (1.0, 0.0, 0.0, 1.0)
else:
    mat = bpy.data.materials[mat_name]
if len(cube.data.materials) > 0:
    cube.data.materials[0] = mat
else:
    cube.data.materials.append(mat)

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

# Cámara cerca y con ángulo
import mathutils
bpy.ops.object.camera_add(location=(0, 4, 2))
cam = bpy.context.active_object
# Apuntar la cámara al cubo
target = cube.location
direction = target - cam.location
rot_quat = direction.to_track_quat('-Z', 'Y')
cam.rotation_euler = rot_quat.to_euler()
bpy.context.scene.camera = cam

# Configurar render
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 1
bpy.context.scene.render.image_settings.file_format = 'PNG'
output_dir = r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/frames_animacion_cubo_rojo/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
frame_path = os.path.join(output_dir, "cubo_rojo_frontal.png")
bpy.context.scene.render.filepath = frame_path
bpy.ops.render.render(write_still=True)

# Guardar archivo .blend para revisión manual
bpy.ops.wm.save_as_mainfile(filepath=r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/cubo_rojo_frontal.blend")

print("Imagen de cubo rojo frontal renderizada y guardada en export/pruebas_cubo/frames_animacion_cubo_rojo. Archivo .blend guardado para revisión manual.")
