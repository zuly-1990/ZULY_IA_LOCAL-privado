import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_10.blend')

col = bpy.data.collections.get("V9_ORIGINALES_OCULTOS")
if col:
    print("Unhiding collection...")
    col.hide_viewport = False
    
depsgraph = bpy.context.evaluated_depsgraph_get()
obj = bpy.data.objects.get("ZULY_Piso_1_Completo")
eval_obj = obj.evaluated_get(depsgraph)
mesh = eval_obj.data
print(f"VERTICES DE PISO 1 TRAS DESOCULTAR: {len(mesh.vertices)}")
