import bpy
import bmesh
import numpy as np
from mathutils import Vector, Matrix, Quaternion
import math

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
MARGEN          = 0.02   # espacio entre piezas en el grid (metros)
ESCALA_PREVIEW  = 1.0    # multiplicador global de separación
GROSOR_FLAT     = 0.001  # Solidify mínimo para que las piezas sean visibles
TOLERANCIA_AREA = 1e-8   # descartar caras degeneradas

# ─────────────────────────────────────────────
# UTILIDADES DE ÁLGEBRA LINEAL
# ─────────────────────────────────────────────

def normal_a_matriz_rotacion(normal_cara: Vector) -> Matrix:
    n = normal_cara.normalized()
    z = Vector((0.0, 0.0, 1.0))

    dot = n.dot(z)
    dot = max(-1.0, min(1.0, dot))   # clamp numérico

    if dot > 1.0 - 1e-9:
        return Matrix.Identity(4)
    if dot < -1.0 + 1e-9:
        return Matrix.Rotation(math.pi, 4, 'X')

    eje = n.cross(z)          # eje de rotación
    eje_len = eje.length
    if eje_len < 1e-9:
        return Matrix.Identity(4)

    eje_n = eje / eje_len     # eje normalizado
    angulo = math.acos(dot)   # θ en radianes

    return Matrix.Rotation(angulo, 4, eje_n)

def calcular_aabb_2d(verts_2d: np.ndarray):
    mn = verts_2d.min(axis=0)
    mx = verts_2d.max(axis=0)
    return mn[0], mn[1], mx[0] - mn[0], mx[1] - mn[1]

# ─────────────────────────────────────────────
# PASO 1: OBTENER OBJETO ACTIVO Y VALIDAR
# ─────────────────────────────────────────────
obj_fuente = bpy.context.active_object
if obj_fuente is None or obj_fuente.type != 'MESH':
    raise RuntimeError("Selecciona un objeto MESH como activo antes de ejecutar.")

depsgraph   = bpy.context.evaluated_depsgraph_get()
obj_eval    = obj_fuente.evaluated_get(depsgraph)
mesh_eval   = obj_eval.to_mesh()

bm_source = bmesh.new()
bm_source.from_mesh(mesh_eval)
bmesh.ops.transform(
    bm_source,
    matrix=obj_fuente.matrix_world,
    verts=bm_source.verts
)
bm_source.verts.ensure_lookup_table()
bm_source.faces.ensure_lookup_table()

# ─────────────────────────────────────────────
# PASO 2: LIMPIAR ESCENA (preservar objeto fuente opcional)
# ─────────────────────────────────────────────
nombre_fuente = obj_fuente.name
obj_fuente.hide_set(True)

for o in list(bpy.data.objects):
    if o.name != nombre_fuente:
        bpy.data.objects.remove(o, do_unlink=True)
for bloque in [bpy.data.meshes, bpy.data.curves, bpy.data.materials]:
    for item in list(bloque):
        if item.users == 0:
            bloque.remove(item)

# ─────────────────────────────────────────────
# MATERIALES GLOBALES (paleta por cara)
# ─────────────────────────────────────────────
PALETA = [
    (0.80, 0.15, 0.15, 1), (0.15, 0.65, 0.15, 1),
    (0.15, 0.35, 0.85, 1), (0.85, 0.65, 0.10, 1),
    (0.65, 0.15, 0.75, 1), (0.10, 0.70, 0.75, 1),
    (0.90, 0.45, 0.10, 1), (0.45, 0.28, 0.15, 1),
]

