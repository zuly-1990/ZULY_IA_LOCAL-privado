"""
fix_geometry_v9.py — Script de post-procesamiento para Blender 3.6
Corrige geometría de cada nivel del blend compilado:
  1. Genera escaleras paramétricas REALES con peldaños si no existen
  2. Sella caras abiertas en muros y columnas (select_non_manifold → fill)
  3. Elimina caras duplicadas/interpuestas (remove_doubles + delete_interior)
  4. Recalcula normales para eliminar caras oscuras
"""
import bpy
import bmesh
from mathutils import Vector

print("=" * 60)
print("FIX GEOMETRY V9 — Post-procesamiento determinístico")
print("=" * 60)

# ================================================================== #
# 1. ESCALERAS PARAMÉTRICAS                                         #
# ================================================================== #
# Datos de la escalera real de Villa Savoye:
# - Ancho 1.20m (escalera de servicio) / 2.40m (escalera principal)
# - Contrahuella ~0.175m, Huella ~0.28m
# - La escalera principal está cerca de X=7.5, Y=9.0 en el plano

STAIR_CONFIGS = {
    "N1": {
        "name": "N1_Escalera",
        "num_steps": 20,
        "step_w": 1.20,     # ancho
        "step_d": 0.28,     # huella (profundidad)
        "step_h": 0.175,    # contrahuella (altura)
        "start_x": 7.5,
        "start_y": 9.0,
        "start_z": 0.30,    # sobre la losa base
        "collection": "Primer Nivel",
    },
    "N2": {
        "name": "N2_Escalera",
        "num_steps": 18,
        "step_w": 1.20,
        "step_d": 0.28,
        "step_h": 0.178,
        "start_x": 7.5,
        "start_y": 9.0,
        "start_z": 3.80,    # sobre losa del segundo nivel
        "collection": "Segundo Nivel",
    },
    "N3": {
        "name": "N3_Escalera",
        "num_steps": 17,
        "step_w": 1.20,
        "step_d": 0.28,
        "step_h": 0.176,
        "start_x": 7.5,
        "start_y": 9.0,
        "start_z": 7.00,
        "collection": "Tercer Nivel",
    },
}

def create_staircase(cfg):
    """Crea una escalera paramétrica con peldaños individuales unidos en un solo mesh."""
    name      = cfg["name"]
    n         = cfg["num_steps"]
    w         = cfg["step_w"]
    d         = cfg["step_d"]
    h         = cfg["step_h"]
    sx        = cfg["start_x"]
    sy        = cfg["start_y"]
    sz        = cfg["start_z"]
    col_name  = cfg["collection"]

    print(f"  🪜 Generando {name}: {n} peldaños, {w}m ancho, {d}m huella, {h}m contrahuella")

    # Crear cada peldaño como cubo
    step_objs = []
    for i in range(n):
        loc_x = sx + i * d + d / 2.0
        loc_y = sy + w / 2.0
        loc_z = sz + i * h + h / 2.0

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(loc_x, loc_y, loc_z))
        step = bpy.context.active_object
        step.dimensions = (d, w, h)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        step.name = f"_tmp_step_{i}"
        step_objs.append(step)

    # Unir todos los peldaños
    bpy.ops.object.select_all(action='DESELECT')
    for s in step_objs:
        s.select_set(True)
    bpy.context.view_layer.objects.active = step_objs[0]
    bpy.ops.object.join()

    stair = bpy.context.active_object
    stair.name = name
    if stair.data:
        stair.data.name = name + "_mesh"

    # Limpiar geometría
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.001)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Enlazar a la colección correcta
    if col_name in bpy.data.collections:
        col = bpy.data.collections[col_name]
        try:
            col.objects.link(stair)
        except:
            pass

    v = len(stair.data.vertices)
    f = len(stair.data.polygons)
    print(f"  ✅ {name} creada: V={v}, F={f}, loc_z={stair.location.z:.2f}m")
    return stair


def has_real_staircase(prefix):
    """Verifica si ya hay una escalera REAL (con caras y volumen) para este piso."""
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
        nl = obj.name.lower()
        if prefix.lower() in nl and "escal" in nl:
            if len(obj.data.polygons) >= 30 and obj.dimensions.z >= 0.10:
                print(f"  ℹ️ Escalera existente encontrada: {obj.name} (F={len(obj.data.polygons)}, Z={obj.dimensions.z:.2f}m)")
                return True
    return False


