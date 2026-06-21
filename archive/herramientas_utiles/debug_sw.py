import bpy
bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_7.blend')
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")
if tree:
    for node in tree.nodes:
        if node.type == 'SWITCH':
            print(f"Switch Node: {node.name}, input_type: {getattr(node, 'input_type', 'NOT_FOUND')}")
            for link in tree.links:
                if link.to_node == node:
                    print(f"  Link to {node.name}.{link.to_socket.name} from {link.from_node.name}")