materiales_pool = []
for i, color in enumerate(PALETA):
    mat = bpy.data.materials.new(f"CNC_Pieza_{i:02d}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value  = 0.6
    materiales_pool.append(mat)

# ─────────────────────────────────────────────
# PASO 3: EXTRAER, ROTAR Y APLANAR CADA CARA
# ─────────────────────────────────────────────
piezas = []

for idx, cara in enumerate(bm_source.faces):
    if cara.calc_area() < TOLERANCIA_AREA:
        continue

    verts_mundo = np.array([[v.co.x, v.co.y, v.co.z] for v in cara.verts], dtype=np.float64)
    normal_mundo = cara.normal.copy()
    R4 = normal_a_matriz_rotacion(normal_mundo)
    R3 = np.array([[R4[i][j] for j in range(3)] for i in range(3)])

    verts_flat = verts_mundo @ R3.T
    centroide_2d = verts_flat[:, :2].mean(axis=0)
    verts_2d_local = verts_flat[:, :2] - centroide_2d

    min_x, min_y, ancho, alto = calcular_aabb_2d(verts_2d_local)

    mesh_pieza = bpy.data.meshes.new(f"Pieza_{idx:03d}_mesh")
    obj_pieza  = bpy.data.objects.new(f"Pieza_{idx:03d}", mesh_pieza)
    bpy.context.collection.objects.link(obj_pieza)

    bm_pieza = bmesh.new()
    bverts = [bm_pieza.verts.new(Vector((float(v[0]), float(v[1]), 0.0))) for v in verts_2d_local]
    try:
        bm_pieza.faces.new(bverts)
    except Exception:
        bmesh.ops.convex_hull(bm_pieza, input=bm_pieza.verts)
    bm_pieza.to_mesh(mesh_pieza)
    bm_pieza.free()
    mesh_pieza.update()

    mod_s = obj_pieza.modifiers.new("Grosor_CNC", 'SOLIDIFY')
    mod_s.thickness      = GROSOR_FLAT
    mod_s.offset         = 1.0
    mod_s.use_even_offset = True

    mat = materiales_pool[idx % len(materiales_pool)]
    mesh_pieza.materials.append(mat)

    piezas.append({
        "obj"        : obj_pieza,
        "ancho"      : ancho,
        "alto"       : alto,
        "min_x"      : min_x,
        "min_y"      : min_y,
    })

bm_source.free()
obj_eval.to_mesh_clear()

# ─────────────────────────────────────────────
# PASO 4: NESTING / GRID PACKING (Strip Packing)
# ─────────────────────────────────────────────
area_total = sum(p["ancho"] * p["alto"] for p in piezas)
ANCHO_MAX_FILA = math.sqrt(area_total) * 1.4

piezas.sort(key=lambda p: p["alto"], reverse=True)

cursor_x   = 0.0
cursor_y   = 0.0
alto_fila  = 0.0

for pieza in piezas:
    ancho = pieza["ancho"] + MARGEN
    alto  = pieza["alto"]  + MARGEN

    if cursor_x + ancho > ANCHO_MAX_FILA and cursor_x > 0:
        cursor_y  += alto_fila
        cursor_x   = 0.0
        alto_fila  = 0.0

    pos_x = cursor_x - pieza["min_x"]
    pos_y = cursor_y - pieza["min_y"]
    pieza["obj"].location = Vector((pos_x, pos_y, 0.0))

    cursor_x  += ancho
    alto_fila  = max(alto_fila, alto)

# ─────────────────────────────────────────────
# PASO 5: PLANO BASE (mesa de corte CNC)
# ─────────────────────────────────────────────
ancho_mesa = ANCHO_MAX_FILA + 0.1
alto_mesa  = cursor_y + alto_fila + 0.1

bpy.ops.mesh.primitive_plane_add(
    size=1.0,
    location=(ancho_mesa / 2 - 0.05, alto_mesa / 2 - 0.05, -0.001)
)
mesa = bpy.context.active_object
mesa.name = "Mesa_CNC"
mesa.scale = (ancho_mesa, alto_mesa, 1.0)
bpy.ops.object.transform_apply(scale=True)

mat_mesa = bpy.data.materials.new("Mat_Mesa_CNC")
mat_mesa.use_nodes = True
bsdf_m = mat_mesa.node_tree.nodes.get("Principled BSDF")
if bsdf_m:
    bsdf_m.inputs["Base Color"].default_value = (0.04, 0.04, 0.04, 1)
    bsdf_m.inputs["Roughness"].default_value  = 0.95
mesa.data.materials.append(mat_mesa)

# ─────────────────────────────────────────────
# PASO 6: CÁMARA CENITAL ORTOGRÁFICA
# ─────────────────────────────────────────────
cx = ancho_mesa / 2 - 0.05
cy = alto_mesa  / 2 - 0.05
altura_cam = max(ancho_mesa, alto_mesa) * 1.1

bpy.ops.object.camera_add(location=(cx, cy, altura_cam))
cam = bpy.context.active_object
cam.name  = "Camara_CNC_Cenital"
cam.rotation_euler = (0, 0, 0)
cam.data.type       = 'ORTHO'
cam.data.ortho_scale = max(ancho_mesa, alto_mesa) * 1.15
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type='AREA', location=(cx, cy, altura_cam * 0.8))
luz = bpy.context.active_object
luz.name = "Luz_CNC"
luz.data.energy = 200.0
luz.data.size   = max(ancho_mesa, alto_mesa)

print("✅ Desdoblamiento CNC completado")
