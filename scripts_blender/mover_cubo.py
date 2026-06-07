import bpy

# Selecciona el cubo activo o crea uno si no existe
if 'Cube' not in bpy.data.objects:
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
    cube.name = 'Cube'
else:
    cube = bpy.data.objects['Cube']

# Mueve el cubo a la posición deseada (ejemplo: x=15, y=0, z=0)
cube.location = (15.0, 0.0, 0.0)

print(f"Cubo movido a: {cube.location}")
