import bpy

BLEND_IN = '/opt/zuly/Villa_Savoye_V9_Modelado3D.blend'
BLEND_OUT = '/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_7.blend'

RADIO_PILOTE = 0.15
ALTO_PILOTE = 3.3      
Z_PILOTE = 1.5         
GRID_X = 14.7  
GRID_Y = 16.2  
Z_CUBIERTA = 9.8       

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
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
    if bpy.context.active_object:
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.object.select_all(action='DESELECT')

def create_master_tree(mat_ladrillo, mat_marcos, mat_concreto):
    tree = bpy.data.node_groups.new(name="ZULY_SISTEMA_BIM_MAESTRO", type='GeometryNodeTree')
    
    # En Blender 3.6, los sockets se crean con inputs.new()
    tree.inputs.new('NodeSocketGeometry', 'Geometry')
    tree.inputs.new('NodeSocketInt', 'Piso_ID')
    tree.outputs.new('NodeSocketGeometry', 'Geometry')
    
    in_node = tree.nodes.new('NodeGroupInput'); in_node.location = (-1500, 0)
    out_node = tree.nodes.new('NodeGroupOutput'); out_node.location = (2500, 0)

    # Función helper para limpiar muros
    def setup_muros(frame_name, color, loc_y, obj_names):
        frame = tree.nodes.new('NodeFrame'); frame.name = frame_name; frame.label = frame_name; frame.use_custom_color = True; frame.color = color
        join = tree.nodes.new('GeometryNodeJoinGeometry'); join.location = (-500, loc_y); join.parent = frame
        weld = tree.nodes.new('GeometryNodeMergeByDistance'); weld.location = (-300, loc_y); weld.inputs['Distance'].default_value = 0.005; weld.parent = frame
        extrude = tree.nodes.new('GeometryNodeExtrudeMesh'); extrude.location = (-100, loc_y); extrude.inputs['Offset Scale'].default_value = 0.02; extrude.parent = frame
        mat = tree.nodes.new('GeometryNodeSetMaterial'); mat.location = (100, loc_y); mat.inputs['Material'].default_value = mat_ladrillo; mat.parent = frame
        tree.links.new(join.outputs[0], weld.inputs[0])
        tree.links.new(weld.outputs[0], extrude.inputs['Mesh'])
        tree.links.new(extrude.outputs['Mesh'], mat.inputs['Geometry'])
        
        y_loc = loc_y + 200
        for name in obj_names:
            obj = bpy.data.objects.get(name)
            if obj:
                oi = tree.nodes.new('GeometryNodeObjectInfo')
                oi.inputs['Object'].default_value = obj
                oi.transform_space = 'RELATIVE'
                oi.location = (-800, y_loc)
                oi.parent = frame
                tree.links.new(oi.outputs['Geometry'], join.inputs[0])
                y_loc -= 100
        return mat.outputs['Geometry']

    # --- PISO 1 (Pilotes + Muros) ---
    out_muros_1 = setup_muros("CARPETA: MUROS PISO 1", (0.8, 0.3, 0.1), 1000, ["Primer Nivel", "Corte 01"])
    f_pil = tree.nodes.new('NodeFrame'); f_pil.name = "CARPETA: PILOTES PISO 1"; f_pil.label = "CARPETA: PILOTES PISO 1"; f_pil.use_custom_color = True; f_pil.color = (0.2, 0.5, 0.8)
    grid = tree.nodes.new('GeometryNodeMeshGrid'); grid.location=(-800, 500); grid.parent=f_pil; grid.inputs['Size X'].default_value=GRID_X; grid.inputs['Size Y'].default_value=GRID_Y; grid.inputs['Vertices X'].default_value=4; grid.inputs['Vertices Y'].default_value=4
    cyl = tree.nodes.new('GeometryNodeMeshCylinder'); cyl.location=(-800, 350); cyl.parent=f_pil; cyl.inputs['Radius'].default_value=RADIO_PILOTE; cyl.inputs['Depth'].default_value=ALTO_PILOTE
    iop = tree.nodes.new('GeometryNodeInstanceOnPoints'); iop.location=(-600, 500); iop.parent=f_pil
    trans = tree.nodes.new('GeometryNodeTransform'); trans.location=(-400, 500); trans.parent=f_pil; trans.inputs['Translation'].default_value=(9.8, 10.8, Z_PILOTE)
    mat_p = tree.nodes.new('GeometryNodeSetMaterial'); mat_p.location=(-200, 500); mat_p.parent=f_pil; mat_p.inputs['Material'].default_value=mat_marcos
    tree.links.new(grid.outputs['Mesh'], iop.inputs['Points']); tree.links.new(cyl.outputs['Mesh'], iop.inputs['Instance'])
    tree.links.new(iop.outputs['Instances'], trans.inputs['Geometry']); tree.links.new(trans.outputs['Geometry'], mat_p.inputs['Geometry'])
    
    join_p1 = tree.nodes.new('GeometryNodeJoinGeometry'); join_p1.location = (400, 800)
    tree.links.new(out_muros_1, join_p1.inputs[0])
    tree.links.new(mat_p.outputs['Geometry'], join_p1.inputs[0])

    # --- PISO 2 ---
    out_muros_2 = setup_muros("CARPETA: MUROS PISO 2", (0.8, 0.4, 0.1), 0, ["Segundo Nivel", "Fachada principal", "Fachada derecho", "Fachada Izquierda", "Fachada opuesta", "Corte 02"])

    # --- PISO 3 (Muros + Cubierta) ---
    out_muros_3 = setup_muros("CARPETA: MUROS PISO 3", (0.8, 0.5, 0.1), -1000, ["Tercer Nivel", "Corte 03"])
    f_techo = tree.nodes.new('NodeFrame'); f_techo.name = "CARPETA: PLACA TECHO"; f_techo.label = "CARPETA: PLACA TECHO"; f_techo.use_custom_color = True; f_techo.color = (0.3, 0.3, 0.3)
    cube = tree.nodes.new('GeometryNodeMeshCube'); cube.location=(-800, -1500); cube.parent=f_techo; cube.inputs['Size'].default_value=(22.0, 22.0, 0.25)
    trans_c = tree.nodes.new('GeometryNodeTransform'); trans_c.location=(-600, -1500); trans_c.parent=f_techo; trans_c.inputs['Translation'].default_value=(9.8, 10.8, Z_CUBIERTA)
    mat_c = tree.nodes.new('GeometryNodeSetMaterial'); mat_c.location=(-400, -1500); mat_c.parent=f_techo; mat_c.inputs['Material'].default_value=mat_concreto
    tree.links.new(cube.outputs['Mesh'], trans_c.inputs['Geometry']); tree.links.new(trans_c.outputs['Geometry'], mat_c.inputs['Geometry'])
    
    join_p3 = tree.nodes.new('GeometryNodeJoinGeometry'); join_p3.location = (400, -1200)
    tree.links.new(out_muros_3, join_p3.inputs[0])
    tree.links.new(mat_c.outputs['Geometry'], join_p3.inputs[0])

    # --- LÓGICA DEL INTERRUPTOR (SWITCH) ---
    f_switch = tree.nodes.new('NodeFrame'); f_switch.name = "SELECTOR BIM OUTLINER"; f_switch.label = "SELECTOR BIM OUTLINER"; f_switch.use_custom_color = True; f_switch.color = (0.6, 0.1, 0.8)
    
    comp1 = tree.nodes.new('FunctionNodeCompare'); comp1.data_type = 'INT'; comp1.operation = 'EQUAL'; comp1.inputs[1].default_value = 1; comp1.location = (1000, 400); comp1.parent = f_switch
    comp2 = tree.nodes.new('FunctionNodeCompare'); comp2.data_type = 'INT'; comp2.operation = 'EQUAL'; comp2.inputs[1].default_value = 2; comp2.location = (1000, 200); comp2.parent = f_switch
    comp3 = tree.nodes.new('FunctionNodeCompare'); comp3.data_type = 'INT'; comp3.operation = 'EQUAL'; comp3.inputs[1].default_value = 3; comp3.location = (1000, 0); comp3.parent = f_switch
    
    sw1 = tree.nodes.new('GeometryNodeSwitch'); sw1.location = (1300, 400); sw1.parent = f_switch
    sw2 = tree.nodes.new('GeometryNodeSwitch'); sw2.location = (1500, 200); sw2.parent = f_switch
    sw3 = tree.nodes.new('GeometryNodeSwitch'); sw3.location = (1700, 0); sw3.parent = f_switch
    
    # Conectar Group Input (Piso_ID) a los compares
    tree.links.new(in_node.outputs['Piso_ID'], comp1.inputs[0])
    tree.links.new(in_node.outputs['Piso_ID'], comp2.inputs[0])
    tree.links.new(in_node.outputs['Piso_ID'], comp3.inputs[0])
    
    # Cadena de Switches: Si no es P3, manda vacío. Si es P3 manda join_p3. Si es P2, manda out_muros_2. Si es P1, manda join_p1.
    tree.links.new(comp3.outputs[0], sw3.inputs['Switch'])
    tree.links.new(join_p3.outputs[0], sw3.inputs['True'])
    
    tree.links.new(comp2.outputs[0], sw2.inputs['Switch'])
    tree.links.new(sw3.outputs[0], sw2.inputs['False'])
    tree.links.new(out_muros_2, sw2.inputs['True'])
    
    tree.links.new(comp1.outputs[0], sw1.inputs['Switch'])
    tree.links.new(sw2.outputs[0], sw1.inputs['False'])
    tree.links.new(join_p1.outputs[0], sw1.inputs['True'])
    
    tree.links.new(sw1.outputs[0], out_node.inputs['Geometry'])
    
    return tree

