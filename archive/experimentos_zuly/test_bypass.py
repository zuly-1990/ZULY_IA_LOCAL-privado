import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_10.blend')
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

# Encontrar Join Geometry de Piso 1 y Output
join_p1 = tree.nodes.get("Join Geometry.001")
out_node = tree.nodes.get("Group Output")

if join_p1 and out_node:
    print("CONECTANDO DIRECTAMENTE JOIN P1 A OUTPUT...")
    # Romper los links existentes del output
    for link in list(out_node.inputs[0].links):
        tree.links.remove(link)
    # Conectar directo
    tree.links.new(join_p1.outputs[0], out_node.inputs[0])

depsgraph = bpy.context.evaluated_depsgraph_get()
obj = bpy.data.objects.get("ZULY_Piso_1_Completo")
eval_obj = obj.evaluated_get(depsgraph)
mesh = eval_obj.data
print(f"VERTICES DE PISO 1 (BYPASS SWITCH): {len(mesh.vertices)}")
