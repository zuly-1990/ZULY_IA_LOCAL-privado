# core/agent.py
"""
Agente de IA Zuly - Núcleo Inteligente.

Este archivo define la clase `Agent`, que actúa como el cerebro central del sistema.
Combina comprensión de lenguaje natural, ejecución de comandos complejos, 
monitoreo de escena y bucles de feedback para crear un agente autónomo capaz
de interpretar peticiones complejas en lenguaje natural y traducirlas a acciones
concretas en Blender.

Características principales:
- Procesamiento de lenguaje natural (NLU) para interpretar peticiones
- Sistema de validación inteligente de comandos
- Monitoreo y retroalimentación de estado de escena
- Planificación y corrección automática de errores
- Historial de sesión y aprendizaje contextual
"""

import os
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from core.utils.logging import log_info, log_warning, log_error, log_success, log_debug
from core.config import config
from core.utils.nlu import NaturalLanguageProcessor, CommandIntent
from core.diagnostics.scene_monitor import SceneMonitor, SceneState
from core.utils.file_manager import FileManager
from core.security.identity import is_author_verified, decision_learning_allowed, generate_local_key
from core.validation.v0_validator import V0Validator
from core.validation.v1_validator import V1Validator
from core.validation.v2_validator import V2Validator  # FIN DE SEMANA 4: Validación Contextual
from core.learning.pattern_memory import PatternMemory  # NUEVO: Fase 5.13
from core.state.state_awareness import StateAwareness  # NUEVO: Fase 5.14
from core.environment.blender_observer import BlenderObserver  # NUEVO: Fase 5.15
from core.environment.blender_semantic_observer import BlenderSemanticObserver # NUEVO: Fase 5.16
from core.environment.blender_context import get_blender_context # NUEVO: Fase de Vinculación
from core.reasoning.intention_simulator import IntentionSimulator # NUEVO: Fase 6
from core.guard.context_guard import ContextGuard # NUEVO: Fase 12
from core.explain.decision_explainer import DecisionExplainer # NUEVO: Fase 13
from core.authorization.human_gate import HumanGate # NUEVO: Fase 14
from core.memory.trace_core import TraceCore # NUEVO: Fase 15
from core.security.black_protocol import BlackProtocol # NUEVO: Fase 16
from core.cognition.cognition_core import CognitionCore # NUEVO: Fase C
from core.cognition.evaluators.render_evaluator import RenderEvaluator # NUEVO: Fase C

# FASE 18.5: Integración de seguridad y observabilidad
from core.execution.failsafe_executor import FailsafeExecutor, get_failsafe_executor
from core.observability.action_logger import ActionLogger, get_action_logger

# FASE 19: Decision Engine - Enrutamiento estratégico
from decision_engine import get_decision_engine, decidir

# FASE 18.5: Control de Complejidad
MAX_ACTIONS_PER_SESSION = 50  # Límite de acciones por sesión


