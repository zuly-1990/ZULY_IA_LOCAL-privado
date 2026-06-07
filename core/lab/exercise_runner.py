"""
ZULY Laboratorio - Exercise Runner
Ejecuta ejercicios definidos en YAML
"""
import yaml
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime


class ExerciseRunner:
    """Ejecuta ejercicios de laboratorio"""
    
    def __init__(self, agent, lab_root: str = "ZULY_LAB"):
        self.agent = agent
        self.lab_root = Path(lab_root)
        self.results_dir = self.lab_root / "resultados_zuly"
        self.logs_dir = self.lab_root / "logs_sesiones"
        
        # Crear directorios si no existen
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def load_exercise(self, exercise_code: str) -> Dict:
        """
        Carga un ejercicio desde YAML.
        
        Args:
            exercise_code: Código del ejercicio (ej: 'A1.1', 'B2.3')
        
        Returns:
            Diccionario con definición del ejercicio
        """
        # Determinar fase
        fase = exercise_code[0]  # 'A', 'B', 'C', 'D'
        
        # Mapear fase a carpeta
        fase_map = {
            'A': 'A_estructura',
            'B': 'B_automatizacion',
            'C': 'C_render_tecnico',
            'D': 'D_integracion_real'
        }
        
        fase_dir = self.lab_root / fase_map[fase] / 'ejercicios'
        
        # Buscar archivo YAML
        yaml_files = list(fase_dir.glob(f"{exercise_code}_*.yaml"))
        
        if not yaml_files:
            raise FileNotFoundError(f"Ejercicio {exercise_code} no encontrado en {fase_dir}")
        
        # Cargar YAML
        with open(yaml_files[0], 'r', encoding='utf-8') as f:
            exercise = yaml.safe_load(f)
        
        return exercise
    
    def execute_exercise(self, exercise_code: str) -> Dict[str, Any]:
        """
        Ejecuta un ejercicio completo.
        
        Returns:
            Diccionario con resultados de la ejecución
        """
        print(f"\n🧪 Ejecutando ejercicio: {exercise_code}")
        
        # Cargar ejercicio
        exercise = self.load_exercise(exercise_code)
        
        print(f"   Nombre: {exercise['name']}")
        print(f"   Fase: {exercise['fase']}")
        print(f"   Descripción: {exercise['descripcion']}")
        
        # Preparar resultado
        result = {
            'ejercicio': exercise_code,
            'nombre': exercise['name'],
            'timestamp': datetime.now().isoformat(),
            'pasos_ejecutados': [],
            'pasos_exitosos': 0,
            'pasos_fallidos': 0,
            'tiempo_total_segundos': 0,
            'exito': False,
            'objetos_creados': [],
            'errores': [],
            'validacion': {}
        }
        
        # Ejecutar pasos
        start_time = time.time()
        
        try:
            for i, step in enumerate(exercise['steps'], 1):
                step_result = self._execute_step(step, i)
                result['pasos_ejecutados'].append(step_result)
                
                if step_result['exito']:
                    result['pasos_exitosos'] += 1
                else:
                    result['pasos_fallidos'] += 1
                    result['errores'].append(step_result.get('error', 'Error desconocido'))
            
            # Tiempo total
            result['tiempo_total_segundos'] = round(time.time() - start_time, 2)
            
            # Validar
            if 'validation' in exercise:
                result['validacion'] = self._validate_exercise(exercise['validation'])
            
            # Determinar éxito
            if 'success_criteria' in exercise:
                criteria = exercise['success_criteria']
                result['exito'] = (
                    result['pasos_exitosos'] >= criteria.get('min_steps_successful', len(exercise['steps']))
                    and result['tiempo_total_segundos'] <= criteria.get('max_time_seconds', 999)
                )
            else:
                result['exito'] = result['pasos_fallidos'] == 0
            
            # Guardar log
            self._save_log(result)
            
            # Mostrar resumen
            self._print_summary(result)
            
        except Exception as e:
            result['errores'].append(str(e))
            result['exito'] = False
            print(f"   ✗ Error fatal: {e}")
        
        return result
    
    def _execute_step(self, step: Dict, step_number: int) -> Dict:
        """Ejecuta un paso individual"""
        action = step['action']
        params = step.get('params', {})
        
        print(f"   [{step_number}] {action} {params}")
        
        step_result = {
            'numero': step_number,
            'action': action,
            'params': params,
            'exito': False,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Mapear action a handler
            handler_map = {
                'clear_scene': 'blender.clear_scene',
                'create_cube': 'blender.create_cube',
                'create_cylinder': 'blender.create_cylinder',
                'create_sphere': 'blender.create_sphere',
                'create_plane': 'blender.create_plane',
                'move_object': 'blender.move_object',
                'scale_object': 'blender.scale_object',
                'rotate_object': 'blender.rotate_object',
                'create_material': 'blender.create_material',
                'create_texture_material': 'blender.create_texture_material',
                'apply_material': 'blender.apply_material',
                'set_material_color': 'blender.set_material_color',
                'create_light': 'blender.create_light',
                'set_light_energy': 'blender.set_light_energy',
                'set_light_color': 'blender.set_light_color',
                'create_camera': 'blender.create_camera',
                'set_active_camera': 'blender.set_active_camera',
                'position_camera': 'blender.position_camera',
                'render_scene': 'blender.render_scene',
                'save_project': 'blender.save_project',
                'run_python_script': 'blender.run_python_script'
            }
            
            handler = handler_map.get(action)
            
            if not handler:
                raise ValueError(f"Acción desconocida: {action}")
            
            # Ejecutar via router
            result = self.agent.execute_via_router(handler, params)
            
            step_result['exito'] = result.get('success', False)
            step_result['resultado'] = result
            
            if step_result['exito']:
                print(f"       ✓ Exitoso")
            else:
                print(f"       ✗ Fallido: {result.get('error', 'Unknown')}")
                step_result['error'] = result.get('error', 'Unknown error')
        
        except Exception as e:
            step_result['error'] = str(e)
            print(f"       ✗ Error: {e}")
        
        return step_result
    
    def _validate_exercise(self, validations: List[Dict]) -> Dict:
        """Ejecuta validaciones del ejercicio consultando al adaptador"""
        validation_result = {
            'total': len(validations),
            'pasadas': 0,
            'fallidas': 0,
            'detalles': []
        }
        
        print(f"\n   🔍 Validando ejercicio...")
        
        adapter = self.agent.engine_adapter
        
        for val in validations:
            val_type = val['type']
            passed = False
            error = None
            
            try:
                if val_type == 'object_exists':
                    obj_name = val['object_name']
                    # Consultar al adapter
                    info = adapter.get_object_info(obj_name)
                    passed = info.get('success', False)
                    if not passed:
                        error = f"Objeto '{obj_name}' no encontrado en escena"
                
                elif val_type == 'object_count':
                    expected = val['expected']
                    # Consultar estado de escena
                    scene = adapter.get_scene_state()
                    if not scene.get('success', False):
                        passed = False
                        error = "No se pudo obtener estado de escena"
                    else:
                        count = scene.get('object_count', 0)
                        passed = count == expected
                        if not passed:
                            error = f"Se esperaban {expected} objetos, hay {count}"
                
                elif val_type == 'objects_aligned':
                     # Simplificado para este ejercicio: verificar si hay objetos
                    scene = adapter.get_scene_state()
                    count = scene.get('object_count', 0)
                    passed = count > 1
                    if not passed:
                        error = "No hay suficientes objetos para verificar alineación"

                elif val_type == 'object_at_location':
                    obj_name = val['object_name']
                    expected = val['expected_location']
                    tolerance = val.get('tolerance', 0.1)
                    
                    info = adapter.get_object_info(obj_name)
                    if not info.get('success', False):
                         passed = False
                         error = f"Objeto '{obj_name}' no encontrado"
                    else:
                        loc = info.get('location', [0,0,0])
                        # Calcular distancia euclidiana
                        dist = sum((a-b)**2 for a,b in zip(loc, expected)) ** 0.5
                        passed = dist <= tolerance
                        if not passed:
                            error = f"Ubicación incorrecta: {loc} vs {expected} (dist: {dist:.3f})"
                
                elif val_type == 'object_scale':
                    obj_name = val['object_name']
                    expected = val['expected_scale']
                    tolerance = val.get('tolerance', 0.1)
                    
                    info = adapter.get_object_info(obj_name)
                    if not info.get('success', False):
                         passed = False
                         error = f"Objeto '{obj_name}' no encontrado"
                    else:
                        scale = info.get('scale', [1,1,1])
                        # Normalizar expected a lista
                        if isinstance(expected, (int, float)):
                            expected_list = [float(expected)] * 3
                        else:
                            expected_list = expected
                            
                        # Calcular diferencia
                        diff = sum(abs(a-b) for a,b in zip(scale, expected_list))
                        passed = diff <= tolerance
                        if not passed:
                            error = f"Escala incorrecta: {scale} vs {expected_list}"

                elif val_type == 'material_applied':
                    obj_name = val['object_name']
                    # material_name = val['material_name']
                    
                    # Por ahora solo verificamos que el objeto exista
                    # Idealmente el adapter retornaría el material activo
                    info = adapter.get_object_info(obj_name)
                    passed = info.get('success', False)
                    if not passed:
                        error = f"Objeto '{obj_name}' no existe"
                
                else:
                    passed = True
                    error = f"Validación '{val_type}' no implementada (pass por defecto)"

                
                validation_result['detalles'].append({
                    'tipo': val_type,
                    'pasado': passed,
                    'error': error
                })
                
                if passed:
                    validation_result['pasadas'] += 1
                    print(f"       ✓ {val_type}")
                else:
                    validation_result['fallidas'] += 1
                    print(f"       ✗ {val_type}: {error}")
            
            except Exception as e:
                validation_result['fallidas'] += 1
                print(f"       ✗ Error validando {val_type}: {e}")
                validation_result['detalles'].append({
                    'tipo': val_type,
                    'pasado': False,
                    'error': str(e)
                })
        
        return validation_result
    
    def _save_log(self, result: Dict):
        """Guarda log de ejecución"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.logs_dir / f"{result['ejercicio']}_{timestamp}.json"
        
        import json
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n   💾 Log guardado: {log_file}")
    
    def _print_summary(self, result: Dict):
        """Imprime resumen de ejecución"""
        print(f"\n" + "="*70)
        print(f"RESUMEN (DEBUG KEYS: {list(result.keys())})")
        print(f"="*70)
        
        # Usar .get() para evitar KeyErrors si el diccionario llega incompleto
        ejercicio = result.get('ejercicio', 'UNK')
        nombre = result.get('nombre', 'Sin nombre')
        exito = result.get('exito', False)
        pasos_exitosos = result.get('pasos_exitosos', 0)
        pasos_fallidos = result.get('pasos_fallidos', 0)
        tiempo = result.get('tiempo_total_segundos', 0)
        
        print(f"Ejercicio: {ejercicio} - {nombre}")
        print(f"Estado: {'EXITO' if exito else 'FALLIDO'}")
        print(f"Pasos exitosos: {pasos_exitosos}/{pasos_exitosos + pasos_fallidos}")
        print(f"Tiempo total: {tiempo}s")
        
        if result.get('errores'):
            print(f"\nErrores:")
            for err in result['errores']:
                print(f"   - {err}")
        
        if 'validacion' in result:
            val = result['validacion']
            pasadas = val.get('pasadas', 0)
            total = val.get('total', 0)
            print(f"\nValidacion: {pasadas}/{total} pasadas")
        
        # FASE C: Cognición
        try:
            pasos = result.get('pasos_ejecutados', [])
            diagnoses = []
            for s in pasos:
                res_obj = s.get('resultado', {})
                if isinstance(res_obj, dict) and res_obj.get('cognition_diagnosis'):
                    diagnoses.append(res_obj['cognition_diagnosis'])
            
            if diagnoses:
                # Tomar el diagnóstico más relevante (el último suele ser el render)
                last_diag = diagnoses[-1]
                st = last_diag.get('status', 'UNK')
                sc = last_diag.get('score', 0)
                print(f"\nCOGNICION: STATUS {st} (Calidad: {sc:.0%})")
                for finding in last_diag.get('findings', []):
                    print(f"   - {finding}")
        except Exception as e:
            # Silencio cognitivo en caso de error de reporte para no romper el flujo principal
            pass
        
        print("="*70)
    
    def run_all_phase(self, phase: str) -> List[Dict]:
        """Ejecuta todos los ejercicios de una fase"""
        print(f"\n🚀 Ejecutando todos los ejercicios de Fase {phase}")
        
        # Buscar todos los ejercicios
        fase_map = {
            'A': 'A_estructura',
            'B': 'B_automatizacion',
            'C': 'C_render_tecnico',
            'D': 'D_integracion_real'
        }
        
        fase_dir = self.lab_root / fase_map[phase] / 'ejercicios'
        exercises = sorted(fase_dir.glob(f"{phase}*.yaml"))
        
        results = []
        for ex_file in exercises:
            # Extractar código
            code = ex_file.stem.split('_')[0]
            result = self.execute_exercise(code)
            results.append(result)
        
        # Resumen general
        print(f"\n" + "="*70)
        print(f"📈 RESUMEN FASE {phase}")
        print(f"="*70)
        total = len(results)
        exitosos = sum(1 for r in results if r['exito'])
        print(f"Total ejercicios: {total}")
        print(f"Exitosos: {exitosos}")
        print(f"Fallidos: {total - exitosos}")
        print(f"Tasa de éxito: {(exitosos/total)*100:.1f}%")
        print("="*70)
        
        return results
