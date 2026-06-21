import bpy
import math

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_12.blend')

master_col = bpy.context.scene.collection
col_ciudad = bpy.data.collections.new("ZULY_100_MODELOS_AUTOMATICOS")
master_col.children.link(col_ciudad)

tree_master = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

tree_city = bpy.data.node_groups.new(name="ZULY_CIUDAD_PARAMETRICA_100", type='GeometryNodeTree')
tree_city.inputs.new('NodeSocketGeometry', 'Geometry')
tree_city.outputs.new('NodeSocketGeometry', 'Geometry')

out_node = tree_city.nodes.new('NodeGroupOutput')
out_node.location = (1500, 0)

# Instanciar el modelo completo (3 pisos unidos)
bim_p1 = tree_city.nodes.new('GeometryNodeGroup')
bim_p1.node_tree = tree_master
bim_p1.inputs['Piso_ID'].default_value = 1
bim_p1.location = (-600, 200)

bim_p2 = tree_city.nodes.new('GeometryNodeGroup')
bim_p2.node_tree = tree_master
bim_p2.inputs['Piso_ID'].default_value = 2
bim_p2.location = (-600, 0)

bim_p3 = tree_city.nodes.new('GeometryNodeGroup')
bim_p3.node_tree = tree_master
bim_p3.inputs['Piso_ID'].default_value = 3
bim_p3.location = (-600, -200)

join_edificio = tree_city.nodes.new('GeometryNodeJoinGeometry')
join_edificio.location = (-300, 0)
tree_city.links.new(bim_p1.outputs[0], join_edificio.inputs[0])
tree_city.links.new(bim_p2.outputs[0], join_edificio.inputs[0])
tree_city.links.new(bim_p3.outputs[0], join_edificio.inputs[0])

# Cuadrícula 10x10 para los 100 modelos
grid = tree_city.nodes.new('GeometryNodeMeshGrid')
grid.inputs['Size X'].default_value = 250.0  # Espacio horizontal
grid.inputs['Size Y'].default_value = 250.0  # Espacio vertical
grid.inputs['Vertices X'].default_value = 10
grid.inputs['Vertices Y'].default_value = 10
grid.location = (-300, 300)

iop = tree_city.nodes.new('GeometryNodeInstanceOnPoints')
iop.location = (500, 100)
tree_city.links.new(grid.outputs['Mesh'], iop.inputs['Points'])
tree_city.links.new(join_edificio.outputs[0], iop.inputs['Instance'])

# --- MEJORA: VARIACION DE ESCALA (ALTURA) ---
rand_scale = tree_city.nodes.new('FunctionNodeRandomValue')
rand_scale.data_type = 'FLOAT'

scale_min = next(inp for inp in rand_scale.inputs if inp.name == 'Min' and inp.type == 'VALUE')
scale_max = next(inp for inp in rand_scale.inputs if inp.name == 'Max' and inp.type == 'VALUE')
scale_min.default_value = 0.6
scale_max.default_value = 1.4
rand_scale.location = (100, -100)

scale_out = next(out for out in rand_scale.outputs if out.name == 'Value' and out.type == 'VALUE')

comb_scale = tree_city.nodes.new('ShaderNodeCombineXYZ')
comb_scale.inputs[0].default_value = 1.0 # X normal
comb_scale.inputs[1].default_value = 1.0 # Y normal
comb_scale.location = (300, -100)
tree_city.links.new(scale_out, comb_scale.inputs[2]) # Z aleatorio
tree_city.links.new(comb_scale.outputs[0], iop.inputs['Scale'])

# --- MEJORA: VARIACION DE ROTACION (Giros de 90 grados) ---
rand_rot = tree_city.nodes.new('FunctionNodeRandomValue')
rand_rot.data_type = 'INT'

rot_min = next(inp for inp in rand_rot.inputs if inp.name == 'Min' and inp.type == 'INT')
rot_max = next(inp for inp in rand_rot.inputs if inp.name == 'Max' and inp.type == 'INT')
rot_min.default_value = 0
rot_max.default_value = 3
rand_rot.location = (-100, -300)

rot_out = next(out for out in rand_rot.outputs if out.name == 'Value' and out.type == 'INT')

math_node = tree_city.nodes.new('ShaderNodeMath')
math_node.operation = 'MULTIPLY'
math_node.inputs[1].default_value = math.pi / 2.0  # 90 grados en radianes
math_node.location = (100, -300)
tree_city.links.new(rot_out, math_node.inputs[0])

comb_rot = tree_city.nodes.new('ShaderNodeCombineXYZ')
comb_rot.inputs[0].default_value = 0.0
comb_rot.inputs[1].default_value = 0.0
comb_rot.location = (300, -300)
tree_city.links.new(math_node.outputs[0], comb_rot.inputs[2]) # Z rotación
tree_city.links.new(comb_rot.outputs[0], iop.inputs['Rotation'])

# Salida
tree_city.links.new(iop.outputs['Instances'], out_node.inputs[0])

# Objeto
obj_city = bpy.data.objects.new("ZULY_CIUDAD_100_MODELOS", bpy.data.meshes.new("Ciudad_BIM"))
col_ciudad.objects.link(obj_city)
mod_city = obj_city.modifiers.new("GN_100_AUTOMATICO", 'NODES')
mod_city.node_group = tree_city

tree_city.use_fake_user = True
bpy.ops.object.select_all(action='DESELECT')
obj_city.select_set(True)
bpy.context.view_layer.objects.active = obj_city

for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'NODE_EDITOR':
            for space in area.spaces:
                if space.type == 'NODE_EDITOR':
                    space.tree_type = 'GeometryNodeTree'
                    space.node_tree = tree_city
                    space.pin = True

bpy.ops.wm.save_as_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_100.blend')
print("✅ CICLO DE 100 MODELOS COMPLETADO")
