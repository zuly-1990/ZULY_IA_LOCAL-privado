# core/agent.py
"""
Agente de IA Zuly - Núcleo Inteligente (REFACTORING FASE 3)

Este archivo define la clase `Agent`, que actúa como el cerebro central del sistema.
VERSIÓN REFACTORIZADA: Delega responsabilidades a SessionManager y ExecutionEngine.

Arquitectura post-refactor:
- Agent: Facade que coordina componentes
- SessionManager: Gestión de sesión y estado
- ExecutionEngine: Ejecución de comandos
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from core.utils.logging import log_info, log_warning, log_error, log_success, log_debug
from core.config import config
from core.utils.nlu import NaturalLanguageProcessor, CommandIntent
from core.session import SessionManager
from core.execution import ExecutionEngine
from core.environment.blender_observer import BlenderObserver
from core.environment.blender_semantic_observer import BlenderSemanticObserver
from core.guard.context_guard import ContextGuard
from core.authorization.human_gate import HumanGate
from core.memory.trace_core import TraceCore
from core.security.black_protocol import BlackProtocol
from core.security.identity import is_author_verified, generate_local_key
from core.learning.pattern_memory import PatternMemory
from core.state.state_awareness import StateAwareness
from core.jues_controller import get_jues_controller

# FASE 18.5: Control de Complejidad
MAX_ACTIONS_PER_SESSION = 50


class Agent:
    """
    Agente de IA Zuly - Facade Coordinador.
    
    Alineado con el Protocolo de Identidad, el agente coordina:
    1. SessionManager - Gestión de sesión y estado
    2. ExecutionEngine - Ejecución de comandos
    3. NLU - Procesamiento de lenguaje natural
    4. Componentes de seguridad y validación
    """
    
    def __init__(self, auto_monitor: bool = True, force_mock: bool = False):
        """
        Inicializa el Agente Zuly con todas sus capacidades.
        
        FASE 3 REFACTOR: Delega a SessionManager y ExecutionEngine.
        """
        log_info("=" * 60)
        log_info("INICIALIZANDO AGENTE ZULY - VERSIÓN REFACTORIZADA FASE 3")
        log_info("=" * 60)
        
        # FASE 17: Inicializar Engine Adapter
        from core.adapters import get_engine_adapter
        self.engine_adapter = get_engine_adapter(force_mock=force_mock)
        adapter_type = "MockAdapter" if force_mock else ("BlenderAdapter" if self.engine_adapter.is_available() else "MockAdapter")
        log_info(f"[FASE 17] Engine Adapter: {adapter_type}")
        
        # Configuración base
        self.config = config
        self.auto_monitor = auto_monitor
        
        # FASE 23: IntentRouter y handlers
        from core.intents.intent_router import IntentRouter
        from core.commands.blender_command_registry import register_blender_handlers
        self.intent_router = IntentRouter()
        register_blender_handlers(self.intent_router)
        log_info(f"[FASE 23] IntentRouter: {len(self.intent_router.command_handlers)} handlers")
        
        # FASE 3 REFACTOR: NUEVOS COMPONENTES ESPECIALIZADOS
        self.session_manager = SessionManager(self.engine_adapter, auto_monitor)
        self.execution_engine = ExecutionEngine(
            intent_router=self.intent_router,
            engine_adapter=self.engine_adapter,
            session_manager=self.session_manager
        )
        log_info("[FASE 3] SessionManager y ExecutionEngine inicializados")
        
        # Observadores (inyectados en SessionManager)
        self.blender_observer = BlenderObserver(adapter=self.engine_adapter)
        self.semantic_observer = BlenderSemanticObserver()
        self.session_manager.set_observers(self.blender_observer, self.semantic_observer)
        
        # Capacidades de IA
        self.nlu = NaturalLanguageProcessor(self.intent_router.command_handlers)
        
        # Componentes de seguridad y decisión
        self.context_guard = ContextGuard()
        self.human_gate = HumanGate()
        self.trace_core = TraceCore()
        self.pattern_memory = PatternMemory()
        self.state_awareness = StateAwareness(self)
        
        # FASE 2.2: JUES Controller
        self.jues_controller = get_jues_controller()
        log_info("[FASE 2.2] JUESController integrado")
        
        # FASE 18.5: Seguridad y Observabilidad
        from core.execution.failsafe_executor import get_failsafe_executor
        from core.observability.action_logger import get_action_logger
        self.failsafe_executor = get_failsafe_executor()
        self.action_logger = get_action_logger()
        
        # Estado de sesión (delegado a SessionManager)
        self.operational_state = "Observación"
        
        # Protocolo de Identidad
        self.authorized = is_author_verified()
        if not self.authorized:
            generate_local_key()
            self.authorized = is_author_verified()
        
        # Logging de inicialización
        pattern_stats = self.pattern_memory.get_stats()
        log_info(f"[OK] NLU inicializado")
        log_info(f"[OK] SessionManager activo")
        log_info(f"[OK] ExecutionEngine listo")
        log_info(f"[OK] Memoria de Patrones: {pattern_stats['total_patterns']} patrones")
        log_info(f"[OK] Identidad: {'VERIFICADA' if self.authorized else 'PENDIENTE'}")
        
        # Registrar sesión en bitácora
        try:
            from core.persistence.session_logger import log_session_start
            log_session_start(self)
        except Exception as e:
            log_debug(f"No se pudo registrar sesión: {e}")
    
    # =========================================================================
    # MÉTODOS DELEGADOS A SessionManager (mantener API compatible)
    # =========================================================================
    
    def get_blender_snapshot(self) -> Dict[str, Any]:
        """Captura snapshot del estado de Blender."""
        return self.session_manager.get_blender_snapshot()
    
    def analyze_scene(self) -> Dict[str, Any]:
        """Analiza el estado completo de la escena."""
        return self.session_manager.analyze_scene()
    
    def compare_blender_snapshots(self, old: Dict, new: Dict) -> Dict:
        """Compara dos snapshots."""
        return self.session_manager.compare_blender_snapshots(old, new)
    
    def get_system_state(self) -> Dict[str, Any]:
        """Obtiene estado completo del sistema."""
        return self.session_manager.get_system_state()
    
    def system_report(self) -> str:
        """Genera reporte legible para humanos."""
        return self.session_manager.system_report()
    
    # =========================================================================
    # PROCESAMIENTO DE PETICIONES NATURALES
    # =========================================================================
    
    def process_natural_request(self, user_request: str, max_retries: int = 2) -> Dict[str, Any]:
        """
        Procesa una petición en lenguaje natural y ejecuta comandos.
        
        FASE 3 REFACTOR: Usa SessionManager y ExecutionEngine.
        """
        log_info(f"\n{'='*60}")
        log_info(f"🧠 PETICIÓN: {user_request}")
        log_info(f"{'='*60}")
        
        self.operational_state = "Procesando NLU"
        
        # Verificar autorización
        if not self.authorized:
            BlackProtocol.activate_lock("Acceso no autorizado")
            return {
                'success': False,
                'error': 'IDENTIDAD_NO_VERIFICADA',
                'status': 'MODO_NEGRO'
            }
        
        # Verificar interferencia de IA
        influence = self._detect_external_influence(user_request)
        if influence:
            BlackProtocol.activate_lock(influence)
            return {
                'success': False,
                'error': 'INTENTO_INFLUENCIA_IA_DETECTADO',
                'status': 'MODO_NEGRO'
            }
        
        # 1. Procesar con NLU
        intents = self.nlu.process(user_request)
        if not intents:
            return {
                'success': False,
                'error': 'No se pudieron interpretar intenciones',
                'suggestions': self._get_suggestions(user_request)
            }
        
        best_intent = intents[0]
        log_info(f"Intención: {best_intent.command_name} ({best_intent.confidence:.0%})")
        
        # 2. Evaluar contexto y autorización
        self.operational_state = "Evaluación"
        current_context = self.analyze_scene().get("context", {})
        
        guard_result = self.context_guard.evaluate(best_intent.command_name, current_context)
        auth_result = self.human_gate.authorize(best_intent.command_name)
        
        if not auth_result.get('authorized', False):
            self.session_manager.register_blocked_attempt("Usuario", "Bloqueo por autorización")
            return {
                'success': False,
                'error': 'BLOQUEO_SEGURIDAD',
                'reason': auth_result.get('reason', 'Autorización denegada')
            }
        
        if guard_result.get('blocked', False):
            self.session_manager.register_blocked_attempt("Usuario", "Bloqueo por contexto")
            return {
                'success': False,
                'error': 'CONTEXTO_BLOQUEADO',
                'reason': guard_result.get('reason', 'Contexto no válido')
            }
        
        # 3. Ejecutar vía ExecutionEngine
        self.operational_state = "Ejecución"
        
        for attempt in range(1, max_retries + 1):
            result = self.execution_engine.execute_intent(best_intent, attempt, max_retries)
            
            if result.get('success'):
                # Éxito: registrar y retornar
                if best_intent.confidence > 0.85:
                    self.session_manager.register_learned_decision(best_intent, result)
                
                self.operational_state = "Completado"
                
                if self.auto_monitor:
                    self.analyze_scene()
                
                return {
                    'success': True,
                    'command': best_intent.command_name,
                    'result': result.get('result'),
                    'confidence': best_intent.confidence,
                    'attempt': attempt
                }
            
            # Fallo: intentar corrección
            if attempt < max_retries:
                corrected = self.execution_engine.attempt_correction(best_intent, result)
                if corrected:
                    log_info(f"🔄 Reintento con corrección: {corrected.command_name}")
                    best_intent = corrected
        
        # Fallo definitivo
        self.operational_state = "Fallo"
        return {
            'success': False,
            'error': result.get('error', 'Error desconocido'),
            'command': best_intent.command_name,
            'attempts': max_retries
        }
    
    def _detect_external_influence(self, text: str) -> Optional[str]:
        """Detecta intentos de influencia externa en el texto."""
        suspicious = [
            "olvida", "ignora", "no importa", "override", "bypass",
            "desactiva protocolo", "desactiva seguridad", "modo admin"
        ]
        for term in suspicious:
            if term in text.lower():
                return f"Término sospechoso: '{term}'"
        return None
    
    def _get_suggestions(self, user_request: str) -> List[str]:
        """Genera sugerencias para comandos no reconocidos."""
        return self.nlu.get_command_suggestions(user_request)[:3]
    
    # =========================================================================
    # MÉTODOS LEGACY (para compatibilidad)
    # =========================================================================
    
    @property
    def context(self):
        """Propiedad legacy para acceder al ExecutionContext."""
        return self.session_manager.execution_context
    
    def execute_via_router(self, handler_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Método legacy - delega a ExecutionEngine."""
        return self.execution_engine.execute_via_router(handler_name, parameters)
