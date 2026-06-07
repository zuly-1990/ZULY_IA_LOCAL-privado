"""
strategy_synthesizer.py
=======================

SINTETIZADOR DE ESTRATEGIAS

LYZU combina handlers de formas NUEVAS y CREATIVAS.

Capacidades:
- Generar combinaciones random de handlers
- Cross-breed (mezclar dos estrategias ganadoras)
- Parametric variation (cambiar parámetros sutilmente)
- Constraint respecting (respetar límites del sistema)

Resultado: LYZU inventa estrategias que nunca ha visto.
"""

import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class SynthesisMethod(Enum):
    """Métodos de síntesis de estrategias"""
    RANDOM_COMBO = "random_combo"        # Combinar handlers random
    CROSS_BREED = "cross_breed"          # Mezclar dos ganadoras
    MUTATION = "mutation"                 # Mutar una estrategia
    PARAMETRIC = "parametric"             # Variar parámetros


@dataclass
class HandlerSignature:
    """Descripción de un handler disponible"""
    name: str
    handler_id: str
    compatible_with: List[str]           # Handlers que van bien con este
    parameter_ranges: Dict[str, Tuple]   # Rango de parámetros válidos
    output_type: str                     # qué produce (object, scene, etc)


class StrategySynthesizer:
    """
    Sintetizador de estrategias.
    LYZU crea combinaciones nuevas de handlers.
    """
    
    def __init__(self, available_handlers: Optional[List[Dict]] = None, verbose: bool = True):
        """
        Inicializa el sintetizador.
        
        Args:
            available_handlers: Lista de handlers disponibles
            verbose: Si True, imprime decisiones
        """
        self.verbose = verbose
        self.handler_library = available_handlers or self._build_default_library()
        self.generated_combinations: List[Dict] = []
        self.successful_combinations: List[Dict] = []
    
    def _log(self, message: str):
        if self.verbose:
            print(f"[SYNTHESIZER] {message}")
    
    def _build_default_library(self) -> List[Dict]:
        """Construye librería default de handlers Blender"""
        return [
            # Primitivos
            {'id': 'primitive_cube', 'name': 'Crear cubo', 'type': 'object', 'compat': ['material', 'light', 'modifier']},
            {'id': 'primitive_sphere', 'name': 'Crear esfera', 'type': 'object', 'compat': ['material', 'light', 'modifier']},
            {'id': 'primitive_cylinder', 'name': 'Crear cilindro', 'type': 'object', 'compat': ['material', 'light', 'modifier']},
            
            # Materiales
            {'id': 'material_create', 'name': 'Crear material', 'type': 'material', 'compat': ['material_apply']},
            {'id': 'material_apply', 'name': 'Aplicar material', 'type': 'material', 'compat': ['object']},
            {'id': 'material_color', 'name': 'Cambiar color', 'type': 'material', 'compat': []},
            
            # Luces
            {'id': 'light_point', 'name': 'Luz puntual', 'type': 'light', 'compat': ['light_energy']},
            {'id': 'light_area', 'name': 'Luz área', 'type': 'light', 'compat': ['light_energy']},
            {'id': 'light_sun', 'name': 'Luz sol', 'type': 'light', 'compat': ['light_energy']},
            
            # Modificadores
            {'id': 'modifier_subdiv', 'name': 'Subdivision surface', 'type': 'modifier', 'compat': []},
            {'id': 'modifier_array', 'name': 'Array modifier', 'type': 'modifier', 'compat': []},
            {'id': 'modifier_bevel', 'name': 'Bevel modifier', 'type': 'modifier', 'compat': []},
            
            # Cámara
            {'id': 'camera_create', 'name': 'Crear cámara', 'type': 'camera', 'compat': ['camera_position']},
            {'id': 'camera_position', 'name': 'Posicionar cámara', 'type': 'camera', 'compat': []},
        ]
    
    def synthesize(self, method: SynthesisMethod, **kwargs) -> List[Dict]:
        """
        Sintetiza nuevas estrategias.
        
        Args:
            method: Método de síntesis
            **kwargs: Parámetros específicos del método
            
        Returns:
            Lista de estrategias sintetizadas
        """
        self._log(f"🔬 Sintetizando estrategias con método: {method.value}")
        
        if method == SynthesisMethod.RANDOM_COMBO:
            return self._synthesize_random_combo(
                num_strategies=kwargs.get('num_strategies', 3),
                max_handlers=kwargs.get('max_handlers', 5)
            )
        
        elif method == SynthesisMethod.CROSS_BREED:
            return self._synthesize_cross_breed(
                strategy1=kwargs.get('strategy1'),
                strategy2=kwargs.get('strategy2'),
                num_offspring=kwargs.get('num_offspring', 2)
            )
        
        elif method == SynthesisMethod.MUTATION:
            return self._synthesize_mutation(
                base_strategy=kwargs.get('base_strategy'),
                num_mutations=kwargs.get('num_mutations', 3)
            )
        
        elif method == SynthesisMethod.PARAMETRIC:
            return self._synthesize_parametric(
                base_strategy=kwargs.get('base_strategy'),
                num_variations=kwargs.get('num_variations', 4)
            )
        
        return []
    
    def _synthesize_random_combo(self, num_strategies: int = 3, max_handlers: int = 5) -> List[Dict]:
        """
        Genera N estrategias random combinando handlers.
        
        LYZU simplemente combina handlers de forma aleatoria.
        """
        strategies = []
        
        for i in range(num_strategies):
            # Seleccionar número random de handlers
            num_handlers = random.randint(1, max_handlers)
            
            # Seleccionar handlers random (respetando compatibilidad)
            handlers_combo = self._select_compatible_handlers(num_handlers)
            
            strategy = {
                'id': f'synth_random_{i}',
                'method': 'random_combo',
                'handlers': handlers_combo,
                'description': self._describe_strategy(handlers_combo),
                'novelty': 'high'  # Es random, por eso novel
            }
            
            strategies.append(strategy)
            self._log(f"  ✓ Estrategia {i+1}: {strategy['description']}")
        
        self.generated_combinations.extend(strategies)
        return strategies
    
    def _synthesize_cross_breed(
        self,
        strategy1: Dict,
        strategy2: Dict,
        num_offspring: int = 2
    ) -> List[Dict]:
        """
        Mezcla dos estrategias ganadoras.
        
        Toma lo mejor de cada una y crea híbridos.
        """
        self._log(f"🧬 Cross-breeding dos estrategias ganadoras...")
        
        offspring = []
        
        for i in range(num_offspring):
            # Tomar handlers de ambas estrategias
            handlers1 = strategy1.get('handlers', [])
            handlers2 = strategy2.get('handlers', [])
            
            # Combinación 1: primeros handlers de s1, últimos de s2
            if i % 2 == 0:
                combined = handlers1[:len(handlers1)//2] + handlers2[len(handlers2)//2:]
            else:
                combined = handlers1[len(handlers1)//2:] + handlers2[:len(handlers2)//2]
            
            strategy = {
                'id': f'synth_breed_{i}',
                'method': 'cross_breed',
                'parent1': strategy1.get('id', 'unknown'),
                'parent2': strategy2.get('id', 'unknown'),
                'handlers': combined,
                'description': f"Híbrida de dos estrategias ganadoras",
                'novelty': 'medium'
            }
            
            offspring.append(strategy)
            self._log(f"  ✓ Descendencia {i+1}: {len(combined)} handlers")
        
        self.generated_combinations.extend(offspring)
        return offspring
    
    def _synthesize_mutation(
        self,
        base_strategy: Dict,
        num_mutations: int = 3
    ) -> List[Dict]:
        """
        Muta una estrategia existente.
        
        Pequeños cambios: agregar/quitar handlers, cambiar parámetros.
        """
        self._log(f"🧪 Mutando estrategia base...")
        
        mutations = []
        base_handlers = base_strategy.get('handlers', [])
        
        for i in range(num_mutations):
            mutated_handlers = base_handlers.copy()
            
            # Tipo de mutación random
            mutation_type = random.choice(['add', 'remove', 'modify'])
            
            if mutation_type == 'add' and len(mutated_handlers) < 7:
                # Agregar handler random
                new_handler = random.choice(self.handler_library)
                mutated_handlers.append(new_handler)
                mutation_desc = f"+ {new_handler['name']}"
            
            elif mutation_type == 'remove' and len(mutated_handlers) > 1:
                # Quitar handler random
                removed = mutated_handlers.pop(random.randint(0, len(mutated_handlers)-1))
                mutation_desc = f"- {removed.get('name', removed.get('id', 'handler'))}"
            
            else:
                # Modificar handler existente
                if mutated_handlers:
                    handler = random.choice(mutated_handlers)
                    mutation_desc = f"modificar {handler.get('name', handler.get('id', 'handler'))}"
                else:
                    mutation_desc = "sin cambios"
            
            strategy = {
                'id': f'synth_mut_{i}',
                'method': 'mutation',
                'parent': base_strategy.get('id', 'unknown'),
                'handlers': mutated_handlers,
                'description': f"Mutación: {mutation_desc}",
                'novelty': 'medium'
            }
            
            mutations.append(strategy)
            self._log(f"  ✓ Mutación {i+1}: {mutation_desc}")
        
        self.generated_combinations.extend(mutations)
        return mutations
    
    def _synthesize_parametric(
        self,
        base_strategy: Dict,
        num_variations: int = 4
    ) -> List[Dict]:
        """
        Varía parámetros de una estrategia.
        
        Mantiene los mismos handlers, cambia valores REALES.
        Ejemplo: energy de 1500 -> 1050-1950, levels de 2 -> 1-3, etc.
        """
        self._log(f"📊 Sintetizando variaciones paramétricas...")
        
        # Parámetros numéricos que se pueden variar
        NUMERIC_PARAMS = {'energy', 'levels', 'count', 'scale', 'offset_x', 'focal_length'}
        
        variations = []
        base_handlers = base_strategy.get('handlers', [])
        
        for i in range(num_variations):
            varied_handlers = []
            applied_changes = []
            
            for handler in base_handlers:
                varied_handler = {k: v for k, v in handler.items()}
                
                # Variar parámetros numéricos dentro de 'params' o en raíz del dict
                params_key = 'params' if 'params' in varied_handler else None
                target = varied_handler[params_key] if params_key else varied_handler
                
                if isinstance(target, dict):
                    for param_name in list(target.keys()):
                        if param_name in NUMERIC_PARAMS and isinstance(target[param_name], (int, float)):
                            factor = random.uniform(0.7, 1.3)  # ±30%
                            original = target[param_name]
                            target[param_name] = round(original * factor, 3)
                            applied_changes.append(f"{param_name}: {original}→{target[param_name]}")
                        elif param_name == 'location' and isinstance(target[param_name], list):
                            # Variar coordenadas de ubicación
                            factor = random.uniform(0.8, 1.2)
                            original = target[param_name]
                            target[param_name] = [round(c * factor, 2) for c in original]
                            applied_changes.append(f"location: escalado {factor:.2f}x")
                
                if params_key:
                    varied_handler[params_key] = target
                
                varied_handlers.append(varied_handler)
            
            change_summary = ', '.join(applied_changes[:3]) if applied_changes else 'sin params numéricos'
            strategy = {
                'id': f'synth_param_{i}',
                'method': 'parametric',
                'parent': base_strategy.get('id', 'unknown'),
                'handlers': varied_handlers,
                'description': f"Variación #{i+1}: {change_summary}",
                'novelty': 'low'
            }
            
            variations.append(strategy)
            self._log(f"  ✓ Variación {i+1}: {change_summary}")
        
        self.generated_combinations.extend(variations)
        return variations

    
    # ========== HERRAMIENTAS DE SÍNTESIS ==========
    
    def _select_compatible_handlers(self, count: int) -> List[Dict]:
        """
        Selecciona N handlers que sean compatibles entre sí.
        """
        if count <= 0:
            return []
        
        selected = []
        available = self.handler_library.copy()
        
        for _ in range(count):
            if not available:
                break
            
            # Seleccionar handler random
            handler = random.choice(available)
            selected.append(handler)
            available.remove(handler)
            
            # Preferir handlers compatibles con el anterior
            if selected and handler.get('compat'):
                compatible = [h for h in available if h['id'] in handler.get('compat', [])]
                if compatible and random.random() < 0.7:  # 70% de probabilidad
                    available = compatible + [h for h in available if h not in compatible]
        
        return selected
    
    def _describe_strategy(self, handlers: List[Dict]) -> str:
        """Genera descripción textual de una estrategia"""
        if not handlers:
            return "Estrategia vacía"
        
        handler_names = [h.get('name', h.get('id', 'desconocido')) for h in handlers]
        
        if len(handlers) == 1:
            return f"Crear {handler_names[0]}"
        elif len(handlers) == 2:
            return f"{handler_names[0]} + {handler_names[1]}"
        else:
            return f"Secuencia compleja: {', '.join(handler_names[:3])}..."
    
    def register_successful(self, strategy: Dict, score: float):
        """Registra una estrategia exitosa para futuro cross-breeding"""
        self.successful_combinations.append({
            'strategy': strategy,
            'score': score,
            'timestamp': str(__import__('datetime').datetime.now())
        })
        
        self._log(f"📌 Estrategia registrada como exitosa (score={score:.1f})")
    
    def get_best_successful_strategies(self, top_n: int = 3) -> List[Dict]:
        """Retorna las N estrategias más exitosas"""
        sorted_strategies = sorted(
            self.successful_combinations,
            key=lambda x: x['score'],
            reverse=True
        )
        return [s['strategy'] for s in sorted_strategies[:top_n]]
    
    def analyze_synthesis_patterns(self) -> Dict[str, any]:
        """Analiza patrones en estrategias sintetizadas"""
        if not self.generated_combinations:
            return {'count': 0}
        
        methods = {}
        for strategy in self.generated_combinations:
            method = strategy.get('method', 'unknown')
            methods[method] = methods.get(method, 0) + 1
        
        return {
            'total_generated': len(self.generated_combinations),
            'methods_used': methods,
            'successful_count': len(self.successful_combinations),
            'success_rate': len(self.successful_combinations) / len(self.generated_combinations) if self.generated_combinations else 0
        }
