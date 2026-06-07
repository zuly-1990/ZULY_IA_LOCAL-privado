"""
lyzu_core.py
============

LYZU Core 1.0 - Núcleo del Agente Autónomo Inteligente

Este es el puente entre ZULY 4.0 y LYZU 1.0. Aquí comienza la evolución
hacia un sistema verdaderamente inteligente y semi-autónomo.

Características:
- Memoria a corto plazo (sesión)
- Contexto conversacional
- Auto-expansión de comandos
- Bitácora contextual
- Integración con Gemini
- Modo híbrido (Humano-en-el-Loop)

Arquitectura:
    Usuario
      ↓
    LYZU Core (este archivo)
      ↓
   Intención Classification
      ↓
   Entity Extraction
      ↓
   Command Execution (Blender / External)
      ↓
    Feedback Loop
      ↓
    Contexto Actualizado
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from pathlib import Path
from core.config import config  # Importamos la instancia de configuración global
from core.intents import EntityExtractor, IntentManager, IntentRouter
from core.utils.logging import log_success, log_warning, log_info
from core.dialog import DialogManager, DialogDecision
from core.stability.safe_guard import SafeGuard, SafeGuardDecision
from core.learning import LearningFreedomEngine
from core.knowledge import KnowledgeGraph
from core.learning.self_assessment import SelfAssessmentEngine
from core.learning.strategy_synthesizer import StrategySynthesizer, SynthesisMethod
from core.cognition import C1ResultEvaluator  # NUEVO: C1 - Evaluador de Resultados
from core.cognition.c2_pattern_storage import PatternStorageV2  # WO-002: Nuevo Almacenamiento Firmado
from core.cognition.c3_abstract_objectives import C3AbstractObjectives  # NUEVO: C3 - Objetivos Abstractos
from core.cognition.c4_auto_tuning_procedural import C4AutoTuningProcedural  # NUEVO: C4 - Auto-tuning


@dataclass
class ConversationTurn:
    """Representa un turno en la conversación."""
    timestamp: str
    user_input: str
    intent: str
    entities: Dict[str, Any]
    command_executed: str
    result: str
    confidence: float


@dataclass
class ContextualMemory:
    """Memoria contextual de la sesión con límite de turnos."""
    session_id: str
    creation_time: str
    turns: List[ConversationTurn] = field(default_factory=list)
    scene_state: Dict = field(default_factory=dict)
    user_preferences: Dict = field(default_factory=dict)
    learned_patterns: List[str] = field(default_factory=list)
    max_turns: int = 500  # Límite de turnos en memoria
    archived_turns_count: int = 0  # Contador de turnos archivados
    
    def add_turn(self, turn: ConversationTurn) -> None:
        """Agrega un turno a la memoria con límite."""
        self.turns.append(turn)
        
        # Si excede el límite, archiva el más viejo
        if len(self.turns) > self.max_turns:
            archived_turn = self.turns.pop(0)
            self.archived_turns_count += 1
            self._save_archived_turn(archived_turn)
            log_info(f"Turno archivado. Total archivados: {self.archived_turns_count}")
    
    def _save_archived_turn(self, turn: ConversationTurn) -> None:
        """Guarda un turno archivado en archivo."""
        try:
            archive_dir = Path('bitacora/archive')
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            # Nombre del archivo basado en timestamp
            timestamp_clean = turn.timestamp.replace(':', '-').replace('.', '-')
            archive_file = archive_dir / f"turn_{timestamp_clean}.json"
            
            with open(archive_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(turn), f, indent=2)
        except Exception as e:
            log_warning(f"Error archivando turno: {e}")
    
    def get_last_n_turns(self, n: int) -> List[ConversationTurn]:
        """Obtiene los últimas n turnos."""
        return self.turns[-n:] if len(self.turns) >= n else self.turns
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de memoria."""
        total_turns = len(self.turns) + self.archived_turns_count
        return {
            'turns_in_memory': len(self.turns),
            'max_turns': self.max_turns,
            'archived_turns': self.archived_turns_count,
            'total_turns_processed': total_turns,
            'memory_usage_pct': (len(self.turns) / self.max_turns) * 100
        }
    
    def to_json(self) -> str:
        """Serializa la memoria a JSON."""
        data = {
            'session_id': self.session_id,
            'creation_time': self.creation_time,
            'turns': [asdict(turn) for turn in self.turns],
            'scene_state': self.scene_state,
            'user_preferences': self.user_preferences,
            'learned_patterns': self.learned_patterns,
            'stats': self.get_memory_stats()
        }
        return json.dumps(data, indent=2)


