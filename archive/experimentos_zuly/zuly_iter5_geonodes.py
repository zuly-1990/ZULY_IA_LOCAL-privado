import bpy

BLEND_IN = '/opt/zuly/Villa_Savoye_V9_Modelado3D.blend'
BLEND_OUT = '/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_5.blend'

RADIO_PILOTE = 0.15
ALTO_PILOTE = 3.8
Z_PILOTE = 1.9
GRID_X = 14.7  
GRID_Y = 16.2  

def create_materials():
    mat_ladrillo = bpy.data.materials.new(name="Ladrillo_Vista")
    mat_ladrillo.use_nodes = True
    nodes = mat_ladrillo.node_tree.nodes
    links = mat_ladrillo.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    brick = nodes.new("ShaderNodeTexBrick")
    brick.inputs['Color1'].default_value = (0.6, 0.2, 0.1, 1)
    brick.inputs['Color2'].default_value = (0.4, 0.15, 0.08, 1)
    brick.inputs['Scale'].default_value = 15.0
    links.new(brick.outputs['Color'], bsdf.inputs['Base Color'])
    bump = nodes.new("ShaderNodeBump")
    bump.inputs['Distance'].default_value = 0.05
    links.new(brick.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    mat_marcos = bpy.data.materials.new(name="Marcos_Metal")
    mat_marcos.use_nodes = True
    bsdf_m = mat_marcos.node_tree.nodes.get("Principled BSDF")
    bsdf_m.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1)
    bsdf_m.inputs['Metallic'].default_value = 0.8
    
    mat_concreto = bpy.data.materials.new(name="Placa_Concreto")
    mat_concreto.use_nodes = True
    bsdf_c = mat_concreto.node_tree.nodes.get("Principled BSDF")
    bsdf_c.inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1)

    return mat_ladrillo, mat_marcos, mat_concreto

def apply_scale_to_all():
    # Evita deformaciones matemáticas aplicando rotación y escala a los originales
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
    if bpy.context.active_object:
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.object.select_all(action='DESELECT')

def create_muros_tree(name, source_objects, material, frame_name, frame_color):
    # Crea un árbol GN hermoso y enmarcado para que los nodos no estén "perdidos"
    tree = bpy.data.node_groups.new(name=name, type='GeometryNodeTree')
    tree.inputs.new('NodeSocketGeometry', 'Geometry')
    tree.outputs.new('NodeSocketGeometry', 'Geometry')
    
    out_node = tree.nodes.new('NodeGroupOutput')
    out_node.location = (800, 0)
    
    frame = tree.nodes.new('NodeFrame')
    frame.name = frame_name
    frame.label = frame_name
    frame.use_custom_color = True
    frame.color = frame_color
    
    join = tree.nodes.new('GeometryNodeJoinGeometry')
    join.location = (0, 0)
    join.parent = frame
    
    weld = tree.nodes.new('GeometryNodeMergeByDistance')
    weld.location = (200, 0)
    weld.inputs['Distance'].default_value = 0.005
    weld.parent = frame
    
    extrude = tree.nodes.new('GeometryNodeExtrudeMesh')
    extrude.location = (400, 0)
    extrude.inputs['Offset Scale'].default_value = 0.02
    extrude.parent = frame
    
    mat_node = tree.nodes.new('GeometryNodeSetMaterial')
    mat_node.location = (600, 0)
    mat_node.inputs['Material'].default_value = material
    mat_node.parent = frame
    
    tree.links.new(join.outputs['Geometry'], weld.inputs['Geometry'])
    tree.links.new(weld.outputs['Geometry'], extrude.inputs['Mesh'])
    tree.links.new(extrude.outputs['Mesh'], mat_node.inputs['Geometry'])
    tree.links.new(mat_node.outputs['Geometry'], out_node.inputs['Geometry'])
    
    # Importar los objetos V9 ocultos
    y_loc = 200
    for obj_name in source_objects:
        obj = bpy.data.objects.get(obj_name)
        if obj:
            oi = tree.nodes.new('GeometryNodeObjectInfo')
            oi.inputs['Object'].default_value = obj
            oi.transform_space = 'RELATIVE' # Toma la pos real ya saneada
            oi.location = (-300, y_loc)
            oi.parent = frame
            tree.links.new(oi.outputs['Geometry'], join.inputs['Geometry'])
            y_loc -= 150
            
    return tree

