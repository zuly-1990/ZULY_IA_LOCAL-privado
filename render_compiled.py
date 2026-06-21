import bpy
import os

print("=== GENERANDO RENDER DEL COMPILADO ===")

# Abrir el blend compilado
filepath = "/opt/zuly/resultados_masivos_v8/Villa_Saboye_V8_Compilado.blend"
bpy.ops.wm.open_mainfile(filepath=filepath)

# Crear una camara si no existe
if "Camara_Render" not in bpy.data.objects:
    bpy.ops.object.camera_add(location=(30, -35, 25), rotation=(1.0, 0.0, 0.7))
    cam = bpy.context.active_object
    cam.name = "Camara_Render"
else:
    cam = bpy.data.objects["Camara_Render"]

bpy.context.scene.camera = cam

# Configurar renderizador
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Luz de sol si no existe
if "Sol_Render" not in bpy.data.objects:
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 20))
    sun = bpy.context.active_object
    sun.name = "Sol_Render"
    sun.data.energy = 5.0

# Posicionar camara apuntando al centro
# Encontrar centro de bounding box de los objetos
x_coords, y_coords, z_coords = [], [], []
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        for vertex in obj.data.vertices:
            world_coord = obj.matrix_world @ vertex.co
            x_coords.append(world_coord.x)
            y_coords.append(world_coord.y)
            z_coords.append(world_coord.z)

if x_coords:
    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    center_z = sum(z_coords) / len(z_coords)
    print(f"Centro calculado: ({center_x}, {center_y}, {center_z})")
    
    # Crear un empty en el centro para que la camara lo mire
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(center_x, center_y, center_z))
    target = bpy.context.active_object
    target.name = "Target_Render"
    
    # Track to constraint
    track = cam.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

# Forzar actualizacion
bpy.context.view_layer.update()

# Renderizar
output_image = "/opt/zuly/resultados_masivos_v8/Villa_Saboye_V8_Render.png"
bpy.context.scene.render.filepath = output_image
bpy.ops.render.render(write_still=True)

print(f"=== RENDER COMPLETADO EN: {output_image} ===")
