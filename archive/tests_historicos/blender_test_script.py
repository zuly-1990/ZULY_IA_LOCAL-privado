
import bpy
import json
from datetime import datetime

# Inicializar escena
bpy.ops.wm.read_factory_settings(use_empty=False)

results = {
    "test_date": datetime.now().isoformat(),
    "commands": [],
    "scene_state": {
        "objects": 0,
        "objects_list": [],
        "frame": 0,
        "render_engine": ""
    }
}

# Estado inicial
initial_objects = len(bpy.data.objects)
results["scene_state"]["objects"] = initial_objects
results["scene_state"]["objects_list"] = [obj.name for obj in bpy.data.objects]
results["scene_state"]["frame"] = bpy.context.scene.frame_current
results["scene_state"]["render_engine"] = bpy.context.scene.render.engine

# Test 1: Crear cubo
try:
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    results["commands"].append({
        "id": 1,
        "action": "create_cube",
        "status": "SUCCESS",
        "timestamp": datetime.now().isoformat()
    })
except Exception as e:
    results["commands"].append({
        "id": 1,
        "action": "create_cube",
        "status": "FAILED",
        "error": str(e),
        "timestamp": datetime.now().isoformat()
    })

# Test 2: Mover objeto
try:
    if len(bpy.context.selected_objects) > 0:
        obj = bpy.context.selected_objects[0]
        obj.location = (2, 0, 0)
    results["commands"].append({
        "id": 2,
        "action": "move_object",
        "status": "SUCCESS",
        "timestamp": datetime.now().isoformat()
    })
except Exception as e:
    results["commands"].append({
        "id": 2,
        "action": "move_object",
        "status": "FAILED",
        "error": str(e),
        "timestamp": datetime.now().isoformat()
    })

# Test 3: Rotar objeto
try:
    if len(bpy.context.selected_objects) > 0:
        obj = bpy.context.selected_objects[0]
        obj.rotation_euler = (0.785, 0.785, 0)  # 45 grados
    results["commands"].append({
        "id": 3,
        "action": "rotate_object",
        "status": "SUCCESS",
        "timestamp": datetime.now().isoformat()
    })
except Exception as e:
    results["commands"].append({
        "id": 3,
        "action": "rotate_object",
        "status": "FAILED",
        "error": str(e),
        "timestamp": datetime.now().isoformat()
    })

# Test 4: Escalar objeto
try:
    if len(bpy.context.selected_objects) > 0:
        obj = bpy.context.selected_objects[0]
        obj.scale = (2, 2, 2)
    results["commands"].append({
        "id": 4,
        "action": "scale_object",
        "status": "SUCCESS",
        "timestamp": datetime.now().isoformat()
    })
except Exception as e:
    results["commands"].append({
        "id": 4,
        "action": "scale_object",
        "status": "FAILED",
        "error": str(e),
        "timestamp": datetime.now().isoformat()
    })

# Test 5: Crear esfera
try:
    bpy.ops.mesh.primitive_uv_sphere_add(location=(3, 0, 0))
    results["commands"].append({
        "id": 5,
        "action": "create_sphere",
        "status": "SUCCESS",
        "timestamp": datetime.now().isoformat()
    })
except Exception as e:
    results["commands"].append({
        "id": 5,
        "action": "create_sphere",
        "status": "FAILED",
        "error": str(e),
        "timestamp": datetime.now().isoformat()
    })

# Estado final
final_objects = len(bpy.data.objects)
results["scene_state"]["final_objects"] = final_objects
results["scene_state"]["objects_created"] = final_objects - initial_objects

# Guardar resultados
import json
output_path = "blender_execution_results.json"
with open(output_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"BLENDER_TEST_COMPLETE: {output_path}")
print("BLENDER_RESULTS:", json.dumps(results))