def build_iter_5():
    print("[ZULY] Construyendo Iteración 5 (Saneamiento BIM y Nodos Visibles)...")
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    
    apply_scale_to_all()
    mat_ladrillo, mat_marcos, mat_concreto = create_materials()

    # Organizar el Outliner: Mover basura a colección oculta
    master_col = bpy.context.scene.collection
    col_oculta = bpy.data.collections.new("V9_ORIGINALES_OCULTOS")
    master_col.children.link(col_oculta)
    
    for obj in bpy.context.scene.objects:
        if obj.type in ['MESH', 'EMPTY', 'CURVE']:
            for c in obj.users_collection:
                c.objects.unlink(obj)
            col_oculta.objects.link(obj)
    col_oculta.hide_viewport = True
    col_oculta.hide_render = True
    
    if bpy.data.collections.get("Collection"):
        bpy.data.collections.get("Collection").hide_viewport = True

    # Colecciones Maestras del Usuario
    col_piso1 = bpy.data.collections.new("PISO_1_Base")
    col_piso2 = bpy.data.collections.new("PISO_2_Principal")
    col_piso3 = bpy.data.collections.new("PISO_3_Cubierta")
    master_col.children.link(col_piso1)
    master_col.children.link(col_piso2)
    master_col.children.link(col_piso3)

    # --- OBJETOS DE PISO 1 ---
    mesh_p1 = bpy.data.meshes.new("Mesh_Piso1")
    obj_p1 = bpy.data.objects.new("Muros_Piso_1", mesh_p1)
    col_piso1.objects.link(obj_p1)
    mod1 = obj_p1.modifiers.new("GN", 'NODES')
    mod1.node_group = create_muros_tree("Nodos_Piso1", ["Primer Nivel", "Corte 01"], mat_ladrillo, "CARPETA: MUROS PISO 1", (0.8, 0.3, 0.1))

    # Pilotes en Piso 1
    obj_pilotes = bpy.data.objects.new("Columnas_Matematicas_Piso1", bpy.data.meshes.new("Malla_Pilotes"))
    col_piso1.objects.link(obj_pilotes)
    mod_pilotes = obj_pilotes.modifiers.new("GN", 'NODES')
    t_pilotes = bpy.data.node_groups.new("Generador_Pilotes", type='GeometryNodeTree')
    mod_pilotes.node_group = t_pilotes
    t_pilotes.inputs.new('NodeSocketGeometry', 'Geometry')
    t_pilotes.outputs.new('NodeSocketGeometry', 'Geometry')
    frame_p = t_pilotes.nodes.new('NodeFrame')
    frame_p.name = "CARPETA: PILOTES"
    frame_p.label = "CARPETA: PILOTES"
    frame_p.use_custom_color = True; frame_p.color = (0.2, 0.5, 0.8)
    grid = t_pilotes.nodes.new('GeometryNodeMeshGrid'); grid.parent=frame_p
    grid.inputs['Size X'].default_value = GRID_X; grid.inputs['Size Y'].default_value = GRID_Y
    grid.inputs['Vertices X'].default_value = 4; grid.inputs['Vertices Y'].default_value = 4
    cyl = t_pilotes.nodes.new('GeometryNodeMeshCylinder'); cyl.parent=frame_p
    cyl.inputs['Radius'].default_value = RADIO_PILOTE; cyl.inputs['Depth'].default_value = ALTO_PILOTE
    iop = t_pilotes.nodes.new('GeometryNodeInstanceOnPoints'); iop.parent=frame_p
    trans = t_pilotes.nodes.new('GeometryNodeTransform'); trans.parent=frame_p
    trans.inputs['Translation'].default_value = (9.8, 10.8, Z_PILOTE)
    mat_p = t_pilotes.nodes.new('GeometryNodeSetMaterial'); mat_p.parent=frame_p
    mat_p.inputs['Material'].default_value = mat_marcos
    out_p = t_pilotes.nodes.new('NodeGroupOutput')
    t_pilotes.links.new(grid.outputs['Mesh'], iop.inputs['Points'])
    t_pilotes.links.new(cyl.outputs['Mesh'], iop.inputs['Instance'])
    t_pilotes.links.new(iop.outputs['Instances'], trans.inputs['Geometry'])
    t_pilotes.links.new(trans.outputs['Geometry'], mat_p.inputs['Geometry'])
    t_pilotes.links.new(mat_p.outputs['Geometry'], out_p.inputs['Geometry'])

    # --- OBJETOS DE PISO 2 ---
    obj_p2 = bpy.data.objects.new("Muros_y_Fachadas_Piso_2", bpy.data.meshes.new("Mesh_Piso2"))
    col_piso2.objects.link(obj_p2)
    mod2 = obj_p2.modifiers.new("GN", 'NODES')
    mod2.node_group = create_muros_tree("Nodos_Piso2", ["Segundo Nivel", "Fachada principal", "Fachada derecho", "Fachada Izquierda", "Fachada opuesta", "Corte 02"], mat_ladrillo, "CARPETA: FACHADAS PISO 2", (0.8, 0.4, 0.1))

    # --- OBJETOS DE PISO 3 ---
    obj_p3 = bpy.data.objects.new("Muros_Piso_3", bpy.data.meshes.new("Mesh_Piso3"))
    col_piso3.objects.link(obj_p3)
    mod3 = obj_p3.modifiers.new("GN", 'NODES')
    mod3.node_group = create_muros_tree("Nodos_Piso3", ["Tercer Nivel", "Corte 03"], mat_ladrillo, "CARPETA: MUROS PISO 3", (0.8, 0.5, 0.1))

    # Placa Final
    obj_placa = bpy.data.objects.new("Placa_Cubierta_Final", bpy.data.meshes.new("Mesh_Placa"))
    col_piso3.objects.link(obj_placa)
    mod_placa = obj_placa.modifiers.new("GN", 'NODES')
    t_placa = bpy.data.node_groups.new("Generador_Placa", type='GeometryNodeTree')
    mod_placa.node_group = t_placa
    t_placa.inputs.new('NodeSocketGeometry', 'Geometry')
    t_placa.outputs.new('NodeSocketGeometry', 'Geometry')
    frame_pl = t_placa.nodes.new('NodeFrame'); frame_pl.name = "CARPETA: PLACA TECHO"; frame_pl.label = "CARPETA: PLACA TECHO"; frame_pl.use_custom_color = True; frame_pl.color = (0.3, 0.3, 0.3)
    cube = t_placa.nodes.new('GeometryNodeMeshCube'); cube.parent=frame_pl
    cube.inputs['Size'].default_value = (22.0, 22.0, 0.25)
    trans_c = t_placa.nodes.new('GeometryNodeTransform'); trans_c.parent=frame_pl
    trans_c.inputs['Translation'].default_value = (9.8, 10.8, 6.7)
    mat_c = t_placa.nodes.new('GeometryNodeSetMaterial'); mat_c.parent=frame_pl
    mat_c.inputs['Material'].default_value = mat_concreto
    out_placa = t_placa.nodes.new('NodeGroupOutput')
    t_placa.links.new(cube.outputs['Mesh'], trans_c.inputs['Geometry'])
    t_placa.links.new(trans_c.outputs['Geometry'], mat_c.inputs['Geometry'])
    t_placa.links.new(mat_c.outputs['Geometry'], out_placa.inputs['Geometry'])

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"✅ Iteración 5 Completada: {BLEND_OUT}")

if __name__ == "__main__":
    build_iter_5()
