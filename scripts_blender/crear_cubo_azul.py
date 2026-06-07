import bpy

# Crear cubo si no existe
if 'Cube' not in bpy.data.objects:
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
    cube.name = 'Cube'
else:
    cube = bpy.data.objects['Cube']

# Crear material azul
mat_name = 'Azul'
if mat_name not in bpy.data.materials:
    mat = bpy.data.materials.new(name=mat_name)
    mat.diffuse_color = (0.0, 0.0, 1.0, 1.0)  # RGBA azul
else:
    mat = bpy.data.materials[mat_name]

# Asignar material al cubo
if cube.data.materials:
    cube.data.materials[0] = mat
else:
    cube.data.materials.append(mat)

# Renderizar imagen en carpeta export/pruebas_cubo
bpy.context.scene.render.filepath = r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/cubo_azul_render.png"
bpy.ops.render.render(write_still=True)

# Guardar archivo .blend en carpeta export/pruebas_cubo
bpy.ops.wm.save_as_mainfile(filepath=r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/cubo_azul.blend")

print("Cubo azul creado, renderizado y guardado en export/pruebas_cubo.")
