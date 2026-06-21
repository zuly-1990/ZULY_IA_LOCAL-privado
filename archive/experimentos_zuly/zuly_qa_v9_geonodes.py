import bpy
import math
import sys
import time

BLEND_OUT = '/opt/zuly/ZULY_VILLA_SAVOYE_PERFECT_V30.blend'

# MEDIDAS ESTRICTAS DE V05 (POSICIONES) y V09 (DETALLE TRADICIONAL)
DIM_LOSA = (19.6, 21.6, 0.3)
RADIO_PILOTE = 0.15
ALTO_PILOTE = 3.5
GRID_X = 14.7  # 4 pilotes distanciados 4.9m
GRID_Y = 16.2  # 4 pilotes distanciados 5.4m
Z_N1 = 3.5
Z_N2 = 6.7

def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def test_api_blender_36(tree):
    # En Blender 3.6 es OBLIGATORIO tener un GroupInput y Output conectados a Geometry.
    tree.inputs.new('NodeSocketGeometry', 'Geometry')
    tree.outputs.new('NodeSocketGeometry', 'Geometry')

    node_in = tree.nodes.new('NodeGroupInput')
    node_in.location = (-1200, 0)
    
    node_out = tree.nodes.new('NodeGroupOutput')
    node_out.location = (1200, 0)
    
    join = tree.nodes.new('GeometryNodeJoinGeometry')
    join.location = (900, 0)
    
    tree.links.new(node_in.outputs['Geometry'], join.inputs[0])
    tree.links.new(join.outputs['Geometry'], node_out.inputs['Geometry'])
    
    return join

def add_losa(tree, join_node, z_loc):
    losa = tree.nodes.new('GeometryNodeMeshCube')
    losa.inputs['Size'].default_value = DIM_LOSA
    t_losa = tree.nodes.new('GeometryNodeTransform')
    t_losa.inputs['Translation'].default_value = (0, 0, z_loc)
    tree.links.new(losa.outputs['Mesh'], t_losa.inputs['Geometry'])
    tree.links.new(t_losa.outputs['Geometry'], join_node.inputs[0])

def add_pilotes(tree, join_node):
    grid = tree.nodes.new('GeometryNodeMeshGrid')
    grid.inputs['Size X'].default_value = GRID_X
    grid.inputs['Size Y'].default_value = GRID_Y
    grid.inputs['Vertices X'].default_value = 4
    grid.inputs['Vertices Y'].default_value = 4

    cyl = tree.nodes.new('GeometryNodeMeshCylinder')
    cyl.inputs['Radius'].default_value = RADIO_PILOTE
    cyl.inputs['Depth'].default_value = ALTO_PILOTE

    iop = tree.nodes.new('GeometryNodeInstanceOnPoints')
    tree.links.new(grid.outputs['Mesh'], iop.inputs['Points'])
    tree.links.new(cyl.outputs['Mesh'], iop.inputs['Instance'])

    t_pilotes = tree.nodes.new('GeometryNodeTransform')
    t_pilotes.inputs['Translation'].default_value = (0, 0, 1.75) # Centro de Z=3.5
    tree.links.new(iop.outputs['Instances'], t_pilotes.inputs['Geometry'])
    tree.links.new(t_pilotes.outputs['Geometry'], join_node.inputs[0])

def add_muros_con_ventanas(tree, join_node):
    # Ventana corrida (fenêtre en longueur)
    # Muros Norte y Sur divididos en parte baja y alta
    for y_loc in [10.65, -10.65]:
        m_inf = tree.nodes.new('GeometryNodeMeshCube')
        m_inf.inputs['Size'].default_value = (19.6, 0.3, 1.0)
        t_inf = tree.nodes.new('GeometryNodeTransform')
        t_inf.inputs['Translation'].default_value = (0, y_loc, Z_N1 + 0.5) # De 3.5 a 4.5
        tree.links.new(m_inf.outputs['Mesh'], t_inf.inputs['Geometry'])
        tree.links.new(t_inf.outputs['Geometry'], join_node.inputs[0])

        m_sup = tree.nodes.new('GeometryNodeMeshCube')
        m_sup.inputs['Size'].default_value = (19.6, 0.3, 1.0)
        t_sup = tree.nodes.new('GeometryNodeTransform')
        t_sup.inputs['Translation'].default_value = (0, y_loc, Z_N1 + 2.7) # De 5.7 a 6.7
        tree.links.new(m_sup.outputs['Mesh'], t_sup.inputs['Geometry'])
        tree.links.new(t_sup.outputs['Geometry'], join_node.inputs[0])

    # Muros Este y Oeste (Paredes completas)
    for x_loc in [9.65, -9.65]:
        m_lat = tree.nodes.new('GeometryNodeMeshCube')
        m_lat.inputs['Size'].default_value = (0.3, 21.6, 3.2)
        t_lat = tree.nodes.new('GeometryNodeTransform')
        t_lat.inputs['Translation'].default_value = (x_loc, 0, Z_N1 + 1.6) # Centro en z=5.1
        tree.links.new(m_lat.outputs['Mesh'], t_lat.inputs['Geometry'])
        tree.links.new(t_lat.outputs['Geometry'], join_node.inputs[0])

