import bpy

# Cargar el archivo Iter 14 (o iter 13, pero iter 14 ya tenia el grid)
bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_14.blend')

# Obtener el árbol maestro original
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

# Encontrar los nodos del terreno de Iter 14
grid_node = None
transform_node = None
for node in tree.nodes:
    if node.type == 'MESH_GRID':
        grid_node = node
    elif node.type == 'TRANSFORM' and node.location.y < -200:
        # El transform que baje en Z
        if node.inputs['Translation'].default_value[2] == -0.05:
            transform_node = node

if grid_node and transform_node:
    # ELIMINAR LOS TAMAÑOS EXAGERADOS HARDCODEADOS
    grid_node.inputs['Size X'].default_value = 0.0
    grid_node.inputs['Size Y'].default_value = 0.0
    
    # LA AUDITORÍA SEVERA: Cálculo Dinámico Basado en Piso 1
    # Buscar la salida del Piso 1 (o la geometría total, mejor la total antes del terreno)
    out_node = tree.nodes.get('Group Output')
    final_join = out_node.inputs[0].links[0].from_node
    
    # Encontrar qué link va al terreno y buscar el nodo de geometría pura
    # Sabemos que final_join junta la geometría original y el terreno
    geom_original_socket = final_join.inputs[0].links[0].from_socket # Asumiendo que el primero es la geometria principal
    
    # Añadimos Bounding Box para medir la geometría REAL
    bbox = tree.nodes.new('GeometryNodeBoundBox')
    bbox.location = (grid_node.location.x - 400, grid_node.location.y)
    tree.links.new(geom_original_socket, bbox.inputs[0])
    
    # Vector Math: Subtract Max - Min para sacar ancho y largo
    vmath_sub = tree.nodes.new('GeometryNodeVectorMath')
    vmath_sub.operation = 'SUBTRACT'
    vmath_sub.location = (grid_node.location.x - 200, grid_node.location.y + 100)
    tree.links.new(bbox.outputs['Max'], vmath_sub.inputs[0])
    tree.links.new(bbox.outputs['Min'], vmath_sub.inputs[1])
    
    # Separate XYZ para obtener X e Y exactos
    sep_xyz = tree.nodes.new('GeometryNodeSeparateXYZ')
    sep_xyz.location = (grid_node.location.x - 50, grid_node.location.y + 100)
    tree.links.new(vmath_sub.outputs[0], sep_xyz.inputs[0])
    
    # Math: Add padding (e.g. 5 metros extra por lado = +10 total)
    math_add_x = tree.nodes.new('ShaderNodeMath')
    math_add_x.operation = 'ADD'
    math_add_x.inputs[1].default_value = 10.0
    math_add_x.location = (grid_node.location.x - 50, grid_node.location.y)
    tree.links.new(sep_xyz.outputs['X'], math_add_x.inputs[0])
    
    math_add_y = tree.nodes.new('ShaderNodeMath')
    math_add_y.operation = 'ADD'
    math_add_y.inputs[1].default_value = 10.0
    math_add_y.location = (grid_node.location.x - 50, grid_node.location.y - 150)
    tree.links.new(sep_xyz.outputs['Y'], math_add_y.inputs[0])
    
    # Conectar el tamaño calculado dinámicamente al Grid
    tree.links.new(math_add_x.outputs[0], grid_node.inputs['Size X'])
    tree.links.new(math_add_y.outputs[0], grid_node.inputs['Size Y'])
    
    # Para centrar correctamente el grid, necesitamos moverlo al centro del Bounding Box
    # Transform (Terreno) Translation XY = (Max+Min)/2
    vmath_add = tree.nodes.new('GeometryNodeVectorMath')
    vmath_add.operation = 'ADD'
    vmath_add.location = (transform_node.location.x - 300, transform_node.location.y - 100)
    tree.links.new(bbox.outputs['Max'], vmath_add.inputs[0])
    tree.links.new(bbox.outputs['Min'], vmath_add.inputs[1])
    
    vmath_scale = tree.nodes.new('GeometryNodeVectorMath')
    vmath_scale.operation = 'SCALE'
    vmath_scale.inputs['Scale'].default_value = 0.5
    vmath_scale.location = (transform_node.location.x - 150, transform_node.location.y - 100)
    tree.links.new(vmath_add.outputs[0], vmath_scale.inputs[0])
    
    # Separate Centro para mezclarlo con el Z_Offset de -0.05
    sep_center = tree.nodes.new('GeometryNodeSeparateXYZ')
    sep_center.location = (transform_node.location.x - 150, transform_node.location.y - 250)
    tree.links.new(vmath_scale.outputs[0], sep_center.inputs[0])
    
    comb_center = tree.nodes.new('GeometryNodeCombineXYZ')
    comb_center.inputs['Z'].default_value = -0.05
    comb_center.location = (transform_node.location.x - 150, transform_node.location.y - 400)
    tree.links.new(sep_center.outputs['X'], comb_center.inputs['X'])
    tree.links.new(sep_center.outputs['Y'], comb_center.inputs['Y'])
    
    tree.links.new(comb_center.outputs[0], transform_node.inputs['Translation'])

# Guardar Iter 15
bpy.ops.wm.save_as_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_15.blend')
print("✅ Iteración 15: Placa calculada algorítmicamente exacta a las proporciones del edificio.")
