import bpy
import json
import math
import os
import numpy as np
from mathutils import Vector

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
NUM_CLAVOS   = 288
RADIO        = 0.5
Z_CLAVOS     = 0.0
GROSOR_HILO  = 0.0003   # bevel_depth en metros (~0.3 mm)
ALTO_CLAVO   = 0.02
RADIO_CLAVO  = 0.003

JSON_PATH = os.path.join(bpy.path.abspath("//"), "secuencia_clavos.json")

# ─────────────────────────────────────────────
# 1. LIMPIAR ESCENA
# ─────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=True)
for bloque in [bpy.data.meshes, bpy.data.curves, bpy.data.materials,
               bpy.data.objects, bpy.data.collections]:
    for item in bloque:
        try:
            bloque.remove(item)
        except Exception:
            pass

# ─────────────────────────────────────────────
# 2. LEER JSON
# ─────────────────────────────────────────────
with open(JSON_PATH, 'r') as f:
    secuencia = json.load(f)

print(f"[STRING ART] Secuencia cargada: {len(secuencia)} pasos")

# ─────────────────────────────────────────────
# 3. CALCULAR COORDENADAS DE LOS 288 CLAVOS
# ─────────────────────────────────────────────
angles = np.linspace(0, 2 * math.pi, NUM_CLAVOS, endpoint=False)
coords_np = np.column_stack([
    RADIO * np.cos(angles),
    RADIO * np.sin(angles),
    np.zeros(NUM_CLAVOS)
])
coords = [Vector(coords_np[i]) for i in range(NUM_CLAVOS)]

# ─────────────────────────────────────────────
# 4. INSTANCIAR CLAVOS (cilindros metálicos)
# ─────────────────────────────────────────────
bpy.ops.mesh.primitive_cylinder_add(
    vertices=8,
    radius=RADIO_CLAVO,
    depth=ALTO_CLAVO,
    location=(0, 0, 0)
)
proto_clavo = bpy.context.active_object
proto_clavo.name = "Proto_Clavo"

mat_clavo = bpy.data.materials.new("Mat_Clavo_Metal")
mat_clavo.use_nodes = True
bsdf = mat_clavo.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value    = (0.8, 0.75, 0.6, 1)
    bsdf.inputs["Metallic"].default_value      = 1.0
    bsdf.inputs["Roughness"].default_value     = 0.2
proto_clavo.data.materials.append(mat_clavo)

clavo_mesh = proto_clavo.data
instancias_clavos = [proto_clavo]

for i in range(1, NUM_CLAVOS):
    inst = bpy.data.objects.new(f"Clavo_{i:03d}", clavo_mesh)
    bpy.context.collection.objects.link(inst)
    instancias_clavos.append(inst)

for i, obj in enumerate(instancias_clavos):
    obj.location = (
        float(coords_np[i, 0]),
        float(coords_np[i, 1]),
        Z_CLAVOS + ALTO_CLAVO / 2
    )

proto_clavo.name = "Clavo_000"
print(f"[STRING ART] {NUM_CLAVOS} clavos instanciados")

# ─────────────────────────────────────────────
# 5. GENERAR LA CURVA DEL HILO
# ─────────────────────────────────────────────
N_PUNTOS = len(secuencia)

indices_arr = np.array(secuencia, dtype=np.int32)
indices_arr = np.clip(indices_arr, 0, NUM_CLAVOS - 1)
puntos_hilo = coords_np[indices_arr]

Z_HILO = Z_CLAVOS + ALTO_CLAVO + 0.0005
puntos_hilo[:, 2] = Z_HILO

curva_data = bpy.data.curves.new("Hilo_Curva", type='CURVE')
curva_data.dimensions     = '3D'
curva_data.resolution_u   = 1
curva_data.bevel_depth    = GROSOR_HILO
curva_data.bevel_resolution = 2

spline = curva_data.splines.new('POLY')
spline.points.add(N_PUNTOS - 1)

coords_4d = np.ones((N_PUNTOS, 4), dtype=np.float32)
coords_4d[:, :3] = puntos_hilo.astype(np.float32)

spline.points.foreach_set("co", coords_4d.ravel())

curva_obj = bpy.data.objects.new("Hilo_StringArt", curva_data)
bpy.context.collection.objects.link(curva_obj)

print(f"[STRING ART] Curva generada: {N_PUNTOS} puntos")

# ─────────────────────────────────────────────
# 6. MATERIAL NEGRO PARA EL HILO
# ─────────────────────────────────────────────
mat_hilo = bpy.data.materials.new("Mat_Hilo_Negro")
mat_hilo.use_nodes = True
bsdf_h = mat_hilo.node_tree.nodes.get("Principled BSDF")
if bsdf_h:
    bsdf_h.inputs["Base Color"].default_value  = (0.01, 0.01, 0.01, 1)
    bsdf_h.inputs["Roughness"].default_value   = 0.8
    bsdf_h.inputs["Specular IOR Level"].default_value = 0.0
curva_data.materials.append(mat_hilo)

# ─────────────────────────────────────────────
# 7. FONDO + CÁMARA + LUZ
# ─────────────────────────────────────────────
bpy.ops.mesh.primitive_plane_add(size=1.4, location=(0, 0, -0.001))
tablero = bpy.context.active_object
tablero.name = "Tablero"
mat_tablero = bpy.data.materials.new("Mat_Tablero")
mat_tablero.use_nodes = True
bsdf_t = mat_tablero.node_tree.nodes.get("Principled BSDF")
if bsdf_t:
    bsdf_t.inputs["Base Color"].default_value  = (0.15, 0.08, 0.04, 1)
    bsdf_t.inputs["Roughness"].default_value   = 0.9
tablero.data.materials.append(mat_tablero)

bpy.ops.object.camera_add(location=(0, 0, 1.4))
cam = bpy.context.active_object
cam.name = "Camara_Cenital"
cam.rotation_euler = (0, 0, 0)
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 1.2
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type='AREA', location=(0, 0, 1.2))
luz = bpy.context.active_object
luz.name = "Luz_Area"
luz.data.energy = 80.0
luz.data.size   = 0.8

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 64
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1920

bpy.ops.wm.save_as_mainfile(filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/string_art_3D.blend")
print("✅ Cuadro 3D de Hilos guardado en string_art_3D.blend")
