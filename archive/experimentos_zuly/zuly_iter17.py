import bpy

# Cargar el archivo Iter 12 (El modelo que tenía la visibilidad perfecta en el viewport con Separate Geometry)
bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_12.blend')

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
        # Hacer visibles todos los objetos BIM por si acaso estaban ocultos
        obj.hide_viewport = False
        obj.hide_render = False
        obj_main = obj

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
        # Asegurarnos de que la vista 3D muestre todo (hacer zoom extents)
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region}
                    try:
                        bpy.ops.view3d.view_all(override, center=False)
                    except:
                        pass

# Guardar Iter 17
bpy.ops.wm.save_as_mainfile(filepath='/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_17.blend')
print("✅ Iteración 17: Modelos visibles en Viewport (basado en Iter 12) y Visor de Nodos anclado.")
