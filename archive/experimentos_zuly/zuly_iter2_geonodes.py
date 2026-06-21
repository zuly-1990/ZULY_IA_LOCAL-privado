import bpy
import math

BLEND_IN = '/opt/zuly/Villa_Savoye_V9_Modelado3D.blend'
BLEND_OUT = '/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_2.blend'

# PARÁMETROS CORREGIDOS (Lógica de Uso)
RADIO_PILOTE = 0.15
ALTO_PILOTE = 3.5     # Altura corregida para tocar la losa
Z_PILOTE = 1.75       # Centro del pilote (la mitad de 3.5)
GRID_X = 14.7  
GRID_Y = 16.2  

def build_iter_2():
    print("[ZULY] Abriendo V9 Tradicional para Iter_2...")
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    
    # 1. Identificar TODOS los objetos arquitectónicos
    nombres_objetos = [
        "Primer Nivel", "Segundo Nivel", "Tercer Nivel",
        "Fachada principal", "Fachada derecho", "Fachada Izquierda", "Fachada opuesta",
        "Corte 01", "Corte 02", "Corte 03"
    ]
    
    objetos_validos = []
    for nombre in nombres_objetos:
        obj = bpy.data.objects.get(nombre)
        if obj:
            obj.hide_viewport = True
            obj.hide_render = True
            objetos_validos.append(obj)
        else:
            print(f"ADVERTENCIA: No se encontró '{nombre}' en V9.")

    # 2. Crear Objeto Maestro
    mesh = bpy.data.meshes.new("Savoye_Nodos_Mesh_Iter2")
    master = bpy.data.objects.new("VILLA_SAVOYE_MAESTRA_NODOS", mesh)
    bpy.context.scene.collection.objects.link(master)
    
    bpy.context.view_layer.objects.active = master
    master.select_set(True)
    
    mod = master.modifiers.new(name="ZULY_HABITABILIDAD", type='NODES')
    tree = bpy.data.node_groups.new(name="Savoye_Nodos_Core", type='GeometryNodeTree')
    mod.node_group = tree
    
    # Inputs/Outputs
    tree.inputs.new('NodeSocketGeometry', 'Geometry')
    tree.outputs.new('NodeSocketGeometry', 'Geometry')
    in_node = tree.nodes.new('NodeGroupInput')
    in_node.location = (-1500, 0)
    out_node = tree.nodes.new('NodeGroupOutput')
    out_node.location = (2000, 0)
    
    join = tree.nodes.new('GeometryNodeJoinGeometry')
    join.location = (1000, 0)
    
    # Nodo de Limpieza Topológica (Suelda caras dobles)
    weld = tree.nodes.new('GeometryNodeMergeByDistance')
    weld.location = (1500, 0)
    weld.inputs['Distance'].default_value = 0.001
    
    tree.links.new(join.outputs[0], weld.inputs['Geometry'])
    tree.links.new(weld.outputs['Geometry'], out_node.inputs['Geometry'])
    
    # 3. Importar Fachadas y Niveles
    y_offset = 800
    for idx, obj_ref in enumerate(objetos_validos):
        oi = tree.nodes.new('GeometryNodeObjectInfo')
        oi.inputs['Object'].default_value = obj_ref
        oi.transform_space = 'RELATIVE'
        oi.location = (-500, y_offset - (idx * 150))
        tree.links.new(oi.outputs['Geometry'], join.inputs[0])
        
    # 4. Pilotes Corregidos (Ya no flotan)
    print("[ZULY] Construyendo Pilotes Estructurales...")
    grid = tree.nodes.new('GeometryNodeMeshGrid')
    grid.inputs['Size X'].default_value = GRID_X
    grid.inputs['Size Y'].default_value = GRID_Y
    grid.inputs['Vertices X'].default_value = 4
    grid.inputs['Vertices Y'].default_value = 4
    grid.location = (-1000, -600)

    cyl = tree.nodes.new('GeometryNodeMeshCylinder')
    cyl.inputs['Radius'].default_value = RADIO_PILOTE
    cyl.inputs['Depth'].default_value = ALTO_PILOTE
    cyl.location = (-1000, -800)

    iop = tree.nodes.new('GeometryNodeInstanceOnPoints')
    iop.location = (-500, -700)
    tree.links.new(grid.outputs['Mesh'], iop.inputs['Points'])
    tree.links.new(cyl.outputs['Mesh'], iop.inputs['Instance'])

    t_pilotes = tree.nodes.new('GeometryNodeTransform')
    t_pilotes.location = (-100, -700)
    t_pilotes.inputs['Translation'].default_value = (9.8, 10.8, Z_PILOTE) 
    tree.links.new(iop.outputs['Instances'], t_pilotes.inputs['Geometry'])
    tree.links.new(t_pilotes.outputs['Geometry'], join.inputs[0])

    # 5. Placa de Terminado (Techo para que no llueva)
    print("[ZULY] Construyendo Cubierta Superior...")
    techo = tree.nodes.new('GeometryNodeMeshCube')
    techo.inputs['Size'].default_value = (19.6, 21.6, 0.3)
    t_techo = tree.nodes.new('GeometryNodeTransform')
    # Ubicación sobre el tercer nivel
    t_techo.inputs['Translation'].default_value = (9.8, 10.8, 9.7)
    tree.links.new(techo.outputs['Mesh'], t_techo.inputs['Geometry'])
    tree.links.new(t_techo.outputs['Geometry'], join.inputs[0])

    # 6. Escalera Helicoidal Paramétrica (Circulación)
    print("[ZULY] Construyendo Escalera de Circulación...")
    step = tree.nodes.new('GeometryNodeMeshCube')
    step.inputs['Size'].default_value = (1.2, 0.3, 0.05)
    
    t_offset = tree.nodes.new('GeometryNodeTransform')
    t_offset.inputs['Translation'].default_value = (1.5, 0, 0)
    tree.links.new(step.outputs['Mesh'], t_offset.inputs['Geometry'])

    line = tree.nodes.new('GeometryNodeMeshLine')
    line.inputs['Count'].default_value = 35
    line.inputs['Offset'].default_value = (0, 0, 0.185) # Altura de paso para llegar a 6.5m aprox
    
    idx = tree.nodes.new('GeometryNodeInputIndex')
    math_node = tree.nodes.new('ShaderNodeMath')
    math_node.operation = 'MULTIPLY'
    math_node.inputs[1].default_value = math.radians(10.28) # 360/35 grados
    tree.links.new(idx.outputs['Index'], math_node.inputs[0])
    
    cmb_rot = tree.nodes.new('ShaderNodeCombineXYZ')
    tree.links.new(math_node.outputs['Value'], cmb_rot.inputs['Z'])
    
    iop_stairs = tree.nodes.new('GeometryNodeInstanceOnPoints')
    tree.links.new(line.outputs['Mesh'], iop_stairs.inputs['Points'])
    tree.links.new(t_offset.outputs['Geometry'], iop_stairs.inputs['Instance'])
    tree.links.new(cmb_rot.outputs['Vector'], iop_stairs.inputs['Rotation'])
    
    t_stairs = tree.nodes.new('GeometryNodeTransform')
    # Ubicar la escalera en el centro del edificio
    t_stairs.inputs['Translation'].default_value = (9.8, 10.8, 0)
    tree.links.new(iop_stairs.outputs['Instances'], t_stairs.inputs['Geometry'])
    tree.links.new(t_stairs.outputs['Geometry'], join.inputs[0])

    # Guardar
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"✅ Iteración 2 Completada: {BLEND_OUT}")

if __name__ == "__main__":
    build_iter_2()
