import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_8.blend')

obj = bpy.data.objects.get("ZULY_Piso_1_Completo")
mod = obj.modifiers.get("GN_SISTEMA_MAESTRO")
if mod:
    print(f"BEFORE: Input_1={mod.get('Input_1')}, use_attr={mod.get('Input_1_use_attribute')}")
    mod["Input_1"] = 1
    mod["Input_1_use_attribute"] = 0
    print(f"AFTER: Input_1={mod.get('Input_1')}, use_attr={mod.get('Input_1_use_attribute')}")

bpy.ops.wm.save_as_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_9.blend')
