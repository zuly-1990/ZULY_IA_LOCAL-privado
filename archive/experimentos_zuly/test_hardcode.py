import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_10.blend')
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

comp1 = tree.nodes.get("Compare")
# Encontrar INT A y INT B
int_a = comp1.inputs[2]
int_b = comp1.inputs[3]

# DESCONECTAR Group Input de INT A
for link in list(int_a.links):
    tree.links.remove(link)

# Hardcodear A = 1, B = 1
int_a.default_value = 1
int_b.default_value = 1

depsgraph = bpy.context.evaluated_depsgraph_get()
obj = bpy.data.objects.get("ZULY_Piso_1_Completo")
eval_obj = obj.evaluated_get(depsgraph)
mesh = eval_obj.data
print(f"VERTICES (HARDCODED COMPARE 1==1): {len(mesh.vertices)}")
