"""
core/execution/execution_engine.py
==================================

Motor de ejecución de comandos del agente Zuly.
Maneja enrutamiento, validación JUES, y corrección de errores.

Extraído de agent.py como parte del refactoring God Objects (Fase 3).
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from core.utils.logging import log_info, log_warning, log_error, log_debug, log_success
from core.utils.nlu import CommandIntent
from core.jues_controller import get_jues_controller


class ExecutionEngine:
    """
    Motor de ejecución de comandos.
    
    Responsabilidades:
    - Enrutar comandos a handlers
    - Validar con JUES
    - Manejar reintentos y correcciones
    - Extraer y preparar parámetros
    """
    
    def __init__(self, intent_router, engine_adapter=None, session_manager=None):
        self.intent_router = intent_router
        self.engine_adapter = engine_adapter
        self.session_manager = session_manager
        self.jues_controller = get_jues_controller()
        
        # Fallback: comandos antiguos (clases con ejecutar/validar)
        self.legacy_commands: Dict[str, Any] = {}
    
    def register_legacy_command(self, name: str, command_class):
        """Registra un comando del sistema antiguo."""
        self.legacy_commands[name] = command_class
    
    def execute_via_router(self, handler_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        FASE 23: Ejecuta comando vía IntentRouter (handlers funcionales).
        
        Args:
            handler_name: Nombre del handler (ej: 'blender.create_cube')
            parameters: Parámetros para el handler
            
        Returns:
            Resultado de la ejecución
        """
        if not self.intent_router:
            return {
                'success': False,
                'error': 'IntentRouter not available',
                'route': 'NO_ROUTER'
            }
        
        handler = self.intent_router.command_handlers.get(handler_name)
        if not handler:
            return {
                'success': False,
                'error': f'Handler not found: {handler_name}',
                'route': 'HANDLER_NOT_FOUND',
                'available': list(self.intent_router.command_handlers.keys())[:10]
            }
        
        try:
            # Inyectar adapter si el handler lo necesita
            if self.engine_adapter and 'adapter' not in parameters:
                parameters = {**parameters, 'adapter': self.engine_adapter}
            
            result = handler(parameters)
            
            return {
                'success': result.get('success', False),
                'result': result,
                'route': 'ROUTER_FUNCTIONAL',
                'handler': handler_name
            }
            
        except Exception as e:
            log_error(f"Error ejecutando {handler_name}: {e}")
            import traceback
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc(),
                'route': 'ROUTER_EXCEPTION'
            }
    
    def execute_intent(self, intent: CommandIntent, attempt: int = 1, max_attempts: int = 1) -> Dict:
        """
        Ejecuta una intención de comando específica.
        
        Args:
            intent: Intención a ejecutar
            attempt: Intento actual
            max_attempts: Máximo de reintentos
            
        Returns:
            Resultado de la ejecución
        """
        command_name = intent.command_name
        parameters = intent.parameters.copy()
        
        log_info(f"Ejecutando: {command_name} (intento {attempt}/{max_attempts})")
        
        # FASE 23: Intentar vía IntentRouter primero
        if self.intent_router and command_name in self.intent_router.command_handlers:
            log_debug(f"[FASE 23] Ejecutando vía IntentRouter: {command_name}")
            
            result = self.execute_via_router(command_name, parameters)
            
            if result.get('success'):
                log_success(f"✓ [FASE 23] Éxito: {command_name}")
                
                # Registrar ejecución exitosa
                if self.session_manager:
                    self.session_manager.register_execution(command_name, True, result)
                
                return {
                    'success': True,
                    'command': command_name,
                    'result': result.get('result'),
                    'route': 'F23_ROUTER'
                }
            else:
                log_warning(f"✗ [FASE 23] Falló: {result.get('error')}")
        
        # FASE 23: FALLBACK - Sistema antiguo (clases con ejecutar/validar)
        log_debug(f"[FASE 23] Handler no en router, intentando sistema antiguo: {command_name}")
        command_class = self.legacy_commands.get(command_name)
        
        if not command_class:
            error_msg = f"Comando no encontrado: {command_name}"
            log_error(error_msg)
            
            if self.session_manager:
                self.session_manager.register_execution(command_name, False, error=error_msg)
            
            return {
                'success': False,
                'command': command_name,
                'error': error_msg,
                'route': 'NOT_FOUND'
            }
        
        # Instanciar y ejecutar comando antiguo
        try:
            instance = command_class()
            
            # Validación V0-V1-V2 (sistema antiguo)
            if hasattr(instance, 'validate'):
                validation = instance.validate(parameters)
                if not validation.get('valid', True):
                    return {
                        'success': False,
                        'command': command_name,
                        'error': validation.get('error', 'Validación falló'),
                        'route': 'VALIDATION_FAILED'
                    }
            
            # Ejecutar
            if hasattr(instance, 'ejecutar'):
                result = instance.ejecutar(parameters, self.engine_adapter)
            else:
                result = instance.execute(parameters, self.engine_adapter)
            
            success = result.get('success', False)
            
            if self.session_manager:
                self.session_manager.register_execution(
                    command_name, success, 
                    result=result if success else None,
                    error=result.get('error') if not success else None
                )
            
            return {
                'success': success,
                'command': command_name,
                'result': result,
                'route': 'LEGACY_CLASS'
            }
            
        except TypeError as e:
            # Parámetros faltantes
            missing = self._extract_missing_params(command_class, e)
            return {
                'success': False,
                'command': command_name,
                'error': f"Parámetros faltantes: {missing}",
                'missing_params': missing,
                'route': 'MISSING_PARAMS'
            }
            
        except Exception as e:
            error_msg = f"Error ejecutando {command_name}: {str(e)}"
            log_error(error_msg)
            
            if self.session_manager:
                self.session_manager.register_execution(command_name, False, error=error_msg)
            
            return {
                'success': False,
                'command': command_name,
                'error': error_msg,
                'route': 'EXECUTION_ERROR',
                'attempt': attempt,
            }
    
    def execute_jues_validation(
        self,
        candidato_id: str,
        validation_v0: Dict[str, Any],
        validation_v1: Dict[str, Any],
        validation_v2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Ejecuta validación JUES completa.
        
        Returns:
            Reporte JUES consolidado
        """
        if not self.jues_controller:
            log_warning("JUESController no disponible")
            return {"puntuacion_jues": 0, "dictamen": "SIN_JUES", "reporte_completo": {}}
        
        # Ejecutar validación
        reporte = self.jues_controller.validar_y_decidir(
            candidato_id=candidato_id,
            v0=validation_v0,
            v1=validation_v1,
            v2=validation_v2
        )
        
        log_info(f"JUES Reporte para {candidato_id}: Puntuación {reporte['puntuacion_jues']:.2f}, Dictamen: {reporte['dictamen']}")
        
        # Guardar en bitácora si es exitoso
        if reporte.get('bitacora_path'):
            log_success(f"✅ Reporte JUES guardado en bitácora: {reporte['bitacora_path']}")
        
        return reporte
    
    def attempt_correction(self, failed_intent: CommandIntent, result: Dict) -> Optional[CommandIntent]:
        """
        Intenta corregir automáticamente una intención que falló.
        
        Returns:
            Nueva intención corregida o None
        """
        error = result.get('error', '')
        missing = result.get('missing_params', [])
        
        if missing:
            # Intentar proporcionar valores por defecto
            new_params = failed_intent.parameters.copy()
            
            for param in missing:
                # Valores por defecto comunes
                defaults = {
                    'location': [0, 0, 0],
                    'scale': 1.0,
                    'name': 'Object',
                    'color': 'white',
                    'size': 1.0,
                }
                if param in defaults:
                    new_params[param] = defaults[param]
                    log_info(f"Corrección: Parámetro '{param}' = {defaults[param]}")
            
            # Crear nueva intención con parámetros corregidos
            return CommandIntent(
                command_name=failed_intent.command_name,
                confidence=failed_intent.confidence * 0.8,  # Menor confianza
                parameters=new_params
            )
        
        return None
    
    def _extract_missing_params(self, command_class: type, error: Exception) -> List[str]:
        """Extrae los parámetros faltantes de un error de TypeError."""
        error_msg = str(error)
        matches = re.findall(r"'(\w+)'", error_msg)
        return matches
    
    def generate_feedback(self, results: List[Dict], scene_summary: Dict) -> str:
        """Genera un mensaje de feedback inteligente sobre la ejecución."""
        if not results:
            return "No se ejecutaron comandos."
        
        successful = [r for r in results if r.get('success')]
        failed = [r for r in results if not r.get('success')]
        
        if len(failed) == 0:
            return f"✓ Éxito total: {len(successful)} comandos ejecutados."
        elif len(successful) == 0:
            errors = [r.get('error', 'Error desconocido') for r in failed]
            return f"✗ Fallo total: {len(failed)} comandos fallaron. Errores: {', '.join(errors[:2])}"
        else:
            return f"⚠ Resultado mixto: {len(successful)} éxitos, {len(failed)} fallos."
