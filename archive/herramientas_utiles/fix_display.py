import bpy

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_11.blend')

tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")
if tree:
    tree.use_fake_user = True
    
    # Hacer que ZULY_Piso_1_Completo sea el objeto activo y seleccionado
    obj_p1 = bpy.data.objects.get("ZULY_Piso_1_Completo")
    if obj_p1:
        bpy.ops.object.select_all(action='DESELECT')
        obj_p1.select_set(True)
        bpy.context.view_layer.objects.active = obj_p1

    # Forzar la visualización en el editor de nodos
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'NODE_EDITOR':
                for space in area.spaces:
                    if space.type == 'NODE_EDITOR':
                        space.tree_type = 'GeometryNodeTree'
                        space.node_tree = tree
                        space.pin = True # Fijar el árbol para que no desaparezca

bpy.ops.wm.save_as_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_12.blend')
print("✅ Fix visual aplicado, guardado como Iter_12")
