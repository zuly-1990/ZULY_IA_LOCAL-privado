import bpy

# Eliminar todos los objetos previos
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear 30 cubos rojos
for i in range(30):
    bpy.ops.mesh.primitive_cube_add(location=(i * 2.0, 0.0, 0.0))
    cube = bpy.context.active_object
    cube.name = f'Cube_{i+1}'
    # Crear material rojo si no existe
    mat_name = 'Rojo'
    if mat_name not in bpy.data.materials:
        mat = bpy.data.materials.new(name=mat_name)
        mat.diffuse_color = (1.0, 0.0, 0.0, 1.0)  # RGBA rojo
    else:
        mat = bpy.data.materials[mat_name]
    # Asignar material al cubo
    if cube.data.materials:
        cube.data.materials[0] = mat
    else:
        cube.data.materials.append(mat)

# Renderizar imagen en carpeta export/pruebas_cubo
bpy.context.scene.render.filepath = r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/30_cubos_rojos_render.png"
bpy.ops.render.render(write_still=True)

# Guardar archivo .blend en carpeta export/pruebas_cubo
bpy.ops.wm.save_as_mainfile(filepath=r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/30_cubos_rojos.blend")

print("30 cubos rojos creados, renderizados y guardados en export/pruebas_cubo.")
