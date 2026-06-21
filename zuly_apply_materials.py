import bpy
import math

BLEND_IN = '/opt/zuly/ZULY_VILLA_SAVOYE_PERFECT_V30.blend'
BLEND_OUT = '/opt/zuly/ZULY_VILLA_SAVOYE_MATS.blend'
RENDER_OUT = '/opt/zuly/Villa_Savoye_Render.png'

def setup_materials():
    # Blanco Corbusier
    mat_blanco = bpy.data.materials.new(name="Blanco_Corbusier")
    mat_blanco.use_nodes = True
    bsdf = mat_blanco.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1) # Blanco roto
        bsdf.inputs['Roughness'].default_value = 0.6 # Estuco

    # Cristal
    mat_cristal = bpy.data.materials.new(name="Cristal")
    mat_cristal.use_nodes = True
    # Limpiar nodos
    for node in mat_cristal.node_tree.nodes:
        mat_cristal.node_tree.nodes.remove(node)
    
    out_node = mat_cristal.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    glass_node = mat_cristal.node_tree.nodes.new(type='ShaderNodeBsdfGlass')
    glass_node.inputs['Color'].default_value = (0.7, 0.8, 0.9, 1)
    glass_node.inputs['IOR'].default_value = 1.45
    mat_cristal.node_tree.links.new(glass_node.outputs['BSDF'], out_node.inputs['Surface'])

    # Concreto
    mat_concreto = bpy.data.materials.new(name="Concreto_Pilotes")
    mat_concreto.use_nodes = True
    bsdf_c = mat_concreto.node_tree.nodes.get("Principled BSDF")
    if bsdf_c:
        bsdf_c.inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1)
        bsdf_c.inputs['Roughness'].default_value = 0.8

    return mat_blanco, mat_cristal, mat_concreto

def apply_materials_to_object(obj, mat_blanco):
    # Aseguramos que el objeto tiene el material base en el slot 0
    if not obj.data.materials:
        obj.data.materials.append(mat_blanco)
    else:
        obj.data.materials[0] = mat_blanco

def setup_environment_and_render():
    # Eliminar luces/camaras viejas si existen
    for obj in bpy.data.objects:
        if obj.type in ['LIGHT', 'CAMERA']:
            bpy.data.objects.remove(obj)

    # Configurar Cielo Físico (Nishita)
    world = bpy.context.scene.world
    world.use_nodes = True
    tree = world.node_tree
    
    for node in tree.nodes:
        tree.nodes.remove(node)
        
    sky = tree.nodes.new('ShaderNodeTexSky')
    sky.sky_type = 'NISHITA'
    sky.sun_elevation = math.radians(35)
    sky.sun_rotation = math.radians(135)
    
    bg = tree.nodes.new('ShaderNodeBackground')
    out = tree.nodes.new('ShaderNodeOutputWorld')
    
    tree.links.new(sky.outputs['Color'], bg.inputs['Color'])
    tree.links.new(bg.outputs['Background'], out.inputs['Surface'])

    # Cámara
    cam_data = bpy.data.cameras.new("Camara_Principal")
    cam_obj = bpy.data.objects.new("Camara_Principal", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    
    # Posicionar cámara para ver toda la casa
    # Casa de 19.6x21.6, centrada en 0,0
    cam_obj.location = (25.0, -25.0, 10.0)
    
    # Apuntar cámara al centro (0,0,3.5)
    # Forma rápida: Constraint Track To
    empty = bpy.data.objects.new("Target", None)
    empty.location = (0, 0, 3.5)
    bpy.context.scene.collection.objects.link(empty)
    
    track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = empty
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    bpy.context.scene.camera = cam_obj

    # Configurar Motor Render (Cycles)
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'CPU' # Usar CPU si no hay GPU segura
    bpy.context.scene.cycles.samples = 64   # Rápido para previsualizar
    
    # Resolución 1080p
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.filepath = RENDER_OUT

def main():
    print("--- INICIANDO FASE DE MATERIALES ---")
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    
    mat_blanco, mat_cristal, mat_concreto = setup_materials()
    
    # Buscar el objeto creado con Geometry Nodes
    obj = bpy.data.objects.get("VILLA_SAVOYE_PERFECTA")
    if obj:
        apply_materials_to_object(obj, mat_blanco)
    else:
        print("ADVERTENCIA: No se encontró 'VILLA_SAVOYE_PERFECTA'.")
        # Si no lo encuentra, lo aplica al primer Mesh
        for o in bpy.data.objects:
            if o.type == 'MESH':
                apply_materials_to_object(o, mat_blanco)
                break
                
    setup_environment_and_render()
    
    # Guardar archivo con materiales
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"✅ Archivo guardado en {BLEND_OUT}")
    
    # Renderizar
    print("📸 Renderizando escena... esto puede tomar un minuto...")
    bpy.ops.render.render(write_still=True)
    print(f"✅ Render guardado en {RENDER_OUT}")

if __name__ == "__main__":
    main()
