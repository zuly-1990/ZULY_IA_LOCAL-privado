import bpy

BLEND_IN = '/opt/zuly/Villa_Savoye_V9_Modelado3D.blend'
BLEND_OUT = '/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_4.blend'

RADIO_PILOTE = 0.15
ALTO_PILOTE = 3.8
Z_PILOTE = 1.9
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
    brick.inputs['Color1'].default_value = (0.6, 0.2, 0.1, 1)
    brick.inputs['Color2'].default_value = (0.4, 0.15, 0.08, 1)
    brick.inputs['Mortar'].default_value = (0.8, 0.8, 0.8, 1)
    brick.inputs['Scale'].default_value = 15.0
    
    links.new(brick.outputs['Color'], bsdf.inputs['Base Color'])
    bump = nodes.new("ShaderNodeBump")
    bump.inputs['Distance'].default_value = 0.05
    links.new(brick.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # 2. Marcos de Puertas y Ventanas
    mat_marcos = bpy.data.materials.new(name="Marcos_Metal")
    mat_marcos.use_nodes = True
    bsdf_m = mat_marcos.node_tree.nodes.get("Principled BSDF")
    bsdf_m.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1)
    bsdf_m.inputs['Metallic'].default_value = 0.8
    bsdf_m.inputs['Roughness'].default_value = 0.3
    
    # 3. Concreto (Placa Cubierta)
    mat_concreto = bpy.data.materials.new(name="Placa_Concreto")
    mat_concreto.use_nodes = True
    bsdf_c = mat_concreto.node_tree.nodes.get("Principled BSDF")
    bsdf_c.inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1)
    bsdf_c.inputs['Roughness'].default_value = 0.9

    return mat_ladrillo, mat_marcos, mat_concreto

def create_cleaning_nodetree(mat_to_assign):
    # Crea un árbol de nodos reutilizable para limpiar mallas importadas
    tree = bpy.data.node_groups.new(name="Limpieza_Malla_GN", type='GeometryNodeTree')
    tree.inputs.new('NodeSocketGeometry', 'Geometry')
    tree.outputs.new('NodeSocketGeometry', 'Geometry')
    
    in_node = tree.nodes.new('NodeGroupInput')
    out_node = tree.nodes.new('NodeGroupOutput')
    
    weld = tree.nodes.new('GeometryNodeMergeByDistance')
    weld.inputs['Distance'].default_value = 0.005
    
    extrude = tree.nodes.new('GeometryNodeExtrudeMesh')
    extrude.inputs['Offset Scale'].default_value = 0.02
    
    mat_node = tree.nodes.new('GeometryNodeSetMaterial')
    mat_node.inputs['Material'].default_value = mat_to_assign
    
    tree.links.new(in_node.outputs['Geometry'], weld.inputs['Geometry'])
    tree.links.new(weld.outputs['Geometry'], extrude.inputs['Mesh'])
    tree.links.new(extrude.outputs['Mesh'], mat_node.inputs['Geometry'])
    tree.links.new(mat_node.outputs['Geometry'], out_node.inputs['Geometry'])
    
    return tree

