
import bpy
import math
import os

# Limpiar la escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear cubo
bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.0))
cube = bpy.context.active_object
cube.name = 'Cube_Amarillo'

# Crear material amarillo
mat_name = 'Amarillo'
if mat_name not in bpy.data.materials:
    mat = bpy.data.materials.new(name=mat_name)
    mat.diffuse_color = (1.0, 1.0, 0.0, 1.0)
else:
    mat = bpy.data.materials[mat_name]
if len(cube.data.materials) > 0:
    cube.data.materials[0] = mat
else:
    cube.data.materials.append(mat)

# Añadir luz principal (frontal)
bpy.ops.object.light_add(type='AREA', location=(0, 8, 8))
light1 = bpy.context.active_object
light1.data.energy = 1500
light1.data.color = (1, 1, 1)

# Añadir luz secundaria (contraluz)
bpy.ops.object.light_add(type='POINT', location=(0, -8, 6))
light2 = bpy.context.active_object
light2.data.energy = 600
light2.data.color = (1, 1, 0.8)

# Añadir cámara frontal
bpy.ops.object.camera_add(location=(0, 8, 4))
cam = bpy.context.active_object
cam.location = (0, 8, 4)
cam.rotation_euler = (math.radians(-30), 0, math.radians(180))
bpy.context.scene.camera = cam

# Configurar render
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 1
bpy.context.scene.render.image_settings.file_format = 'PNG'
output_dir = r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/frames_animacion_cubo_amarillo/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
frame_path = os.path.join(output_dir, "cubo_frontal.png")
bpy.context.scene.render.filepath = frame_path
bpy.ops.render.render(write_still=True)

# Guardar archivo .blend
bpy.ops.wm.save_as_mainfile(filepath=r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/animacion_cubo_amarillo_rotando_z.blend")

print("Imagen de cubo amarillo frontal renderizada y guardada en export/pruebas_cubo/frames_animacion_cubo_amarillo.")
