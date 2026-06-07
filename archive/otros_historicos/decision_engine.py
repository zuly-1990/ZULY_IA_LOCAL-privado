"""
decision_engine.py

Motor de decisión central para ZULY.
Enruta peticiones a patrones establecidos o al agente autónomo.

ARQUITECTURA:
    user_query → decision_engine.decidir() 
               → buscar_patron() 
               → if patron: usar_patron()
               → else: usar_agente()
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Callable
from datetime import datetime
from core.utils.logging import log_info, log_warning, log_error, log_success, log_debug

# FASE 20: Integración con pattern_to_handler_mapper
try:
    from pattern_to_handler_mapper import execute_handler, get_handler, is_pattern_available
    _MAPPER_AVAILABLE = True
except ImportError:
    log_warning("pattern_to_handler_mapper no disponible (aún)")
    _MAPPER_AVAILABLE = False


class PatternIndex:
    """Índice centralizado de patrones operativos."""
    
    def __init__(self, index_path: str = "patterns/index.json"):
        self.index_path = Path(index_path)
        self.patterns = {}
        self.load_index()
    
    def load_index(self):
        """Carga el índice de patrones desde JSON."""
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r', encoding='utf-8') as f:
                    self.patterns = json.load(f)
                log_success(f"Índice cargado: {len(self.patterns)} patrones")
            except Exception as e:
                log_warning(f"Error cargando índice: {e}")
                self.patterns = {}
        else:
            log_info(f"Índice no existe: {self.index_path}")
            self.patterns = {}
    
    def save_index(self):
        """Guarda el índice actual a JSON."""
        try:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(self.patterns, f, indent=2, ensure_ascii=False)
            log_success(f"Índice guardado: {len(self.patterns)} patrones")
        except Exception as e:
            log_error(f"Error guardando índice: {e}")
    
    def add_pattern(self, name: str, handler: str, tags: List[str], origin: str = "manual"):
        """Añade un patrón al índice."""
        self.patterns[name] = {
            "handler": handler,
            "tags": tags,
            "origin": origin,
            "created": datetime.now().isoformat()
        }
        self.save_index()
        log_info(f"Patrón añadido: {name}")
    
    def search_by_keyword(self, query: str) -> Optional[Tuple[str, Dict]]:
        """Busca patrón: estrategia simple pero efectiva."""
        query_lower = query.lower()
        
        best_match = None
        best_score = 0
        
        for pattern_name, pattern_data in self.patterns.items():
            pattern_lower = pattern_name.lower()
            
            # Exacta: ganador automático
            if query_lower == pattern_lower.replace('_', ' '):
                return (pattern_name, pattern_data)
            
            score = 0
            
            # ✓ Check 1: Palabras del patrón en query
            pattern_words = pattern_lower.replace('_', ' ').split()
            query_words = query_lower.split()
            
            for pw in pattern_words:
                for qw in query_words:
                    if pw == qw:
                        score += 100  # Coincidencia exacta de palabra
                    elif pw.startswith(qw[:3]) or qw.startswith(pw[:3]):
                        score += 50   # Al menos 3 letras coinciden
            
            # ✓ Check 2: Tags
            for tag in pattern_data.get("tags", []):
                for qw in query_words:
                    if tag == qw:
                        score += 150  # Tag coincide exactamente
                    elif tag.startswith(qw):
                        score += 75   # Tag comienza con palabra
            
            if score > best_score:
                best_score = score
                best_match = (pattern_name, pattern_data)
        
        # Retornar solo si hay score significativo
        return best_match if best_score >= 25 else None
    
    def list_patterns(self, folder: str = None) -> List[str]:
        """Lista patrones disponibles (opcionalmente filtrados por carpeta)."""
        if folder:
            # Buscar patrones en carpeta específica
            folder_path = Path(f"patterns/{folder}")
            if folder_path.exists():
                return [f.stem for f in folder_path.glob("*.json")]
        return list(self.patterns.keys())


class DecisionEngine:
    """Motor de decisión que enruta peticiones."""
    
    def __init__(self, patterns_dir: str = "patterns"):
        self.patterns_dir = Path(patterns_dir)
        self.index = PatternIndex(f"{patterns_dir}/index.json")
        self.decision_history = []
        
        # Crear carpetas si no existen
        self.patterns_dir.mkdir(exist_ok=True)
        (self.patterns_dir / "stable").mkdir(exist_ok=True)
        (self.patterns_dir / "drafts").mkdir(exist_ok=True)
        (self.patterns_dir / "rejected").mkdir(exist_ok=True)
    
    def decidir(self, query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Decide si usar patrón o agente autónomo.
        
        Args:
            query: Petición del usuario en lenguaje natural
            user_context: Contexto adicional (opcional)
        
        Returns:
            Dict con decisión:
            {
                "tipo": "usar_patron" | "usar_agente",
                "confianza": 0.0-1.0,
                "datos": {...},
                "razon": "explicación"
            }
        """
        decision_record = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "decision": None,
            "confianza": 0.0
        }
        
        # PASO 1: Buscar si existe patrón conocido
        resultado_busqueda = self.index.search_by_keyword(query)
        
        if resultado_busqueda:
            pattern_name, pattern_data = resultado_busqueda
            
            # PASO 2: Validar confianza (MEJORADA)
            confianza = self._calcular_confianza(query, pattern_name, pattern_data)
            
            if confianza >= 0.6:  # Umbral bajado a 0.6 (era 0.7)
                decision_record["decision"] = "usar_patron"
                decision_record["confianza"] = confianza
                
                self.decision_history.append(decision_record)
                
                return {
                    "tipo": "usar_patron",
                    "confianza": confianza,
                    "patron": pattern_name,
                    "handler": pattern_data.get("handler"),
                    "datos": pattern_data,
                    "razon": f"Patrón conocido con confianza {confianza:.1%}"
                }
        
        # PASO 3: Si no hay patrón confiable, derivar al agente
        decision_record["decision"] = "usar_agente"
        decision_record["confianza"] = 0.0
        self.decision_history.append(decision_record)
        
        return {
            "tipo": "usar_agente",
            "confianza": 0.0,
            "query": query,
            "context": user_context or {},
            "razon": "Query nuevo o baja confianza - usar agente autónomo"
        }
    
    def _calcular_confianza(self, query: str, pattern_name: str, pattern_data: Dict) -> float:
        """Calcula confianza de coincidencia patrón (mejorada)."""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        pattern_name_lower = pattern_name.lower()
        pattern_words = set(pattern_name_lower.replace('_', ' ').split())
        
        # Coincidencia exacta en nombre
        if query_lower == pattern_name_lower or query_lower == pattern_name_lower.replace('_', ' '):
            return 0.95
        
        # Calcular overlap de palabras
        overlap = len(query_words & pattern_words)
        total_words = len(query_words | pattern_words)
        
        if total_words == 0:
            return 0.5
        
        word_similarity = overlap / total_words
        
        # Coincidencia en tags
        tag_matches = 0
        for tag in pattern_data.get("tags", []):
            if any(word in tag.lower() for word in query_words):
                tag_matches += 1
        
        tag_bonus = min(tag_matches * 0.15, 0.3)  # Max bonus 0.3 de tags
        
        # Confianza final: 50% palabras + 50% tags + bonus
        confianza = (word_similarity * 0.5) + tag_bonus
        
        return min(max(confianza, 0.5), 0.95)  # Clamp [0.5, 0.95]
    
    def decidir_y_ejecutar(
        self, 
        query: str, 
        parameters: Dict[str, Any] = None, 
        adapter = None
    ) -> Dict[str, Any]:
        """
        FASE 20: Decide Y EJECUTA si encuentra patrón.
        
        Este es el interfaz de alto nivel que combina:
        1. Decisión (¿patrón o agente?)
        2. Ejecución (si patrón, ejecuta handler)
        
        Args:
            query: Petición del usuario
            parameters: Parámetros para el handler (si aplica)
            adapter: EngineAdapter (Blender, Mock, etc)
            
        Returns:
            Dict con decisión + resultado de ejecución (si aplica)
            
        Examples:
            >>> result = engine.decidir_y_ejecutar(
            ...     "crear un cubo",
            ...     {"location": [0, 0, 0]},
            ...     adapter
            ... )
            >>> if result["tipo"] == "patron_ejecutado":
            ...     print(f"✓ {result['objeto']}")
        """
        if not _MAPPER_AVAILABLE:
            log_warning("[FASE 20] Mapper no disponible - retornando solo decisión")
            return self.decidir(query)
        
        # Paso 1: Decidir
        decision = self.decidir(query)
        
        # Paso 2: Si hay patrón, intentar ejecutar
        if decision["tipo"] == "usar_patron":
            patron = decision["patron"]
            
            # Verificar que el handler está mapeado
            if not is_pattern_available(patron):
                log_warning(f"Patrón '{patron}' sin handler mapeado")
                decision["execution_status"] = "NO_HANDLER_MAPPED"
                return decision
            
            # Ejecutar handler
            log_info(f"[FASE 20] Ejecutando patrón: {patron}")
            
            # Parámetros por defecto
            params = parameters or {}
            
            # Ejecutar
            exec_result = execute_handler(patron, params, adapter)
            
            # Combinar decisión + ejecución
            decision.update({
                "execution_status": "EXECUTED",
                "execution_result": exec_result,
                "success": exec_result.get("success", False),
                "objeto": exec_result.get("object_name", exec_result.get("name")),
                "error": exec_result.get("error")
            })
            
            # Cambiar tipo para claridad
            decision["tipo"] = "patron_ejecutado"
            
            return decision
        
        else:
            # Sin patrón - solo retorna decisión
            decision["execution_status"] = "AGENT_REQUIRED"
            return decision
    
    def guardar_borrador(self, query: str, resultado: Dict[str, Any], handler_usado: str = None):
        """Guarda un borrador de patrón para posterior análisis."""
        borrador = {
            "query": query,
            "handler": handler_usado,
            "resultado": resultado,
            "timestamp": datetime.now().isoformat(),
            "estado": "borrador"
        }
        
        # Guardar en drafts/
        borrador_path = self.patterns_dir / "drafts" / f"draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(borrador_path, 'w', encoding='utf-8') as f:
                json.dump(borrador, f, indent=2, ensure_ascii=False)
            log_success(f"Borrador guardado: {borrador_path}")
            return True
        except Exception as e:
            log_error(f"Error guardando borrador: {e}")
            return False
    
    def promover_borrador_a_patron(self, borrador_path: str, patron_name: str, tags: List[str]):
        """Promociona un borrador a patrón estable."""
        try:
            with open(borrador_path, 'r', encoding='utf-8') as f:
                borrador = json.load(f)
            
            # Crear patrón estable
            handler = borrador.get("handler")
            self.index.add_pattern(patron_name, handler, tags, origin="promoted_from_draft")
            
            # Mover archivo
            patron_path = self.patterns_dir / "stable" / f"{patron_name}.json"
            with open(patron_path, 'w', encoding='utf-8') as f:
                json.dump(borrador, f, indent=2, ensure_ascii=False)
            
            log_success(f"Borrador promovido a patrón: {patron_name}")
            return True
        except Exception as e:
            log_error(f"Error promoviendo borrador: {e}")
            return False
    
    def rechazar_borrador(self, borrador_path: str, razon: str = ""):
        """Rechaza un borrador (lo mueve a rejected/)."""
        try:
            borrador_file = Path(borrador_path)
            rechazado_path = self.patterns_dir / "rejected" / borrador_file.name
            
            # Añadir metadatos de rechazo
            with open(borrador_path, 'r', encoding='utf-8') as f:
                borrador = json.load(f)
            
            borrador["razon_rechazo"] = razon
            borrador["rechazado_en"] = datetime.now().isoformat()
            
            with open(rechazado_path, 'w', encoding='utf-8') as f:
                json.dump(borrador, f, indent=2, ensure_ascii=False)
            
            log_warning(f"Borrador rechazado: {rechazado_path}")
            return True
        except Exception as e:
            log_error(f"Error rechazando borrador: {e}")
            return False


