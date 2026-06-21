import bpy
import math

# Cargar el archivo Iter 13
bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_13.blend')

# Obtener el árbol maestro original
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

# Eliminar los nodos defectuosos del terreno anterior
# En Iter 13 añadí Bounding Box y Transform
for node in tree.nodes:
    if node.type == 'BOUNDING_BOX' or node.type == 'TRANSFORM':
        tree.nodes.remove(node)

# Encontrar el JoinGeometry final (donde metí los outlines y el terreno)
# El JoinGeometry final está conectado directamente al Group Output
out_node = tree.nodes.get('Group Output')
final_join = out_node.inputs[0].links[0].from_node

# Desconectar todo lo que estaba conectado al final_join (terreno viejo)
# En Iter 13 conecté: [0] Geometría [1] Outlines [2] Terreno (Transform)
# El terreno era el índice 2. Simplemente cortamos ese enlace.
for link in final_join.inputs[0].links:
    if link.from_node.type == 'TRANSFORM': # Este era el terreno viejo
        tree.links.remove(link)

# --- MEJORA: TERRENO CON PROPORCIONES CORRECTAS ---
# En vez de deformar el Bounding Box, creamos un plano perfecto y uniforme
grid = tree.nodes.new('GeometryNodeMeshGrid')
grid.inputs['Size X'].default_value = 150.0  # 150 metros X
grid.inputs['Size Y'].default_value = 150.0  # 150 metros Y
grid.location = (out_node.location.x - 400, out_node.location.y - 300)

# Moverlo un poco hacia abajo para que no corte el piso
transform_ground = tree.nodes.new('GeometryNodeTransform')
transform_ground.inputs['Translation'].default_value = (0, 0, -0.05) 
transform_ground.location = (out_node.location.x - 200, out_node.location.y - 300)
tree.links.new(grid.outputs[0], transform_ground.inputs[0])

# Unir el nuevo terreno perfecto
tree.links.new(transform_ground.outputs[0], final_join.inputs[0])

# --- FIJACION OBLIGATORIA DEL VISOR DE NODOS (EL AUDITOR) ---
tree.use_fake_user = True

# Asegurarse de que el objeto ZULY_Piso_1_Completo esté seleccionado y activo
obj_main = None
for obj in bpy.context.scene.objects:
    if "Piso" in obj.name or "BIM" in obj.name or "Completo" in obj.name:
        obj_main = obj
        break

if obj_main:
    bpy.ops.object.select_all(action='DESELECT')
    obj_main.select_set(True)
    bpy.context.view_layer.objects.active = obj_main

# Obligar a la interfaz a fijarse en el árbol maestro
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'NODE_EDITOR':
            for space in area.spaces:
                if space.type == 'NODE_EDITOR':
                    space.tree_type = 'GeometryNodeTree'
                    space.node_tree = tree
                    space.pin = True

# Guardar Iter 14
bpy.ops.wm.save_as_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_14.blend')
print("✅ Iteración 14: Proporciones de placa corregidas y Visor de Nodos anclado.")
