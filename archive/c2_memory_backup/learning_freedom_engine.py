"""
learning_freedom_engine.py
=========================

MOTOR DE LIBERTAD DE APRENDIZAJE

LYZU experimenta libremente, genera múltiples estrategias,
evalúa resultados y aprende cuál es mejor.
SIN validación del usuario para decisiones inteligentes.

Filosofía:
  - Usuario dice "algo lindo"
  - LYZU genera 5 estrategias diferentes
  - LYZU ejecuta todas en paralelo
  - LYZU compara resultados (score 0-100)
  - LYZU elige la MEJOR automáticamente
  - Usuario ve: resultado espectacular
  - LYZU aprende: qué estrategia funcionó mejor

Características:
- Experimentación paralela
- Scoring automático de resultados
- Persistencia de patrones de éxito
- Cross-breeding de estrategias ganadoras
- Constraint enforcement (límites de tiempo/recursos)
"""

import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from pathlib import Path
from enum import Enum


class StrategyType(Enum):
    """Tipos de estrategias que LYZU puede generar"""
    PRIMITIVE = "primitive"              # Crear un objeto simple
    COMPOSITION = "composition"          # Múltiples objetos
    TRANSFORMATION = "transformation"    # Modificar objeto existente
    MATERIAL_DECORATION = "material"     # Aplicar materiales/texturas
    LIGHTING = "lighting"                # Agregar/modificar luces
    CAMERA = "camera"                    # Posicionar cámara
    HYBRID = "hybrid"                    # Combinación compleja


@dataclass
class HandlerCall:
    """Representa una llamada a un handler"""
    handler_name: str
    parameters: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return {
            'handler': self.handler_name,
            'params': self.parameters
        }


@dataclass
class Strategy:
    """Una estrategia es una secuencia de handlers"""
    id: str
    strategy_type: StrategyType
    handlers: List[HandlerCall]
    description: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'type': self.strategy_type.value,
            'handlers': [h.to_dict() for h in self.handlers],
            'description': self.description,
            'created_at': self.created_at
        }


@dataclass
class ScenarioResult:
    """Resultado de ejecutar una estrategia"""
    strategy: Strategy
    success: bool
    output: Any
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    objects_created: int = 0
    
    # Scores de evaluación
    aesthetic_score: float = 0.0      # 0-100: Qué tan bonito
    complexity_score: float = 0.0     # 0-100: Qué tan complejo
    novelty_score: float = 0.0        # 0-100: Qué tan nuevo/único
    efficiency_score: float = 0.0     # 0-100: Qué tan eficiente (tiempo/objetos)
    overall_score: float = 0.0        # 0-100: Score final
    
    def to_dict(self) -> Dict:
        return {
            'strategy_id': self.strategy.id,
            'success': self.success,
            'error': self.error,
            'execution_time_ms': self.execution_time_ms,
            'objects_created': self.objects_created,
            'scores': {
                'aesthetic': self.aesthetic_score,
                'complexity': self.complexity_score,
                'novelty': self.novelty_score,
                'efficiency': self.efficiency_score,
                'overall': self.overall_score
            }
        }


