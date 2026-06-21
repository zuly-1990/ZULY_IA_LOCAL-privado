import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_11.blend')

print("--- REVISIÓN DE NODOS ---")
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")
if not tree:
    print("EL ARBOL DE NODOS NO EXISTE EN EL ARCHIVO")
else:
    print(f"Arbol encontrado: {tree.name}, Nodos internos: {len(tree.nodes)}")

for obj_name in ["ZULY_Piso_1_Completo", "ZULY_Piso_2_Completo", "ZULY_Piso_3_Completo"]:
    obj = bpy.data.objects.get(obj_name)
    if obj:
        mod = obj.modifiers.get("GN_SISTEMA_MAESTRO")
        if mod:
            if mod.node_group:
                print(f"{obj_name}: Modificador tiene asignado el grupo '{mod.node_group.name}'")
            else:
                print(f"{obj_name}: Modificador NO TIENE GRUPO ASIGNADO")
        else:
            print(f"{obj_name}: No tiene el modificador")
