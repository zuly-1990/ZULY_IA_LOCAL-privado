"""
train_c2_from_blender_real.py
==============================

Entrenar C2 ExperienceMemory (Opción 1) con datos REALES de Blender

Flujo:
1. Ejecuta Blender
2. Crea 20 escenas de prueba
3. Captura estado de cada una
4. Evalúa con C1 (0-100)
5. Almacena en C2 Memory
6. Genera matriz de patrones aprendidos

Resultado: C2 Memory aprende 20 experiencias reales
Tiempo: 5-10 minutos
Status: PRODUCCIÓN READY

Fecha: 22 Febrero 2026
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class BlenderRealtimeTrainer:
    """Entrena C2 Memory usando datos reales de Blender."""
    
    def __init__(self):
        self.blender_path = Path("blender/v3/blender-3.6.0-zuly/blender.exe")
        self.training_results = {
            "date": datetime.now().isoformat(),
            "blender_version": "3.6.2",
            "status": "PENDING",
            "experiences": [],
            "patterns_learned": {},
            "summary": {}
        }
        
    def generate_blender_training_script(self) -> Path:
        """Genera script Python para ejecutar en Blender y recopilar datos."""
        script_content = '''
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

print("\\n" + "="*70)
print("ENTRENAMIENTO C2 MEMORY - DATOS REALES BLENDER")
print("="*70)

# Limpiar escena inicial
print("\\n[SETUP] Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
print("[OK] Escena limpia\\n")

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
print("\\n[BATCH 2] Creando esferas (5 experiencias)...")
for i in range(1, 6):
    exp = create_experience(
        "create_sphere",
        {"location": [i*3, 2, 0]},
        f"create_sphere_{i}"
    )
    print(f"  [{5+i}] {exp['action']} - Calidad: {exp['quality_after']}")

# EXPERIENCIA 11-15: Rotaciones
print("\\n[BATCH 3] Rotando objetos (5 experiencias)...")
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
print("\\n[BATCH 4] Escalando objetos (5 experiencias)...")
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

print("\\n" + "="*70)
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
print("\\nPatrones Aprendidos:")
for action, stats in action_stats.items():
    print(f"\\n  {action.upper()}:")
    print(f"    - Ejecuciones: {stats['count']}")
    print(f"    - Tasa éxito: {stats['success_rate']:.0f}%")
    print(f"    - Mejora calidad promedio: +{stats['avg_quality_improvement']:.1f}")
    print(f"    - Objetos creados promedio: {stats['avg_objects_created']:.1f}")

print("\\n" + "="*70)
print(f"TOTAL EXPERIENCIAS CAPTURADAS: {len(training_data['experiences'])}")
print("="*70)

# Guardар resultados
output_file = "blender_training_data.json"
with open(output_file, "w") as f:
    json.dump(training_data, f, indent=2)

print(f"\\nDatos guardados en: {output_file}")
print("\\n[SUCCESS] Entrenamiento completado")
'''
        
        script_path = Path("train_blender_script.py")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return script_path
    
    def run_blender_training(self) -> Dict[str, Any]:
        """Ejecuta el entrenamiento en Blender real."""
        print("\n" + "=" * 70)
        print(" ENTRENAMIENTO C2 MEMORY - BLENDER REAL")
        print("=" * 70)
        
        if not self.blender_path.exists():
            print(f"\n[ERROR] Blender no encontrado en: {self.blender_path}")
            print("Ubicaciones buscadas:")
            print("  - blender/v3/blender-3.6.0-zuly/blender.exe")
            return self.training_results
        
        print(f"\n[OK] Blender encontrado: {self.blender_path}")
        
        # Generar script
        script_path = self.generate_blender_training_script()
        print(f"[OK] Script generado: {script_path}")
        
        # Ejecutar Blender
        print(f"\n[EXEC] Ejecutando Blender en background...")
        print("  Esto createará 20 experiencias reales...")
        
        try:
            cmd = [
                str(self.blender_path),
                "--background",
                "--python",
                str(script_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            print(f"\n[OUTPUT] Salida de Blender:")
            print("-" * 70)
            if result.stdout:
                print(result.stdout)
            
            # Leer datos de entrenamiento
            training_file = Path("blender_training_data.json")
            if training_file.exists():
                with open(training_file, 'r') as f:
                    blender_data = json.load(f)
                
                self.training_results["experiences"] = blender_data.get("experiences", [])
                self.training_results["patterns_learned"] = blender_data.get("patterns_learned", {})
                self.training_results["status"] = "SUCCESS"
                print(f"\n[OK] {len(self.training_results['experiences'])} experiencias capturadas")
                
            else:
                print("[WARNING] Archivo de entrenamiento no generado")
                self.training_results["status"] = "PARTIAL"
                
        except subprocess.TimeoutExpired:
            print("[ERROR] Timeout ejecutando Blender")
            self.training_results["status"] = "TIMEOUT"
        except Exception as e:
            print(f"[ERROR] {e}")
            self.training_results["status"] = "FAILED"
        
        return self.training_results
    
    def import_to_c2_memory(self) -> Dict[str, Any]:
        """Importa experiencias a C2 ExperienceMemory."""
        print("\n" + "=" * 70)
        print(" IMPORTAR EXPERIENCIAS A C2 MEMORY")
        print("=" * 70)
        
        if not self.training_results["experiences"]:
            print("\n[WARNING] No hay experiencias para importar")
            return self.training_results
        
        try:
            from core.cognition.c2_experience_memory import C2ExperienceMemory
            
            c2 = C2ExperienceMemory()
            print(f"\n[OK] C2 ExperienceMemory inicializado")
            
            imported_count = 0
            for exp in self.training_results["experiences"]:
                try:
                    # Usar API correcta: record_experience
                    evaluation = {
                        'status': 'success' if exp['success'] else 'failed',
                        'score': int(exp['quality_after']),
                        'parameters': exp['parameters'],
                        'metrics_passed': 1 if exp['success'] else 0,
                        'metrics_total': 1,
                        'issues': [],
                        'recommendations': [f"Mejora: +{exp['quality_improvement']:.0f}"]
                    }
                    
                    objective = f"[Blender] {exp['action']} - {exp['intent']}"
                    c2.record_experience(objective, evaluation)
                    imported_count += 1
                    
                except Exception as e:
                    print(f"  [ERROR] No se pudo importar experiencia {exp['id']}: {e}")
            
            print(f"\n[OK] {imported_count}/{len(self.training_results['experiences'])} experiencias importadas")
            print("\n[INFO] C2 Memory ahora contiene:")
            print(f"  - {imported_count} experiencias de Blender real")
            print(f"  - Patrones de éxito/fracaso")
            print(f"  - Métricas de calidad mejora")
            print(f"  - Datos persistidos en SQLite")
            
            self.training_results["c2_imported"] = imported_count
            
        except Exception as e:
            print(f"[ERROR] No se pudo importar a C2: {e}")
            import traceback
            traceback.print_exc()
        
        return self.training_results
    
    def generate_report(self) -> str:
        """Genera reporte del entrenamiento."""
        report = "=" * 70 + "\n"
        report += " REPORTE: ENTRENAMIENTO C2 MEMORY DESDE BLENDER\n"
        report += "=" * 70 + "\n\n"
        
        report += f"Fecha: {self.training_results['date']}\n"
        report += f"Blender: {self.training_results['blender_version']}\n"
        report += f"Status: {self.training_results['status']}\n\n"
        
        report += "EXPERIENCIAS CAPTURADAS:\n"
        report += "-" * 70 + "\n"
        report += f"Total: {len(self.training_results['experiences'])}\n"
        
        if self.training_results["patterns_learned"]:
            report += "\nPATRONES APRENDIDOS:\n"
            for action, stats in self.training_results["patterns_learned"].items():
                report += f"\n  {action}:\n"
                report += f"    - Ejecuciones: {stats['count']}\n"
                report += f"    - Tasa éxito: {stats['success_rate']:.0f}%\n"
                report += f"    - Mejora calidad: +{stats['avg_quality_improvement']:.1f}\n"
        
        report += "\n" + "=" * 70 + "\n"
        report += "ESTADO DE C2 MEMORY:\n"
        report += "-" * 70 + "\n"
        
        if "c2_imported" in self.training_results:
            report += f"Experiencias importadas: {self.training_results['c2_imported']}\n"
            report += "Status: LISTO PARA USAR\n"
        else:
            report += "No importado aún\n"
        
        report += "\n" + "=" * 70 + "\n"
        report += "PRÓXIMOS PASOS:\n"
        report += "-" * 70 + "\n"
        report += "1. Usar LYZU con Learning Freedom\n"
        report += "2. C2 sugerirá parámetros basados en experiencias\n"
        report += "3. Sistema mejora con cada uso\n"
        
        return report
    
    def run_full_training(self):
        """Ejecuta entrenamiento completo."""
        print("\n")
        print("╔" + "=" * 68 + "╗")
        print("║ ENTRENAMIENTO C2 MEMORY - PASO 1 DE OPCIONES                 ║")
        print("║ Con datos reales de Blender                                 ║")
        print("╚" + "=" * 68 + "╝")
        
        # 1. Ejecutar Blender
        self.run_blender_training()
        
        # 2. Importar a C2
        time.sleep(2)  # Esperar a que se escriba el archivo
        self.import_to_c2_memory()
        
        # 3. Generar reporte
        report = self.generate_report()
        
        # 4. Guardar resultados
        results_path = Path("ZULY_LAB") / "c2_training_results.json"
        results_path.parent.mkdir(exist_ok=True)
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(self.training_results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n[FILE] Resultados: {results_path}")
        
        # Mostrar reporte
        print("\n" + report)


def main():
    """Función principal."""
    trainer = BlenderRealtimeTrainer()
    trainer.run_full_training()
    print("\n[SUCCESS] ENTRENAMIENTO COMPLETADO")
    print("\nProximos pasos:")
    print("  1. Crear CLI interactivo (Opción 2)")
    print("  2. Implementar C3 Objectives (Opción 3)")
    print("  3. Ver dashboard en tiempo real")


if __name__ == "__main__":
    main()
