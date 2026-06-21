import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_7.blend')

obj = bpy.data.objects.get("ZULY_Piso_1_Completo")
if obj:
    mod = obj.modifiers.get("GN_SISTEMA_MAESTRO")
    if mod:
        print("KEYS IN MODIFIER:")
        for k in mod.keys():
            print(f"Key: {k}, Value: {mod[k]}")
        print("DONE KEYS")
