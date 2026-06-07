import bpy
import math

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
    mat.diffuse_color = (1.0, 1.0, 0.0, 1.0)  # RGBA amarillo
else:
    mat = bpy.data.materials[mat_name]

# Asignar material al cubo
if cube.data.materials:
    cube.data.materials[0] = mat
else:
    cube.data.materials.append(mat)

# Añadir cámara
bpy.ops.object.camera_add(location=(5.0, -10.0, 5.0))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

# Rotar el cubo en el eje Z (180 grados)
cube.rotation_euler = (0.0, 0.0, math.radians(180))

# Renderizar imagen en carpeta export/pruebas_cubo
bpy.context.scene.render.filepath = r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/cubo_amarillo_rotando_z_render.png"
bpy.ops.render.render(write_still=True)

# Guardar archivo .blend en carpeta export/pruebas_cubo
bpy.ops.wm.save_as_mainfile(filepath=r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/cubo_amarillo_rotando_z.blend")

print("Cubo amarillo rotando en eje Z creado, renderizado y guardado en export/pruebas_cubo.")
