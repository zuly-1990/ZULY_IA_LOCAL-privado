import bpy
import bmesh
from mathutils import Vector, Matrix, Euler, Quaternion
import math

# ============================================================
# MOBILIARIO TRANSFORMABLE — ORIGAMI KINEMATICS
# Silla plegable tipo bisagra con Armature + IK Constraints
# Compatible con Blender 4.0+
# ============================================================

# ── 1. LIMPIAR ESCENA COMPLETAMENTE ──────────────────────────
def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for col in bpy.data.collections:
        bpy.data.collections.remove(col)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for arm in bpy.data.armatures:
        bpy.data.armatures.remove(arm)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

limpiar_escena()

# ── PARÁMETROS GLOBALES ───────────────────────────────────────
ANCHO_TOTAL   = 0.50   # metros → 50 cm ancho de la silla
LARGO_TOTAL   = 0.45   # metros → 45 cm largo
GROSOR_MM     = 0.015  # 15 mm (Solidify)
GAP           = 0.003  # 3 mm de separación entre paneles (junta de bisagra)

# El asiento central ocupa el 40% del ancho, los laterales 30% cada uno
ANCHO_CENTRAL = ANCHO_TOTAL * 0.40
ANCHO_LATERAL = ANCHO_TOTAL * 0.30   # cada panel lateral

# Posiciones X de los centros de cada panel
# Panel izquierdo: su centro en X = -(ANCHO_CENTRAL/2 + GAP + ANCHO_LATERAL/2)
X_LEFT   = -(ANCHO_CENTRAL / 2 + GAP + ANCHO_LATERAL / 2)
X_CENTER =  0.0
X_RIGHT  =  (ANCHO_CENTRAL / 2 + GAP + ANCHO_LATERAL / 2)