# Singleton global
_engine = None

def get_decision_engine() -> DecisionEngine:
    """Obtiene instancia global del motor de decisión."""
    global _engine
    if _engine is None:
        _engine = DecisionEngine()
    return _engine


def decidir(query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Interfaz rápida para tomar decisiones.
    
    Usage:
        decision = decidir("crear un cubo rojo")
        
        if decision["tipo"] == "usar_patron":
            ejecutar_patron(decision)
        else:
            resultado = agente.procesar(decision["query"])
    """
    engine = get_decision_engine()
    return engine.decidir(query, user_context)


if __name__ == "__main__":
    # Demostración básica
    engine = DecisionEngine()
    
    # Agregar algunos patrones de ejemplo
    engine.index.add_pattern(
        "crear_cubo",
        "create_cube_handler",
        ["cubo", "crear", "objeto", "primitiva"],
        "manual"
    )
    
    engine.index.add_pattern(
        "rotacion_objeto",
        "rotate_object_handler",
        ["rotar", "rotacion", "giro"],
        "manual"
    )
    
    # Probar decisiones
    print("\n🧠 TESTS DE DECISION ENGINE\n")
    
    test_queries = [
        "crear un cubo",
        "crea un cubo rojo",
        "haz un cubo",
        "rota el objeto 45 grados",
        "haz algo muy especial que nunca hice"
    ]
    
    for query in test_queries:
        decision = engine.decidir(query)
        print(f"Query: '{query}'")
        print(f"  → Tipo: {decision['tipo']}")
        print(f"  → Confianza: {decision['confianza']:.1%}")
        print(f"  → Razón: {decision['razon']}\n")
