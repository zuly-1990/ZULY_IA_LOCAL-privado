import bpy
import math

BLEND_IN = '/opt/zuly/Villa_Savoye_V9_Modelado3D.blend'
BLEND_OUT = '/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_3.blend'

# PARÁMETROS CORREGIDOS (Lógica Estructural)
RADIO_PILOTE = 0.15
ALTO_PILOTE = 3.8     # Ahora se anclan profundamente en la losa
Z_PILOTE = 1.9        # Centro matemático (mitad de 3.8)
GRID_X = 14.7  
GRID_Y = 16.2  

def create_materials():
    # 1. Ladrillo a la Vista
    mat_ladrillo = bpy.data.materials.new(name="Ladrillo_Vista")
    mat_ladrillo.use_nodes = True
    nodes = mat_ladrillo.node_tree.nodes
    links = mat_ladrillo.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    brick = nodes.new("ShaderNodeTexBrick")
    brick.inputs['Color1'].default_value = (0.6, 0.2, 0.1, 1) # Rojo ladrillo
    brick.inputs['Color2'].default_value = (0.4, 0.15, 0.08, 1) # Rojo oscuro
    brick.inputs['Mortar'].default_value = (0.8, 0.8, 0.8, 1) # Cemento
    brick.inputs['Scale'].default_value = 15.0
    
    links.new(brick.outputs['Color'], bsdf.inputs['Base Color'])
    # Para darle relieve
    bump = nodes.new("ShaderNodeBump")
    bump.inputs['Distance'].default_value = 0.05
    links.new(brick.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # 2. Marcos de Puertas y Ventanas (Metal Oscuro)
    mat_marcos = bpy.data.materials.new(name="Marcos_Metal")
    mat_marcos.use_nodes = True
    bsdf_m = mat_marcos.node_tree.nodes.get("Principled BSDF")
    bsdf_m.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1)
    bsdf_m.inputs['Metallic'].default_value = 0.8
    bsdf_m.inputs['Roughness'].default_value = 0.3
    
    return mat_ladrillo, mat_marcos

