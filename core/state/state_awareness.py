"""
Sistema de Autoconciencia Operativa del Estado - Fase 5.14

Responsabilidad:
- Leer estado actual del agente
- Consolidarlo en estructura clara
- Exponerlo como snapshot pasivo
- NO modificar nada

Filosofía:
"Un sistema que no sabe en qué estado está no puede ser confiable."

PROHIBIDO:
- Ejecutar comandos
- Tomar decisiones
- Cambiar comportamiento
- Reutilizar patrones
- Alterar flujos

ZULY SE MIRA AL ESPEJO. NO ACTÚA.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from core.security.black_protocol import BlackProtocol # NUEVO: Fase 16


class StateAwareness:
    """
    Sistema de Autoconciencia Operativa del Estado.
    
    Permite a ZULY saber en qué estado está,
    SIN cambiar comportamiento,
    SIN tomar decisiones,
    SIN ejecutar acciones.
    
    Autoconciencia = LECTURA INTERNA DEL ESTADO
    """
    
    def __init__(self, agent):
        """
        Inicializa el sistema de autoconciencia.
        
        Args:
            agent: Referencia al agente para leer su estado
        """
        self.agent = agent
    
    def snapshot(self) -> Dict[str, Any]:
        """
        Captura snapshot del estado actual del sistema.
        
        Este método SOLO LEE, NO MODIFICA.
        
        Returns:
            Diccionario con estado completo del sistema
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "operational_state": self._get_operational_state(),
            "security": self._get_security_state(),
            "validation": self._get_validation_state(),
            "learning": self._get_learning_state(),
            "execution": self._get_execution_state(),
            "environment": self._get_environment_state()  # NUEVO: Fase 5.16
        }
    
    def _get_environment_state(self) -> Dict[str, Any]:
        """
        Lee estado del entorno (Blender).
        """
        observer = getattr(self.agent, 'blender_observer', None)
        count = 0
        if observer:
            # Si el observer tiene el método snapshot, usémoslo o accedamos directo a la función nueva
            # Para ser consistentes con la filosofía de 'snapshot', deberíamos leer del snapshot del observer
            # Pero la instrucción 5 dice: state["blender_projects_detected"] = len(files)
            # Hagámoslo robusto.
            try:
                # Opción A: Obtener snapshot completo del observer (puede ser costoso si escanea disco siempre)
                # Opción B: Llamar método específico si existe (observe_blend_files)
                if hasattr(observer, 'observe_blend_files'):
                    files = observer.observe_blend_files()
                    count = len(files) if files else 0
            except Exception:
                count = -1 # Error state
        
        return {
            "blender_projects_detected": count
        }
    
    def _get_operational_state(self) -> str:
        """
        Lee estado operativo actual.
        
        Estados posibles:
        - OBSERVACIÓN
        - EJECUCIÓN_CON_APRENDIZAJE
        - BLOQUEO_ÉTICO
        
        Returns:
            Estado operativo como string
        """
        # Leer directamente del agent (NO modificar)
        raw_state = getattr(self.agent, 'operational_state', 'UNKNOWN')
        
        # Normalizar a formato estándar
        if 'Observación' in raw_state or 'observación' in raw_state.lower():
            return 'OBSERVACIÓN'
        elif 'Aprendizaje' in raw_state or 'aprendizaje' in raw_state.lower():
            return 'EJECUCIÓN_CON_APRENDIZAJE'
        elif 'Bloqueo' in raw_state or 'bloqueo' in raw_state.lower():
            return 'BLOQUEO_ÉTICO'
        else:
            return raw_state
    
    def _get_security_state(self) -> Dict[str, bool]:
        """
        Lee estado de seguridad.
        
        Returns:
            Diccionario con estado de seguridad
        """
        return {
            "author_verified": getattr(self.agent, 'authorized', False),
            "vault_active": getattr(self.agent, 'authorized', False),
            "black_protocol": BlackProtocol.get_status_report()
        }
    
    def _get_validation_state(self) -> Dict[str, Any]:
        """
        Lee estado de validación V0.
        
        Returns:
            Diccionario con último estado de validación
        """
        # Intentar obtener última validación del contexto
        context = getattr(self.agent, 'context', None)
        if context and hasattr(context, 'execution_history') and context.execution_history:
            last_execution = context.execution_history[-1]
            
            # Extraer información de validación si existe
            result = last_execution.get('result', {})
            if isinstance(result, dict):
                validation = result.get('validation', {})
                results = result.get('results', [])
                
                # Intentar obtener efecto del primer resultado
                last_effect = 'none'
                if results and len(results) > 0:
                    first_result = results[0]
                    if isinstance(first_result, dict):
                        last_effect = first_result.get('effect', 'none')
                
                return {
                    "last_v0": "OK" if validation.get('verified', False) else "FAIL" if validation else "NONE",
                    "last_effect": last_effect
                }
        
        return {
            "last_v0": "NONE",
            "last_effect": "none"
        }
    
    def _get_learning_state(self) -> Dict[str, Any]:
        """
        Lee estado de aprendizaje y memoria.
        
        Returns:
            Diccionario con estado de memoria
        """
        # Verificar si tiene pattern_memory
        pattern_memory = getattr(self.agent, 'pattern_memory', None)
        
        if pattern_memory:
            stats = pattern_memory.get_stats()
            
            # Obtener último patrón si existe
            last_pattern_id = None
            if pattern_memory.patterns:
                last_pattern = pattern_memory.patterns[-1]
                last_pattern_id = last_pattern.get('pattern_id', None)
            
            return {
                "enabled": self._get_operational_state() == 'EJECUCIÓN_CON_APRENDIZAJE',
                "patterns_total": stats.get('total_patterns', 0),
                "last_pattern_id": last_pattern_id
            }
        
        return {
            "enabled": False,
            "patterns_total": 0,
            "last_pattern_id": None
        }
    
    def _get_execution_state(self) -> Dict[str, Any]:
        """
        Lee estado de última ejecución.
        
        Returns:
            Diccionario con estado de ejecución
        """
        context = getattr(self.agent, 'context', None)
        if context and hasattr(context, 'execution_history') and context.execution_history:
            last_execution = context.execution_history[-1]
            
            # FASE 3: Detección básica de rollback
            rollback_detected = self._detect_rollback(context.execution_history)
            
            return {
                "last_success": last_execution.get('success', False),
                "attempts": len([e for e in context.execution_history 
                               if e.get('command') == last_execution.get('command')]),
                "rollback": rollback_detected,
                "rollback_count": sum(1 for e in context.execution_history if e.get('rollback', False))
            }
        
        return {
            "last_success": None,
            "attempts": 0,
            "rollback": False,
            "rollback_count": 0
        }
    
    def _detect_rollback(self, execution_history: list) -> bool:
        """
        FASE 3: Detecta si hubo rollback comparando ejecuciones recientes.
        
        Heurística: Si hay múltiples intentos del mismo comando con alternancia
        éxito/fracaso, probablemente hubo rollback manual.
        
        Args:
            execution_history: Historial de ejecuciones del contexto
            
        Returns:
            True si se detecta posible rollback
        """
        if len(execution_history) < 2:
            return False
        
        # Analizar últimas 3 ejecuciones
        recent = execution_history[-3:]
        
        # Patrón: mismo comando, éxito seguido de fracaso (posible undo)
        commands = [e.get('command') for e in recent]
        successes = [e.get('success', False) for e in recent]
        
        # Si el último comando se intentó antes y tuvo éxito, pero ahora falló
        if len(set(commands)) == 1 and commands[0] is not None:  # Mismo comando
            if len(successes) >= 2 and successes[-2] and not successes[-1]:
                # Éxito anterior, fracaso reciente del MISMO comando
                return True
        
        # Patrón: alternancia rápida éxito/fracaso/éxito (undo + redo)
        if len(successes) >= 3:
            if successes[-3] and not successes[-2] and successes[-1]:
                return True
        
        return False
