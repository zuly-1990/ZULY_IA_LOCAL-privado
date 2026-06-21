import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_10.blend')
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

out_node = tree.nodes.get("Group Output")
in_node = tree.nodes.get("Group Input")
join_p1 = tree.nodes.get("Join Geometry.001")

# Encontrar los nodos
comp1 = tree.nodes.get("Compare")
sw1 = tree.nodes.get("Switch")

# Buscar los sockets dinámicamente
int_a = None
int_b = None
for inp in comp1.inputs:
    if inp.name == 'A' and inp.type == 'INT': int_a = inp
    if inp.name == 'B' and inp.type == 'INT': int_b = inp

false_in = None
true_in = None
for inp in sw1.inputs:
    if inp.name == 'False' and inp.type == 'GEOMETRY': false_in = inp
    if inp.name == 'True' and inp.type == 'GEOMETRY': true_in = inp

geom_out = None
for out in sw1.outputs:
    if out.type == 'GEOMETRY': geom_out = out

print(f"INT A: {int_a.identifier if int_a else 'NO'}, INT B: {int_b.identifier if int_b else 'NO'}")
print(f"FALSE GEOM: {false_in.identifier if false_in else 'NO'}, TRUE GEOM: {true_in.identifier if true_in else 'NO'}")
print(f"GEOM OUT: {geom_out.identifier if geom_out else 'NO'}")

# Limpiar links del switch y reconectar dinámicamente
for link in list(sw1.inputs[0].links): tree.links.remove(link)
for link in list(sw1.inputs[1].links): tree.links.remove(link)
for link in list(false_in.links): tree.links.remove(link)
for link in list(true_in.links): tree.links.remove(link)
for link in list(geom_out.links): tree.links.remove(link)

tree.links.new(comp1.outputs[0], sw1.inputs['Switch'])
tree.links.new(join_p1.outputs[0], true_in)
tree.links.new(geom_out, out_node.inputs[0])

depsgraph = bpy.context.evaluated_depsgraph_get()
obj = bpy.data.objects.get("ZULY_Piso_1_Completo")
eval_obj = obj.evaluated_get(depsgraph)
mesh = eval_obj.data
print(f"VERTICES DESPUES DEL FIX DINAMICO: {len(mesh.vertices)}")
