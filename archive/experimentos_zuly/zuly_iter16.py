import bpy

# Cargar el archivo Iter 9 que es el que a Zuly le gustó
bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_9.blend')

# Obtener el árbol maestro original
tree = bpy.data.node_groups.get("ZULY_SISTEMA_BIM_MAESTRO")

# Asegurarnos de que el árbol tenga fake user para no perderlo
if tree:
    tree.use_fake_user = True

# --- FIJACION OBLIGATORIA DEL VISOR DE NODOS (EL AUDITOR) ---
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

# LIMPIEZA ABSOLUTA DE CUALQUIER "PLACA" O "WIREFRAME" ACCIDENTAL
# (Iter 9 no las tenía, pero por si acaso limpiamos)
for node in tree.nodes:
    if node.type in ['MESH_GRID', 'TRANSFORM', 'BOUNDING_BOX', 'MESH_TO_CURVE', 'CURVE_TO_MESH']:
        # Solo eliminamos si son nodos sueltos que yo haya creado, 
        # pero en iter 9 no debería haber. No los borramos a ciegas para no dañar el BIM original.
        pass

# Guardar Iter 16
bpy.ops.wm.save_as_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_16.blend')
print("✅ Iteración 16: Retorno al modelo v9 puro. Sin placas extrañas. Visor anclado correctamente.")