def build_iter_4():
    print("[ZULY] Construyendo Iteración 4 (Arquitectura BIM)...")
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    
    mat_ladrillo, mat_marcos, mat_concreto = create_materials()
    
    tree_ladrillo = create_cleaning_nodetree(mat_ladrillo)
    tree_marcos = create_cleaning_nodetree(mat_marcos)

    # Crear Colecciones
    master_col = bpy.context.scene.collection
    col_piso1 = bpy.data.collections.new("PISO_1_Base")
    col_piso2 = bpy.data.collections.new("PISO_2_Principal")
    col_piso3 = bpy.data.collections.new("PISO_3_Cubierta")
    master_col.children.link(col_piso1)
    master_col.children.link(col_piso2)
    master_col.children.link(col_piso3)

    # Clasificación de objetos V9
    obj_piso1 = ["Primer Nivel", "Corte 01"]
    obj_piso2 = ["Segundo Nivel", "Fachada principal", "Fachada derecho", "Fachada Izquierda", "Fachada opuesta", "Corte 02"]
    obj_piso3 = ["Tercer Nivel", "Corte 03"]

    def process_objects(obj_names, target_col, tree_a, tree_b):
        for name in obj_names:
            obj = bpy.data.objects.get(name)
            if obj:
                # Mover a colección destino
                for old_col in obj.users_collection:
                    old_col.objects.unlink(obj)
                target_col.objects.link(obj)
                
                # Asignar modificador GN (Limpieza y Material)
                mod = obj.modifiers.new(name="Limpieza_GN", type='NODES')
                # Si es corte, usar tree_marcos, si es muro/fachada usar tree_ladrillo
                if "Corte" in name:
                    mod.node_group = tree_b
                else:
                    mod.node_group = tree_a
                
                # Asegurar visibilidad
                obj.hide_viewport = False
                obj.hide_render = False

    process_objects(obj_piso1, col_piso1, tree_ladrillo, tree_marcos)
    process_objects(obj_piso2, col_piso2, tree_ladrillo, tree_marcos)
    process_objects(obj_piso3, col_piso3, tree_ladrillo, tree_marcos)

    # Ocultar la colección principal antigua que tenía todo mezclado (Collection)
    if bpy.data.collections.get("Collection"):
        bpy.data.collections.get("Collection").hide_viewport = True

    # --- PILOTES EN PISO 1 ---
    mesh_pilotes = bpy.data.meshes.new("Malla_Pilotes_GN")
    obj_pilotes = bpy.data.objects.new("Columnas_Estructurales", mesh_pilotes)
    col_piso1.objects.link(obj_pilotes)
    
    mod_pilotes = obj_pilotes.modifiers.new(name="GN_Pilotes", type='NODES')
    t_pilotes = bpy.data.node_groups.new("Generador_Pilotes", type='GeometryNodeTree')
    mod_pilotes.node_group = t_pilotes
    
    t_pilotes.inputs.new('NodeSocketGeometry', 'Geometry')
    t_pilotes.outputs.new('NodeSocketGeometry', 'Geometry')
    in_n = t_pilotes.nodes.new('NodeGroupInput')
    out_n = t_pilotes.nodes.new('NodeGroupOutput')
    
    grid = t_pilotes.nodes.new('GeometryNodeMeshGrid')
    grid.inputs['Size X'].default_value = GRID_X
    grid.inputs['Size Y'].default_value = GRID_Y
    grid.inputs['Vertices X'].default_value = 4
    grid.inputs['Vertices Y'].default_value = 4
    
    cyl = t_pilotes.nodes.new('GeometryNodeMeshCylinder')
    cyl.inputs['Radius'].default_value = RADIO_PILOTE
    cyl.inputs['Depth'].default_value = ALTO_PILOTE
    
    iop = t_pilotes.nodes.new('GeometryNodeInstanceOnPoints')
    t_pilotes.links.new(grid.outputs['Mesh'], iop.inputs['Points'])
    t_pilotes.links.new(cyl.outputs['Mesh'], iop.inputs['Instance'])
    
    trans = t_pilotes.nodes.new('GeometryNodeTransform')
    trans.inputs['Translation'].default_value = (9.8, 10.8, Z_PILOTE)
    t_pilotes.links.new(iop.outputs['Instances'], trans.inputs['Geometry'])
    
    mat_p = t_pilotes.nodes.new('GeometryNodeSetMaterial')
    mat_p.inputs['Material'].default_value = mat_marcos
    t_pilotes.links.new(trans.outputs['Geometry'], mat_p.inputs['Geometry'])
    t_pilotes.links.new(mat_p.outputs['Geometry'], out_n.inputs['Geometry'])


    # --- PLACA FINAL EN PISO 3 ---
    mesh_placa = bpy.data.meshes.new("Malla_Placa_Cubierta")
    obj_placa = bpy.data.objects.new("Placa_Cubierta_Final", mesh_placa)
    col_piso3.objects.link(obj_placa)
    
    mod_placa = obj_placa.modifiers.new(name="GN_Placa", type='NODES')
    t_placa = bpy.data.node_groups.new("Generador_Placa", type='GeometryNodeTree')
    mod_placa.node_group = t_placa
    t_placa.inputs.new('NodeSocketGeometry', 'Geometry')
    t_placa.outputs.new('NodeSocketGeometry', 'Geometry')
    out_placa = t_placa.nodes.new('NodeGroupOutput')
    
    cube = t_placa.nodes.new('GeometryNodeMeshCube')
    # Tamaño suficiente para tapar el edificio (aprox 21x20m y 0.2m de grosor)
    cube.inputs['Size'].default_value = (22.0, 22.0, 0.25)
    
    trans_c = t_placa.nodes.new('GeometryNodeTransform')
    # Ubicarla arriba del nivel 3 (Z=7.0m aprox)
    trans_c.inputs['Translation'].default_value = (9.8, 10.8, 6.7)
    
    mat_c = t_placa.nodes.new('GeometryNodeSetMaterial')
    mat_c.inputs['Material'].default_value = mat_concreto
    
    t_placa.links.new(cube.outputs['Mesh'], trans_c.inputs['Geometry'])
    t_placa.links.new(trans_c.outputs['Geometry'], mat_c.inputs['Geometry'])
    t_placa.links.new(mat_c.outputs['Geometry'], out_placa.inputs['Geometry'])


    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"✅ Iteración 4 Completada: {BLEND_OUT}")

if __name__ == "__main__":
    build_iter_4()