def add_escalera_parametrica(tree, join_node):
    step = tree.nodes.new('GeometryNodeMeshCube')
    step.inputs['Size'].default_value = (0.9, 0.28, 0.04)
    
    t_offset = tree.nodes.new('GeometryNodeTransform')
    t_offset.inputs['Translation'].default_value = (1.8, 0, 0)
    tree.links.new(step.outputs['Mesh'], t_offset.inputs['Geometry'])

    line = tree.nodes.new('GeometryNodeMeshLine')
    line.inputs['Count'].default_value = 35
    line.inputs['Offset'].default_value = (0, 0, 0.1914)
    
    idx = tree.nodes.new('GeometryNodeInputIndex')
    math_node = tree.nodes.new('ShaderNodeMath')
    math_node.operation = 'MULTIPLY'
    math_node.inputs[1].default_value = math.radians(10)
    tree.links.new(idx.outputs['Index'], math_node.inputs[0])
    
    cmb_rot = tree.nodes.new('ShaderNodeCombineXYZ')
    tree.links.new(math_node.outputs['Value'], cmb_rot.inputs['Z'])
    
    iop = tree.nodes.new('GeometryNodeInstanceOnPoints')
    tree.links.new(line.outputs['Mesh'], iop.inputs['Points'])
    tree.links.new(t_offset.outputs['Geometry'], iop.inputs['Instance'])
    tree.links.new(cmb_rot.outputs['Vector'], iop.inputs['Rotation'])
    
    t_final = tree.nodes.new('GeometryNodeTransform')
    t_final.inputs['Translation'].default_value = (2.5, -2.5, 0)
    tree.links.new(iop.outputs['Instances'], t_final.inputs['Geometry'])
    tree.links.new(t_final.outputs['Geometry'], join_node.inputs[0])

def add_solarium(tree, join_node):
    sol1 = tree.nodes.new('GeometryNodeMeshCube')
    sol1.inputs['Size'].default_value = (11.0, 0.3, 2.0)
    t_sol1 = tree.nodes.new('GeometryNodeTransform')
    t_sol1.inputs['Translation'].default_value = (0, 5.75, Z_N2 + 1.1)
    tree.links.new(sol1.outputs['Mesh'], t_sol1.inputs['Geometry'])
    tree.links.new(t_sol1.outputs['Geometry'], join_node.inputs[0])

    sol2 = tree.nodes.new('GeometryNodeMeshCube')
    sol2.inputs['Size'].default_value = (11.0, 0.3, 2.0)
    t_sol2 = tree.nodes.new('GeometryNodeTransform')
    t_sol2.inputs['Translation'].default_value = (0, -5.75, Z_N2 + 1.1)
    tree.links.new(sol2.outputs['Mesh'], t_sol2.inputs['Geometry'])
    tree.links.new(t_sol2.outputs['Geometry'], join_node.inputs[0])

def build_perfect_model():
    print("[ZULY QA] Ejecutando bucle de perfección basado en V9 y V05...")
    limpiar_escena()
    
    # 1. Crear malla y objeto real
    mesh = bpy.data.meshes.new("Savoye_Geom")
    obj = bpy.data.objects.new("VILLA_SAVOYE_PERFECTA", mesh)
    bpy.context.scene.collection.objects.link(obj)
    
    # 2. Hacerlo activo y seleccionado (¡CRÍTICO PARA QUE SE VEAN LOS NODOS!)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # 3. Modificador y Árbol
    mod = obj.modifiers.new(name="ZULY_GEONODES", type='NODES')
    tree = bpy.data.node_groups.new(name="Savoye_Parametric_Core", type='GeometryNodeTree')
    mod.node_group = tree
    
    # 4. Input y Output obligatorios
    join_node = test_api_blender_36(tree)
    
    # 5. Módulos fraccionados
    print("[ZULY QA] Generando Pilotes y Losa N0...")
    add_pilotes(tree, join_node)
    add_losa(tree, join_node, 0.3)
    
    print("[ZULY QA] Generando Nivel 1 y Ventanas...")
    add_losa(tree, join_node, Z_N1)
    add_muros_con_ventanas(tree, join_node)
    
    print("[ZULY QA] Generando Escalera Paramétrica...")
    add_escalera_parametrica(tree, join_node)
    
    print("[ZULY QA] Generando Nivel 2 y Solarium...")
    add_losa(tree, join_node, Z_N2)
    add_solarium(tree, join_node)
    
    # 6. Guardar archivo
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"\n✅ ZULY_RESULT: Modelo Perfecto guardado en {BLEND_OUT}")

if __name__ == "__main__":
    build_perfect_model()
