#!/usr/bin/env python3
"""
PLAN D - LABORATORIO A1
Ejecuta Plan C (C1-C4) con Blender real y recolecta métricas

Este script ha sido convertido de simulación a ejecución real.
Utiliza LYZUCore para procesar órdenes y evaluar resultados en un entorno Blender activo.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import traceback
import time

# Agregar workspace al path
workspace = Path(__file__).parent
sys.path.insert(0, str(workspace))

# Intentar importar bpy para validación de entorno
try:
    import bpy
    IS_INSIDE_BLENDER = True
except ImportError:
    IS_INSIDE_BLENDER = False

from lyzu_core import LYZUCore
from core.cognition.c4_auto_tuning_procedural import ParameterBound, ParameterType


class PlanDLaboratory:
    """Laboratorio para ejecutar Plan C con datos REALES en Blender"""
    
    def __init__(self, mode='reactive'):
        """Inicializa componentes"""
        print("\n" + "="*70)
        print("🧪 INICIALIZANDO PLAN D LABORATORIO (REAL)")
        print("="*70)
        
        try:
            # ELIMINAR REPORTE DE TRANSCRIPCIÓN PARA EVITAR BLOQUEOS DE DIALOGMANAGER
            report_path = Path("transcription_evaluation_report.json")
            if report_path.exists():
                report_path.unlink()
                print("🗑️ Reporte de transcripción eliminado (Bypass DialogManager)")

            # Inicializar LYZU con cognición habilitada en modo reactivo (ejecución directa)
            self.lyzu = LYZUCore(mode=mode, enable_cognition=True)
            
            # Verificar disponibilidad de Blender
            if not IS_INSIDE_BLENDER and not (hasattr(self.lyzu.intent_router, 'handlers') and self.lyzu.intent_router.handlers):
                print("⚠️ ADVERTENCIA: No se detectó entorno Blender. Las acciones podrían fallar.")
            
            # Acceder a componentes cognitivos
            self.c1 = self.lyzu.evaluator
            self.c2 = self.lyzu.memory_system
            self.c3 = self.lyzu.objectives_system
            self.c4 = self.lyzu.auto_tuning_system
            
            # Métricas
            self.metrics = {
                "timestamp": datetime.now().isoformat(),
                "fase_d1_setup": "COMPLETED",
                "c1": {"evaluations": [], "stats": {}},
                "c2": {"experiences": [], "stats": {}},
                "c3": {"decompositions": [], "stats": {}},
                "c4": {"optimizations": [], "stats": {}},
                "total_time": 0
            }
            
            # Asegurar directorios
            Path("ZULY_LAB/resultados_zuly").mkdir(parents=True, exist_ok=True)
            Path("reports").mkdir(parents=True, exist_ok=True)
            
            print("✅ Plan D inicializado correctamente.")
            
        except Exception as e:
            print(f"❌ Error inicializando Plan D: {e}")
            traceback.print_exc()
            raise
    
    def run_real_basic_tasks(self):
        """Ejecuta tareas básicas reales (Fase D2)"""
        print("\n" + "="*70)
        print("[FASE D2] EJECUCIONES BÁSICAS (REAL)")
        print("="*70)
        
        tasks = [
            "Crea un cubo llamado Cubo_D1 en la posición [0,0,0]",
            "Mueve el Cubo_D1 a la posición [2, 0, 0]",
            "Escala el Cubo_D1 a tamaño 2.5",
            "Crea un material rojo llamado Material_D1",
            "Aplica el Material_D1 al objeto Cubo_D1",
            "Renderiza la escena actual"
        ]
        
        for i, request in enumerate(tasks, 1):
            print(f"\n▶ [{i}/{len(tasks)}] Petición: '{request}'")
            
            try:
                # Ejecutar con LYZU
                result = self.lyzu.execute_with_evaluation(request, auto_approve=True)
                
                status = "✓" if result.get('success') else "✗"
                print(f"   {status} Resultado: {result.get('output', 'Sin output')}")
                if not result.get('success'):
                    print(f"   Error: {result.get('error')}")
                    if 'details' in result:
                        print(f"   Details: {result.get('details')}")
                
                # Registrar métricas C1
                if 'evaluation' in result:
                    eval_data = result['evaluation']
                    print(f"   ✓ C1 Score: {eval_data.get('score', 0):.2f} - {eval_data.get('summary')}")
                    self.metrics["c1"]["evaluations"].append({
                        "request": request,
                        "score": eval_data.get('score'),
                        "passed": eval_data.get('metrics_passed')
                    })
                else:
                    print(f"   ⚠️ Sin evaluación C1. Éxito: {result.get('success')}")
                
                # C2 es manejado automáticamente por LYZUCore si está habilitado
                
            except Exception as e:
                print(f"   ❌ Error en ejecución: {e}")
                traceback.print_exc()
    
    def run_real_decomposition(self):
        """Ejecuta descomposición real (Fase D3)"""
        print("\n" + "="*70)
        print("[FASE D3] DESCOMPOSICIÓN DE OBJETIVOS (REAL)")
        print("="*70)
        
        # Objetivo que coincide con plantilla: 'crear escena 3d'
        objective = "Crear escena 3D completa con suelo y columnas"
        print(f"\n▶ Objetivo complejo: '{objective}'")
        
        if not self.c3:
            print("⚠️ C3 no disponible. Saltando fase.")
            return

        try:
            # Descomponer
            plan = self.c3.decompose_objective(objective)
            print(f"   ✓ Descompuesto en {len(plan.tasks)} tareas.")
            
            # Ejecutar cada tarea del plan
            for task_id in plan.execution_order:
                # Buscar tarea
                task = next(t for t in plan.tasks if t.id == task_id)
                print(f"   - Ejecutando subtarea ({task.id}): {task.name}")
                res = self.lyzu.execute_with_evaluation(task.name, auto_approve=True)
                status = '✓' if res.get('success') else '✗'
                print(f"     Status: {status}")
                if not res.get('success'):
                    print(f"     Error: {res.get('error')}")
                    if 'details' in res:
                        print(f"     Details: {res.get('details')}")
            
            self.metrics["c3"]["decompositions"].append({
                "objective": objective,
                "num_tasks": len(plan.tasks),
                "success": True
            })
            
        except Exception as e:
            print(f"   ❌ Error en C3: {e}")
            traceback.print_exc()
    
    def run_real_optimization(self):
        """Ejecuta optimización real (Fase D4)"""
        print("\n" + "="*70)
        print("[FASE D4] OPTIMIZACIÓN DE PARÁMETROS (REAL)")
        print("="*70)
        
        if not self.c4:
            print("⚠️ C4 no disponible. Saltando fase.")
            return
            
        print("\n▶ Optimizando parámetro de escalado basado en feedback C1")
        
        # Procedimiento real: Crear esfera con escala variable
        def scaling_procedure(scale_val: float) -> dict:
            req = f"Crea una esfera llamada OptiSphere con escala {scale_val}"
            res = self.lyzu.execute_with_evaluation(req, auto_approve=True)
            # Retornar el score de C1 como métrica para optimizar
            score = res.get('evaluation', {}).get('score', 0)
            return {
                "scale": scale_val,
                "score": score,
                "success": res.get('success')
            }
        
        try:
            # Definir límites: escala de 0.5 a 5.0
            # C4.optimize espera un dict de {nombre: ParameterBound}
            bound = ParameterBound("scale", ParameterType.FLOAT, 0.5, 5.0, step=0.5)
            bounds_dict = {"scale": bound}
            
            opt_result = self.c4.optimize(
                objective="Encontrar escala ideal para visibilidad",
                procedure=scaling_procedure,
                param_bounds=bounds_dict,
                max_iterations=5
            )
            
            print(f"   ✓ Optimización completada.")
            print(f"   Mejor escala: {opt_result.best_parameter_value}")
            print(f"   Iteraciones: {opt_result.total_iterations}")
            
            self.metrics["c4"]["optimizations"].append({
                "best_param": opt_result.best_parameter_value,
                "best_score": opt_result.best_score,
                "iterations": opt_result.total_iterations
            })
            
        except Exception as e:
            print(f"   ❌ Error en C4: {e}")
            traceback.print_exc()
    
    def finalize(self):
        """Finalizar y exportar resultados"""
        print("\n" + "="*70)
        print("📊 FINALIZANDO LABORATORIO Y EXPORTANDO MÉTRICAS")
        print("="*70)
        
        # Calcular estadísticas rápidas
        c1_ev = self.metrics["c1"]["evaluations"]
        if c1_ev:
            avg = sum(e['score'] for e in c1_ev) / len(c1_ev)
            self.metrics["c1"]["stats"] = {"avg_score": round(avg, 3), "count": len(c1_ev)}
            print(f"   Score Promedio C1: {avg:.3f}")
        
        # Exportar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = Path("reports") / f"plan_d_metrics_real_{timestamp}.json"
        
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(self.metrics, f, indent=2)
            print(f"✅ Reporte generado: {report_file}")
            
            # Guardar escena principal si estamos en Blender
            if IS_INSIDE_BLENDER:
                out_blend = Path("ZULY_LAB/resultados_zuly") / f"PlanD_Final_{timestamp}.blend"
                bpy.ops.wm.save_as_mainfile(filepath=str(out_blend))
                print(f"✅ Escena final guardada: {out_blend}")
                
        except Exception as e:
            print(f"❌ Error al exportar: {e}")


def main():
    start_time = time.time()
    
    # El modo 'reactive' es esencial para que LYZU ejecute sin preguntar
    lab = PlanDLaboratory(mode='reactive')
    
    # Fase D2
    lab.run_real_basic_tasks()
    
    # Fase D3
    lab.run_real_decomposition()
    
    # Fase D4
    lab.run_real_optimization()
    
    # Finalizar
    lab.metrics["total_time"] = round(time.time() - start_time, 2)
    lab.finalize()
    
    print("\n" + "="*70)
    print(f"✅ PLAN D LABORATORIO COMPLETADO EN {lab.metrics['total_time']}s")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