def build_iter_7():
    print("[ZULY] Construyendo Iteración 7 (Arquitectura Switch Maestro)...")
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    apply_scale_to_all()
    mat_ladrillo, mat_marcos, mat_concreto = create_materials()

    master_col = bpy.context.scene.collection
    col_oculta = bpy.data.collections.new("V9_ORIGINALES_OCULTOS")
    master_col.children.link(col_oculta)
    for obj in bpy.context.scene.objects:
        if obj.type in ['MESH', 'EMPTY', 'CURVE']:
            for c in obj.users_collection: c.objects.unlink(obj)
            col_oculta.objects.link(obj)
    col_oculta.hide_viewport = True; col_oculta.hide_render = True
    if bpy.data.collections.get("Collection"): bpy.data.collections.get("Collection").hide_viewport = True

    col_piso1 = bpy.data.collections.new("PISO_1_Base")
    col_piso2 = bpy.data.collections.new("PISO_2_Principal")
    col_piso3 = bpy.data.collections.new("PISO_3_Cubierta")
    master_col.children.link(col_piso1); master_col.children.link(col_piso2); master_col.children.link(col_piso3)

    master_tree = create_master_tree(mat_ladrillo, mat_marcos, mat_concreto)

    # CREACIÓN DE LOS OBJETOS FINALES EN LAS COLECCIONES
    # Objeto Piso 1
    obj_p1 = bpy.data.objects.new("ZULY_Piso_1_Completo", bpy.data.meshes.new("Malla_BIM"))
    col_piso1.objects.link(obj_p1)
    mod1 = obj_p1.modifiers.new("GN_SISTEMA_MAESTRO", 'NODES')
    mod1.node_group = master_tree
    mod1["Socket_1"] = 1 # Piso_ID en Blender API interna para el primer socket agregado suele ser Socket_1 o Socket_0. Lo mejor es setearlo por el nombre si es posible, o por índice.
    
    # En Blender 3.x, los sockets de inputs del modifier se setean como mod["Input_2"] = 1
    # Pero el identificador puede variar. Lo buscaremos iterando:
    def set_piso_id(mod, val):
        for identifier in mod.keys():
            if "Input_" in identifier or "Socket_" in identifier:
                try:
                    mod[identifier] = val
                except:
                    pass

    set_piso_id(mod1, 1)

    # Objeto Piso 2
    obj_p2 = bpy.data.objects.new("ZULY_Piso_2_Completo", bpy.data.meshes.new("Malla_BIM"))
    col_piso2.objects.link(obj_p2)
    mod2 = obj_p2.modifiers.new("GN_SISTEMA_MAESTRO", 'NODES')
    mod2.node_group = master_tree
    set_piso_id(mod2, 2)

    # Objeto Piso 3
    obj_p3 = bpy.data.objects.new("ZULY_Piso_3_Completo", bpy.data.meshes.new("Malla_BIM"))
    col_piso3.objects.link(obj_p3)
    mod3 = obj_p3.modifiers.new("GN_SISTEMA_MAESTRO", 'NODES')
    mod3.node_group = master_tree
    set_piso_id(mod3, 3)

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"✅ Iteración 7 Completada: {BLEND_OUT}")

if __name__ == "__main__":
    build_iter_7()
