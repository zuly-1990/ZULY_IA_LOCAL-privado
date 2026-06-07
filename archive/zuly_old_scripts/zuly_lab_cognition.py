#!/usr/bin/env python3
"""
ZULY_LAB CON COGNICIÓN (Plan D)

Integra Plan C (C1-C4) con ZULY_LAB para entrenamiento con datos reales

Uso:
  python zuly_lab_cognition.py run A1.1              # Ejecuta ejercicio A1.1
  python zuly_lab_cognition.py run-all A             # Ejecuta toda fase A
  python zuly_lab_cognition.py report A              # Genera reporte
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import yaml
import traceback

# Setup path
workspace = Path(__file__).parent
sys.path.insert(0, str(workspace))

from lyzu_core import LYZUCore


class ZulyLabCognition:
    """ZULY_LAB con Plan C integrado"""
    
    def __init__(self):
        """Inicializa laboratorio con cognición"""
        self.lab_root = Path("ZULY_LAB")
        
        print("[INIT] Inicializando ZULY_LAB con Cognición...")
        
        # Inicializar LYZU con Plan C
        self.lyzu = LYZUCore(enable_cognition=True)
        self.c1 = self.lyzu.result_evaluator
        self.c2 = self.lyzu.experience_memory
        self.c3 = self.lyzu.objective_system
        self.c4 = self.lyzu.auto_tuning_system
        
        # Directorios
        self.logs_dir = self.lab_root / "logs_sesiones"
        self.patterns_dir = self.lab_root / "dataset_patrones"
        self.results_dir = self.lab_root / "resultados_zuly"
        
        # Crear directorios si no existen
        for d in [self.logs_dir, self.patterns_dir, self.results_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        print("✅ ZULY_LAB Cognición inicializado")
    
    def find_exercise_file(self, exercise_id: str) -> Path:
        """Busca archivo YAML de ejercicio"""
        # Ejemplo: "A1.1" → buscar "A_estructura/ejercicios/A1.1_*.yaml"
        fase = exercise_id[0]  # 'A', 'B', 'C', 'D'
        
        # Determinar carpeta
        fase_map = {
            'A': 'A_estructura',
            'B': 'B_automatizacion',
            'C': 'C_render_tecnico',
            'D': 'D_integracion_real'
        }
        
        fase_dir = self.lab_root / fase_map[fase] / 'ejercicios'
        
        # Buscar archivo
        for yaml_file in fase_dir.glob(f"{exercise_id}_*.yaml"):
            return yaml_file
        
        raise FileNotFoundError(f"Ejercicio {exercise_id} no encontrado")
    
    def load_exercise(self, exercise_id: str) -> dict:
        """Carga ejercicio desde YAML"""
        yaml_file = self.find_exercise_file(exercise_id)
        
        with open(yaml_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def simulate_execution(self, exercise: dict) -> dict:
        """Simula ejecución de pasos del ejercicio"""
        print(f"\n  ▶ Ejecutando {len(exercise['steps'])} pasos...")
        
        result = {
            "ejercicio": exercise.get('numero', 'unknown'),
            "timestamp": datetime.now().isoformat(),
            "steps_executed": len(exercise['steps']),
            "steps_successful": len(exercise['steps']),  # Simular éxito
            "objects_created": {},
            "materials_applied": [],
            "total_time_seconds": exercise.get('tiempo_estimado_segundos', 5),
            "success": True
        }
        
        # Simular creación de objetos basada en steps
        for i, step in enumerate(exercise['steps']):
            action = step['action']
            print(f"    [{i+1}] {action}")
            
            if action == 'create_cube':
                result['objects_created']['Cube'] = step['params'].get('name', 'Cube')
            elif action == 'create_material':
                result['materials_applied'].append(step['params'].get('name', 'Material'))
        
        return result
    
    def run_exercise(self, exercise_id: str) -> dict:
        """Ejecuta ejercicio y captura con Plan C"""
        print(f"\n{'='*70}")
        print(f"EJECUTANDO: {exercise_id}")
        print(f"{'='*70}")
        
        try:
            # Cargar ejercicio
            exercise = self.load_exercise(exercise_id)
            print(f"✓ Ejercicio: {exercise['name']}")
            print(f"✓ Descripción: {exercise['descripcion']}")
            
            # Ejecutar pasos (simulado)
            result = self.simulate_execution(exercise)
            print(f"✓ Ejecución completada ({result['steps_executed']} pasos)")
            
            # C1: EVALUAR
            objective = exercise['descripcion']
            evaluation = self.c1.evaluate(objective, result)
            print(f"✓ C1 Evaluación: score={evaluation.score:.2f}")
            
            # Guardar log (C1)
            log_file = self.logs_dir / f"{exercise_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            log_data = {
                "ejercicio": exercise_id,
                "timestamp": datetime.now().isoformat(),
                "resultado": result,
                "c1_evaluation": {
                    "objective": objective,
                    "score": evaluation.score,
                    "metrics": evaluation.metrics if hasattr(evaluation, 'metrics') else {},
                    "diagnostics": evaluation.diagnostics if hasattr(evaluation, 'diagnostics') else []
                }
            }
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2)
            print(f"✓ Log guardado: {log_file.name}")
            
            # C2: GUARDAR PATRÓN si score > 0.8
            if evaluation.score > 0.8:
                self.c2.store_experience(
                    objective=objective,
                    procedure=" → ".join([f"{s['action']}({s['params']})" for s in exercise['steps']]),
                    result=result
                )
                
                # Guardar patrón en YAML
                pattern_file = self.patterns_dir / f"{exercise_id}_pattern.yaml"
                pattern_data = {
                    "ejercicio": exercise_id,
                    "nombre": exercise['name'],
                    "objetivo": objective,
                    "pasos": len(exercise['steps']),
                    "score": evaluation.score,
                    "timestamp": datetime.now().isoformat(),
                    "heuristics": [
                        "Patrón exitoso: ver steps en ejercicio original",
                        f"Score alcanzado: {evaluation.score:.2f}"
                    ]
                }
                
                with open(pattern_file, 'w', encoding='utf-8') as f:
                    yaml.dump(pattern_data, f)
                
                print(f"✓ Patrón guardado: {pattern_file.name}")
            
            # C3: DESCOMPOSICIÓN
            try:
                plan = self.c3.decompose_objective(objective)
                print(f"✓ C3 Descomposición: {len(plan.tasks)} tareas")
            except:
                print(f"  (C3 descomposición: no aplica)")
            
            # Retornar resumen
            return {
                "ejercicio": exercise_id,
                "score": evaluation.score,
                "success": evaluation.score > 0.8,
                "patrón_guardado": evaluation.score > 0.8
            }
        
        except Exception as e:
            print(f"❌ Error: {e}")
            traceback.print_exc()
            return {
                "ejercicio": exercise_id,
                "score": 0,
                "success": False,
                "error": str(e)
            }
    
    def run_phase(self, fase: str) -> list:
        """Ejecuta todos los ejercicios de una fase"""
        print(f"\n{'='*70}")
        print(f"FASE {fase.upper()}")
        print(f"{'='*70}")
        
        fase_map = {
            'A': 'A_estructura',
            'B': 'B_automatizacion',
            'C': 'C_render_tecnico',
            'D': 'D_integracion_real'
        }
        
        fase_dir = self.lab_root / fase_map[fase] / 'ejercicios'
        
        if not fase_dir.exists():
            print(f"No existe {fase_dir}")
            return []
        
        # Buscar ejercicios
        ejercicios = sorted(fase_dir.glob(f"{fase.upper()}*.yaml"))
        print(f"\nEncontrados {len(ejercicios)} ejercicios")
        
        resultados = []
        for yaml_file in ejercicios:
            # Extraer ID del archivo
            exercise_id = yaml_file.stem.split('_')[0]  # "A1.1" de "A1.1_cubo_basico.yaml"
            resultado = self.run_exercise(exercise_id)
            resultados.append(resultado)
        
        # Generar reporte
        self.generate_phase_report(fase, resultados)
        
        return resultados
    
    def generate_phase_report(self, fase: str, resultados: list):
        """Genera reporte de fase"""
        print(f"\n{'='*70}")
        print(f"REPORTE FASE {fase.upper()}")
        print(f"{'='*70}\n")
        
        total = len(resultados)
        exitosos = len([r for r in resultados if r.get('success')])
        patrones = len([r for r in resultados if r.get('patrón_guardado')])
        scores = [r['score'] for r in resultados if r.get('score')]
        
        print(f"Ejercicios ejecutados: {exitosos}/{total}")
        print(f"Patrones guardados: {patrones}")
        print(f"Score promedio: {sum(scores)/len(scores):.2f}" if scores else "Score: N/A")
        print(f"\nDetalles:")
        for r in resultados:
            status = "✓" if r.get('success') else "✗"
            print(f"  {status} {r['ejercicio']}: score={r['score']:.2f}")


def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python zuly_lab_cognition.py run A1.1         # Ejecuta ejercicio")
        print("  python zuly_lab_cognition.py run-all A        # Ejecuta fase")
        sys.exit(1)
    
    command = sys.argv[1]
    
    lab = ZulyLabCognition()
    
    if command == "run" and len(sys.argv) > 2:
        exercise_id = sys.argv[2]
        lab.run_exercise(exercise_id)
    
    elif command == "run-all" and len(sys.argv) > 2:
        fase = sys.argv[2]
        lab.run_phase(fase)
    
    else:
        print(f"Comando desconocido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
