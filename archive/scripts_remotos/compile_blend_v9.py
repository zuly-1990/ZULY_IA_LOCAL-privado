import bpy
import os

print("=== INICIANDO COMPILACIÓN V9 INTENTO 3 — OBJETOS SEPARADOS POR COLECCIONES ===")

# Limpiar escena completa
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for mesh in list(bpy.data.meshes):
    try: bpy.data.meshes.remove(mesh)
    except: pass
for col in list(bpy.data.collections):
    try: bpy.data.collections.remove(col)
    except: pass

# ------------------------------------------------------------------ #
# Helper: crear o recuperar una colección y enlazarla a un padre
# ------------------------------------------------------------------ #
def get_or_create_collection(name, parent_col=None):
    if name in bpy.data.collections:
        col = bpy.data.collections[name]
    else:
        col = bpy.data.collections.new(name)
        if parent_col:
            parent_col.children.link(col)
        else:
            bpy.context.scene.collection.children.link(col)
    return col

# ------------------------------------------------------------------ #
# Helper: asegurar que el objeto NO está ya vinculado a la escena
# ------------------------------------------------------------------ #
def safe_link_scene(obj):
    try:
        bpy.context.scene.collection.objects.link(obj)
    except:
        pass

def safe_link_col(col, obj):
    try:
        col.objects.link(obj)
    except:
        pass

# ------------------------------------------------------------------ #
# Colecciones raíz
# ------------------------------------------------------------------ #
root_3d      = get_or_create_collection("Modelo 3D — Villa Savoye")
root_2d      = get_or_create_collection("Planos 2D (Referencia)")
root_fachs   = get_or_create_collection("Fachadas y Cortes")

# ------------------------------------------------------------------ #
# Mapeo de tipo de elemento por nombre del objeto
# ------------------------------------------------------------------ #
TIPO_MAP = {
    "Losa_Base":    ["losa_base", "losa base"],
    "Losa_Techo":   ["losa_techo", "losa techo", "losa techo"],
    "Muros":        ["muro", "_muros"],
    "Muretes":      ["murete", "_muretes"],
    "Columnas":     ["columna", "_columnas"],
    "Ventanas":     ["ventana", "cristal", "ventanal"],
    "Puertas":      ["puerta", "puertita"],
    "Escalera":     ["escalera", "escal"],
    "Curvos":       ["curvo", "curve"],
    "Proyecciones": ["proyeccion", "flecha"],
}

def inferir_tipo(obj_name):
    """Intenta inferir el tipo de elemento a partir del nombre del objeto."""
    nl = obj_name.lower()
    for tipo, keywords in TIPO_MAP.items():
        for kw in keywords:
            if kw in nl:
                return tipo
    return None

folder = "/opt/zuly/resultados_masivos_v9/"

# ------------------------------------------------------------------ #
# NIVELES 3D — cargar TODOS los objetos y organizar en colecciones
# ------------------------------------------------------------------ #
niveles = [
    ("01 Primer Nivel v08_v9_3d.blend",  "Primer Nivel",  "N1", 3.50, 0.0),
    ("02 Segundo Nivel v02_v9_3d.blend", "Segundo Nivel", "N2", 3.20, 3.50),
    ("03 Tercer Nivel v02_v9_3d.blend",  "Tercer Nivel",  "N3", 3.00, 6.70),
]