def _entities_to_dict(entities: Dict[str, Any]) -> Dict[str, Any]:
    """Convierte un diccionario de entidades (con objetos Entity) a dict de valores planos."""
    result = {}
    for key, value in entities.items():
        if hasattr(value, 'value'):  # Es un objeto Entity
            result[key] = value.value
        elif isinstance(value, dict) and 'value' in value:  # Ya es un dict con value
            result[key] = value['value']
        else:
            result[key] = value
    return result


class LYZUCore:
    """
    Núcleo inteligente de LYZU.
    
    Actúa como mediador entre:
    1. Órdenes del usuario
    2. Intenciones (clasificadas)
    3. Comandos ejecutables
    4. Feedback del sistema
    
    Mantiene contexto conversacional y aprende patrones.
    """
    
    def __init__(self, mode: str = 'hybrid', enable_learning_freedom: bool = True, enable_cognition: bool = True):
        """
        Inicializa LYZU Core.
        
        Args:
            mode: 'reactive' (solo ejecuta), 'hybrid' (Humano-en-loop),
                  'autonomous' (autónomo, requiere validación)
            enable_learning_freedom: Si True, activa Libertad de Aprendizaje
            enable_cognition: Si True, activa C1/C2 - Cognición Base (Plan C)
        """
        self.mode = mode
        self.version = "3.0"
        self.is_simulation = False  # PROTECCION: Bandera para evitar memorias falsas
        
        # Componentes de IA
        self.entity_extractor = EntityExtractor()
        self.intent_manager = IntentManager()
        self.intent_router = IntentRouter()
        self.dialog_manager = DialogManager()
        self.safe_guard = SafeGuard()
        
        # NUEVO: C1 - Evaluador de Resultados (Plan C: Cognición Base)
        self.cognition_enabled = enable_cognition
        if enable_cognition:
            try:
                self.evaluator = C1ResultEvaluator()
                log_success("C1 - Evaluador de Resultados activado (Plan C)")
            except Exception as e:
                log_warning(f"Error inicializando C1: {e}. Continuando sin evaluación.")
                self.evaluator = None
        else:
            self.evaluator = None
        
        # WO-002: Memoria de Experiencias con Firma del Autor
        if enable_cognition:
            try:
                self.memory_system = PatternStorageV2()
                log_success("C2 - Memoria de Experiencias activado (Plan C)")
            except Exception as e:
                log_warning(f"Error inicializando C2: {e}. Continuando sin memoria aprendida.")
                self.memory_system = None
        else:
            self.memory_system = None
        
        # NUEVO: C3 - Objetivos Abstractos (Plan C: Cognición Base)
        if enable_cognition:
            try:
                self.objectives_system = C3AbstractObjectives()
                log_success("C3 - Objetivos Abstractos activado (Plan C)")
            except Exception as e:
                log_warning(f"Error inicializando C3: {e}. Continuando sin descomposición.")
                self.objectives_system = None
        else:
            self.objectives_system = None
        
        # NUEVO: C4 - Auto-tuning Procedural (Plan C: Cognición Base)
        if enable_cognition:
            try:
                self.auto_tuning_system = C4AutoTuningProcedural()
                log_success("C4 - Auto-tuning Procedural activado (Plan C)")
            except Exception as e:
                log_warning(f"Error inicializando C4: {e}. Continuando sin auto-tuning.")
                self.auto_tuning_system = None
        else:
            self.auto_tuning_system = None
        
        # Registrar handlers de Blender
        self._register_command_handlers()
        
        # VERIFICACION DE DIAGNOSTICO
        self._verify_handlers_status()
        
        # Memoria contextual
        self.memory = ContextualMemory(
            session_id=self._generate_session_id(),
            creation_time=datetime.now().isoformat()
        )
        
        # NUEVA: Libertad de Aprendizaje (Módulos de Learning Freedom)
        self.learning_freedom_enabled = enable_learning_freedom
        if enable_learning_freedom:
            # Usamos el límite configurado en config.py
            self.learning_engine = LearningFreedomEngine(
                max_strategies=config.MAX_AUTONOMOUS_ITERATIONS, 
                verbose=True,
                max_history=100  # Límite de memoria para experimentos
            )
            self.knowledge_graph = KnowledgeGraph()
            self.self_assessment = SelfAssessmentEngine(verbose=True)
            self.strategy_synthesizer = StrategySynthesizer(verbose=True)
            log_success("Learning Freedom Framework activado")
        else:
            self.learning_engine = None
            self.knowledge_graph = None
            self.self_assessment = None
            self.strategy_synthesizer = None
        
        # Configuración
        self.confidence_threshold = 0.5
        self.auto_execute = mode != 'hybrid'
        
        log_success(f"LYZU Core {self.version} initialized in {mode} mode (Learning Freedom: {'ON' if enable_learning_freedom else 'OFF'}, Cognition: {'ON' if enable_cognition else 'OFF'})")
    
    def _register_command_handlers(self) -> None:
        """Registra todos los handlers de Blender disponibles."""
        try:
            from core.commands.blender_command_registry import register_blender_handlers
            register_blender_handlers(self.intent_router)
        except ImportError as e:
            log_warning(f"Could not import blender handlers: {e}")
            # Intento de deteccion de entorno
            self._register_mock_handlers()
        except Exception as e:
            log_warning(f"Error registering handlers: {e}")
            log_warning(f"Error critico registrando handlers: {e}")

    def _register_mock_handlers(self) -> None:
        """Registra handlers falsos para desarrollo fuera de Blender."""
        mock_commands = [
            'blender.create_primitive', 'blender.render_scene', 
            'blender.transform', 'blender.material'
        ]
        
        def create_mock_handler(cmd_name):
            def handler(params):
                return {
                    'status': 'success', 
                    'output': f'[SIMULACION - NO REAL] {cmd_name} validado. Geometría no creada.',
                    'simulation': True
                }
            return handler

        for cmd in mock_commands:
            self.intent_router.register_handler(cmd, create_mock_handler(cmd))
        
        log_info(f"  + {len(mock_commands)} handlers simulados registrados.")

    def _verify_handlers_status(self):
        """Diagnostico de handlers registrados."""
        count = len(self.intent_router.handlers) if hasattr(self.intent_router, 'handlers') else 0
        if count == 0:
            log_warning("ALERTA: No hay comandos registrados. El agente no podra ejecutar acciones.")
        else:
            log_info(f"Estado del Sistema: {count} comandos listos para ejecutar.")
    
    def process_user_input(self, user_input: str, auto_approve: bool = False) -> Dict[str, Any]:
        """
        Procesa una orden del usuario.
        
        Pipeline:
        1. Extrae entidades
        2. Clasifica intención
        3. Valida parámetros
        4. Prepara comando
        5. Ejecuta (según modo)
        
        Args:
            user_input: Orden en lenguaje natural
            auto_approve: Si True, ejecuta sin confirmación (solo en modo hybrid)
            
        Returns:
            Resultado de la operación
        """
        start_time = time.time()
        
        # 1. Extraer entidades
        entities = self.entity_extractor.extract(user_input)
        is_valid, errors = self.entity_extractor.validate_entities(entities)
        
        if not is_valid:
            log_warning(f"Entity validation errors: {errors}")
        
        # 2. Clasificar intención
        intent = self.intent_manager.classify(user_input, entities)
        
        # --- NUEVO FILTRO: DIALOG (FASE 1) ---
        decision, message, metadata = self.dialog_manager.validate_intent(intent, context={'mode': self.mode})
        
        if decision == DialogDecision.REJECT:
            return {
                'success': False,
                'error': 'Dialog Rejection',
                'message': message,
                'details': metadata,
                'execution_time_ms': (time.time() - start_time) * 1000
            }
        
        if decision == DialogDecision.CLARIFY:
            return {
                'success': False,
                'pending_clarification': True,
                'message': message,
                'details': metadata,
                'execution_time_ms': (time.time() - start_time) * 1000
            }

        # --- NUEVO FILTRO: SAFEGUARD (FASE 4) ---
        sg_decision, sg_message, sg_metadata = self.safe_guard.verify(intent, context={'mode': self.mode})
        
        if sg_decision == SafeGuardDecision.BLOCKED:
            return {
                'success': False,
                'error': 'SafeGuard Bloqueo',
                'message': sg_message,
                'details': sg_metadata,
                'execution_time_ms': (time.time() - start_time) * 1000
            }
        
        if sg_decision == SafeGuardDecision.CONFIRM:
            return {
                'success': False,
                'pending_confirmation': True,
                'message': sg_message,
                'details': sg_metadata,
                'intent': intent.name,
                'command': intent.command,
                'parameters': _entities_to_dict(entities),
                'execution_time_ms': (time.time() - start_time) * 1000
            }

        # Continúa el flujo original si todo es aprobado
        log_info(f"Filtros superados. Procediendo a ejecución: {intent.name}")

        # 3. Validar parámetros (Mantenido por compatibilidad legacy)
        command_ready, validation_errors = self._validate_command_parameters(intent, entities)
        if not command_ready:
            return {
                'success': False,
                'error': 'Invalid parameters',
                'details': validation_errors,
                'execution_time_ms': (time.time() - start_time) * 1000
            }
        
        # Convertir entidades a dict serializable
        entities_dict = _entities_to_dict(entities)
        
        # 4. Preparar comando
        command_dict = {
            'command': intent.command,
            'name': intent.name,
            'parameters': entities_dict
        }
        
        # 5. Ejecutar (según modo)
        if self.mode == 'reactive' or auto_approve:
            result = self.intent_router.route_and_execute(command_dict, entities_dict)
            execution_result = {
                'success': result.status.value == 'success',
                'output': result.output,
                'error': result.error,
                'attempts': result.attempts,
                'execution_time_ms': (time.time() - start_time) * 1000,
                'intent': intent.name,
                'confidence': intent.confidence
            }
            
            # NUEVO: C1 - Evaluar resultado si está habilitado
            if self.evaluator and not self.is_simulation and result.status.value == 'success':
                try:
                    scene_data = self._get_current_scene_state()
                    evaluation = self.evaluator.evaluate(
                        objective=user_input,
                        scene_data=scene_data
                    )
                    # Agregar evaluación al resultado
                    execution_result['evaluation'] = {
                        'status': evaluation.status.value,
                        'score': round(evaluation.diagnostic.score_overall, 3),
                        'summary': evaluation.diagnostic.summary,
                        'metrics_passed': evaluation.diagnostic.metrics_passed,
                        'metrics_total': evaluation.diagnostic.metrics_total,
                        'strengths': evaluation.diagnostic.strengths,
                        'issues': evaluation.diagnostic.issues,
                        'recommendations': evaluation.diagnostic.recommendations[:3]  # Top 3
                    }
                    log_info(f"C1 Evaluación (Score: {execution_result['evaluation']['score']}): {evaluation.diagnostic.summary}")

                    # WO-002: El guardado en C2 ya NO es automático.
                    # El sistema marca el resultado como 'PENDIENTE_DE_FIRMA'.
                    execution_result['pending_author_signature'] = True
                    log_info("Esperando firma del autor para persistir en C2...")
                except Exception as e:
                    log_warning(f"Error en evaluación C1: {e}")
                    # No romper el flujo, solo registrar warning
            
            # Registro automático solo si fue exitosa
            if result.status.value == 'success':
                # La función registrar_aprendizaje no está definida en este contexto.
                # El sistema C2 (Memoria de Experiencias) ya se encarga de registrar el aprendizaje arriba.
                # Se omite para evitar NameError.
                pass
        else:  # hybrid mode
            execution_result = {
                'success': None,  # Pendiente de aprobación
                'pending_approval': True,
                'command': command_dict,
                'intent': intent.name,
                'confidence': intent.confidence,
                'description': self.intent_manager.get_intent_description(intent.name),
                'execution_time_ms': (time.time() - start_time) * 1000
            }
        
        # 6. Registrar en memoria
        turn = ConversationTurn(
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            intent=intent.name,
            entities=entities_dict,
            command_executed=command_dict['command'],
            result=json.dumps(execution_result),
            confidence=intent.confidence
        )
        self.memory.add_turn(turn)
        
        return execution_result
    
    def approve_and_execute(self, command_dict: Dict, entities: Dict) -> Dict[str, Any]:
        """
        Aprueba y ejecuta un comando pendiente (modo hybrid).
        
        Args:
            command_dict: Comando a ejecutar
            entities: Entidades del comando
            
        Returns:
            Resultado de la ejecución
        """
        if self.mode != 'hybrid':
            return {'success': False, 'error': 'approve_and_execute only works in hybrid mode'}
        
        result = self.intent_router.route_and_execute(command_dict, entities)
        return {
            'success': result.status.value == 'success',
            'output': result.output,
            'error': result.error,
            'attempts': result.attempts
        }
    
    def process_with_learning_freedom(self, user_request: str) -> Dict[str, Any]:
        """
        Procesa una solicitud usando Libertad de Aprendizaje.
        
        Pipeline:
        1. Genera 5 estrategias alternativas
        2. Ejecuta todas en paralelo
        3. Auto-selecciona la mejor
        4. Aprende del resultado
        
        Args:
            user_request: Solicitud del usuario
            
        Returns:
            Resultado con ganador seleccionado
        """
        if not self.learning_freedom_enabled:
            log_warning("Learning Freedom no está activado")
            return {'success': False, 'error': 'Learning Freedom not enabled'}
            
        # 0. VERIFICACIÓN DE SEGURIDAD (PRESUPUESTO)
        if not self._check_daily_budget():
            log_warning(f"Límite de presupuesto diario (${config.MAX_DAILY_BUDGET_USD}) alcanzado.")
            return {
                'success': False, 
                'error': f'Daily budget limit (${config.MAX_DAILY_BUDGET_USD}) reached. Safety break activated.'
            }
        
        start_time = time.time()
        
        # 1. Extraer intención base
        entities = self.entity_extractor.extract(user_request)
        intent = self.intent_manager.classify(user_request, entities)
        
        log_info(f"[LF] Procesando: {user_request}")
        log_info(f"[LF] Intención detectada: {intent.name} ({intent.confidence:.1%})")
        
        # 2. Generar estrategias alternativas
        strategies = self.learning_engine.generate_strategies(
            user_prompt=user_request,
            intent=intent.name,
            entities=_entities_to_dict(entities)
        )
        
        log_info(f"[LF] Generadas {len(strategies)} estrategias alternativas")
        
        # 3. Ejecutar todas las estrategias
        results = self.learning_engine.execute_strategies(
            strategies=strategies,
            intent_router=self.intent_router
        )
        
        log_info(f"[LF] Ejecutadas {len(results)} estrategias")
        
        # Actualizar costo estimado (N estrategias * costo por visión)
        # Asumimos que cada estrategia ejecutada requirió una validación visual
        estimated_cost = len(strategies) * config.COST_PER_VISION_CALL
        self._update_daily_cost(estimated_cost)
        
        # 4. Encontrar mejor resultado
        execution_time_total = time.time() - start_time
        
        best_result = None
        best_score = -1
        
        for i, result in enumerate(results):
            score = result.overall_score if hasattr(result, 'overall_score') else result.get('overall_score', 0)
            
            log_info(f"[LF] Strategy {i+1}: score={score:.1f} success={result.success if hasattr(result, 'success') else result.get('success')}")
            
            if score > best_score:
                best_score = score
                best_result = result
        
        # 5. Registrar en Knowledge Graph
        if best_result:
            if not self.is_simulation:  # PROTECCION: Solo guardar si es REAL
                strategy_name = best_result.strategy.strategy_type if hasattr(best_result, 'strategy') else 'UNKNOWN'
                self.knowledge_graph.add_object(
                    name=f"LF_Result_{strategy_name}",
                    object_type='STRATEGY_RESULT',
                    properties={
                        'user_request': user_request,
                        'strategy': strategy_name,
                        'score': best_score,
                        'timestamp': datetime.now().isoformat()
                    }
                )
        elif self.is_simulation:
            log_info("[SEGURIDAD] Modo Simulación: Resultado NO guardado en memoria permanente para evitar corrupción.")
        
        # 6. Aprender del resultado
        if best_result and best_result in results:
            if not self.is_simulation:  # PROTECCION
                self.learning_engine.learn_from_experiment(
                    strategies=strategies,
                    winner_index=results.index(best_result)
                )
        
        strategy_name = best_result.strategy.strategy_type if (best_result and hasattr(best_result, 'strategy')) else 'NONE'
        log_success(f"[LF] Ganador: {strategy_name} (score: {best_score:.1f})")
        
        return {
            'success': True,
            'winner': best_result.to_dict() if (best_result and hasattr(best_result, 'to_dict')) else {'error': 'No result'},
            'all_strategies': len(strategies),
            'best_score': best_score,
            'estimated_cost': estimated_cost,
            'execution_time_ms': execution_time_total * 1000,
            'assessment': {
                'score': best_score,
                'strategy_type': strategy_name
            }
        }
    
    def _validate_command_parameters(self, intent: Any, entities: Dict) -> Tuple[bool, List[str]]:
        """Valida que los parámetros sean apropiados para el comando."""
        errors = []
        
        # Obtener nombre de la intención (puede ser dataclass o dict)
        intent_name = intent.name if hasattr(intent, 'name') else intent.get('name')
        
        # Validar entidades según intención
        if intent_name == 'crear_objeto':
            if 'objeto' not in entities:
                errors.append("objeto_requerido")
        
        elif intent_name == 'mover_objeto':
            if 'posicion' not in entities:
                errors.append("posicion_requerida")
        
        return len(errors) == 0, errors
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Obtiene resumen del contexto actual."""
        last_turns = self.memory.get_last_n_turns(5)
        
        return {
            'session_id': self.memory.session_id,
            'mode': self.mode,
            'turns_count': len(self.memory.turns),
            'last_turns': [
                {
                    'timestamp': t.timestamp,
                    'intent': t.intent,
                    'confidence': t.confidence,
                    'success': 'success' in t.result
                }
                for t in last_turns
            ],
            'scene_state': self.memory.scene_state
        }
    
    def save_session(self, filepath: str = None) -> str:
        """
        Guarda la sesión actual.
        
        Args:
            filepath: Ruta donde guardar (opcional)
            
        Returns:
            Ruta del archivo guardado
        """
        if filepath is None:
            filepath = f"bitacora/session_{self.memory.session_id}.json"
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.memory.to_json())
        
        log_info(f"Session saved to {filepath}")
        return filepath
    
    def _generate_session_id(self) -> str:
        """Genera un ID único para la sesión."""
        return f"session_{int(time.time() * 1000)}"
    
    def list_commands(self) -> Dict[str, str]:
        """Lista todos los comandos disponibles."""
        return self.intent_manager.list_intents()

    # ============================================================================
    # Métodos de Seguridad y Presupuesto
    # ============================================================================
    
    def _get_budget_file(self) -> Path:
        return Path(config.BUDGET_TRACKER_FILE)

    def _check_daily_budget(self) -> bool:
        """Verifica si aún tenemos presupuesto para hoy."""
        try:
            file_path = self._get_budget_file()
            if not file_path.exists():
                return True
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            today = datetime.now().strftime("%Y-%m-%d")
            # Si es un nuevo día, reseteamos (asumimos True)
            if data.get('date') != today:
                return True
            
            return data.get('spent', 0.0) < config.MAX_DAILY_BUDGET_USD
        except Exception as e:
            log_warning(f"Error checking budget: {e}")
            return True # En caso de error de lectura, permitimos continuar (fail-open)

    def _update_daily_cost(self, amount: float) -> None:
        """Registra el gasto estimado."""
        try:
            file_path = self._get_budget_file()
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            if file_path.exists():
                with open(file_path, 'r') as f:
                    existing = json.load(f)
                    if existing.get('date') == today:
                        data = existing
            
            data['spent'] += amount
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            log_warning(f"Error updating budget: {e}")
    
    # ========================================================================
    # NUEVO: Integración con C1 - Evaluador de Resultados (Plan C)
    # ========================================================================
    
    def _get_current_scene_state(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual de la escena.
        
        Returns:
            Diccionario con estado de la escena (objetos, materiales, etc)
        """
        # Intenta obtener del adapter real si está disponible
        try:
            if hasattr(self, 'adapter') and self.adapter:
                # Si existe adapter real (BlenderAdapter)
                return self.adapter.get_scene_summary()
        except:
            pass
        
        # Fallback: retorna memoria de escena o mock
        return self.memory.scene_state if self.memory.scene_state else {
            'object_count': 0,
            'materials': [],
            'total_volume': 0.0
        }
    
    def execute_with_evaluation(self, user_input: str, 
                               auto_approve: bool = True) -> Dict[str, Any]:
        """
        Ejecuta un comando y lo evalúa con C1.
        
        NUEVO (Integración Plan C):
        Este método garantiza que C1 evaluará el resultado.
        
        Args:
            user_input: Orden del usuario
            auto_approve: Si True, ejecuta sin esperar aprobación
            
        Returns:
            Resultado con evaluación incluida (si C1 está habilitado)
        """
        result = self.process_user_input(user_input, auto_approve)
        # Ya incluye evaluación si self.evaluator existe (vea process_user_input)
        return result
    
    def get_evaluation_summary(self) -> Optional[Dict[str, Any]]:
        """
        Retorna resumen de evaluaciones realizadas.
        
        Returns:
            Resumen de historial de C1, o None si C1 no está habilitado
        """
        if not self.evaluator:
            return None
        
        return self.evaluator.get_history_summary()
    
    # ========== NUEVOS MÉTODOS PARA C2 ==========
    
    def get_memory_insights(self, limit_days: int = 7) -> Optional[Dict[str, Any]]:
        """
        Obtiene insights de la memoria de experiencias (C2).
        
        Args:
            limit_days: Período a analizar
            
        Returns:
            Diccionario con insights, o None si C2 no está habilitado
        """
        if not self.memory_system:
            return None
        
        return self.memory_system.get_insights(limit_days)
    
    def get_suggestions_for_objective(self, objective: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene sugerencias basadas en experiencias previas (C2).
        
        Args:
            objective: Objetivo para el cual se quieren sugerencias
            
        Returns:
            Diccionario con sugerencias, o None si C2 no está habilitado
        """
        if not self.memory_system:
            return None
        
        return self.memory_system.get_suggestions_for(objective)
    
    def export_memory(self, filepath: str) -> bool:
        """
        Exporta memoria de experiencias a JSON (C2).
        
        Args:
            filepath: Ruta del archivo a exportar
            
        Returns:
            True si se exportó exitosamente
        """
        if not self.memory_system:
            return False
        
        return self.memory_system.export_memory(Path(filepath))
    
    # ========== NUEVOS MÉTODOS PARA C3 ==========
    
    def decompose_objective(self, objective: str, context: Optional[Dict[str, Any]] = None):
        """
        Descompone un objetivo complejo en subtareas (C3).
        
        Args:
            objective: Objetivo a descomponer
            context: Contexto adicional
            
        Returns:
            ExecutionPlan con tareas descompuestas, o None si C3 no está habilitado
        """
        if not self.objectives_system:
            return None
        
        return self.objectives_system.decompose_objective(objective, context)
    
    def get_next_tasks_for_plan(self, plan, completed_ids: List[str]):
        """
        Obtiene siguientes tareas a ejecutar (C3).
        
        Args:
            plan: ExecutionPlan de C3
            completed_ids: IDs de tareas ya completadas
            
        Returns:
            Lista de tareas listas para ejecutar, o None si C3 no está habilitado
        """
        if not self.objectives_system:
            return None
        
        return self.objectives_system.get_next_tasks(plan, completed_ids)
    
    def export_plan(self, plan, filepath: str) -> bool:
        """
        Exporta plan de objetivos a JSON (C3).
        
        Args:
            plan: ExecutionPlan de C3
            filepath: Ruta del archivo
            
        Returns:
            True si se exportó exitosamente
        """
        if not self.objectives_system:
            return False
        
        return self.objectives_system.export_plan(plan, Path(filepath))
    
    # ========================================================================
    # Métodos C4 - Auto-tuning Procedural
    # ========================================================================
    
    def optimize_parameter(self, objective: str, procedure, param_bounds: Dict,
                          initial_value=None, c1_evaluator=None, c2_memory=None,
                          strategy=None, target_score: float = 0.95,
                          max_iterations: int = 50, no_improvement_limit: int = 5):
        """
        Ejecuta ciclo de optimización automática de parámetros
        
        Args:
            objective: Nombre del objetivo a optimizar
            procedure: Función que ejecuta el procedimiento (param) -> result
            param_bounds: Dict {name: ParameterBound}
            initial_value: Valor inicial (si None, usa centro del rango)
            c1_evaluator: Evaluador C1 opcional
            c2_memory: Memoria C2 opcional
            strategy: Estrategia de optimización
            target_score: Score objetivo (0-1)
            max_iterations: Máximo de iteraciones
            no_improvement_limit: Paradas sin mejora
            
        Returns:
            OptimizationResult con resultado final
        """
        if not self.auto_tuning_system:
            return None
        
        # Usar estrategia por defecto si no se especifica
        if strategy is None:
            from core.cognition.c4_auto_tuning_procedural import OptimizationStrategy
            strategy = OptimizationStrategy.HILL_CLIMBING
        
        return self.auto_tuning_system.optimize(
            objective=objective,
            procedure=procedure,
            param_bounds=param_bounds,
            initial_value=initial_value,
            c1_evaluator=c1_evaluator,
            c2_memory=c2_memory,
            strategy=strategy,
            target_score=target_score,
            max_iterations=max_iterations,
            no_improvement_limit=no_improvement_limit
        )
    
    def export_optimization(self, result, filepath: str) -> bool:
        """
        Exporta resultado de optimización a JSON
        
        Args:
            result: OptimizationResult
            filepath: Ruta del archivo
            
        Returns:
            bool: True si éxito
        """
        if not self.auto_tuning_system or result is None:
            return False
        
        return self.auto_tuning_system.export_result(result, filepath)
    
    def get_optimization_summary(self, result) -> Optional[Dict]:
        """
        Genera resumen de resultado de optimización
        
        Args:
            result: OptimizationResult
            
        Returns:
            Dict con estadísticas
        """
        if not self.auto_tuning_system or result is None:
            return None
        
        return self.auto_tuning_system.get_summary(result)

def demo_lyzu_interactive():
    """Demo interactiva de LYZU Core en modo hybrid."""
    print("\n" + "="*70)
    print("LYZU Core 1.0 - Demostración Interactiva (Modo Hybrid)")
    print("="*70)
    print("\nComandos de ejemplo:")
    print("  - 'Crea un cubo'")
    print("  - 'Crea una esfera roja'")
    print("  - 'Mueve el cubo a 5,10,15'")
    print("  - 'Renderiza la escena'")
    print("  - 'Salir' para terminar")
    print("-" * 70 + "\n")
    
    lyzu = LYZUCore(mode='hybrid')
    
    while True:
        user_input = input("👤 You: ").strip()
        
        if user_input.lower() in ['exit', 'salir', 'quit']:
            print("\n✅ Sesión guardada.")
            lyzu.save_session()
            break
        
        if not user_input:
            continue
        
        # Procesar entrada
        result = lyzu.process_user_input(user_input)
        
        if result.get('pending_approval'):
            print(f"\n🤖 LYZU (Pending Approval):")
            print(f"   Intent: {result['intent']}")
            print(f"   Confidence: {result['confidence']:.1%}")
            print(f"   Description: {result['description']}")
            print(f"   Command: {result['command']['command']}")
            
            approval = input("\n   ✅ Approve? (yes/no): ").strip().lower()
            if approval in ['yes', 'y', 'si', 'sí']:
                exec_result = lyzu.approve_and_execute(
                    result['command'],
                    result.get('entities', {})
                )
                print(f"\n✅ Executed: {exec_result}")
            else:
                print("CANCELADO")
        else:
            print(f"\n🤖 LYZU:")
            if result['success']:
                print(f"   ✅ Success: {result.get('output')}")
            else:
                print(f"   ERROR: {result.get('error')}")
        
        print(f"   ⏱️  {result['execution_time_ms']:.0f}ms\n")


if __name__ == '__main__':
    demo_lyzu_interactive()