# ── 2. CREAR LOS 3 PANELES ───────────────────────────────────
def crear_panel(nombre, centro_x, ancho, largo, color_rgba):
    """
    Crea un plano de dimensiones (ancho × largo) centrado en (centro_x, 0, 0).
    Agrega Solidify para simular grosor de 15 mm.
    """
    bpy.ops.mesh.primitive_plane_add(size=1, location=(centro_x, 0, 0))
    obj = bpy.context.active_object
    obj.name = nombre

    # Escalar dimensiones exactas
    obj.scale = (ancho, largo, 1.0)
    bpy.ops.object.transform_apply(scale=True)

    # Modificador Solidify → grosor 15 mm hacia abajo (-Z local)
    mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod.thickness        = GROSOR_MM
    mod.offset           = -1.0   # crece hacia -Z (cara inferior plana en Z=0)
    mod.use_even_offset  = True

    # Material de color para distinguir paneles
    mat = bpy.data.materials.new(name=f"Mat_{nombre}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color_rgba
        bsdf.inputs["Roughness"].default_value  = 0.4
    obj.data.materials.append(mat)

    return obj

panel_left   = crear_panel("Panel_Izquierdo", X_LEFT,   ANCHO_LATERAL, LARGO_TOTAL, (0.8, 0.3, 0.1, 1))
panel_center = crear_panel("Panel_Central",   X_CENTER, ANCHO_CENTRAL, LARGO_TOTAL, (0.9, 0.7, 0.2, 1))
panel_right  = crear_panel("Panel_Derecho",   X_RIGHT,  ANCHO_LATERAL, LARGO_TOTAL, (0.8, 0.3, 0.1, 1))

# ── 3. CREAR EL ARMATURE (ESQUELETO) ─────────────────────────
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm_obj  = bpy.context.active_object
arm_obj.name = "Armature_Silla"
arm_data = arm_obj.data
arm_data.name = "Silla_Rig"
arm_data.display_type = 'STICK'
arm_obj.show_in_front   = True

bones = arm_data.edit_bones
for b in list(bones):
    bones.remove(b)

# ── HUESO RAÍZ (ancla en el suelo) ───────────────────────────
root = bones.new("root")
root.head = Vector((0, 0, -0.30))
root.tail = Vector((0, 0,  0.00))
root.use_deform = False

# ── HUESO DEL ASIENTO (seat) ──────────────────────────────────
seat = bones.new("seat")
seat.head   = Vector((0, 0, 0.00))
seat.tail   = Vector((0, 0, 0.30))
seat.parent = root
seat.use_connect = True
seat.use_deform  = True

# ── HUESO BISAGRA IZQUIERDA (hinge_L) ────────────────────────
X_HINGE_L = -(ANCHO_CENTRAL / 2 + GAP / 2)
hinge_L = bones.new("hinge_L")
hinge_L.head = Vector((X_HINGE_L, -LARGO_TOTAL / 2, 0))
hinge_L.tail = Vector((X_HINGE_L,  LARGO_TOTAL / 2, 0))
hinge_L.parent       = seat
hinge_L.use_connect  = False
hinge_L.use_deform   = False

# ── HUESO PATA IZQUIERDA (leg_L) ─────────────────────────────
leg_L = bones.new("leg_L")
leg_L.head = Vector((X_LEFT, 0, 0))
leg_L.tail = Vector((X_LEFT - ANCHO_LATERAL, 0, 0))
leg_L.parent      = hinge_L
leg_L.use_connect = False
leg_L.use_deform  = True

# ── HUESO BISAGRA DERECHA (hinge_R) ──────────────────────────
X_HINGE_R = (ANCHO_CENTRAL / 2 + GAP / 2)
hinge_R = bones.new("hinge_R")
hinge_R.head = Vector((X_HINGE_R, -LARGO_TOTAL / 2, 0))
hinge_R.tail = Vector((X_HINGE_R,  LARGO_TOTAL / 2, 0))
hinge_R.parent      = seat
hinge_R.use_connect = False
hinge_R.use_deform  = False

# ── HUESO PATA DERECHA (leg_R) ───────────────────────────────
leg_R = bones.new("leg_R")
leg_R.head = Vector((X_RIGHT, 0, 0))
leg_R.tail = Vector((X_RIGHT + ANCHO_LATERAL, 0, 0))
leg_R.parent      = hinge_R
leg_R.use_connect = False
leg_R.use_deform  = True

# ── IK TARGET (empty para controlar el seat) ─────────────────
ik_target_bone = bones.new("IK_Target")
ik_target_bone.head = Vector((0, 0, 0.30))
ik_target_bone.tail = Vector((0, 0, 0.35))
ik_target_bone.use_deform = False

bpy.ops.object.mode_set(mode='OBJECT')

# ── 4. POSE MODE: AGREGAR RESTRICCIONES ──────────────────────
bpy.ops.object.mode_set(mode='POSE')
pose_bones = arm_obj.pose.bones

# ── IK CONSTRAINT EN EL HUESO "seat" ─────────────────────────
pb_seat = pose_bones["seat"]
ik = pb_seat.constraints.new(type='IK')
ik.name            = "IK_Asiento"
ik.target          = arm_obj
ik.subtarget       = "IK_Target"
ik.chain_count     = 2
ik.use_rotation    = True
ik.iterations      = 500
ik.use_stretch     = False

# ── LIMIT ROTATION EN BISAGRAS ────────────────────────────────
for nombre_bisagra in ["hinge_L", "hinge_R"]:
    pb = pose_bones[nombre_bisagra]
    lr = pb.constraints.new(type='LIMIT_ROTATION')
    lr.name            = "Bisagra_Limite"
    lr.owner_space     = 'LOCAL'
    lr.use_limit_x     = True
    lr.min_x           = 0.0
    lr.max_x           = 0.0
    lr.use_limit_y     = True
    lr.min_y           = math.radians(-90)
    lr.max_y           = math.radians(  0)
    lr.use_limit_z     = True
    lr.min_z           = 0.0
    lr.max_z           = 0.0
    lr.influence       = 1.0

# ── COPY ROTATION ─────────────────────────────────────────────
pb_left  = pose_bones["leg_L"]
pb_right = pose_bones["leg_R"]

def agregar_copy_rotation(pb, target_obj, subtarget):
    cr = pb.constraints.new(type='COPY_ROTATION')
    cr.name        = "Sigue_Bisagra"
    cr.target      = target_obj
    cr.subtarget   = subtarget
    cr.owner_space  = 'LOCAL'
    cr.target_space = 'LOCAL'
    cr.use_x       = False
    cr.use_y       = True
    cr.use_z       = False
    cr.mix_mode    = 'REPLACE'
    cr.influence   = 1.0

agregar_copy_rotation(pb_left,  arm_obj, "hinge_L")
agregar_copy_rotation(pb_right, arm_obj, "hinge_R")

bpy.ops.object.mode_set(mode='OBJECT')

# ── 5. PARENT PANELES AL ARMATURE (Bone Parenting) ───────────
for (obj, bone) in [(panel_center, "seat"),
                    (panel_left,   "leg_L"),
                    (panel_right,  "leg_R")]:
    obj.parent      = arm_obj
    obj.parent_type = 'BONE'
    obj.parent_bone = bone
    obj.matrix_parent_inverse = (
        arm_obj.matrix_world @
        Matrix.Translation(arm_obj.pose.bones[bone].head)
    ).inverted()

# ── 6. CREAR EMPTY PARA CONTROLAR EL IK TARGET ───────────────
bpy.ops.object.empty_add(type='SPHERE', radius=0.03, location=(0, 0, 0.30))
ik_ctrl = bpy.context.active_object
ik_ctrl.name = "CTRL_Asiento"

bpy.ops.object.select_all(action='DESELECT')
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='POSE')

pb_ik_target = pose_bones["IK_Target"]
ct = pb_ik_target.constraints.new(type='COPY_LOCATION')
ct.name        = "Sigue_CTRL"
ct.target      = ik_ctrl
ct.owner_space  = 'WORLD'
ct.target_space = 'WORLD'

bpy.ops.object.mode_set(mode='OBJECT')

# ── 7. CONFIGURAR CÁMARA Y LUZ ───────────────────────────────
bpy.ops.object.camera_add(location=(1.2, -1.2, 0.9))
cam = bpy.context.active_object
cam.rotation_euler = Euler((math.radians(65), 0, math.radians(45)), 'XYZ')
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type='SUN', location=(2, 2, 3))
sol = bpy.context.active_object
sol.data.energy = 3.0

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = ik_ctrl
ik_ctrl.select_set(True)

# Guardar
bpy.ops.wm.save_as_mainfile(filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/origami_silla.blend")
print("✅ Silla Origami guardada con éxito en origami_silla.blend")
