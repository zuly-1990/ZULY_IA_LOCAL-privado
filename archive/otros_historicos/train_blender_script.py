
import json
import bpy
from datetime import datetime

# Configuración
training_data = {
    "date": datetime.now().isoformat(),
    "blender_version": bpy.app.version_string,
    "experiences": []
}

# Funciones auxiliares
def get_scene_state():
    """Captura estado actual de la escena."""
    return {
        "object_count": len(bpy.data.objects),
        "objects": [
            {
                "name": obj.name,
                "type": obj.type,
                "location": list(obj.location),
                "scale": list(obj.scale),
                "rotation": list(obj.rotation_euler)
            }
            for obj in bpy.data.objects
        ],
        "frame": bpy.context.scene.frame_current,
        "render_engine": bpy.context.scene.render.engine
    }

def evaluate_scene_quality():
    """Evalúa calidad de la escena (0-100)."""
    state = get_scene_state()
    score = 50  # Baseline
    
    # Méricas de calidad
    if len(state["objects"]) > 3:
        score += 10  # Más objetos = más complejo
    
    # Verificar variedad de tipos
    types = set(obj["type"] for obj in state["objects"])
    score += min(len(types) * 5, 20)
    
    # Verificar que objetos no estén en posición por defecto
    for obj in state["objects"]:
        if obj["location"] != [0, 0, 0]:
            score += 5
        if obj["rotation"] != [0, 0 ,0]:
            score += 3
    
    return min(score, 100)

def create_experience(action, parameters, intent):
    """Crea una experiencia y la guarda."""
    # Capturar estado ANTES
    state_before = get_scene_state()
    
    # Ejecutar acción
    try:
        if action == "create_cube":
            bpy.ops.mesh.primitive_cube_add(location=tuple(parameters.get("location", [0,0,0])))
            success = True
        elif action == "create_sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(location=tuple(parameters.get("location", [0,0,0])))
            success = True
        elif action == "move_object":
            if bpy.context.selected_objects:
                bpy.context.selected_objects[0].location = tuple(parameters.get("location", [0,0,0]))
            success = True
        elif action == "rotate_object":
            if bpy.context.selected_objects:
                bpy.context.selected_objects[0].rotation_euler = tuple(parameters.get("rotation", [0,0,0]))
            success = True
        elif action == "scale_object":
            if bpy.context.selected_objects:
                bpy.context.selected_objects[0].scale = tuple(parameters.get("scale", [1,1,1]))
            success = True
        else:
            success = False
    except:
        success = False
    
    # Capturar estado DESPUÉS
    state_after = get_scene_state()
    
    # Evaluar calidad
    quality_before = evaluate_scene_quality()
    quality_after = evaluate_scene_quality()
    
    # Crear experiencia
    experience = {
        "id": len(training_data["experiences"]) + 1,
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "intent": intent,
        "parameters": parameters,
        "success": success,
        "state_before": state_before,
        "state_after": state_after,
        "quality_before": quality_before,
        "quality_after": quality_after,
        "quality_improvement": quality_after - quality_before,
        "objects_created": len(state_after["objects"]) - len(state_before["objects"])
    }
    
    training_data["experiences"].append(experience)
    return experience

# =====================================================================
# PLAN DE ENTRENAMIENTO (20 experiencias reales)
# =====================================================================

print("\n" + "="*70)
print("ENTRENAMIENTO C2 MEMORY - DATOS REALES BLENDER")
print("="*70)

# Limpiar escena inicial
print("\n[SETUP] Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
print("[OK] Escena limpia\n")

# EXPERIENCIA 1-5: Crear objetos básicos
print("[BATCH 1] Creando objetos básicos (5 experiencias)...")
for i in range(1, 6):
    exp = create_experience(
        "create_cube",
        {"location": [i*3, 0, 0]},
        f"create_basic_cube_{i}"
    )
    print(f"  [{i}] {exp['action']} - Calidad antes: {exp['quality_before']}, después: {exp['quality_after']}")

# EXPERIENCIA 6-10: Crear esferas
print("\n[BATCH 2] Creando esferas (5 experiencias)...")
for i in range(1, 6):
    exp = create_experience(
        "create_sphere",
        {"location": [i*3, 2, 0]},
        f"create_sphere_{i}"
    )
    print(f"  [{5+i}] {exp['action']} - Calidad: {exp['quality_after']}")

# EXPERIENCIA 11-15: Rotaciones
print("\n[BATCH 3] Rotando objetos (5 experiencias)...")
for i in range(1, 6):
    import math
    angle = (i * 45) * (math.pi / 180)
    exp = create_experience(
        "rotate_object",
        {"rotation": [angle, angle, 0]},
        f"rotate_object_{i}"
    )
    print(f"  [{10+i}] rotate_object - Calidad: {exp['quality_after']}")

# EXPERIENCIA 16-20: Escalado
print("\n[BATCH 4] Escalando objetos (5 experiencias)...")
for i in range(1, 6):
    exp = create_experience(
        "scale_object",
        {"scale": [1+(i*0.2), 1+(i*0.2), 1]},
        f"scale_object_{i}"
    )
    print(f"  [{15+i}] scale_object - Calidad: {exp['quality_after']}")

# =====================================================================
# ANÁLISIS DE PATRONES
# =====================================================================

print("\n" + "="*70)
print("ANÁLISIS DE PATRONES APRENDIDOS")
print("="*70)

# Calcular estadísticas
action_stats = {}
for exp in training_data["experiences"]:
    action = exp["action"]
    if action not in action_stats:
        action_stats[action] = {
            "count": 0,
            "success_count": 0,
            "total_quality_improvement": 0,
            "avg_objects_created": 0
        }
    
    action_stats[action]["count"] += 1
    if exp["success"]:
        action_stats[action]["success_count"] += 1
    action_stats[action]["total_quality_improvement"] += exp["quality_improvement"]
    action_stats[action]["avg_objects_created"] += exp["objects_created"]

# Calcular promedios
for action in action_stats:
    count = action_stats[action]["count"]
    action_stats[action]["success_rate"] = action_stats[action]["success_count"] / count * 100
    action_stats[action]["avg_quality_improvement"] = action_stats[action]["total_quality_improvement"] / count
    action_stats[action]["avg_objects_created"] = action_stats[action]["avg_objects_created"] / count

training_data["patterns_learned"] = action_stats

# Mostrar resultados
print("\nPatrones Aprendidos:")
for action, stats in action_stats.items():
    print(f"\n  {action.upper()}:")
    print(f"    - Ejecuciones: {stats['count']}")
    print(f"    - Tasa éxito: {stats['success_rate']:.0f}%")
    print(f"    - Mejora calidad promedio: +{stats['avg_quality_improvement']:.1f}")
    print(f"    - Objetos creados promedio: {stats['avg_objects_created']:.1f}")

print("\n" + "="*70)
print(f"TOTAL EXPERIENCIAS CAPTURADAS: {len(training_data['experiences'])}")
print("="*70)

# Guardар resultados
output_file = "blender_training_data.json"
with open(output_file, "w") as f:
    json.dump(training_data, f, indent=2)

print(f"\nDatos guardados en: {output_file}")
print("\n[SUCCESS] Entrenamiento completado")
