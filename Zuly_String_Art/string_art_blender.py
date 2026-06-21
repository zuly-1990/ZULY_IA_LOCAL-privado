import bpy
import json
import math
import os

SEQUENCE_FILE = "/opt/zuly/pin_sequence.json"
OUTPUT_BLEND = "/opt/zuly/Zuly_String_Art_3D.blend"

NUM_PINS = 250
RADIUS = 1.0 # 1 meter radius in Blender

def get_pin_coord(pin_index):
    angle = 2 * math.pi * pin_index / NUM_PINS
    # En el plano XZ para que parezca un cuadro de frente
    x = RADIUS * math.cos(angle)
    z = RADIUS * math.sin(angle)
    return (x, 0, z)

def main():
    # Limpiar escena
    bpy.ops.wm.read_factory_settings(use_empty=True)

    if not os.path.exists(SEQUENCE_FILE):
        print("Sequence file not found!")
        return

    with open(SEQUENCE_FILE, "r") as f:
        sequence = json.load(f)

    print(f"Loaded sequence with {len(sequence)} steps.")

    # Generar los vértices (1 vértice por cada clavo visitado)
    vertices = []
    edges = []
    
    for i in range(len(sequence)):
        pin = sequence[i]
        vertices.append(get_pin_coord(pin))
        if i > 0:
            edges.append((i-1, i))

    # Crear la malla base para el hilo
    mesh = bpy.data.meshes.new("ThreadMesh")
    mesh.from_pydata(vertices, edges, [])
    mesh.update()

    obj = bpy.data.objects.new("StringArt_Thread", mesh)
    bpy.context.scene.collection.objects.link(obj)

    # Convertir a curva para darle grosor
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='CURVE')
    
    # Darle grosor al hilo
    curve = obj.data
    curve.bevel_depth = 0.001 # 1 milímetro de grosor
    curve.bevel_resolution = 0

    # Crear material negro para el hilo
    mat = bpy.data.materials.new(name="Thread_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.9
    curve.materials.append(mat)

    # Crear marco circular base (madera)
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=RADIUS + 0.05, depth=0.05, location=(0, 0.025, 0), rotation=(math.pi/2, 0, 0))
    marco = bpy.context.active_object
    marco.name = "Marco_Madera"
    
    mat_madera = bpy.data.materials.new(name="Madera_Material")
    mat_madera.use_nodes = True
    bsdf_m = mat_madera.node_tree.nodes.get("Principled BSDF")
    if bsdf_m:
        bsdf_m.inputs['Base Color'].default_value = (0.4, 0.2, 0.1, 1.0)
    marco.data.materials.append(mat_madera)

    # Añadir los clavitos metálicos
    for i in range(NUM_PINS):
        x, y, z = get_pin_coord(i)
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.005, depth=0.04, location=(x, -0.02, z), rotation=(math.pi/2, 0, 0))

    # Guardar
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
    print("Saved Blender file successfully.")

if __name__ == "__main__":
    main()
