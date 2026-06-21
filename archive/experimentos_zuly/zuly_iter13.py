import bpy

# Cargar el archivo Iter 12
bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_12.blend')

# Obtener el árbol maestro original
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

# Buscar el nodo JoinGeometry final que une todos los pisos
join_node = None
for node in tree.nodes:
    if node.type == 'JOIN_GEOMETRY' and not node.outputs[0].is_linked:
        # Wait, if it's connected to Output, that's the one
        pass
        
# En su lugar, busquemos el Group Output
out_node = tree.nodes.get('Group Output')
if out_node:
    # Obtener el socket conectado a la salida (la geometría final)
    final_geom_link = out_node.inputs[0].links[0]
    final_geom_node = final_geom_link.from_node
    final_geom_socket = final_geom_link.from_socket

    # Eliminar el enlace directo al output
    tree.links.remove(final_geom_link)

    # --- MEJORA 1: TERRENO PARAMETRICO (BASE SITE) ---
    bbox = tree.nodes.new('GeometryNodeBoundBox')
    bbox.location = (out_node.location.x - 600, out_node.location.y - 200)
    tree.links.new(final_geom_socket, bbox.inputs[0])

    # Extraer cara inferior del Bounding Box para hacer el terreno
    # O simplemente escalar el Bounding Box en X e Y
    transform_ground = tree.nodes.new('GeometryNodeTransform')
    transform_ground.inputs['Scale'].default_value = (3.0, 3.0, 0.01) # Aplastar en Z, expandir en XY
    transform_ground.inputs['Translation'].default_value = (0, 0, -0.05) # Bajarlo un poco
    transform_ground.location = (out_node.location.x - 400, out_node.location.y - 200)
    tree.links.new(bbox.outputs[0], transform_ground.inputs[0])

    # --- MEJORA 2: OUTLINES ARQUITECTONICOS (MULLIONS/WIREFRAME) ---
    mesh_to_curve = tree.nodes.new('GeometryNodeMeshToCurve')
    mesh_to_curve.location = (out_node.location.x - 600, out_node.location.y + 200)
    tree.links.new(final_geom_socket, mesh_to_curve.inputs[0])

    curve_to_mesh = tree.nodes.new('GeometryNodeCurveToMesh')
    curve_to_mesh.location = (out_node.location.x - 400, out_node.location.y + 200)
    tree.links.new(mesh_to_curve.outputs[0], curve_to_mesh.inputs[0])

    # Perfil para el wireframe (un círculo muy delgado)
    profile = tree.nodes.new('GeometryNodeCurvePrimitiveCircle')
    profile.inputs['Radius'].default_value = 0.02 # 2 cm de grosor
    profile.inputs['Resolution'].default_value = 4
    profile.location = (out_node.location.x - 600, out_node.location.y + 400)
    tree.links.new(profile.outputs[0], curve_to_mesh.inputs['Profile Curve'])

    # Material negro para las líneas
    mat_lines = tree.nodes.new('GeometryNodeSetMaterial')
    mat_lines.location = (out_node.location.x - 200, out_node.location.y + 200)
    tree.links.new(curve_to_mesh.outputs[0], mat_lines.inputs[0])
    
    # Crear el material si no existe
    mat = bpy.data.materials.get("ZULY_BORDES")
    if not mat:
        mat = bpy.data.materials.new("ZULY_BORDES")
        mat.diffuse_color = (0.01, 0.01, 0.01, 1)
    mat_lines.inputs['Material'].default_value = mat

    # --- UNIR TODO Y ENVIAR A LA SALIDA ---
    final_join = tree.nodes.new('GeometryNodeJoinGeometry')
    final_join.location = (out_node.location.x - 50, out_node.location.y)
    
    # 1. Geometría original
    tree.links.new(final_geom_socket, final_join.inputs[0])
    # 2. Outlines Arquitectónicos (Marcos)
    tree.links.new(mat_lines.outputs[0], final_join.inputs[0])
    # 3. Terreno Paramétrico
    tree.links.new(transform_ground.outputs[0], final_join.inputs[0])

    tree.links.new(final_join.outputs[0], out_node.inputs[0])

# Guardar Iter 13
bpy.ops.wm.save_as_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_13.blend')
print("✅ Iteración 13 generada exitosamente con mejoras arquitectónicas nodales.")