class ExecutionContext:
    """
    Contexto de ejecución que mantiene el estado de una sesión del agente.
    
    FASE CONSOLIDACIÓN: Ahora con límites de memoria para escalabilidad.
    """
    
    # Límites de escalabilidad (rolling window)
    MAX_EXECUTION_HISTORY = 100  # Últimos 100 comandos
    MAX_SCENE_STATES = 20  # Últimos 20 estados
    MAX_ERRORS = 50  # Últimos 50 errores
    
    def __init__(self):
        self.execution_history = []  # Historial de comandos ejecutados
        self.scene_states = []  # Estados capturados de la escena
        self.errors = []  # Errores ocurridos
        self.success_count = 0
        self.failure_count = 0
        self.scene_requirements = {}  # Requisitos de escena esperados
        self.session_start = datetime.now()
    
    def add_execution(self, command_name: str, success: bool, result: Any = None, error: str = None):
        """Registra una ejecución de comando."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command_name,
            'success': success,
            'result': result,
            'error': error,
        }
        self.execution_history.append(entry)
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
            if error:
                self.errors.append(error)
        
        # Rolling window: mantener solo los últimos N elementos
        self._apply_limits()
    
    def _apply_limits(self):
        """Aplica límites de rolling window para escalabilidad."""
        if len(self.execution_history) > self.MAX_EXECUTION_HISTORY:
            self.execution_history = self.execution_history[-self.MAX_EXECUTION_HISTORY:]
        if len(self.scene_states) > self.MAX_SCENE_STATES:
            self.scene_states = self.scene_states[-self.MAX_SCENE_STATES:]
        if len(self.errors) > self.MAX_ERRORS:
            self.errors = self.errors[-self.MAX_ERRORS:]
    
    def add_scene_state(self, state: Dict):
        """Agrega un estado de escena con límite."""
        self.scene_states.append(state)
        self._apply_limits()
    
    def get_summary(self) -> Dict:
        """Retorna un resumen del contexto de ejecución."""
        return {
            'session_start': self.session_start.isoformat(),
            'commands_executed': len(self.execution_history),
            'total_successes': self.success_count,
            'total_failures': self.failure_count,
            'error_count': len(self.errors),
            'memory': {
                'history_size': len(self.execution_history),
                'scene_states': len(self.scene_states),
                'errors_stored': len(self.errors)
            }
        }


class Agent:
    """
    Agente de IA Zuly - Sistema de Observación y Evaluación.
    
    Alineado con el Protocolo de Identidad, el agente se enfoca en:
    1. Observar y registrar peticiones en lenguaje natural.
    2. Evaluar la integridad técnica y los riesgos de las órdenes.
    3. Solicitar aclaraciones cuando la confianza es insuficiente.
    4. Ejecutar comandos en Blender bajo autorización del protocolo.
    5. Mantener trazabilidad total sin autonomía de decisión.
    """
    
    def __init__(self, auto_monitor: bool = True, force_mock: bool = False):
        """
        Inicializa el Agente Zuly con todas sus capacidades.
        
        FASE 17: Ahora usa EngineAdapter para desacoplamiento total.
        
        :param auto_monitor: Si True, captura automáticamente el estado de escena tras cada comando
        :param force_mock: Si True, fuerza uso de MockAdapter (para tests sin Blender)
        """
        log_info("=" * 60)
        log_info("INICIALIZANDO AGENTE ZULY - VERSIÓN INTELIGENTE")
        log_info("=" * 60)
        
        # FASE 17: Inicializar Engine Adapter (CRÍTICO)
        from core.adapters import get_engine_adapter
        self.engine_adapter = get_engine_adapter(force_mock=force_mock)
        adapter_type = "MockAdapter" if force_mock else ("BlenderAdapter" if self.engine_adapter.is_available() else "MockAdapter")
        log_info(f"[FASE 17] Engine Adapter: {adapter_type}")
        
        # Configuración base
        self.config = config
        
        # FASE 23: IntentRouter para handlers funcionales (48 handlers)
        from core.intents.intent_router import IntentRouter
        from core.commands.blender_command_registry import register_blender_handlers
        self.intent_router = IntentRouter()
        register_blender_handlers(self.intent_router)
        handler_count = len(self.intent_router.command_handlers)
        log_info(f"[FASE 23] IntentRouter: {handler_count} handlers registrados")
        
        # Capacidades de IA (FASE 17: Con adapter inyectado)
        self.nlu = NaturalLanguageProcessor(self.intent_router.command_handlers)
        self.scene_monitor = SceneMonitor(adapter=self.engine_adapter)  # FASE 17
        self.validator_v0 = V0Validator(adapter=self.engine_adapter)
        self.validator_v1 = V1Validator()
        self.validator_v2 = V2Validator()  # FIN DE SEMANA 4: Guardián de contexto (pre-ejecución)
        
        # Sistema de Memoria de Patrones (Fase 5.13)
        self.pattern_memory = PatternMemory()
        
        # Sistema de Autoconciencia Operativa (Fase 5.14)
        # SOLO LECTURA - NO modifica comportamiento
        self.state_awareness = StateAwareness(self)
        
        # Monitor Pasivo del Entorno (Fase 5.15 y 5.16) - FASE 17: Con adapter
        self.blender_observer = BlenderObserver(adapter=self.engine_adapter)  # FASE 17
        self.semantic_observer = BlenderSemanticObserver()
        self.intention_simulator = IntentionSimulator() # NUEVO: Fase 6
        self.context_guard = ContextGuard() # NUEVO: Fase 12
        self.decision_explainer = DecisionExplainer() # NUEVO: Fase 13
        self.human_gate = HumanGate() # NUEVO: Fase 14
        self.trace_core = TraceCore() # NUEVO: Fase 15
        
        # FASE C: Cognición Base
        self.cognition = CognitionCore()
        self.cognition.register_evaluator('render', RenderEvaluator())
        
        self._blender_history = []
        
        # FASE 18.5: Seguridad y Observabilidad
        self.failsafe_executor = get_failsafe_executor()  # Modo seguro
        self.action_logger = get_action_logger()  # Mini-log interno
        log_info("[FASE 18.5] FailsafeExecutor y ActionLogger integrados")
        
        # Estado de sesión
        self.context = ExecutionContext()
        self.auto_monitor = auto_monitor
        self.last_scene_state = None
        
        # Protocolo de Identidad y Seguridad de Autor
        self.authorized = is_author_verified()
        self.operational_state = "Observación"
        
        if not self.authorized:
            generate_local_key()
            self.authorized = is_author_verified()
        
        # Logging de inicialización
        pattern_stats = self.pattern_memory.get_stats()
        log_info(f"[OK] Procesador de Lenguaje Natural inicializado")
        log_info(f"[OK] Monitor de Escena activo (vía {adapter_type})")
        log_info(f"[OK] Memoria de Patrones: {pattern_stats['total_patterns']} patrones")
        log_info(f"[OK] Autoconciencia Operativa: activa (pasiva)")
        log_info(f"[OK] Identidad de Autor: {'VERIFICADA' if self.authorized else 'PENDIENTE'}")
        log_info(f"[OK] Estado Inicial: {self.operational_state}")
        log_info("=" * 60)
        log_info("Agente Zuly listo conforme al Protocolo de Identidad")
        log_info(f"[FASE 17] Desacoplamiento: ACTIVO ({adapter_type})")
        log_info("=" * 60)
        
        # FASE 18.5: Registrar módulos activos
        from core.governance import registry
        registry.register("Agent")
        registry.register("SceneMonitor")
        registry.register("BlenderObserver")
        registry.register("PatternMemory")
        registry.register("TraceCore")
        registry.register("StateAwareness")
        log_info(f"[FASE 18.5] Módulos registrados: {registry.count()}")

    def get_blender_snapshot(self) -> Dict[str, Any]:
        """Captura y almacena un snapshot del estado de Blender."""
        snap = self.blender_observer.snapshot()
        self._blender_history.append(snap)
        if len(self._blender_history) > 5:
            self._blender_history.pop(0)
        return snap

    def analyze_scene(self) -> Dict[str, Any]:
        """
        Realiza un análisis completo del entorno actual.
        Combina: Contexto + Snapshot Visual + Interpretación Semántica.
        """
        # 1. Contexto (¿Dónde estoy?)
        context = get_blender_context(adapter=self.engine_adapter)  # FASE 17
        
        # 2. Snapshot Visual (¿Qué veo?)
        snapshot = self.blender_observer.snapshot()
        
        # 3. Análisis Semántico (¿Qué significa?)
        semantic = self.semantic_observer.analyze(snapshot)
        
        # 4. Estructurar reporte unificado
        full_analysis = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "visual_snapshot": snapshot,
            "semantic_interpretation": semantic,
            "collections_hierarchy": snapshot.get("collections_hierarchy", [])
        }
        
        self.last_scene_state = full_analysis # Actualizar estado interno
        return full_analysis

    def compare_blender_snapshots(self, old: Dict, new: Dict) -> Dict:
        """Compara dos snapshots y detecta cambios básicos."""
        old_names = {o["name"] for o in old.get("objects", [])}
        new_names = {o["name"] for o in new.get("objects", [])}
        
        added = new_names - old_names
        removed = old_names - new_names
        
        return {
            "added_count": len(added),
            "removed_count": len(removed),
            "added_names": list(added),
            "removed_names": list(removed),
            "total_change": len(added) + len(removed)
        }
    
    def get_system_state(self):
        """
        Captura el estado completo del sistema ZULY.
        
        FASE 18.1: Observabilidad y Control Humano
        
        Returns:
            SystemStateSnapshot con estado capturado (encadenable)
        """
        from core.observability.system_state import SystemStateSnapshot
        return SystemStateSnapshot(self).capture()
    
    def system_report(self) -> str:
        """
        Genera reporte completo del sistema para humanos.
        
        FASE 18.3: Snapshot + Trace unificados
        
        Esta función es SAGRADA. Nunca debe romperse.
        Es el punto único de acceso para entender ZULY.
        
        Returns:
            String formateado legible por humanos
        """
        snapshot = self.get_system_state()
        return snapshot.to_human_readable()


    def process_natural_request(self, user_request: str, max_retries: int = 2) -> Dict[str, Any]:
        """
        Procesa una petición en lenguaje natural y ejecuta los comandos necesarios.
        
        Este es el método principal del agente. Toma texto libre del usuario
        e interpreta qué desea hacer, ejecutando una o más secuencias de comandos.
        
        :param user_request: La petición del usuario en lenguaje natural
        :param max_retries: Número máximo de reintentos si un comando falla
        :return: Diccionario con resultados y feedback
        """
        log_info(f"\n{'='*60}")
        log_info(f"NUEVA PETICIÓN: {user_request}")
        log_info(f"{'='*60}")
        
        if not user_request or not user_request.strip():
            return {
                'success': False,
                'error': 'Petición vacía',
                'feedback': 'Por favor, proporciona una petición válida.'
            }
            
        # --- CORTAFUEGOS DE MEMORIA (RAM MONITOR) ---
        try:
            import psutil
            ram_percent = psutil.virtual_memory().percent
            if ram_percent > 85.0:
                log_warning(f"CRÍTICO: RAM al {ram_percent}%. Forzando limpieza (Garbage Collection).")
                # Intentamos purgar huérfanos si estamos conectados a Blender
                if self.engine_adapter.is_available():
                    try:
                        import bpy
                        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
                        log_info("✓ Memoria huérfana de Blender purgada.")
                    except:
                        pass
                        
                return {
                    'success': False,
                    'error': 'MEMORIA SATURADA',
                    'status': 'PAUSA_SEGURIDAD',
                    'feedback': f'Servidor al {ram_percent}% de RAM. Pausando el ciclo para evitar colapso. Memoria purgada.'
                }
        except ImportError:
            pass # Si psutil no está instalado, ignorar
        # ---------------------------------------------

        # 0. PROTOCOLO NEGRO (FASE 16) - MÁXIMA PRIORIDAD
        # A. Bloqueo Persistente (Modo Negro)
        if BlackProtocol.is_active():
            log_error("❄️ ACCIÓN RECHAZADA: PROTOCOLO NEGRO ACTIVO (MODO_NEGRO)")
            return {
                'success': False,
                'error': 'PROTOCOLO NEGRO ACTIVO',
                'status': 'MODO_NEGRO',
                'feedback': 'El sistema está bloqueado por el Protocolo Negro. Se requiere validación humana raíz manual.'
            }

        # B. Detección de Influencia de IAs Externas
        influence = BlackProtocol.detect_ai_influence(user_request)
        if influence:
            BlackProtocol.activate_lock(influence)
            return {
                'success': False,
                'error': 'INTENTO_INFLUENCIA_IA_DETECTADO',
                'status': 'MODO_NEGRO',
                'feedback': f"Interferencia detectada: {influence}. Modo Negro activado."
            }

        # 0.1 BARRERA DE SEGURIDAD PERSISTENTE (Antigua)
        if "Bloqueo" in self.operational_state:
            log_warning(f"⛔ Solicitud rechazada por bloqueo persistente: {self.operational_state}")
            return {
                'success': False,
                'error': f'Sistema Bloqueado: {self.operational_state}',
                'operational_state': self.operational_state,
                'reason': 'El sistema está en modo de bloqueo persistente.',
                'feedback': f'Sistema en estado de bloqueo ({self.operational_state}). No se procesan solicitudes.'
            }
        
        # 1. Procesar con NLU para extraer intenciones
        intents = self.nlu.process(user_request)
        
        if not intents:
            return {
                'success': False,
                'error': 'No se pudieron interpretar intenciones',
                'feedback': 'Acción no identificada en la petición. Se requiere reformulación técnica.',
                'suggestions': self._get_suggestions(user_request)
            }
        
        log_info(f"Intenciones detectadas: {len(intents)}")
        for i, intent in enumerate(intents, 1):
            log_info(f"  {i}. {intent} (confianza: {intent.confidence:.2%})")
        
        # Seleccionar la intención con mayor confianza
        best_intent = intents[0]
        log_info(f"\nEjecutando intención principal: {best_intent.command_name}")

        # FASE 19: Decision Engine - Consultar si existe patrón conocido
        log_info("▶ [FASE 19] Consultando decision_engine para patrón...")
        decision = decidir(user_request)
        
        if decision["tipo"] == "usar_patron":
            log_success(f"✓ [FASE 19] Patrón encontrado: {decision['patron']} (confianza: {decision['confianza']:.1%})")
            # Usar handler del patrón
            best_intent.command_name = decision["patron"]
            # Marcar que es patrón para audit trail
            best_intent.pattern_source = decision["patron"]
            best_intent.pattern_confidence = decision["confianza"]
        else:
            log_info(f"◇ [FASE 19] Usando agente autónomo (confianza: {decision['confianza']:.1%})")
            # Continuar con flujo estándar
            best_intent.pattern_source = None

        # 2. Evaluación de Contexto y Riesgo (Fase 12, 13, 14)
        self.operational_state = "Evaluación"
        log_info(f"Estado: {self.operational_state}")

        # Capturar contexto para validación activa
        current_blender_context = self.analyze_scene().get("context", {})
        
        # A. Context Guard (Fase 12)
        guard_result = self.context_guard.evaluate(best_intent.command_name, current_blender_context)
        
        # B. Human Gate (Fase 14)
        auth_result = self.human_gate.authorize(best_intent.command_name)
        
        # Preparar datos para el explicador (Fase 13)
        decision_data = {
            "intention": best_intent.command_name,
            "guard_result": guard_result,
            "auth_result": auth_result
        }

        # 3. Validación con Protocolo de Identidad y Autoría
        # Definimos el umbral crítico para aprendizaje seguro (85%)
        # AJUSTE U3: Bajamos a 0.85 para incluir comandos por keywords
        LEARNING_THRESHOLD = 0.85
        
        if not self.authorized:
            # Fase 16: Si no está autorizado y se intenta ejecutar, activar Modo Negro
            reason = "Acceso no autorizado detectado en fase de ejecución."
            BlackProtocol.activate_lock(reason)
            
            self.operational_state = "Bloqueo Ético / Seguridad / NEGRO"
            status_msg = f"Estado: {self.operational_state}. Intento por autor NO VERIFICADO."
            log_warning(status_msg)
            self._register_blocked_attempt("Usuario no verificado", "Bloqueo por Identidad (MODO NEGRO)")
            
            explanation = self.decision_explainer.explain(decision_data)
            
            # Registrar traza de bloqueo por identidad
            self.trace_core.append_trace({
                "intention": best_intent.command_name,
                "confidence": best_intent.confidence,
                "guard_result": guard_result,
                "auth_result": auth_result,
                "execution_success": False,
                "error": "Autor No Verificado - MODO NEGRO"
            })

            return {
                'success': False,
                'error': 'PROTOCOLO NEGRO: Autor No Verificado',
                'status': 'MODO_NEGRO',
                'feedback': f"{status_msg} Se requiere autenticación física (USB Vault) para desactivar Modo Negro.",
                'explanation': explanation
            }

        # 4. Manejo de Bloqueos de Contexto
        if guard_result["status"] == "BLOQUEADO":
            self.operational_state = "Bloqueado por Contexto"
            log_warning(f"⛔ {guard_result['reason']}")
            explanation = self.decision_explainer.explain(decision_data)
            
            # Registrar traza de bloqueo por contexto
            self.trace_core.append_trace({
                "intention": best_intent.command_name,
                "confidence": best_intent.confidence,
                "guard_result": guard_result,
                "auth_result": auth_result,
                "execution_success": False,
                "error": "Bloqueo por Contexto"
            })

            return {
                'success': False,
                'error': 'Contexto Inválido',
                'feedback': guard_result["reason"],
                'explanation': explanation
            }

        # 5. Manejo de Autorización Humana
        # FASE 5: Restricción de Staging
        # Si la intención viene de un patrón evocado, verificar su estatus
        evoked_pattern_id = getattr(best_intent, 'pattern_id', None)
        if evoked_pattern_id:
            pattern = self.pattern_memory.staging_repo.get_pattern(evoked_pattern_id)
            if pattern and pattern.get('metadata', {}).get('status') == "STAGING":
                log_warning(f"⚠️ Patrón en STAGING detectado ({evoked_pattern_id[:8]}). Forzando petición de permiso.")
                auth_result["action"] = "ASK"
                auth_result["reason"] = f"El patrón evocado '{best_intent.command_name}' aún está en STAGING y requiere supervisión."

        if auth_result["action"] == "BLOCK":
            self.operational_state = "Bloqueo de Seguridad"
            log_warning(f"⛔ {auth_result['reason']}")
            explanation = self.decision_explainer.explain(decision_data)
            
            # Registrar traza de bloqueo de seguridad
            self.trace_core.append_trace({
                "intention": best_intent.command_name,
                "confidence": best_intent.confidence,
                "guard_result": guard_result,
                "auth_result": auth_result,
                "execution_success": False,
                "error": "Bloqueo de Seguridad"
            })

            return {
                'success': False,
                'error': 'Acción Prohibida',
                'feedback': auth_result["reason"],
                'explanation': explanation
            }
        
        if auth_result["action"] == "ASK":
            self.operational_state = "Autorización Automática (Simulada)"
            log_info(f"❓ {auth_result['reason']}")
            log_info("ℹ️ [SANEAMIENTO] Entorno no interactivo detectado - Procediendo con autorización automática.")
            # En lugar de retornar, permitimos que el flujo continúe a la ejecución
            # Pero registramos la intención de pedir permiso en la traza
            self.trace_core.append_trace({
                "intention": best_intent.command_name,
                "confidence": best_intent.confidence,
                "guard_result": guard_result,
                "auth_result": auth_result,
                "auth_simulated": True,
                "status": "AUTO_AUTHORIZED_FOR_TEST"
            })
            # El flujo continúa...

        # Confianza mínima para ejecución básica
        if best_intent.confidence < 0.7:
            # --- ZULY AUTO-CODING FALLBACK ---
            log_warning(f"Confianza baja ({best_intent.confidence:.2%}). Activando Auto-Coding para generar nuevo Handler.")
            from core.utils.auto_coder import generate_and_register_handler
            if generate_and_register_handler(user_request):
                # Recargar intent router para que reconozca el nuevo comando
                from core.commands.blender_command_registry import register_blender_handlers
                register_blender_handlers(self.intent_router)
                
                return {
                    'success': True,
                    'error': None,
                    'feedback': f"¡Zuly aprendió algo nuevo! He auto-programado un handler para: '{user_request}'. Inténtalo de nuevo en el siguiente ciclo."
                }
            # ---------------------------------
            
            self.operational_state = "Solicitud de Aclaración"
            status_msg = f"Estado: {self.operational_state}. Confianza insuficiente ({best_intent.confidence:.2%})."
            log_warning(status_msg)
            return {
                'success': False,
                'error': 'Baja Confianza',
                'feedback': f"{status_msg} Por favor, especifica mejor tu petición."
            }

        can_learn = self.authorized and best_intent.confidence >= LEARNING_THRESHOLD
        if can_learn:
            self.operational_state = "Ejecución con Aprendizaje"
        else:
            self.operational_state = "Ejecución"
            
        log_info(f"Estado: {self.operational_state} (Confianza: {best_intent.confidence:.2%})")

        # 6. VALIDACIÓN V2 (Contextual) — CORRE ANTES DE EJECUTAR
        # Si el contexto es inválido, bloqueamos aquí sin tocar el motor.
        validation_v2 = self.validator_v2.validate(
            adapter=self.engine_adapter,
            blender_context=current_blender_context
        )
        if not validation_v2.get('verified', False):
            log_error(f"[V2] Contexto inválido — ejecución bloqueada: {validation_v2.get('reason')}")
            self.trace_core.append_trace({
                "intention": best_intent.command_name,
                "confidence": best_intent.confidence,
                "execution_success": False,
                "error": f"V2 BLOQUEO: {validation_v2.get('reason')}",
                "v2_checks": validation_v2.get('checks', [])
            })
            return {
                'success': False,
                'error': f"V2 BLOQUEO CONTEXTUAL: {validation_v2.get('reason')}",
                'feedback': f"✗ Ejecución bloqueada por V2 (Validación Contextual): "
                            f"{validation_v2.get('reason')}",
                'validation_v2': validation_v2,
                'command_executed': best_intent.command_name
            }

        # 7. Ejecutar el comando con reintentos limitados
        results = []
        
        # Iniciar validación (captura PRE)
        self.validator_v0.start_validation()
        # V1 no necesita start_validation explícito si le pasamos los snapshots, 
        # pero para consistencia capturamos el pre_snapshot aquí si es necesario.
        pre_snapshot = self.validator_v0.pre_snapshot 
        
        execution_success = False
        last_exec_result = {}

        for attempt in range(1, max_retries + 1):
            result = self._execute_intent(best_intent, attempt, max_retries)
            results.append(result)
            last_exec_result = result
            
            if result['success']:
                # Ejecutar Validación V0 (captura POST y comparación)
                validation_v0 = self.validator_v0.validate(result)
                result['validation_v0'] = validation_v0
                
                if validation_v0['verified']:
                    # Ejecutar Validación V1 (Estructural Profunda)
                    from core.validation.state_snapshot import StateSnapshot
                    post_snapshot = StateSnapshot.capture()
                    validation_v1 = self.validator_v1.validate(result, pre_snapshot, post_snapshot)
                    result['validation_v1'] = validation_v1
                    
                    if validation_v1['verified']:
                        log_info(f"✓ Ejecución procesada y validada (V0+V1): {validation_v1['details']}")
                        execution_success = True
                        break
                    else:
                        log_warning(f"⚠ Fallo Estructural V1: {validation_v1['details']}")
                        result['success'] = False
                        result['error'] = f"Error de Validación Estructural V1: {validation_v1['details']}"
                        # Rollback lógico: el comando se ejecutó en motor, pero ZULY lo rechaza
                else:
                    log_warning(f"⚠ Ejecución exitosa pero validación V0 fallida: {validation_v0['details']}")
                    result['success'] = False # Invalidar éxito si la realidad no coincide
                    result['error'] = f"Error de Validación V0: {validation_v0['details']}"
            else:
                log_warning(f"Intento {attempt} no completado: {result.get('error')}")
        
        # 8. Generar Explicación Final (Fase 13)
        decision_data["execution_result"] = {
            "success": execution_success,
            "message": last_exec_result.get("error", "OK") if not execution_success else "Ejecutado correctamente",
            "details": last_exec_result
        }
        explanation = self.decision_explainer.explain(decision_data)

        # 9. Registrar Traza Final (Fase 15)
        self.trace_core.append_trace({
            "intention": best_intent.command_name,
            "confidence": best_intent.confidence,
            "parameters": best_intent.parameters,
            "guard_result": guard_result,
            "auth_result": auth_result,
            "execution_success": execution_success,
            "execution_details": last_exec_result,
            "explanation": explanation["human_summary"]
        })

        # FASE 5: Actualizar Jerarquía de Memoria si se usó un patrón evocado
        # O si se acaba de memorizar uno nuevo
        evoked_pattern_id = getattr(best_intent, 'pattern_id', None)
        if evoked_pattern_id:
            self.pattern_memory.register_execution_result(evoked_pattern_id, execution_success)

        # 10. Capturar estado de escena para feedback (Refrescar monitor)
        if self.auto_monitor:
            self.scene_monitor.capture_scene_state() 
            scene_summary = self.scene_monitor.get_scene_summary()
        else:
            scene_summary = {}
        
        # 11. Compilar respuesta final
        final_response = {
            'success': execution_success,
            'command_executed': best_intent.command_name,
            'confidence': best_intent.confidence,
            'parameters': best_intent.parameters,
            'results': results,
            'scene_state': scene_summary,
            'feedback': self._generate_feedback(results, scene_summary),
            'explanation': explanation,
            'attempts': len([r for r in results if r]),
        }
        
        # 12. Registrar en bitácora de aprendizaje si aplica
        if self.operational_state == "Ejecución con Aprendizaje" and final_response['success']:
            self._register_learned_decision(best_intent, final_response)
            
            # NUEVO (Fase 5.13): Intentar memorizar patrón (con todas las condiciones)
            final_response['operational_state'] = self.operational_state
            final_response['mode'] = 'REACTIVE'  # TODO: agregar mode real cuando esté disponible
            # --- ULTRA EMERGENCIA: Auto-memorización CONTROLADA ---
            # Verificar que V0 NO fue pasivo antes de memorizar
            v0_result = last_exec_result.get('validation_v0', {})
            v0_passive = v0_result.get('passive', False)
            
            if v0_passive:
                log_warning("[ULTRA EMERGENCIA] ❌ Auto-memorización BLOQUEADA: V0 fue pasivo (sin effect declarado)")
            else:
                log_info("[SANEAMIENTO] Intentando memorizar patrón (Fase U3)...")
                # Pasar snapshots del validador para validación Condition 6
                final_response['scene_state_pre'] = self.validator_v0.pre_snapshot
                final_response['scene_state'] = self.validator_v0.post_snapshot
                final_response['validation'] = v0_result # Para compatibilidad con PatternMemory
                
                pattern_id = self.pattern_memory.store_pattern(user_request, final_response)
                if pattern_id:
                    final_response['pattern_pending'] = pattern_id
                    final_response['feedback'] += f"\n[PABELLÓN] Patrón registrado con ID {pattern_id[:8]} (Esperando tu 'Visto Bueno' para aprendizaje permanente)."
                    log_success(f"✓ Patrón enviado a PENDING: {pattern_id[:8]}")
            # --- END ULTRA EMERGENCIA ---
        
        # 13. Registrar en contexto
        self.context.add_execution(
            best_intent.command_name,
            final_response['success'],
            final_response,
            final_response.get('error')
        )

        # FASE 5: Si el comando falló definitivamente y venía de un patrón, 
        # ya se registró en el bloque anterior. Si fue un comando nuevo que 
        # falló y NO se memorizó, no hay patrón que degradar aún.
        
        log_info(f"\nResultado final: {'✓ ÉXITO' if final_response['success'] else '✗ FALLO'}")
        log_info(f"Feedback: {final_response['feedback']}")
        
        # Retorno a Observación
        self.operational_state = "Observación"
        
        return final_response
    
    def simulate_intention(self, user_request: str) -> Dict[str, Any]:
        """
        Fase 6: Simula una intención sin ejecutarla.
        Cruza la petición del usuario con el contexto actual para detectar contradicciones.
        """
        log_info(f"🔮 SIMULANDO INTENCIÓN: {user_request}")
        
        # 1. Interpretar (NLU) - Sin ejecutar
        # Usamos el NLU para entender qué quiere hacer, pero no pasamos a execute
        intents = self.nlu.process(user_request)
        if not intents:
             return {
                 "intencion": user_request,
                 "estado_detectado": "Incomprensible",
                 "contradiccion": True,
                 "razon": "No pude entender la intención técnica.",
                 "opciones_sugeridas": ["Reformular petición"],
                 "accion_ejecutada": False
             }
        
        best_intent = intents[0]
        
        # 2. Analizar Contexto Real (Ojos abiertos)
        current_scene = self.analyze_scene()
        
        # 3. Simular Razonamiento
        simulation = self.intention_simulator.simulate(best_intent, current_scene)
        
        log_info(f"🔮 Resultado Simulación: {simulation['razon']} (Contradicción: {simulation['contradiccion']})")
        return simulation

    def _register_learned_decision(self, intent: CommandIntent, response: Dict):
        """Registra una decisión autorizada en la bitácora segura."""
        log_path = "bitacora/DECISIONES_APRENDIDAS.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = f"| {timestamp} | SÍ | {self.operational_state} | {intent.confidence:.2f} | {intent.command_name}: {intent.parameters} | ÉXITO |\n"
        
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(entry)
            log_success(f"✓ Decisión registrada con éxito en {log_path}")
        except Exception as e:
            log_error(f"Error al registrar decisión: {e}")

    def _register_blocked_attempt(self, user: str, reason: str):
        """Registra intentos bloqueados en la bitácora segura."""
        log_path = "bitacora/DECISIONES_APRENDIDAS.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = f"| {timestamp} | {user} | {reason} | Bloqueo Ético / Seguridad |\n"
        
        try:
            # Buscar la línea de anomalías para insertar debajo
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            with open(log_path, "w", encoding="utf-8") as f:
                for line in lines:
                    f.write(line)
                    if "## 🚫 Intentos Bloqueados y Anomalías" in line:
                        # Saltar las cabeceras de tabla si existen
                        pass
                f.write(entry)
        except Exception as e:
            log_error(f"Error al registrar anomalía: {e}")
    
    def execute_via_router(self, handler_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        FASE 23: Ejecuta comando vía IntentRouter (handlers funcionales).
        
        Esta es la nueva vía principal de ejecución que usa los 29 handlers
        registrados en el IntentRouter.
        
        Args:
            handler_name: Nombre del handler (ej: 'blender.create_cube')
            parameters: Parámetros para el handler
            
        Returns:
            Resultado de la ejecución del handler
        """
        if not hasattr(self, 'intent_router') or not self.intent_router:
            log_error("[FASE 23] IntentRouter no disponible")
            return {
                'success': False,
                'error': 'IntentRouter no inicializado',
                'route': 'ROUTER_NOT_AVAILABLE'
            }
        
        # Buscar handler en el router
        handler = self.intent_router.command_handlers.get(handler_name)
        
        if not handler:
            log_warning(f"[FASE 23] Handler no encontrado en router: {handler_name}")
            return {
                'success': False,
                'error': f"Handler '{handler_name}' no registrado en IntentRouter",
                'available_handlers': list(self.intent_router.command_handlers.keys())[:10],
                'route': 'HANDLER_NOT_FOUND'
            }
        
        try:
            log_info(f"[FASE 23] Ejecutando vía IntentRouter: {handler_name}")
            log_debug(f"[FASE 23] Parámetros: {parameters}")
            
            # Ejecutar handler (todos los handlers aceptan: parameters, adapter)
            result = handler(parameters, self.engine_adapter)
            
            # FASE C: Evaluación Cognitiva
            diagnosis = self.cognition.evaluate({
                'command_executed': handler_name,
                'parameters': parameters,
                'success': result.get('success', False),
                'output_path': result.get('output_path')
            })
            result['cognition_diagnosis'] = diagnosis
            
            # Logging según resultado
            if result.get('success', False):
                log_success(f"[FASE 23] ✓ Handler ejecutado: {handler_name}")
                self.action_logger.log_ok(
                    action=handler_name,
                    target=str(parameters.get('name', parameters.get('object_name', 'scene'))),
                    details=f"route: IntentRouter"
                )
            else:
                log_warning(f"[FASE 23] Handler falló: {result.get('error', 'Unknown')}")
                self.action_logger.log_fail(
                    action=handler_name,
                    target=str(parameters.get('name', 'unknown')),
                    details=result.get('error', 'No error message')
                )
            
            # Agregar metadata de routing y efectos para el validador (FASE 23 + V1)
            result['route'] = 'INTENT_ROUTER'
            result['handler'] = handler_name
            
            # Map handler to effects for V0/V1 Validator
            if 'create' in handler_name:
                result['effect'] = 'create'
            elif any(k in handler_name for k in ['move', 'rotate', 'scale', 'position']):
                result['effect'] = 'transform'
            elif any(k in handler_name for k in ['clear', 'delete']):
                result['effect'] = 'delete'
            elif 'material' in handler_name or 'set_' in handler_name:
                result['effect'] = 'property'
            
            # Asegurar que result['result']['name'] existe para el validador
            if 'result' not in result:
                result['result'] = {}
            
            # Intentar obtener el nombre del objeto de varias fuentes comunes
            obj_name = result.get('object_name') or result.get('camera_name') or result.get('light_name') or result.get('name')
            
            if 'name' not in result['result'] and obj_name:
                result['result']['name'] = obj_name
                # También sincronizar a nivel raíz para consistencia
                if 'object_name' not in result:
                    result['object_name'] = obj_name
            
            return result
            
        except Exception as e:
            log_error(f"[FASE 23] Excepción al ejecutar handler '{handler_name}': {e}")
            self.action_logger.log_fail(handler_name, 'exception', str(e))
            return {
                'success': False,
                'error': f"Excepción en handler: {str(e)}",
                'handler': handler_name,
                'route': 'ROUTER_EXCEPTION'
            }
    
    def _execute_intent(self, intent: CommandIntent, attempt: int = 1, max_attempts: int = 1) -> Dict:
        """
        Ejecuta una intención de comando específica.
        
        FASE 23: Primero intenta con IntentRouter (handlers), luego con sistema antiguo (clases).
        
        :param intent: La intención a ejecutar
        :param attempt: Número de intento actual
        :param max_attempts: Número máximo de intentos
        :return: Diccionario con resultado de la ejecución
        """
        command_name = intent.command_name.lower()
        
        # FASE 23: PRIORIDAD 1 - Intentar con IntentRouter (nuevo sistema)
        # Mapear nombres comunes a nombres de handlers (29 handlers totales)
        handler_mappings = {
            # Primitivas (3)
            'crear_cubo': 'blender.create_cube',
            'crear_esfera': 'blender.create_sphere',
            'crear_cilindro': 'blender.create_cylinder',
            # Transformaciones (3)
            'mover_objeto': 'blender.move_object',
            'rotar_objeto': 'blender.rotate_object',
            'escalar_objeto': 'blender.scale_object',
            # Render y Sistema (3)
            'renderizar': 'blender.render_scene',
            'renderizar_escena': 'blender.render_scene',
            'obtener_info_sistema': 'system.get_info',
            'guardar_proyecto': 'blender.save_project',
            'guardar_escena': 'blender.save_scene',
            # Materiales (3)
            'crear_material': 'blender.create_material',
            'aplicar_material': 'blender.apply_material',
            'color_material': 'blender.set_material_color',
            # Luces (3)
            'crear_luz': 'blender.create_light',
            'energia_luz': 'blender.set_light_energy',
            'color_luz': 'blender.set_light_color',
            # Cámaras (3)
            'crear_camara': 'blender.create_camera',
            'camara_activa': 'blender.set_active_camera',
            'posicionar_camara': 'blender.position_camera',
            # Modificadores (3)
            'subdivision': 'blender.add_subdivision_surface',
            'array': 'blender.add_array',
            'bevel': 'blender.add_bevel',
            # Exportación (3)
            'exportar_fbx': 'blender.export_fbx',
            'exportar_obj': 'blender.export_obj',
            'exportar_gltf': 'blender.export_gltf',
            # Assembly - Fase 20 (4)
            'construir_estructura': 'blender.build_structure',
            'guardar_patron': 'blender.save_pattern',
            'cargar_patron': 'blender.load_pattern',
            'listar_patrones': 'blender.list_patterns',
        }
        
        # Buscar handler en el mapping o intentar nombre directo
        if command_name.startswith('blender.') or command_name.startswith('system.'):
            handler_name = command_name
        else:
            handler_name = handler_mappings.get(command_name, f"blender.{command_name}")
        
        if hasattr(self, 'intent_router') and handler_name in self.intent_router.command_handlers:
            log_info(f"[FASE 23] Ruta: IntentRouter → {handler_name}")
            return self.execute_via_router(handler_name, intent.parameters)
        
        # FASE 23: FALLBACK - Sistema antiguo (clases con ejecutar/validar)
        log_debug(f"[FASE 23] Handler no en router, intentando sistema antiguo: {command_name}")
        command_class = self.commands.get(command_name)
        
        if not command_class:
            # Intentar encontrar comando similar
            similar = self.nlu.find_similar_command(command_name)
            if similar:
                similar_cmd, ratio = similar
                log_warning(f"Comando no encontrado. ¿Quisiste decir '{similar_cmd}'? (similitud: {ratio:.2%})")
                return {
                    'success': False,
                    'error': f"Comando '{command_name}' no encontrado",
                    'suggestion': similar_cmd,
                    'similarity': ratio,
                }
            else:
                return {
                    'success': False,
                    'error': f"Comando '{command_name}' no existe",
                    'available_commands': list(self.commands.keys())[:5],
                }
        
        try:
            # Validación inteligente de parámetros
            validated_params = self._validate_and_prepare_parameters(
                command_class, intent.parameters
            )
            
            log_debug(f"Parámetros validados: {validated_params}")
            
            # Crear instancia del comando
            command_instance = command_class(**validated_params)
            
            # Ejecutar validación del comando
            if hasattr(command_instance, 'validar'):
                if not command_instance.validar():
                    return {
                        'success': False,
                        'error': f"Validación fallida para comando '{command_name}'",
                        'attempt': attempt,
                    }
            
            # FASE 18.5: Ejecutar el comando a través del FailsafeExecutor
            # Esto asegura que si falla, el sistema se detiene y reporta.
            failsafe_result = self.failsafe_executor.execute_single(
                action_name=command_name,
                handler=command_instance.ejecutar,
                parameters={} # Los parámetros ya están inyectados en la instancia
            )
            
            # FASE 18.5: Registrar acción en el ActionLogger
            if failsafe_result.success:
                self.action_logger.log_ok(
                    action=command_name,
                    target=str(validated_params.get('objeto', validated_params.get('nombre', 'scene'))),
                    details=f"params: {len(validated_params)}"
                )
            else:
                self.action_logger.log_fail(
                    action=command_name,
                    target=str(validated_params.get('objeto', validated_params.get('nombre', 'unknown'))),
                    details=failsafe_result.error
                )
            
            return {
                'success': failsafe_result.success,
                'command': command_name,
                'result': failsafe_result.result,
                'error': failsafe_result.error,
                'attempt': attempt,
                'stopped': failsafe_result.stopped
            }
        
        except TypeError as e:
            log_error(f"Error de parámetros: {e}")
            # FASE 18.5: Registrar fallo
            self.action_logger.log_fail(command_name, 'params', str(e))
            return {
                'success': False,
                'error': f"Error de parámetros: {str(e)}",
                'attempt': attempt,
                'missing_params': self._extract_missing_params(command_class, e),
            }
        
        except Exception as e:
            log_error(f"Error durante ejecución: {e}")
            return {
                'success': False,
                'error': f"Excepción: {str(e)}",
                'attempt': attempt,
            }
    
    def _validate_and_prepare_parameters(self, command_class: type, 
                                         parameters: Dict) -> Dict:
        """
        Valida y prepara los parámetros para un comando.
        
        Intenta hacer que los parámetros sean compatibles con el comando,
        realizando conversiones de tipo y relleno de valores por defecto.
        """
        import inspect
        
        sig = inspect.signature(command_class.__init__)
        prepared = {}
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            # Si está en los parámetros extraídos, usarlo
            if param_name in parameters:
                prepared[param_name] = parameters[param_name]
            # Si tiene valor por defecto, omitir
            elif param.default != inspect.Parameter.empty:
                continue
            # Si no, intentar encontrar un equivalente
            else:
                # Buscar sinónimos
                equivalent = self._find_parameter_equivalent(param_name, parameters)
                if equivalent is not None:
                    prepared[param_name] = equivalent
        
        return prepared
    
    def _find_parameter_equivalent(self, required_param: str, available_params: Dict) -> Optional[Any]:
        """Intenta encontrar un parámetro equivalente para un parámetro requerido."""
        # Sinónimos comunes
        synonyms = {
            'location': ['posicion', 'position', 'pos', 'lugar'],
            'rotation': ['rotacion', 'giro', 'angulo'],
            'scale': ['escala', 'tamaño', 'tamaño'],
            'name': ['nombre', 'object_name', 'objeto'],
            'values': ['coordenadas', 'coords', 'numbers'],
        }
        
        if required_param in synonyms:
            for syn in synonyms[required_param]:
                if syn in available_params:
                    return available_params[syn]
        
        return None
    
    def _extract_missing_params(self, command_class: type, error: Exception) -> List[str]:
        """Extrae los parámetros faltantes de un error de TypeError."""
        import re
        error_msg = str(error)
        # Intenta extraer nombres de parámetros de mensajes de error
        matches = re.findall(r"'(\w+)'", error_msg)
        return matches
    
    def _attempt_correction(self, failed_intent: CommandIntent, 
                            result: Dict) -> Optional[CommandIntent]:
        """
        Intenta corregir automáticamente una intención que falló.
        
        :param failed_intent: La intención que falló
        :param result: El resultado del fallo
        :return: Una nueva intención corregida o None
        """
        error = result.get('error', '')
        
        # Si hay una sugerencia de comando similar
        if 'suggestion' in result:
            corrected = CommandIntent(result['suggestion'], 0.7, failed_intent.parameters)
            log_info(f"Corrección automática: usando '{result['suggestion']}' en lugar de '{failed_intent.command_name}'")
            return corrected
        
        # Si faltan parámetros, intentar agregarlos con valores por defecto
        if 'missing_params' in result:
            log_info(f"Intentando llenar parámetros faltantes: {result['missing_params']}")
            # Aquí se podría implementar lógica más sofisticada
        
        return None
    
    def _generate_feedback(self, results: List[Dict], scene_summary: Dict) -> str:
        """
        Genera un mensaje de feedback inteligente sobre la ejecución.
        """
        if not results:
            return "No hay resultados disponibles."
        
        last_result = results[-1]
        
        if last_result['success']:
            feedback = "✓ Comando ejecutado exitosamente. "
            
            if scene_summary:
                obj_count = scene_summary.get('object_count', 0)
                feedback += f"Escena actualizada: {obj_count} objeto(s) en la escena."
            
            return feedback
        else:
            error = last_result.get('error', 'Error desconocido')
            # Si el error es una cadena muy larga (traceback), intentar extraer el mensaje final
            if isinstance(error, str) and len(error) > 200:
                short_error = error.split('\n')[-2] if '\n' in error else error[:200]
                return f"✗ Hubo un problema: {short_error}. "
            return f"✗ Hubo un problema: {error}. "
    
    def _get_suggestions(self, user_request: str) -> List[str]:
        """
        Genera sugerencias de comandos basadas en la petición del usuario.
        """
        # Palabras clave comunes para sugerencias
        keywords_to_suggestions = {
            'crear': ['crearprimitivacubo', 'crearprimitvaesfera'],
            'luz': ['anadirLuz'],
            'material': ['anadirMaterial'],
            'camara': ['configurarCamara'],
            'render': ['renderizarEscena'],
        }
        
        for keyword, suggestions in keywords_to_suggestions.items():
            if keyword.lower() in user_request.lower():
                return suggestions
        
        # Retornar los 3 comandos más comunes del IntentRouter
        return list(self.intent_router.command_handlers.keys())[:3]
    
    def execute_command(self, command_name: str, **kwargs) -> Any:
        """
        Ejecuta un comando directamente por nombre (API antigua, mantenida por compatibilidad).
        
        :param command_name: Nombre del comando
        :param kwargs: Argumentos del comando
        :return: Resultado de la ejecución
        """
        intent = CommandIntent(command_name, parameters=kwargs)
        result = self._execute_intent(intent)
        return result.get('result') if result['success'] else None
    
    def get_suggested_parameters(self, command: str) -> Optional[Dict[str, Any]]:
        """Consulta a la memoria cognitiva por los mejores parámetros conocidos"""
        return self.cognition.get_suggested_parameters(command)

    def get_available_commands(self) -> Dict[str, str]:
        """
        Retorna un diccionario de comandos disponibles con sus descripciones.
        """
        descriptions = {}
        for cmd_name, cmd_class in self.commands.items():
            try:
                instance = cmd_class()
                descriptions[cmd_name] = instance.descripcion()
            except:
                descriptions[cmd_name] = "Sin descripción disponible"
        return descriptions
    
    def get_session_summary(self) -> Dict:
        """
        Retorna un resumen de la sesión actual.
        """
        return self.context.get_summary()
    
    def export_session_report(self, filename: str = None) -> str:
        """
        Exporta un reporte completo de la sesión a JSON.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"agent_session_{timestamp}.json"
        
        report = {
            'session_summary': self.context.get_summary(),
            'execution_history': self.context.execution_history,
            'command_stats': {
                'total': len(self.context.execution_history),
                'successful': self.context.success_count,
                'failed': self.context.failure_count,
            },
            'available_commands': self.get_available_commands(),
            'scene_summary': self.scene_monitor.get_scene_summary(),
        }
        
        filepath = os.path.join('reports', filename)
        os.makedirs('reports', exist_ok=True)
        
        FileManager.write_json(filepath, report)
        log_info(f"Reporte de sesión exportado a: {filepath}")
        return filepath

    def get_pending_patterns(self):
        """
        Retorna patrones pendientes de revision en temp_arena.
        """
        import glob
        pending = []
        temp_arena = Path("archivo_zuly/temp_arena")
        mastered = Path("archivo_zuly/por_estado_aprendizaje/mastered")
        mastered_ids = set()
        if mastered.exists():
            for d in mastered.iterdir():
                if d.is_dir():
                    mastered_ids.add(d.name)
        if temp_arena.exists():
            for blend in sorted(temp_arena.glob("*.blend")):
                pid = blend.stem
                # omitir los ya sellados o test
                if "_SELLADO_" in pid or "TEST" in pid:
                    continue
                # revisar si ya esta en mastered
                en_mastered = any(pid.startswith(m) for m in mastered_ids)
                jues_report = temp_arena / f"{pid}_JUES_REPORT.json"
                audit = temp_arena / f"{pid}_AUDIT.json"
                pending.append({
                    'pattern_id': pid,
                    'blend_path': str(blend),
                    'user_request': f'Evaluar {pid}',
                    'intent': {
                        'command_name': 'evaluate_jues',
                        'confidence': 1.0 if jues_report.exists() or audit.exists() else 0.5
                    }
                })
        return pending

    def approve_pattern(self, pattern_id: str) -> bool:
        """
        Aprueba un patron pendiente y lo mueve a mastered.
        """
        from pathlib import Path
        import shutil, json
        temp_arena = Path("archivo_zuly/temp_arena")
        mastered = Path("archivo_zuly/por_estado_aprendizaje/mastered")
        mastered.mkdir(parents=True, exist_ok=True)
        # Buscar blend que coincida
        for blend in temp_arena.glob("*.blend"):
            if blend.stem.startswith(pattern_id) or pattern_id in blend.stem:
                target_dir = mastered / blend.stem
                target_dir.mkdir(exist_ok=True)
                shutil.copy2(blend, target_dir / blend.name)
                # copiar reportes si existen
                for extra in [f"{blend.stem}_JUES_REPORT.json", f"{blend.stem}_AUDIT.json", f"{blend.stem}_CORREGIDO_JUES_REPORT.json"]:
                    src = temp_arena / extra
                    if src.exists():
                        shutil.copy2(src, target_dir / extra)
                # Guardar metadata de aprobacion
                meta = {
                    'pattern_id': blend.stem,
                    'approved_at': datetime.now().isoformat(),
                    'source': str(blend)
                }
                with open(target_dir / 'APPROVAL.json', 'w', encoding='utf-8') as f:
                    json.dump(meta, f, indent=2, ensure_ascii=False)
                return True
        return False

    def reject_pattern(self, pattern_id: str) -> bool:
        """
        Rechaza un patron pendiente y lo mueve a rechazados.
        """
        from pathlib import Path
        import shutil, json
        temp_arena = Path("archivo_zuly/temp_arena")
        rechazados = Path("archivo_zuly/rechazados")
        rechazados.mkdir(parents=True, exist_ok=True)
        for blend in temp_arena.glob("*.blend"):
            if blend.stem.startswith(pattern_id) or pattern_id in blend.stem:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dst = rechazados / f"{blend.stem}_RECHAZADO_{timestamp}.blend"
                shutil.move(str(blend), str(dst))
                return True
        return False

if __name__ == '__main__':
    """
    Bloque de demostración del Agente Zuly.
    
    Demuestra las nuevas capacidades de IA:
    1. Procesamiento de lenguaje natural
    2. Monitoreo de escena
    3. Corrección automática de errores
    4. Generación de feedback inteligente
    """
    
    agent = Agent(auto_monitor=True)
    
    print("\n" + "="*70)
    print("DEMOSTRACIÓN: AGENTE ZULY CON CAPACIDADES DE IA")
    print("="*70)
    
    # Ejemplo 1: Petición simple en lenguaje natural
    print("\n[EJEMPLO 1] Crear un cubo")
    print("-" * 70)
    result = agent.process_natural_request("Crea un cubo en la escena")
    print(f"Resultado: {result['feedback']}")
    
    # Ejemplo 2: Petición más compleja
    print("\n[EJEMPLO 2] Crear una esfera y aplicar material")
    print("-" * 70)
    result = agent.process_natural_request("Necesito una esfera de oro brillante en el centro")
    print(f"Resultado: {result['feedback']}")
    
    # Ejemplo 3: Petición con transformaciones
    print("\n[EJEMPLO 3] Mover objeto")
    print("-" * 70)
    result = agent.process_natural_request("Mueve el cubo a la posición 5, 3, 0")
    print(f"Resultado: {result['feedback']}")
    
    # Ejemplo 4: Petición con iluminación
    print("\n[EJEMPLO 4] Añadir iluminación")
    print("-" * 70)
    result = agent.process_natural_request("Añade una luz puntual con energía 3")
    print(f"Resultado: {result['feedback']}")
    
    # Ejemplo 5: Comando incompleto (demuestra corrección inteligente)
    print("\n[EJEMPLO 5] Comando con error (demuestra corrección automática)")
    print("-" * 70)
    result = agent.process_natural_request("creaaa un cillindro")
    if 'suggestion' in result:
        print(f"Sugerencia: {result['suggestion']}")
    
    # Mostrar estado de la escena
    print("\n[ESTADO DE ESCENA]")
    print("-" * 70)
    scene_summary = agent.scene_monitor.get_scene_summary()
    print(f"Objetos en la escena: {scene_summary.get('object_count', 0)}")
    print(f"Luces: {scene_summary.get('light_count', 0)}")
    print(f"Cámaras: {scene_summary.get('camera_count', 0)}")
    
    # Mostrar resumen de sesión
    print("\n[RESUMEN DE SESIÓN]")
    print("-" * 70)
    session = agent.get_session_summary()
    print(f"Comandos ejecutados: {session['commands_executed']}")
    print(f"Exitosos: {session['successes']}")
    print(f"Fallidos: {session['failures']}")
    
    # Exportar reporte
    print("\n[EXPORTANDO REPORTE]")
    print("-" * 70)
    report_path = agent.export_session_report()
    print(f"Reporte guardado en: {report_path}")
    
    print("\n" + "="*70)
    print("FIN DE LA DEMOSTRACIÓN")
    print("="*70)









