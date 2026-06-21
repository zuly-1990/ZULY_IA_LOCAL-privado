def get_multi_layer_render_code(base_path: str) -> str:
    """
    Pilar 3: Visión Multi-Capa (Art Director IA)
    Devuelve un bloque de código Python (bpy) que configura Blender
    para renderizar 3 pases distintos:
    1. Color Base (Beauty Pass)
    2. Mapa de Profundidad (Z-Depth)
    3. Wireframe (Topología)
    """
    code = f"""
import bpy
import os

# Configuración base de rutas
output_base = r"{base_path}"
bpy.context.scene.render.filepath = os.path.join(output_base, "render_color.png")

# 1. Habilitar nodos de composición para el Mapa de Profundidad
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

# Limpiar nodos existentes
for node in tree.nodes:
    tree.nodes.remove(node)

# Crear nodos para Z-Depth
render_layers = tree.nodes.new('CompositorNodeRLayers')
normalize = tree.nodes.new('CompositorNodeNormalize')
file_output = tree.nodes.new('CompositorNodeOutputFile')

# Configurar File Output para Z-Depth
file_output.base_path = output_base
file_output.file_slots[0].path = "render_depth"
file_output.format.file_format = 'PNG'

# Conectar Z-pass -> Normalize -> File Output
links.new(render_layers.outputs['Depth'], normalize.inputs[0])
links.new(normalize.outputs[0], file_output.inputs[0])

# Activar pase Z
bpy.context.view_layer.use_pass_z = True

# 2. Render Principal (Genera Color y Depth al mismo tiempo)
print("[Multi-Layer Vision] Renderizando Color y Depth Map...")
bpy.ops.render.render(write_still=True)

# 3. Preparar material Wireframe para toda la escena
print("[Multi-Layer Vision] Preparando Wireframe Pass...")
wire_mat = bpy.data.materials.new(name="Wireframe_Material")
wire_mat.use_nodes = True
wnodes = wire_mat.node_tree.nodes
wlinks = wire_mat.node_tree.links

for n in wnodes:
    wnodes.remove(n)

# Nodos de Wireframe (Emission + Wireframe Node)
mat_out = wnodes.new('ShaderNodeOutputMaterial')
emission = wnodes.new('ShaderNodeEmission')
wireframe = wnodes.new('ShaderNodeWireframe')
color_ramp = wnodes.new('ShaderNodeValToRGB')

# Configurar color del wireframe (Blanco sobre negro)
color_ramp.color_ramp.elements[0].position = 0.0
color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1) # Fondo
color_ramp.color_ramp.elements[1].position = 0.01
color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1) # Líneas

wlinks.new(wireframe.outputs['Fac'], color_ramp.inputs['Fac'])
wlinks.new(color_ramp.outputs['Color'], emission.inputs['Color'])
wlinks.new(emission.outputs['Emission'], mat_out.inputs['Surface'])

# Aplicar material override a la vista para renderizar el wireframe
bpy.context.view_layer.material_override = wire_mat
bpy.context.scene.render.filepath = os.path.join(output_base, "render_wireframe.png")

print("[Multi-Layer Vision] Renderizando Wireframe...")
# Desactivar nodos de composición temporalmente para no sobrescribir el Z-Depth
bpy.context.scene.use_nodes = False
bpy.ops.render.render(write_still=True)

# Restaurar estado
bpy.context.view_layer.material_override = None
print("[Multi-Layer Vision] ¡Proceso de 3 capas completado!")
"""
    return code