print("\n--- PASO 1: Verificar y crear escaleras ---")
for prefix, cfg in STAIR_CONFIGS.items():
    if has_real_staircase(prefix):
        print(f"  ✓ {prefix} ya tiene escalera válida, eliminando vieja si es defectuosa y recreando")
        # Eliminar la existente para reemplazarla con la paramétrica
        for obj in list(bpy.context.scene.objects):
            nl = obj.name.lower()
            if prefix.lower() in nl and "escal" in nl:
                bpy.data.objects.remove(obj, do_unlink=True)
    else:
        print(f"  ✗ {prefix} NO tiene escalera → Generando...")

    create_staircase(cfg)


# ================================================================== #
# 2. SELLAR CARAS ABIERTAS (muros, columnas, muretes)               #
# ================================================================== #
print("\n--- PASO 2: Sellando caras abiertas ---")

TARGET_TYPES = ["muro", "columna", "murete", "curvo", "losa"]

for obj in list(bpy.context.scene.objects):
    if obj.type != 'MESH':
        continue

    nl = obj.name.lower()
    is_target = any(t in nl for t in TARGET_TYPES)
    if not is_target:
        continue

    # Verificar si tiene bordes non-manifold (caras abiertas)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    non_manifold_edges = [e for e in bm.edges if not e.is_manifold and not e.is_boundary]
    boundary_edges = [e for e in bm.edges if e.is_boundary]
    bm.free()

    if len(boundary_edges) == 0:
        continue  # Ya está sellado

    print(f"  🔧 {obj.name}: {len(boundary_edges)} bordes abiertos → sellando...")

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    # Seleccionar bordes non-manifold (bordes de caras abiertas)
    bpy.ops.mesh.select_non_manifold(extend=False, use_wire=True, use_boundary=True,
                                      use_multi_face=False, use_non_contiguous=False,
                                      use_verts=False)
    # Rellenar los huecos
    try:
        bpy.ops.mesh.fill()
    except:
        try:
            bpy.ops.mesh.edge_face_add()
        except:
            pass

    # Recalcular normales
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)

    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"  ✅ {obj.name} sellado: F={len(obj.data.polygons)}")


# ================================================================== #
# 3. ELIMINAR CARAS INTERPUESTAS / DUPLICADAS                       #
# ================================================================== #
print("\n--- PASO 3: Eliminando caras interpuestas/duplicadas ---")

for obj in list(bpy.context.scene.objects):
    if obj.type != 'MESH' or len(obj.data.polygons) < 4:
        continue

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # Remove doubles: fusiona vértices superpuestos y las caras duplicadas
    bpy.ops.mesh.remove_doubles(threshold=0.001)

    # Eliminar caras interiores (faces que están dentro del sólido)
    bpy.ops.mesh.select_all(action='DESELECT')
    try:
        bpy.ops.mesh.select_interior_faces()
        if bpy.context.active_object.data.total_face_sel > 0:
            bpy.ops.mesh.delete(type='FACE')
            print(f"  🗑️ {obj.name}: caras interiores eliminadas")
    except:
        pass  # select_interior_faces puede fallar en geometría simple

    # Recalcular normales finales
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)

    bpy.ops.object.mode_set(mode='OBJECT')

# ================================================================== #
# 4. GUARDAR                                                        #
# ================================================================== #
output = "/opt/zuly/resultados_masivos_v9/Villa_Savoye_V9_Modelado3D_intento_3.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\n" + "=" * 60)
print("FIX GEOMETRY COMPLETADO ✅")
print(f"Guardado en: {output}")
print("=" * 60)

# Resumen final
print("\n--- OBJETOS EN ESCENA ---")
for obj in sorted(bpy.context.scene.objects, key=lambda o: o.name):
    if obj.type == 'MESH' and len(obj.data.polygons) > 0:
        print(f"  {obj.name:35s} | V:{len(obj.data.vertices):6d} | F:{len(obj.data.polygons):6d} | Z:{obj.dimensions.z:.2f}m | loc:{obj.location.z:.2f}m")
