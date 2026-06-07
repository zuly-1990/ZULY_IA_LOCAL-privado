import bpy

# Elimina todos los objetos existentes
def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# Crea un cubo verde y lo rota en el eje X
def crear_cubo_verde_rotado():
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    cubo = bpy.context.active_object
    # Aplica material verde
    mat = bpy.data.materials.new(name="Verde")
    mat.diffuse_color = (0, 1, 0, 1)  # RGBA
    cubo.data.materials.append(mat)
    # Rota 45 grados en X
    from math import radians
    cubo.rotation_euler[0] = radians(45)

if __name__ == "__main__":
    limpiar_escena()
    crear_cubo_verde_rotado()
    # Guarda solo el archivo .blend
    bpy.ops.wm.save_as_mainfile(filepath="cubo_verde_rotado.blend")
