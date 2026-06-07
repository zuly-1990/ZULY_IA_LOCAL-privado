import bpy

import gc
# Eliminar todos los objetos previos y limpiar la escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for block in bpy.data.meshes:
    bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)
for block in bpy.data.cameras:
    if block.users == 0:
        bpy.data.cameras.remove(block)
gc.collect()

# Crear material rojo
mat_rojo = bpy.data.materials.get('Rojo')
if not mat_rojo:
    mat_rojo = bpy.data.materials.new(name='Rojo')
    mat_rojo.diffuse_color = (1.0, 0.0, 0.0, 1.0)

# Crear material azul
mat_azul = bpy.data.materials.get('Azul')
if not mat_azul:
    mat_azul = bpy.data.materials.new(name='Azul')
    mat_azul.diffuse_color = (0.0, 0.0, 1.0, 1.0)

# Crear 15 cubos rojos
for i in range(15):
    bpy.ops.mesh.primitive_cube_add(location=(i * 2.0, 0.0, 0.0))
    cube = bpy.context.active_object
    cube.name = f'Cube_Rojo_{i+1}'
    if cube.data.materials:
        cube.data.materials[0] = mat_rojo
    else:
        cube.data.materials.append(mat_rojo)

# Crear 15 cubos azules
for i in range(15):
    bpy.ops.mesh.primitive_cube_add(location=(i * 2.0, 4.0, 0.0))
    cube = bpy.context.active_object
    cube.name = f'Cube_Azul_{i+1}'
    if cube.data.materials:
        cube.data.materials[0] = mat_azul
    else:
        cube.data.materials.append(mat_azul)

cam = None
if not bpy.data.cameras:
    bpy.ops.object.camera_add(location=(15.0, -20.0, 15.0))
    cam = bpy.context.active_object
    cam.name = 'Camera'
else:
    # Usar la primera cámara disponible
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            cam = obj
            break
if cam:
    bpy.context.scene.camera = cam

# Renderizar imagen en carpeta export/pruebas_cubo
bpy.context.scene.render.filepath = r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/15_rojos_15_azules_render.png"
bpy.ops.render.render(write_still=True)

# Guardar archivo .blend en carpeta export/pruebas_cubo
bpy.ops.wm.save_as_mainfile(filepath=r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/15_rojos_15_azules.blend")

print("15 cubos rojos y 15 azules creados, renderizados y guardados en export/pruebas_cubo.")
