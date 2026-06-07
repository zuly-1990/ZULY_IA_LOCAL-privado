import bpy
import sys
import os

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_blanco_pips_multicolor.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

DIE_NAME = "Parques_Die_Multicolor"

# Un color distinto por cara (RGB 0–1). Cuerpo del dado: blanco.
FACE_MATERIALS = {
    "F1": ("Pip_F1", [1.0, 0.15, 0.15, 1.0]),
    "F2": ("Pip_F2", [0.15, 0.85, 0.2, 1.0]),
    "F3": ("Pip_F3", [0.2, 0.35, 1.0, 1.0]),
    "F4": ("Pip_F4", [1.0, 0.92, 0.2, 1.0]),
    "F5": ("Pip_F5", [0.85, 0.2, 0.95, 1.0]),
    "F6": ("Pip_F6", [0.15, 0.9, 0.95, 1.0]),
}


def create_multicolor_pips_dice():
    log_info("=== DADO BLANCO + PUNTOS MULTICOLOR (handlers estándar + mínimo bpy) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)

    agent.execute_via_router("blender.clear_scene", {})

    agent.execute_via_router(
        "blender.create_material",
        {
            "name": "Die_White",
            "color": [0.98, 0.98, 0.98, 1],
            "roughness": 0.12,
            "metallic": 0.0,
        },
    )
    for _face, (mat_name, rgba) in FACE_MATERIALS.items():
        agent.execute_via_router(
            "blender.create_material",
            {
                "name": mat_name,
                "color": rgba,
                "roughness": 0.75,
                "metallic": 0.0,
            },
        )

    agent.execute_via_router(
        "blender.create_cube",
        {"location": [0, 0, 1], "scale": 1.0, "name": DIE_NAME},
    )

    agent.execute_via_router(
        "blender.apply_material",
        {"object_name": DIE_NAME, "material_name": "Die_White"},
    )

    # Sin handler de subdivisión en EDIT: un único bloque bpy
    agent.execute_via_router(
        "blender.run_python_script",
        {
            "script_content": f"""
import bpy
obj = bpy.data.objects.get('{DIE_NAME}')
if obj:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=4)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599
"""
        },
    )

    agent.execute_via_router(
        "blender.add_bevel",
        {"object_name": DIE_NAME, "width": 0.25, "segments": 16},
    )

    pips_map = {
        "F1": [[0, 0, 1.95]],
        "F2": [[0.5, -0.95, 1.5], [-0.5, -0.95, 0.5]],
        "F3": [[0.95, 0.5, 1.5], [0.95, 0, 1], [0.95, -0.5, 0.5]],
        "F4": [
            [-0.95, 0.5, 1.5],
            [-0.95, 0.5, 0.5],
            [-0.95, -0.5, 1.5],
            [-0.95, -0.5, 0.5],
        ],
        "F5": [
            [0.5, 0.95, 1.5],
            [-0.5, 0.95, 0.5],
            [0.5, 0.95, 0.5],
            [-0.5, 0.95, 1.5],
            [0, 0.95, 1],
        ],
        "F6": [
            [0.5, 0.5, 0.05],
            [0.5, -0.5, 0.05],
            [-0.5, 0.5, 0.05],
            [-0.5, -0.5, 0.05],
            [0.5, 0, 0.05],
            [-0.5, 0, 0.05],
        ],
    }

    counter = 0
    for face, locs in pips_map.items():
        mat_name = FACE_MATERIALS[face][0]
        rgb = FACE_MATERIALS[face][1][:3]
        for loc in locs:
            pip_name = f"Pip_MC_{face}_{counter}"
            agent.execute_via_router(
                "blender.create_sphere",
                {
                    "location": loc,
                    "radius": 0.18,
                    "name": pip_name,
                    "color": rgb,
                    "subdivisions": 32,
                    "ring_count": 16,
                },
            )
            agent.execute_via_router(
                "blender.apply_material",
                {"object_name": pip_name, "material_name": mat_name},
            )
            agent.execute_via_router(
                "blender.add_boolean_modifier",
                {
                    "object_name": DIE_NAME,
                    "operand_object": pip_name,
                    "operation": "DIFFERENCE",
                    "hide_operand": False,
                    "material_mode": "TRANSFER",
                },
            )
            agent.execute_via_router(
                "blender.apply_modifier",
                {"object_name": DIE_NAME, "apply_last": True},
            )
            agent.execute_via_router(
                "blender.delete_object",
                {"object_name": pip_name},
            )
            counter += 1

    agent.execute_via_router(
        "blender.add_weighted_normal",
        {"object_name": DIE_NAME, "keep_sharp": True},
    )
    agent.execute_via_router(
        "blender.apply_modifier",
        {"object_name": DIE_NAME, "apply_last": True},
    )

    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADO MULTICOLOR GUARDADO: {SAVE_PATH} ===")
        print(f"ZULY_LISTO_BLEND={SAVE_PATH}")
    except Exception as e:
        log_error(f"Error guardando dado multicolor: {e}")
        print(f"ZULY_ERROR={e}")


if __name__ == "__main__":
    create_multicolor_pips_dice()
