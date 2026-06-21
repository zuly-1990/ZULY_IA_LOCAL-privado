import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_10.blend')
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

out_node = tree.nodes.get("Group Output")
in_node = tree.nodes.get("Group Input")
join_p1 = tree.nodes.get("Join Geometry.001")

# Limpiar todos los links del output
for link in list(out_node.inputs[0].links): tree.links.remove(link)

# Crear Separate Geometry y Compare
sep = tree.nodes.new('GeometryNodeSeparateGeometry')
comp = tree.nodes.new('FunctionNodeCompare')
comp.data_type = 'INT'
comp.operation = 'EQUAL'
comp.inputs[2].default_value = 1
comp.inputs[3].default_value = 1

# Enlazar
tree.links.new(join_p1.outputs[0], sep.inputs['Geometry'])
tree.links.new(comp.outputs[0], sep.inputs['Selection'])
tree.links.new(sep.outputs['Selection'], out_node.inputs[0])

depsgraph = bpy.context.evaluated_depsgraph_get()
obj = bpy.data.objects.get("ZULY_Piso_1_Completo")
eval_obj = obj.evaluated_get(depsgraph)
mesh = eval_obj.data
print(f"VERTICES USANDO SEPARATE GEOMETRY: {len(mesh.vertices)}")
