import bpy

BLEND_IN = '/opt/zuly/Villa_Savoye_V9_Modelado3D.blend'
BLEND_OUT = '/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_1.blend'

# PILOTES PARAMÉTRICOS
RADIO_PILOTE = 0.15
ALTO_PILOTE = 3.3
GRID_X = 14.7  
GRID_Y = 16.2  

def build_iter_1():
    print("[ZULY] Abriendo V9 Tradicional...")
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    
    # 1. Identificar objetos detallados
    obj_n1 = bpy.data.objects.get("Primer Nivel")
    obj_n2 = bpy.data.objects.get("Segundo Nivel")
    obj_n3 = bpy.data.objects.get("Tercer Nivel")
    
    if not (obj_n1 and obj_n2 and obj_n3):
        print("ERROR: Faltan niveles en V9. El ensamble fallará.")
        return

    # Ocultar originales del viewport y render (solo serán fuentes de datos)
    for o in [obj_n1, obj_n2, obj_n3]:
        o.hide_viewport = True
        o.hide_render = True
        
    # 2. Crear Objeto Maestro de Nodos
    mesh = bpy.data.meshes.new("Savoye_Nodos_Mesh")
    master = bpy.data.objects.new("VILLA_SAVOYE_MAESTRA_NODOS", mesh)
    bpy.context.scene.collection.objects.link(master)
    
    bpy.context.view_layer.objects.active = master
    master.select_set(True)
    
    mod = master.modifiers.new(name="ZULY_HIBRIDO_NODOS", type='NODES')
    tree = bpy.data.node_groups.new(name="Savoye_Nodos_Core", type='GeometryNodeTree')
    mod.node_group = tree
    
    # Inputs/Outputs obligatorios (Blender 3.6 API)
    tree.inputs.new('NodeSocketGeometry', 'Geometry')
    tree.outputs.new('NodeSocketGeometry', 'Geometry')
    in_node = tree.nodes.new('NodeGroupInput')
    in_node.location = (-1500, 0)
    out_node = tree.nodes.new('NodeGroupOutput')
    out_node.location = (1500, 0)
    
    join = tree.nodes.new('GeometryNodeJoinGeometry')
    join.location = (1000, 0)
    tree.links.new(join.outputs[0], out_node.inputs['Geometry'])
    
    # 3. Nodos Object Info (Inyección de mallas V9)
    y_offset = 300
    for idx, obj_ref in enumerate([obj_n1, obj_n2, obj_n3]):
        oi = tree.nodes.new('GeometryNodeObjectInfo')
        oi.inputs['Object'].default_value = obj_ref
        oi.transform_space = 'RELATIVE' # Toma la posición milimétrica del original
        oi.location = (-500, y_offset - (idx * 200))
        tree.links.new(oi.outputs['Geometry'], join.inputs[0])
        
    # 4. Generación PARAMÉTRICA de Pilotes
    print("[ZULY] Construyendo Pilotes Procedurales...")
    grid = tree.nodes.new('GeometryNodeMeshGrid')
    grid.inputs['Size X'].default_value = GRID_X
    grid.inputs['Size Y'].default_value = GRID_Y
    grid.inputs['Vertices X'].default_value = 4
    grid.inputs['Vertices Y'].default_value = 4
    grid.location = (-1000, -400)

    cyl = tree.nodes.new('GeometryNodeMeshCylinder')
    cyl.inputs['Radius'].default_value = RADIO_PILOTE
    cyl.inputs['Depth'].default_value = ALTO_PILOTE
    cyl.location = (-1000, -600)

    iop = tree.nodes.new('GeometryNodeInstanceOnPoints')
    iop.location = (-500, -500)
    tree.links.new(grid.outputs['Mesh'], iop.inputs['Points'])
    tree.links.new(cyl.outputs['Mesh'], iop.inputs['Instance'])

    t_pilotes = tree.nodes.new('GeometryNodeTransform')
    t_pilotes.location = (-100, -500)
    # Centrar los pilotes matemáticos bajo la losa tradicional (que está en X=9.8, Y=10.8)
    t_pilotes.inputs['Translation'].default_value = (9.8, 10.8, 1.65) 
    tree.links.new(iop.outputs['Instances'], t_pilotes.inputs['Geometry'])
    
    tree.links.new(t_pilotes.outputs['Geometry'], join.inputs[0])

    # Guardar
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"✅ Hibridación completada: {BLEND_OUT}")

if __name__ == "__main__":
    build_iter_1()
