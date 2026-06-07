import bpy
import math
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

# Crear cubo amarillo en el centro
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = 'Cubo_Amarillo'
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

# Luz principal frontal
bpy.ops.object.light_add(type='AREA', location=(0, 6, 6))
light1 = bpy.context.active_object
light1.data.energy = 1000
light1.data.color = (1, 1, 1)

# Cámara frontal
bpy.ops.object.camera_add(location=(0, 4, 2))
cam = bpy.context.active_object
cam.data.lens = 50
bpy.context.scene.camera = cam

# Apuntar la cámara al cubo
import mathutils
direction = cube.location - cam.location
rot_quat = direction.to_track_quat('-Z', 'Y')
cam.rotation_euler = rot_quat.to_euler()

# Animación: rotar en eje Z y aparecer/desaparecer
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=1)
cube.keyframe_insert(data_path="hide_viewport", frame=1)
cube.keyframe_insert(data_path="hide_render", frame=1)

# Aparece en frame 10
cube.hide_viewport = False
cube.hide_render = False
cube.keyframe_insert(data_path="hide_viewport", frame=10)
cube.keyframe_insert(data_path="hide_render", frame=10)

# Rota 360° en 40 frames
cube.rotation_euler = (0, 0, math.radians(360))
cube.keyframe_insert(data_path="rotation_euler", frame=50)

# Desaparece en frame 60
cube.hide_viewport = True
cube.hide_render = True
cube.keyframe_insert(data_path="hide_viewport", frame=60)
cube.keyframe_insert(data_path="hide_render", frame=60)

# Configurar render
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60
bpy.context.scene.render.image_settings.file_format = 'PNG'
output_dir = r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/animacion_cubo_amarillo_rotando/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
bpy.context.scene.render.filepath = os.path.join(output_dir, "frame_")
bpy.ops.render.render(animation=True)

# Guardar archivo .blend para revisión manual
bpy.ops.wm.save_as_mainfile(filepath=r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/animacion_cubo_amarillo_rotando.blend")

print("Animación de cubo amarillo rotando creada y guardada. Frames y .blend disponibles para revisión.")
