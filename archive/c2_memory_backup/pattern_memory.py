"""
Sistema de Memoria de Patrones Estructurales - Fase 5.13
FIN DE SEMANA 2: Evocación Contextual integrada

Responsabilidad:
- Almacenar patrones SOLO si pasan validación V0
- Buscar patrones similares CON VALIDACIÓN CONTEXTUAL (PASIVO, no ejecuta)
- Persistir patrones en disco

Regla de Oro:
"Nada se memoriza si no pasa validación V0 con status OK."
"Nada se evoca si el contexto no coincide."

Tipo: Aprendizaje Pasivo (observa, no decide)
"""

import os
import uuid
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List
from difflib import SequenceMatcher

from core.utils.logging import log_info, log_warning, log_success, log_error
from core.learning.repositories import StagingPatternRepository, VerifiedPatternRepository, QuarantinePatternRepository, PendingPatternRepository
from core.learning.contextual_matcher import ContextualMatcher


class PatternMemory:
    """
    Sistema de Memoria de Patrones Estructurales.
    
    Almacena patrones de comandos exitosos que han sido validados físicamente.
    
    Condiciones OBLIGATORIAS para memorizar:
    1. validation.verified == True (V0 pasó)
    2. confidence >= 0.85 (alta confianza)
    3. success == True (ejecución exitosa)
    4. mode != HYBRID (sin intervención humana)
    5. attempts == 1 (sin rollback)
    
    FdS 2: Evocación ahora requiere match contextual obligatorio.
    """
    
    def __init__(self, storage_dir: str = "memory"):
        """
        Inicializa el sistema de memoria de patrones empleando Clean Architecture.
        
        Args:
            storage_dir: Directorio base de almacenamiento (default: "memory")
        """
        # Si recibimos un archivo en lugar de un directorio (como hacían los tests antiguos)
        # extraemos el directorio base para mantener compatibilidad
        if storage_dir and os.path.isfile(storage_dir):
            storage_dir = os.path.dirname(storage_dir)
        
        if not storage_dir:
            storage_dir = "memory"

        self.staging_repo = StagingPatternRepository(storage_dir=storage_dir)
        self.verified_repo = VerifiedPatternRepository(storage_dir=storage_dir)
        self.quarantine_repo = QuarantinePatternRepository(storage_dir=storage_dir)
        self.pending_repo = PendingPatternRepository(storage_dir=storage_dir)
        self.contextual_matcher = ContextualMatcher()
        
        # Para búsquedas pasivas, podemos unir staging y verified temporalmente.
        # En la Fase 6, solo buscaremos en verified.
        self.patterns: List[Dict] = self.staging_repo.load_all() + self.verified_repo.load_all()
        
        log_info(f"[PatternMemory] Inicializada en '{storage_dir}' con {len(self.patterns)} patrones totales")
    
    def can_memorize(self, execution_result: Dict) -> Tuple[bool, str]:
        """
        Verifica si un resultado cumple las 5 condiciones para ser memorizado.
        
        Args:
            execution_result: Resultado de la ejecución del comando
            
        Returns:
            (puede_memorizar, razón)
        """
        # Condición 1: Validación V0 OK
        validation = execution_result.get('validation', {})
        if not validation.get('verified', False):
            return False, "Validación V0 no pasó"
        
        # ULTRA EMERGENCIA — Condición 1b: V0 NO debe ser pasivo
        # Si V0 aprobó en modo pasivo (sin effect declarado), el resultado
        # NO fue verificado físicamente y NO debe memorizarse
        v0_result = execution_result.get('validation_v0', validation)
        if v0_result.get('passive', False):
            return False, "V0 fue pasivo (sin effect declarado) — resultado no verificado físicamente"
        
        # Condición 2: Confianza >= 0.85
        confidence = execution_result.get('confidence', 0.0)
        if confidence < 0.85:
            return False, f"Confianza insuficiente ({confidence:.2f} < 0.85)"
        
        # Condición 3: Ejecución exitosa
        if not execution_result.get('success', False):
            return False, "Ejecución no exitosa"
        
        # Condición 4: Sin intervención humana
        # AJUSTE CRÍTICO: Usar constante/campo 'mode', no string matching
        mode = execution_result.get('mode', 'REACTIVE')
        if mode == 'HYBRID':
            return False, "Requirió intervención humana (modo HYBRID)"
        
        # Fallback: verificar operational_state si no hay 'mode'
        if mode == 'REACTIVE':  # Solo si no hay mode explícito
            op_state = execution_result.get('operational_state', '')
            if 'hybrid' in op_state.lower() or 'aprobación' in op_state.lower():
                return False, "Requirió intervención humana"
        
        # Condición 5: Sin reintentos
        attempts = execution_result.get('attempts', 1)
        if attempts > 1:
            return False, f"Hubo reintentos ({attempts} intentos)"

        # Condición 6: Snapshot no vacío
        scene_before = execution_result.get('scene_state_pre', {})
        scene_after = execution_result.get('scene_state', {})
        if not scene_before and not scene_after:
             return False, "Snapshots de escena vacíos — no hay evidencia física del cambio"
        
        return True, "Cumple todas las condiciones (7/7)"
    
    def store_pattern(self, user_request: str, 
                     execution_result: Dict) -> Optional[str]:
        """
        Almacena un patrón si cumple las 5 condiciones obligatorias.
        
        Args:
            user_request: Petición original del usuario
            execution_result: Resultado completo de la ejecución
            
        Returns:
            pattern_id si se memorizó, None si se rechazó
        """
        can_store, reason = self.can_memorize(execution_result)
        
        if not can_store:
            log_warning(f"❌ Patrón NO memorizado: {reason}")
            return None
        
        # ULTRA EMERGENCIA — Condición 1c: Deduplicación
        # Si ya existe un patrón idéntico o muy similar (>0.95), no duplicamos aprendizaje
        existing = self._find_by_text_only(user_request, threshold=0.95)
        if existing:
            log_warning(f"⚠️ Deduplicación: El patrón para '{user_request}' ya existe (ID: {existing['pattern_id'][:8]})")
            return existing['pattern_id']

        # Extraer información del resultado
        results_list = execution_result.get('results', [{}])
        first_result = results_list[0] if results_list else {}
        
        scene_before = execution_result.get('scene_state_pre', {})
        # Hash SHA256 básico del contexto para seguridad estructural
        env_hash = hashlib.sha256(str(scene_before.get('objects', [])).encode('utf-8')).hexdigest()
        
        pattern = {
            "pattern_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "user_request": user_request,
            "intent": {
                "command_name": execution_result.get('command_executed'),
                "confidence": execution_result.get('confidence'),
                "parameters": execution_result.get('parameters', {})
            },
            "execution": {
                "success": True,
                "effect": first_result.get('effect'),
                "result": first_result.get('result', {})
            },
            "validation": {
                "verified": True,
                "details": execution_result.get('validation', {}).get('details', ''),
                "level": "V0"
            },
            "context": {
                "origin": execution_result.get('origin', 'laboratory'),
                "blender_version": execution_result.get('scene_state', {}).get('blender_version', '3.6.0'),
                "active_mode": execution_result.get('scene_state', {}).get('active_mode', 'OBJECT'),
                "engine_adapter_version": execution_result.get('engine_adapter_version', 'v1.0'),
                "environment_hash": env_hash,
                "operational_state": execution_result.get('operational_state'),
                "mode": execution_result.get('mode', 'REACTIVE'),
                "rollback_triggered": execution_result.get('rollback', False),  # FASE 3: Track rollback
                "scene_before": scene_before,
                "scene_after": execution_result.get('scene_state', {})
            },
            "metadata": {
                "uses": 0,
                "successes": 0,
                "fails": 0,
                "consecutive_successes": 0,
                "last_used": None,
                "created": datetime.now().isoformat(),
                "status": "STAGING"
            }
        }
        
        self.patterns.append(pattern)
        self.pending_repo.add_pattern(pattern)
        
        log_success(f"✓ Patrón guardado en PENDING (esperando visto bueno): {pattern['pattern_id'][:8]}... | '{user_request}'")
        return pattern['pattern_id']

    def approve_pending_pattern(self, pattern_id: str) -> bool:
        """
        Aprueba un patrón pendiente y lo mueve a STAGING.
        """
        pattern = self.pending_repo.get_pattern(pattern_id)
        if not pattern:
            log_error(f"No se encontró el patrón pendiente {pattern_id}")
            return False

        # Cambiar status y mover
        pattern['metadata']['status'] = "STAGING"
        self.pending_repo.delete_pattern(pattern_id)
        self.staging_repo.add_pattern(pattern)
        
        # Actualizar lista en memoria si es necesario (ya está en self.patterns si store_pattern lo añadió)
        # Pero mejor recargar self.patterns para consistencia
        self.patterns = self.staging_repo.load_all() + self.verified_repo.load_all()
        
        log_success(f"⭐ VISTO BUENO: Patrón {pattern_id[:8]} aprobado y movido a STAGING")
        return True

    def reject_pending_pattern(self, pattern_id: str) -> bool:
        """
        Rechaza un patrón pendiente y lo elimina.
        """
        if self.pending_repo.delete_pattern(pattern_id):
            # Eliminar también de la lista en memoria
            self.patterns = [p for p in self.patterns if p['pattern_id'] != pattern_id]
            log_info(f"🗑️ RECHAZADO: Patrón pendiente {pattern_id[:8]} eliminado")
            return True
        return False

    def register_execution_result(self, pattern_id: str, success: bool):
        """
        Registra el resultado de una ejecución para un patrón y gestiona su jerarquía.
        
        Reglas de Semana 5:
        - 3 éxitos consecutivos -> VERIFIED
        - 2 fallos totales -> QUARANTINE
        """
        pattern = next((p for p in self.patterns if p['pattern_id'] == pattern_id), None)
        if not pattern:
            log_error(f"No se encontró el patrón {pattern_id} para registrar resultado.")
            return

        meta = pattern['metadata']
        meta['uses'] += 1
        meta['last_used'] = datetime.now().isoformat()

        if success:
            meta['successes'] += 1
            meta['consecutive_successes'] += 1
            log_info(f"Éxito registrado para patrón {pattern_id[:8]}. Consecutivos: {meta['consecutive_successes']}")
        else:
            meta['fails'] += 1
            meta['consecutive_successes'] = 0
            log_warning(f"Fallo registrado para patrón {pattern_id[:8]}. Total fallos: {meta['fails']}")

        self._evaluate_hierarchy(pattern)

    def _evaluate_hierarchy(self, pattern: Dict):
        """Evalúa si un patrón debe cambiar de repositorio."""
        meta = pattern['metadata']
        current_status = meta['status']
        pattern_id = pattern['pattern_id']

        new_status = current_status

        # Lógica de Promoción: 3 éxitos consecutivos
        if current_status == "STAGING" and meta['consecutive_successes'] >= 3:
            new_status = "VERIFIED"
            log_success(f"⭐ PROMOCIÓN: Patrón {pattern_id[:8]} ascendido a VERIFIED")

        # Lógica de Degradación: 2 fallos
        elif meta['fails'] >= 2:
            new_status = "QUARANTINE"
            log_error(f"☣️ DEGRADACIÓN: Patrón {pattern_id[:8]} movido a QUARANTINE")

        if new_status != current_status:
            self._move_pattern(pattern, current_status, new_status)

    def _move_pattern(self, pattern: Dict, old_status: str, new_status: str):
        """Mueve físicamente un patrón entre repositorios."""
        pattern_id = pattern['pattern_id']
        pattern['metadata']['status'] = new_status

        # Eliminar del repo viejo
        if old_status == "STAGING":
            self.staging_repo.delete_pattern(pattern_id)
        elif old_status == "VERIFIED":
            self.verified_repo.delete_pattern(pattern_id)
        
        # Agregar al repo nuevo
        if new_status == "VERIFIED":
            self.verified_repo.add_pattern(pattern)
        elif new_status == "QUARANTINE":
            self.quarantine_repo.add_pattern(pattern)
        
        # En STAGING no debería re-entrar desde Verified/Quarantine normalmente en este flujo
        elif new_status == "STAGING":
            self.staging_repo.add_pattern(pattern)

        log_info(f"Patrón {pattern_id[:8]} movido de {old_status} a {new_status}")
    
    def find_similar_pattern(self, user_request: str,
                           current_context: Dict = None,
                           threshold: float = 0.75) -> Optional[Dict]:
        """
        Busca un patrón similar a la petición del usuario CON validación contextual.
        
        FdS 2: Ahora requiere current_context para validar el entorno.
        Si no se proporciona, funciona en modo legacy (solo texto) con warning.
        
        CRÍTICO: Solo INFORMA, NO ejecuta automáticamente (eso es Fase 5.15+)
        
        Args:
            user_request: Petición del usuario
            current_context: Contexto actual del entorno (hash, mode, version, scene, adapter)
            threshold: Umbral de similitud textual (0.0 a 1.0)
            
        Returns:
            Patrón más similar que pase validación contextual, o None
        """
        if not self.patterns:
            return None
        
        # ─── MODO LEGACY: sin contexto → solo texto + warning ───
        if current_context is None:
            log_warning("[PatternMemory] ⚠️ find_similar_pattern() llamado SIN contexto — modo legacy (solo texto). "
                       "FdS 2 requiere current_context para evocación segura.")
            return self._find_by_text_only(user_request, threshold)
        
        # ─── MODO FdS 2: texto + contexto ───
        # Paso 1: Filtrar candidatos por similitud textual
        candidates = []
        for pattern in self.patterns:
            text_score = SequenceMatcher(
                None, 
                user_request.lower(), 
                pattern['user_request'].lower()
            ).ratio()
            
            if text_score >= threshold:
                candidates.append((pattern, text_score))
        
        if not candidates:
            log_info("[PatternMemory] Sin candidatos textuales para evocación")
            return None
        
        # Paso 2: Validar contexto de cada candidato
        best_match = None
        best_combined_score = 0.0
        
        for pattern, text_score in candidates:
            ctx_match, ctx_score, ctx_reason = self.contextual_matcher.contextual_match(
                pattern, current_context
            )
            
            if ctx_match:
                # Score combinado: 40% texto + 60% contexto
                combined = (text_score * 0.4) + (ctx_score * 0.6)
                if combined > best_combined_score:
                    best_combined_score = combined
                    best_match = pattern
                    log_info(f"📋 Candidato contextual aprobado: texto={text_score:.2f} "
                            f"ctx={ctx_score:.2f} combinado={combined:.2f}")
            else:
                log_warning(f"🚫 Candidato textual bloqueado por contexto: "
                          f"'{pattern['user_request'][:40]}...' — {ctx_reason}")
        
        if best_match:
            # Actualizar metadata de uso — persistir en el repo correcto
            best_match['metadata']['uses'] += 1
            best_match['metadata']['last_used'] = datetime.now().isoformat()
            self._persist_pattern_update(best_match)
            
            log_info(f"📋 Patrón evocado con match contextual (score combinado: {best_combined_score:.2%})")
        
        return best_match
    
    def _find_by_text_only(self, user_request: str, threshold: float) -> Optional[Dict]:
        """
        Búsqueda legacy por texto solamente. Usado cuando no hay contexto disponible.
        DEPRECATED: Se mantiene para compatibilidad, pero debe migrar a contextual.
        """
        best_match = None
        best_score = 0.0
        
        for pattern in self.patterns:
            score = SequenceMatcher(
                None,
                user_request.lower(),
                pattern['user_request'].lower()
            ).ratio()
            
            if score > best_score and score >= threshold:
                best_score = score
                best_match = pattern
        
        if best_match:
            best_match['metadata']['uses'] += 1
            best_match['metadata']['last_used'] = datetime.now().isoformat()
            self._persist_pattern_update(best_match)
            
            log_info(f"📋 Patrón similar encontrado [LEGACY/texto] (similitud: {best_score:.2%})")
        
        return best_match
    
    def _persist_pattern_update(self, pattern: Dict):
        """Persiste actualización de un patrón en su repo correspondiente."""
        status = pattern.get('metadata', {}).get('status', 'STAGING')
        try:
            if status == 'VERIFIED':
                self.verified_repo.update_pattern(pattern['pattern_id'], pattern)
            else:
                self.staging_repo.update_pattern(pattern['pattern_id'], pattern)
        except Exception as e:
            log_error(f"Error persistiendo actualización de patrón: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estadísticas de la memoria de patrones.
        
        Returns:
            Diccionario con estadísticas
        """
        if not self.patterns:
            return {
                "total_patterns": 0,
                "total_uses": 0,
                "most_used": None
            }
        
        total_uses = sum(p['metadata']['uses'] for p in self.patterns)
        most_used = max(self.patterns, key=lambda p: p['metadata']['uses'])
        
        return {
            "total_patterns": len(self.patterns),
            "total_uses": total_uses,
            "most_used": {
                "request": most_used['user_request'],
                "uses": most_used['metadata']['uses']
            } if most_used['metadata']['uses'] > 0 else None
        }
    def audit_quarantine(self):
        """
        Audita patrones en cuarentena y detecta posibles mal clasificados.

        Un patron está MAL clasificado si tiene exitos >= 3 y fallos == 0,
        probable causa: scene_after vacio al momento de creacion.

        Returns:
            Dict con candidatos a recuperar y resumen de auditoria
        """
        quarantine_patterns = self.quarantine_repo.load_all()

        candidates_to_recover = []
        truly_quarantined = []

        for p in quarantine_patterns:
            meta = p.get('metadata', {})
            successes = meta.get('successes', 0)
            fails = meta.get('fails', 0)
            scene_after = p.get('context', {}).get('scene_after', {})

            if successes >= 3 and fails == 0 and not scene_after:
                candidates_to_recover.append({
                    'pattern_id': p['pattern_id'],
                    'user_request': p['user_request'],
                    'successes': successes,
                    'reason': 'Exitos suficientes pero scene_after vacio — re-ejecucion recomendada'
                })
                log_warning(
                    f"[audit_quarantine] Patron recuperable: '{p['user_request']}' "
                    f"({successes} exitos, 0 fallos, snapshot ausente)."
                )
            else:
                truly_quarantined.append(p['pattern_id'][:8])

        return {
            'total_quarantine': len(quarantine_patterns),
            'candidates_to_recover': candidates_to_recover,
            'truly_quarantined_count': len(truly_quarantined),
            'audit_timestamp': datetime.now().isoformat()
        }