def build_iter_3():
    print("[ZULY] Construyendo Iteración 3...")
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    
    mat_ladrillo, mat_marcos = create_materials()

    nombres_fachadas = ["Primer Nivel", "Segundo Nivel", "Fachada principal", "Fachada derecho", "Fachada Izquierda", "Fachada opuesta"]
    nombres_cortes = ["Corte 01", "Corte 02", "Corte 03", "Tercer Nivel"]

    # Ocultar originales
    for o in bpy.data.objects:
        if o.name in nombres_fachadas + nombres_cortes:
            o.hide_viewport = True
            o.hide_render = True

    # Objeto Maestro
    mesh = bpy.data.meshes.new("Savoye_Nodos_Mesh_Iter3")
    master = bpy.data.objects.new("VILLA_SAVOYE_MAESTRA_NODOS", mesh)
    bpy.context.scene.collection.objects.link(master)
    bpy.context.view_layer.objects.active = master
    master.select_set(True)
    
    mod = master.modifiers.new(name="ZULY_CARPETAS_Y_MATERIALES", type='NODES')
    tree = bpy.data.node_groups.new(name="Savoye_Nodos_Core", type='GeometryNodeTree')
    mod.node_group = tree
    
    tree.inputs.new('NodeSocketGeometry', 'Geometry')
    tree.outputs.new('NodeSocketGeometry', 'Geometry')
    in_node = tree.nodes.new('NodeGroupInput')
    in_node.location = (-2000, 0)
    out_node = tree.nodes.new('NodeGroupOutput')
    out_node.location = (2500, 0)
    
    join = tree.nodes.new('GeometryNodeJoinGeometry')
    join.location = (1000, 0)
    
    # --- LIMPIEZA TOPOLÓGICA ---
    # Soldadura
    weld = tree.nodes.new('GeometryNodeMergeByDistance')
    weld.location = (1500, 0)
    weld.inputs['Distance'].default_value = 0.005
    # Engrosamiento (Para tapar caras abiertas)
    extrude = tree.nodes.new('GeometryNodeExtrudeMesh')
    extrude.location = (1800, 0)
    extrude.inputs['Offset Scale'].default_value = 0.02 # Le da 2cm de grosor a los muros de papel
    
    tree.links.new(join.outputs[0], weld.inputs['Geometry'])
    tree.links.new(weld.outputs['Geometry'], extrude.inputs['Mesh'])
    tree.links.new(extrude.outputs['Mesh'], out_node.inputs['Geometry'])

    # --- CARPETAS (FRAMES) VISUALES ---
    frame_muros = tree.nodes.new('NodeFrame')
    frame_muros.name = "CARPETA: MUROS Y FACHADAS (LADRILLO)"
    frame_muros.label = "CARPETA: MUROS Y FACHADAS (LADRILLO)"
    frame_muros.use_custom_color = True
    frame_muros.color = (0.8, 0.3, 0.1)

    frame_marcos = tree.nodes.new('NodeFrame')
    frame_marcos.name = "CARPETA: CORTES Y MARCOS"
    frame_marcos.label = "CARPETA: CORTES Y MARCOS"
    frame_marcos.use_custom_color = True
    frame_marcos.color = (0.2, 0.2, 0.2)
    
    frame_pilotes = tree.nodes.new('NodeFrame')
    frame_pilotes.name = "CARPETA: ESTRUCTURA MATEMÁTICA"
    frame_pilotes.label = "CARPETA: ESTRUCTURA MATEMÁTICA"
    frame_pilotes.use_custom_color = True
    frame_pilotes.color = (0.2, 0.6, 0.8)

    # --- INYECTAR Y ASIGNAR MATERIALES ---
    y_offset = 1000
    
    # 1. Fachadas y Muros -> Ladrillo
    join_fachadas = tree.nodes.new('GeometryNodeJoinGeometry')
    join_fachadas.location = (0, 800)
    join_fachadas.parent = frame_muros
    mat_nodo_f = tree.nodes.new('GeometryNodeSetMaterial')
    mat_nodo_f.location = (200, 800)
    mat_nodo_f.inputs['Material'].default_value = mat_ladrillo
    mat_nodo_f.parent = frame_muros
    tree.links.new(join_fachadas.outputs[0], mat_nodo_f.inputs['Geometry'])
    tree.links.new(mat_nodo_f.outputs['Geometry'], join.inputs[0])

    for obj_name in nombres_fachadas:
        obj = bpy.data.objects.get(obj_name)
        if obj:
            oi = tree.nodes.new('GeometryNodeObjectInfo')
            oi.inputs['Object'].default_value = obj
            oi.transform_space = 'RELATIVE'
            oi.location = (-500, y_offset)
            oi.parent = frame_muros
            tree.links.new(oi.outputs['Geometry'], join_fachadas.inputs[0])
            y_offset -= 150

    # 2. Cortes y Marcos -> Metal
    y_offset = -200
    join_cortes = tree.nodes.new('GeometryNodeJoinGeometry')
    join_cortes.location = (0, -200)
    join_cortes.parent = frame_marcos
    mat_nodo_c = tree.nodes.new('GeometryNodeSetMaterial')
    mat_nodo_c.location = (200, -200)
    mat_nodo_c.inputs['Material'].default_value = mat_marcos
    mat_nodo_c.parent = frame_marcos
    tree.links.new(join_cortes.outputs[0], mat_nodo_c.inputs['Geometry'])
    tree.links.new(mat_nodo_c.outputs['Geometry'], join.inputs[0])

    for obj_name in nombres_cortes:
        obj = bpy.data.objects.get(obj_name)
        if obj:
            oi = tree.nodes.new('GeometryNodeObjectInfo')
            oi.inputs['Object'].default_value = obj
            oi.transform_space = 'RELATIVE'
            oi.location = (-500, y_offset)
            oi.parent = frame_marcos
            tree.links.new(oi.outputs['Geometry'], join_cortes.inputs[0])
            y_offset -= 150

    # --- PILOTES ANCLADOS Y TECHO ---
    grid = tree.nodes.new('GeometryNodeMeshGrid')
    grid.inputs['Size X'].default_value = GRID_X
    grid.inputs['Size Y'].default_value = GRID_Y
    grid.inputs['Vertices X'].default_value = 4
    grid.inputs['Vertices Y'].default_value = 4
    grid.location = (-1000, -1000)
    grid.parent = frame_pilotes

    cyl = tree.nodes.new('GeometryNodeMeshCylinder')
    cyl.inputs['Radius'].default_value = RADIO_PILOTE
    cyl.inputs['Depth'].default_value = ALTO_PILOTE
    cyl.location = (-1000, -1200)
    cyl.parent = frame_pilotes

    iop = tree.nodes.new('GeometryNodeInstanceOnPoints')
    iop.location = (-500, -1100)
    iop.parent = frame_pilotes
    tree.links.new(grid.outputs['Mesh'], iop.inputs['Points'])
    tree.links.new(cyl.outputs['Mesh'], iop.inputs['Instance'])

    t_pilotes = tree.nodes.new('GeometryNodeTransform')
    t_pilotes.location = (-100, -1100)
    t_pilotes.inputs['Translation'].default_value = (9.8, 10.8, Z_PILOTE) 
    t_pilotes.parent = frame_pilotes
    tree.links.new(iop.outputs['Instances'], t_pilotes.inputs['Geometry'])
    
    mat_pilote = tree.nodes.new('GeometryNodeSetMaterial')
    mat_pilote.location = (200, -1100)
    mat_pilote.inputs['Material'].default_value = mat_marcos
    mat_pilote.parent = frame_pilotes
    tree.links.new(t_pilotes.outputs['Geometry'], mat_pilote.inputs['Geometry'])
    tree.links.new(mat_pilote.outputs['Geometry'], join.inputs[0])

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"✅ Iteración 3 Completada: {BLEND_OUT}")

if __name__ == "__main__":
    build_iter_3()
