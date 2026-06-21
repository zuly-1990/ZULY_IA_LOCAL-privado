import bpy

print("=== INICIANDO AUDITORIA ZULY ===")
bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_10.blend')

obj = bpy.data.objects.get("ZULY_Piso_1_Completo")
if not obj:
    print("OBJETO NO ENCONTRADO")
else:
    # 1. Evaluar geometría resultante
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.data
    num_verts = len(mesh.vertices) if mesh else 0
    print(f"VERTICES DE PISO 1 EN PANTALLA: {num_verts}")
    if num_verts == 0:
        print("-> FALLO CRÍTICO: La geometría es INVISIBLE (0 vértices).")

    # 2. Verificar modificador
    mod = obj.modifiers.get("GN_SISTEMA_MAESTRO")
    if mod:
        print("\nVALORES DEL MODIFICADOR:")
        for k in mod.keys():
            print(f"{k} = {mod[k]}")

    # 3. Analizar el Árbol de Nodos
    tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")
    if tree:
        print("\nINSPECCIÓN DE ENLACES (SWITCHES Y COMPARES):")
        for node in tree.nodes:
            if node.type == 'SWITCH':
                print(f"SWITCH NODE: {node.name}, input_type: {getattr(node, 'input_type', 'N/A')}")
                for inp in node.inputs:
                    if inp.is_linked:
                        print(f"  Input '{inp.name}' <- {inp.links[0].from_node.name}.{inp.links[0].from_socket.name}")
                    else:
                        print(f"  Input '{inp.name}' (unlinked)")
            if node.type == 'COMPARE':
                print(f"COMPARE NODE: {node.name}")
                for inp in node.inputs:
                    if inp.is_linked:
                        print(f"  Input '{inp.name}' <- {inp.links[0].from_node.name}.{inp.links[0].from_socket.name}")
                    else:
                        print(f"  Input '{inp.name}' = {inp.default_value}")
        
        print("\nGROUP INPUT NODE SOCKETS:")
        in_node = tree.nodes.get("Group Input")
        if in_node:
            for out in in_node.outputs:
                print(f"  Output '{out.name}' type: {out.type}")
        
        # Comprobar si `tree.inputs` tiene los sockets
        print("\nTREE INPUTS DECLARADOS:")
        for inp in tree.inputs:
            print(f"  Input '{inp.name}' type: {inp.type}, identifier: {inp.identifier}")

print("=== FIN AUDITORIA ===")