for filename, nivel_name, prefix, target_z, stack_z in niveles:
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        print(f"ERROR: No existe {filepath}")
        continue

    print(f"\n{'='*50}")
    print(f"Cargando {nivel_name} desde {filename}")
    print(f"{'='*50}")

    # Colección del nivel
    nivel_col = get_or_create_collection(nivel_name, root_3d)

    # Cargar TODOS los objetos del blend
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = data_from.objects

    total_cargados = 0
    for obj in data_to.objects:
        if obj is None or obj.type != 'MESH':
            continue

        # Renombrar si no tiene el prefijo correcto
        obj_name_orig = obj.name
        if not obj.name.startswith(prefix + "_"):
            tipo = inferir_tipo(obj.name)
            if tipo:
                new_name = f"{prefix}_{tipo}"
            else:
                new_name = f"{prefix}_{obj.name}"
            # Evitar colisiones
            counter = 1
            base = new_name
            while new_name in bpy.data.objects and bpy.data.objects[new_name] is not obj:
                new_name = f"{base}_{counter}"
                counter += 1
            obj.name = new_name

        # Enlazar a la escena y a la colección del nivel
        safe_link_scene(obj)
        safe_link_col(nivel_col, obj)

        # Aplicar offset Z del piso (apilado)
        obj.location.z += stack_z

        v_count = len(obj.data.vertices)
        f_count = len(obj.data.polygons)
        z_dim   = round(obj.dimensions.z, 3)
        print(f"  ✅ {obj.name:35s} | V:{v_count:6d} | F:{f_count:6d} | Z_dim:{z_dim:5.2f}m | loc_z:{obj.location.z:.2f}m")
        total_cargados += 1

    print(f"  → {nivel_name}: {total_cargados} objetos cargados")

    # ---------- Vectores DXF de referencia (a X+35m) ---------- #
    dxf_filename = filename.replace('_v9_3d.blend', '.dxf')
    dxf_filepath = os.path.join("/opt/zuly/planos_temp/Planos y premodelado/", dxf_filename)
    if os.path.exists(dxf_filepath):
        nivel_2d_col = get_or_create_collection(f"Plano 2D — {nivel_name}", root_2d)
        old_objs = set(bpy.context.scene.objects)
        try:
            bpy.ops.preferences.addon_enable(module='io_import_dxf')
            bpy.ops.import_scene.dxf(filepath=dxf_filepath)
        except Exception as e:
            print(f"  ⚠️ Error importando DXF {dxf_filename}: {e}")
            continue

        new_objs = [o for o in bpy.context.scene.objects if o not in old_objs]
        curves = [o for o in new_objs if o.type in ['CURVE', 'MESH']]

        if curves:
            bpy.ops.object.select_all(action='DESELECT')
            for c in curves:
                c.select_set(True)
            bpy.context.view_layer.objects.active = curves[0]
            try:
                bpy.ops.object.convert(target='CURVE')
                bpy.ops.object.join()
            except Exception as e:
                print(f"  ⚠️ Error convirtiendo DXF curves: {e}")

            vec_obj = bpy.context.active_object
            vec_obj.name = f"Plano2D_{nivel_name.replace(' ', '_')}"
            vec_obj.location.x += 35.0
            vec_obj.location.z = stack_z
            safe_link_col(nivel_2d_col, vec_obj)
            print(f"  📐 Plano 2D '{nivel_name}' → X={vec_obj.location.x:.0f}m, Z={stack_z:.2f}m")

# ------------------------------------------------------------------ #
# FACHADAS Y CORTES — objeto único por archivo en colección raíz
# ------------------------------------------------------------------ #
planos_2d = [
    ("04 Fachada Principal v01_v9_3d.blend",       "Fachada Principal"),
    ("05 Fachada Lateral Derecho v01_v9_3d.blend", "Fachada Lateral Derecha"),
    ("06 Fachada Lateral Izquierdo v01_v9_3d.blend","Fachada Lateral Izquierda"),
    ("07 Fachada Posterior v01_v9_3d.blend",        "Fachada Posterior"),
    ("08 Corte 01_v9_3d.blend",                     "Corte 01"),
    ("08 Corte 02_v9_3d.blend",                     "Corte 02"),
    ("08 Corte 03_v9_3d.blend",                     "Corte 03"),
]

for filename, fachada_name in planos_2d:
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        print(f"  ⚠️ No existe: {filepath}")
        continue

    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = data_from.objects

    mesh_objs = [o for o in data_to.objects if o is not None and o.type == 'MESH']
    if mesh_objs:
        best = max(mesh_objs, key=lambda o: len(o.data.vertices))
        best.name = fachada_name
        safe_link_scene(best)
        safe_link_col(root_fachs, best)
        print(f"  📋 {fachada_name:35s} | V:{len(best.data.vertices):6d}")

# ------------------------------------------------------------------ #
# Purgar datos huérfanos
# ------------------------------------------------------------------ #
try:
    bpy.data.orphans_purge()
except:
    pass

# ------------------------------------------------------------------ #
# Guardar intento_3
# ------------------------------------------------------------------ #
output_path = os.path.join(folder, "Villa_Savoye_V9_Modelado3D_intento_3.blend")
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("\n" + "="*60)
print("=== COMPILADO INTENTO 3 COMPLETADO ✅ ===")
print(f"Guardado en: {output_path}")
print("="*60)
print("\n--- RESUMEN DE COLECCIONES ---")
for col in bpy.data.collections:
    objs_mesh = [o for o in col.objects if o.type == 'MESH']
    if objs_mesh:
        print(f"  📁 {col.name}: {len(objs_mesh)} objetos")
        for o in objs_mesh:
            print(f"       • {o.name:35s} | V:{len(o.data.vertices):6d} | F:{len(o.data.polygons):6d} | loc_z:{o.location.z:.2f}m")
print("="*60)