class LearningFreedomEngine:
    """
    Motor de libertad de aprendizaje para LYZU.
    
    Responsabilidades:
    1. Generar múltiples estrategias alternativas
    2. Ejecutar estrategias en paralelo
    3. Evaluar resultados con múltiples criterios
    4. Seleccionar ganador automáticamente
    5. Aprender de los resultados
    """
    
    def __init__(self, max_strategies: int = 5, verbose: bool = True, max_history: int = 100):
        """
        Inicializa el motor de libertad.
        
        Args:
            max_strategies: Máximo número de estrategias a generar
            verbose: Si True, imprime decisiones
            max_history: Límite de experimentos en memoria
        """
        self.max_strategies = max_strategies
        self.verbose = verbose
        self.max_history = max_history
        
        # Historial de experimentos
        self.experiment_history: List[Dict] = []
        self.strategy_database: Dict[str, Strategy] = {}
        # learning_log: user_prompt -> [(strategy_type, score), ...]
        # Ahora persistido en disco para sobrevivir reinicios
        self.learning_log: Dict[str, List[Tuple[str, float]]] = {}
        
        # Caché de resultados
        self.result_cache: Dict[str, ScenarioResult] = {}
        
        # Configuración
        self.persistence_dir = Path('bitacora/learning_freedom')
        self.persistence_dir.mkdir(parents=True, exist_ok=True)
        
        # Cargar learning_log persistido (si existe)
        self._load_learning_log()
        
        self._log(f"Learning Freedom Engine inicializado (max_strategies={max_strategies}, prompts conocidos={len(self.learning_log)})")
    
    def _log(self, message: str):
        """Log interno con timestamp"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")
    
    def generate_strategies(self, user_prompt: str, intent: str, entities: Dict, insights: Optional[Dict] = None) -> List[Strategy]:
        """
        Genera múltiples estrategias DIFERENTES para un prompt del usuario.
        
        Args:
            user_prompt: Lo que pidió el usuario
            intent: Intención clasificada
            entities: Entidades extraídas
            insights: Datos de C2 sobre qué ha funcionado antes
            
        Returns:
            Lista de estrategias para experimentar
        """
        self._log(f"📋 Generando {self.max_strategies} estrategias para: '{user_prompt}'")
        
        strategies = []
        strategy_types = list(StrategyType)
        
        for i in range(self.max_strategies):
            # Seleccionar tipo de estrategia (variado)
            strategy_type = strategy_types[i % len(strategy_types)]
            
            # Generar estrategia basada en tipo
            strategy = self._generate_strategy_by_type(
                strategy_type, 
                user_prompt, 
                intent, 
                entities,
                variant=i,
                insights=insights
            )
            
            if strategy:
                strategies.append(strategy)
                self.strategy_database[strategy.id] = strategy
                self._log(f"  Estrategia {i+1}: {strategy_type.value} - {strategy.description}")
        
        return strategies
    
    def _generate_strategy_by_type(
        self, 
        strategy_type: StrategyType, 
        prompt: str, 
        intent: str,
        entities: Dict,
        variant: int = 0,
        insights: Optional[Dict] = None
    ) -> Optional[Strategy]:
        """
        Genera una estrategia específica según su tipo.
        """
        strategy_id = f"strat_{int(time.time() * 1000)}_{variant}"
        
        handlers = []
        description = ""
        
        # Usar insights de memoria si existen para ajustar parámetros base
        suggested_scale = insights.get('best_scale', 1.0) if insights else 1.0
        suggested_color = insights.get('best_color', 'white') if insights else None

        if strategy_type == StrategyType.PRIMITIVE:
            # Estrategia simple: crear un objeto
            obj_type = entities.get('object_type') or random.choice(['cube', 'sphere', 'cylinder', 'cone'])
            
            # Aplicar escala sugerida por la experiencia
            params = {'name': f'{obj_type}_1', 'scale': suggested_scale}
            handlers = [
                HandlerCall(f'blender.create_{obj_type}', params)
            ]
            description = f"Crear {obj_type} simple"
        
        elif strategy_type == StrategyType.COMPOSITION:
            # Estrategia: múltiples objetos
            obj_type = entities.get('object_type', 'cube')
            # IMPROVISACIÓN: Variedad
            obj_type = entities.get('object_type') or random.choice(['cube', 'sphere', 'cylinder'])
            count = entities.get('quantity', 3)
            handlers = [
                HandlerCall(f'blender.create_{obj_type}', {'name': f'{obj_type}_base'}),
                HandlerCall('blender.add_array_modifier', {
                    'object': f'{obj_type}_base',
                    'count': count,
                    'offset_x': 2.5
                })
            ]
            description = f"Crear {count} {obj_type}s en array"
        
        elif strategy_type == StrategyType.TRANSFORMATION:
            # Estrategia: crear + modificar
            obj_type = entities.get('object_type', 'cube')
            obj_type = entities.get('object_type') or 'cube'
            handlers = [
                HandlerCall(f'blender.create_{obj_type}', {'name': f'{obj_type}_1'}),
                HandlerCall('blender.add_subdivision_surface_handler', {
                    'object': f'{obj_type}_1',
                    'levels': 2
                }),
                HandlerCall('blender.add_bevel_modifier_handler', {
                    'object': f'{obj_type}_1'
                })
            ]
            description = f"Crear {obj_type} + suavizar + bevel"
        
        elif strategy_type == StrategyType.MATERIAL_DECORATION:
            # Estrategia: objeto + material
            obj_type = entities.get('object_type', 'cube')
            color = entities.get('color', 'red')
            obj_type = entities.get('object_type') or random.choice(['cube', 'sphere'])
            color = entities.get('color') or random.choice(['red', 'blue', 'gold', 'silver', 'green'])
            handlers = [
                HandlerCall(f'blender.create_{obj_type}', {'name': f'{obj_type}_1'}),
                HandlerCall('blender.create_material_handler', {
                    'name': f'Material_{color}',
                    'base_color': self._color_to_rgba(color)
                }),
                HandlerCall('blender.apply_material_handler', {
                    'object': f'{obj_type}_1',
                    'material': f'Material_{color}'
                })
            ]
            description = f"Crear {obj_type} {color} con material"
        
        elif strategy_type == StrategyType.LIGHTING:
            # Estrategia: objeto + iluminación
            obj_type = entities.get('object_type', 'cube')
            obj_type = entities.get('object_type') or 'monkey' if random.random() > 0.5 else 'sphere' # Monkey (Suzanne) es bueno para luz
            handlers = [
                HandlerCall(f'blender.create_{obj_type}', {'name': f'{obj_type}_1'}),
                HandlerCall('blender.create_light_handler', {
                    'name': 'luz_punto',
                    'light_type': 'POINT',
                    'energy': 1500,
                    'location': [5, 5, 5]
                }),
                HandlerCall('blender.create_light_handler', {
                    'name': 'luz_area',
                    'light_type': 'AREA',
                    'energy': 1000,
                    'location': [-3, 2, 4]
                })
            ]
            description = f"Crear {obj_type} + iluminación dual"
        
        elif strategy_type == StrategyType.CAMERA:
            # Estrategia: escena con cámara posicionada
            obj_type = entities.get('object_type', 'cube')
            obj_type = entities.get('object_type') or 'cube'
            handlers = [
                HandlerCall(f'blender.create_{obj_type}', {'name': f'{obj_type}_1'}),
                HandlerCall('blender.create_camera_handler', {
                    'name': 'camera_1',
                    'focal_length': 50
                }),
                HandlerCall('blender.position_camera_handler', {
                    'camera': 'camera_1',
                    'location': [7, 7, 5],
                    'look_at': [0, 0, 0]
                }),
                HandlerCall('blender.set_active_camera_handler', {
                    'camera': 'camera_1'
                })
            ]
            description = f"Crear {obj_type} + cámara cinematográfica"
        
        elif strategy_type == StrategyType.HYBRID:
            # Estrategia compleja: combinación de todo
            obj_type = entities.get('object_type', 'cube')
            color = entities.get('color', 'blue')
            obj_type = entities.get('object_type') or random.choice(['cube', 'sphere', 'cylinder'])
            color = entities.get('color') or random.choice(['gold', 'purple', 'cyan'])
            handlers = [
                HandlerCall(f'blender.create_{obj_type}', {'name': f'{obj_type}_main'}),
                HandlerCall('blender.add_subdivision_surface_handler', {
                    'object': f'{obj_type}_main',
                    'levels': 2
                }),
                HandlerCall('blender.create_material_handler', {
                    'name': f'Material_{color}_metallic',
                    'base_color': self._color_to_rgba(color),
                    'metallic': 0.7,
                    'roughness': 0.2
                }),
                HandlerCall('blender.apply_material_handler', {
                    'object': f'{obj_type}_main',
                    'material': f'Material_{color}_metallic'
                }),
                HandlerCall('blender.create_light_handler', {
                    'name': 'luz_key',
                    'light_type': 'AREA',
                    'energy': 1200,
                    'location': [4, 3, 6]
                }),
                HandlerCall('blender.create_camera_handler', {
                    'name': 'camera_gold',
                    'focal_length': 35
                }),
                HandlerCall('blender.position_camera_handler', {
                    'camera': 'camera_gold',
                    'location': [6, 6, 4],
                    'look_at': [0, 0, 0]
                })
            ]
            description = f"Escena completa: {obj_type} {color} + materiales + luces + cámara"
        
        if handlers:
            return Strategy(
                id=strategy_id,
                strategy_type=strategy_type,
                handlers=handlers,
                description=description
            )
        
        return None
    
    def execute_strategies(self, strategies: List[Strategy], intent_router) -> List[ScenarioResult]:
        """
        Ejecuta todas las estrategias y captura resultados.
        
        Args:
            strategies: Estrategias a ejecutar
            intent_router: Router para ejecutar handlers
            
        Returns:
            Lista de resultados (con scores)
        """
        self._log(f"🚀 Ejecutando {len(strategies)} estrategias en paralelo...")
        
        results = []
        for i, strategy in enumerate(strategies):
            self._log(f"  [{i+1}/{len(strategies)}] Ejecutando: {strategy.description}")
            
            result = self._execute_single_strategy(strategy, intent_router)
            results.append(result)
            
            if result.success:
                self._log(f"    Score: {result.overall_score:.1f}/100")
            else:
                self._log(f"    Error: {result.error}")
        
        return results
    
    def _execute_single_strategy(self, strategy: Strategy, intent_router) -> ScenarioResult:
        """
        Ejecuta una estrategia individual y calcula score.
        """
        start_time = time.time()
        
        try:
            # Ejecutar todos los handlers en secuencia
            execution_results = []
            objects_created = 0
            
            for handler_call in strategy.handlers:
                # Preparar comando
                command = {
                    'command': handler_call.handler_name,
                    'parameters': handler_call.parameters
                }
                
                # Ejecutar
                result = intent_router.route_and_execute(command, handler_call.parameters)
                execution_results.append(result)
                
                # Contar objetos creados
                if 'create' in handler_call.handler_name:
                    objects_created += 1
            
            execution_time = (time.time() - start_time) * 1000
            
            # Calcular scores
            aesthetic_score = self._calculate_aesthetic_score(strategy)
            complexity_score = self._calculate_complexity_score(strategy)
            novelty_score = self._calculate_novelty_score(strategy)
            efficiency_score = self._calculate_efficiency_score(execution_time, objects_created)
            
            # Score general (ponderado)
            overall_score = (
                aesthetic_score * 0.40 +        # 40% estética
                complexity_score * 0.25 +       # 25% complejidad
                novelty_score * 0.20 +          # 20% novedad
                efficiency_score * 0.15         # 15% eficiencia
            )
            
            return ScenarioResult(
                strategy=strategy,
                success=True,
                output=execution_results,
                execution_time_ms=execution_time,
                objects_created=objects_created,
                aesthetic_score=aesthetic_score,
                complexity_score=complexity_score,
                novelty_score=novelty_score,
                efficiency_score=efficiency_score,
                overall_score=overall_score
            )
        
        except Exception as e:
            return ScenarioResult(
                strategy=strategy,
                success=False,
                output=None,
                error=str(e),
                execution_time_ms=(time.time() - start_time) * 1000,
                objects_created=0
            )
    
    def select_winner(self, results: List[ScenarioResult]) -> Optional[ScenarioResult]:
        """
        Selecciona la mejor estrategia basada en scores.
        LYZU toma esta decisión automáticamente.
        """
        if not results or not any(r.success for r in results):
            return None
        
        # Filtrar solo resultados exitosos
        successful = [r for r in results if r.success]
        
        if not successful:
            return None
        
        # Seleccionar mejor overall_score
        winner = max(successful, key=lambda r: r.overall_score)
        
        self._log(f"\n🏆 GANADOR SELECCIONADO AUTOMÁTICAMENTE:")
        self._log(f"   Estrategia: {winner.strategy.description}")
        self._log(f"   Score: {winner.overall_score:.1f}/100")
        self._log(f"   Tiempo: {winner.execution_time_ms:.0f}ms")
        self._log(f"   Objetos: {winner.objects_created}")
        
        return winner
    
    def learn_from_experiment(self, user_prompt: str, results: List[ScenarioResult], winner: Optional[ScenarioResult]):
        """
        Registra el experimento en la base de conocimiento.
        LYZU recuerda qué funcionó mejor para este tipo de request.
        """
        experiment = {
            'timestamp': datetime.now().isoformat(),
            'user_prompt': user_prompt,
            'total_strategies': len(results),
            'successful_strategies': len([r for r in results if r.success]),
            'winner_strategy': winner.strategy.id if winner else None,
            'winner_score': winner.overall_score if winner else 0.0,
            'all_results': [r.to_dict() for r in results]
        }
        
        self.experiment_history.append(experiment)
        
        # Gestión de memoria: Rotación de historial
        if len(self.experiment_history) > self.max_history:
            self.experiment_history.pop(0)
        
        # Registrar en learning_log por prompt
        if user_prompt not in self.learning_log:
            self.learning_log[user_prompt] = []
        
        if winner:
            # Guardar tipo+descripción en lugar del objeto Strategy (no serializable directamente)
            self.learning_log[user_prompt].append(
                (winner.strategy.strategy_type.value, winner.overall_score)
            )
        
        # Guardar persistentemente — tanto el experimento como el learning_log
        self._persist_experiment(experiment)
        self._save_learning_log()
        
        self._log(f"📚 Experimento registrado en base de conocimiento")
    
    def _persist_experiment(self, experiment: Dict):
        """Guarda experimento individual en archivo"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = self.persistence_dir / f"experiment_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(experiment, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self._log(f"Error guardando experimento: {e}")
    
    def _save_learning_log(self):
        """Persiste el learning_log completo en disco."""
        try:
            log_path = self.persistence_dir / 'learning_log.json'
            # learning_log contiene (strategy_type_str, score) — ambos serializables
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(self.learning_log, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self._log(f"Error guardando learning_log: {e}")
    
    def _load_learning_log(self):
        """Carga el learning_log persistido desde disco (si existe)."""
        log_path = self.persistence_dir / 'learning_log.json'
        if not log_path.exists():
            return
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            # raw es Dict[str, List[List[str, float]]] — convertir listas a tuplas
            self.learning_log = {
                prompt: [(entry[0], entry[1]) for entry in entries]
                for prompt, entries in raw.items()
            }
            self._log(f"📂 learning_log cargado: {len(self.learning_log)} prompts conocidos")
        except Exception as e:
            self._log(f"Error cargando learning_log: {e}")
            self.learning_log = {}
    
    # ========== FUNCIONES DE SCORING ==========
    
    def _calculate_aesthetic_score(self, strategy: Strategy) -> float:
        """
        Calcula score estético (0-100).
        Basado en: tipo de estrategia, materiales, iluminación.
        """
        score = 50.0  # Base
        
        # Bonus si tiene materiales
        if any('material' in h.handler_name for h in strategy.handlers):
            score += 15
        
        # Bonus si tiene iluminación
        if any('light' in h.handler_name for h in strategy.handlers):
            score += 15
        
        # Bonus si tiene cámara
        if any('camera' in h.handler_name for h in strategy.handlers):
            score += 10
        
        # Bonus si tiene modificadores
        if any('modifier' in h.handler_name for h in strategy.handlers):
            score += 10
        
        return min(score, 100.0)
    
    def _calculate_complexity_score(self, strategy: Strategy) -> float:
        """
        Calcula score de complejidad (0-100).
        Más handlers = más complejo.
        """
        num_handlers = len(strategy.handlers)
        
        # Escala: 1-3 handlers = low, 4-6 = medium, 7+ = high
        if num_handlers <= 2:
            return 30.0
        elif num_handlers <= 4:
            return 60.0
        elif num_handlers <= 6:
            return 80.0
        else:
            return 100.0
    
    def _calculate_novelty_score(self, strategy: Strategy) -> float:
        """
        Calcula score de novedad (0-100).
        Estrategias de un tipo que no ha ganado recientemente = más altas.
        """
        strategy_type = strategy.strategy_type.value

        # Contar cuántas veces este TIPO de estrategia ha ganado
        count = 0
        for exp in self.experiment_history:
            winner_id = exp.get('winner_strategy')
            if winner_id and winner_id in self.strategy_database:
                winner_strat = self.strategy_database[winner_id]
                if winner_strat.strategy_type.value == strategy_type:
                    count += 1

        # Menos victorias de este tipo = más novedad
        novelty = max(0, 100 - (count * 15))
        return novelty
    
    def _calculate_efficiency_score(self, execution_time_ms: float, objects_created: int) -> float:
        """
        Calcula score de eficiencia (0-100).
        Rápido + muchos objetos = eficiente.
        """
        # Penalizar si tarda mucho (> 5 segundos = mala)
        time_score = max(0, 100 - (execution_time_ms / 50))
        
        # Bonus si crea múltiples objetos
        objects_score = min(100, objects_created * 20)
        
        efficiency = (time_score * 0.6) + (objects_score * 0.4)
        return min(efficiency, 100.0)
    
    def _color_to_rgba(self, color_name: str) -> Tuple[float, float, float, float]:
        """Convierte nombre de color a RGBA"""
        colors = {
            'red': (1.0, 0.0, 0.0, 1.0),
            'green': (0.0, 1.0, 0.0, 1.0),
            'blue': (0.0, 0.0, 1.0, 1.0),
            'yellow': (1.0, 1.0, 0.0, 1.0),
            'orange': (1.0, 0.6, 0.0, 1.0),
            'purple': (1.0, 0.0, 1.0, 1.0),
            'white': (1.0, 1.0, 1.0, 1.0),
            'black': (0.0, 0.0, 0.0, 1.0),
        }
        return colors.get(color_name.lower(), (0.5, 0.5, 0.5, 1.0))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estadísticas de aprendizaje"""
        total_experiments = len(self.experiment_history)
        successful_experiments = len([e for e in self.experiment_history 
                                     if e['successful_strategies'] > 0])
        
        avg_score = 0.0
        if self.experiment_history:
            avg_score = sum(e['winner_score'] for e in self.experiment_history) / total_experiments
        
        return {
            'total_experiments': total_experiments,
            'successful_experiments': successful_experiments,
            'average_winner_score': avg_score,
            'known_prompts': len(self.learning_log),
            'strategy_database_size': len(self.strategy_database)
        }
