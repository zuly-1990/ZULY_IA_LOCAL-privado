import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_10.blend')
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

print("OBJECT INFO NODES:")
count = 0
for node in tree.nodes:
    if node.type == 'OBJECT_INFO':
        count += 1
        obj = node.inputs['Object'].default_value
        print(f"  {node.name} -> Object: {obj.name if obj else 'NONE'}")
print(f"TOTAL OBJECT INFO NODES: {count}")
