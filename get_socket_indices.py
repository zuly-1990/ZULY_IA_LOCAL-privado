import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_9.blend')
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

comp = tree.nodes.new('FunctionNodeCompare')
print("COMPARE INPUTS:")
for i, inp in enumerate(comp.inputs):
    print(f"  [{i}] {inp.name} ({inp.type})")
print("COMPARE OUTPUTS:")
for i, out in enumerate(comp.outputs):
    print(f"  [{i}] {out.name} ({out.type})")

sw = tree.nodes.new('GeometryNodeSwitch')
print("\nSWITCH INPUTS:")
for i, inp in enumerate(sw.inputs):
    print(f"  [{i}] {inp.name} ({inp.type})")
print("SWITCH OUTPUTS:")
for i, out in enumerate(sw.outputs):
    print(f"  [{i}] {out.name} ({out.type})")
