"""
ContextualMatcher — Validador de Contexto para Evocación de Patrones
FIN DE SEMANA 2: Reescritura de Evocación

Responsabilidad:
- Comparar el contexto almacenado de un patrón con el contexto actual
- Decidir si es seguro evocar un patrón basándose en múltiples dimensiones
- Registrar en log detallado las razones de bloqueo

Regla de Oro:
"Si el hash estructural no coincide, NO EVOCAR. Punto."

Dimensiones de comparación (ponderadas):
1. environment_hash (0.35) — SHA256 de scene_before — VETO ABSOLUTO
2. active_mode      (0.25) — OBJECT/EDIT/SCULPT
3. blender_version  (0.10) — Compatibilidad major.minor
4. scene_before     (0.20) — Lista de objetos presentes (Jaccard)
5. engine_adapter   (0.10) — Versión del adapter
"""

from typing import Dict, Tuple, List
from core.utils.logging import log_info, log_warning


class ContextualMatcher:
    """
    Validador de contexto para evocación segura de patrones.
    
    Compara el contexto almacenado del patrón con el contexto actual
    del entorno antes de permitir la evocación.
    """

    # Pesos de cada dimensión — suman 1.0
    WEIGHT_HASH = 0.35
    WEIGHT_MODE = 0.25
    WEIGHT_VERSION = 0.10
    WEIGHT_SCENE = 0.20
    WEIGHT_ADAPTER = 0.10

    # Umbral mínimo para aprobar match contextual
    DEFAULT_THRESHOLD = 0.70

    def contextual_match(self, pattern: Dict, current_context: Dict,
                         threshold: float = None) -> Tuple[bool, float, str]:
        """
        Compara el contexto almacenado del patrón con el contexto actual.

        Args:
            pattern: Patrón almacenado con su campo 'context'
            current_context: Contexto actual del entorno con las mismas claves
            threshold: Umbral de aprobación (default 0.70)

        Returns:
            (match, score, reason)
            - match: True si el patrón es seguro de evocar
            - score: Puntuación de similitud contextual (0.0 a 1.0)
            - reason: Explicación detallada del resultado
        """
        if threshold is None:
            threshold = self.DEFAULT_THRESHOLD

        pattern_ctx = pattern.get('context', {})
        if not pattern_ctx:
            return False, 0.0, "Patrón sin contexto almacenado — evocación bloqueada"

        score = 0.0
        failures: List[str] = []

        # ─── Dimensión 1: environment_hash (VETO ABSOLUTO) ───
        hash_score, hash_reason = self._compare_hash(pattern_ctx, current_context)
        if hash_score == 0.0:
            # Veto absoluto: hash no coincide → bloqueo inmediato
            log_warning(f"🚫 [ContextualMatcher] VETO ABSOLUTO: {hash_reason}")
            return False, 0.0, f"VETO: {hash_reason}"
        score += hash_score

        # ─── Dimensión 2: active_mode (VETO si no coincide) ───
        mode_score, mode_reason = self._compare_mode(pattern_ctx, current_context)
        if mode_score == 0.0 and self._both_have_value(pattern_ctx, current_context, 'active_mode'):
            # Veto: ejecutar un patrón OBJECT en modo EDIT es peligroso
            log_warning(f"🚫 [ContextualMatcher] VETO MODO: {mode_reason}")
            return False, 0.0, f"VETO: {mode_reason}"
        score += mode_score

        # ─── Dimensión 3: blender_version (VETO si major.minor difiere) ───
        version_score, version_reason = self._compare_version(pattern_ctx, current_context)
        if version_score == 0.0 and self._both_have_value(pattern_ctx, current_context, 'blender_version'):
            # Veto: APIs de Blender cambian entre majors
            log_warning(f"🚫 [ContextualMatcher] VETO VERSIÓN: {version_reason}")
            return False, 0.0, f"VETO: {version_reason}"
        score += version_score

        # ─── Dimensión 4: scene_before (Jaccard) ───
        scene_score, scene_reason = self._compare_scene(pattern_ctx, current_context)
        score += scene_score
        if scene_score < self.WEIGHT_SCENE:
            failures.append(scene_reason)

        # ─── Dimensión 5: engine_adapter_version ───
        adapter_score, adapter_reason = self._compare_adapter(pattern_ctx, current_context)
        score += adapter_score
        if adapter_score == 0.0:
            failures.append(adapter_reason)

        # ─── Decisión final ───
        match = score >= threshold

        if match:
            reason = f"Contexto compatible (score: {score:.2f}/{threshold:.2f})"
            log_info(f"✅ [ContextualMatcher] {reason}")
        else:
            reason_parts = "; ".join(failures) if failures else "Score insuficiente"
            reason = f"Contexto incompatible (score: {score:.2f}/{threshold:.2f}): {reason_parts}"
            log_warning(f"🚫 [ContextualMatcher] {reason}")

        return match, round(score, 4), reason

    # ═══════════════════════════════════════════════════
    # COMPARADORES INDIVIDUALES
    # ═══════════════════════════════════════════════════

    def _compare_hash(self, pattern_ctx: Dict, current_ctx: Dict) -> Tuple[float, str]:
        """Compara environment_hash — VETO ABSOLUTO si no coincide."""
        p_hash = pattern_ctx.get('environment_hash', '')
        c_hash = current_ctx.get('environment_hash', '')

        if not p_hash or not c_hash:
            return 0.0, "Hash de entorno ausente (patrón o contexto actual sin hash)"

        if p_hash == c_hash:
            return self.WEIGHT_HASH, "Hash coincide"
        else:
            return 0.0, f"Hash estructural no coincide (patrón: {p_hash[:12]}... vs actual: {c_hash[:12]}...)"

    def _compare_mode(self, pattern_ctx: Dict, current_ctx: Dict) -> Tuple[float, str]:
        """Compara active_mode (OBJECT, EDIT, SCULPT, etc.)."""
        p_mode = pattern_ctx.get('active_mode', '').upper()
        c_mode = current_ctx.get('active_mode', '').upper()

        if not p_mode or not c_mode:
            # Si alguno no tiene modo, penalizar parcialmente
            return self.WEIGHT_MODE * 0.5, "Modo activo ausente en uno de los contextos"

        if p_mode == c_mode:
            return self.WEIGHT_MODE, f"Modo activo coincide ({p_mode})"
        else:
            return 0.0, f"Modo activo diferente (patrón: {p_mode} vs actual: {c_mode})"

    def _compare_version(self, pattern_ctx: Dict, current_ctx: Dict) -> Tuple[float, str]:
        """Compara blender_version — match por major.minor."""
        p_ver = pattern_ctx.get('blender_version', '')
        c_ver = current_ctx.get('blender_version', '')

        if not p_ver or not c_ver:
            return self.WEIGHT_VERSION * 0.5, "Versión de Blender ausente en contexto"

        p_parts = p_ver.split('.')
        c_parts = c_ver.split('.')

        try:
            # Comparar major.minor (ignorar patch)
            if p_parts[0] == c_parts[0] and p_parts[1] == c_parts[1]:
                return self.WEIGHT_VERSION, f"Versión Blender compatible ({p_ver} ≈ {c_ver})"
            else:
                return 0.0, f"Versión Blender incompatible (patrón: {p_ver} vs actual: {c_ver})"
        except (IndexError, ValueError):
            return 0.0, f"Versión Blender no parseable (patrón: {p_ver}, actual: {c_ver})"

    def _compare_scene(self, pattern_ctx: Dict, current_ctx: Dict) -> Tuple[float, str]:
        """Compara scene_before usando Jaccard similarity sobre nombres de objetos."""
        p_scene = pattern_ctx.get('scene_before', {})
        c_scene = current_ctx.get('scene_before', {})

        p_objects = self._extract_object_names(p_scene)
        c_objects = self._extract_object_names(c_scene)

        if not p_objects and not c_objects:
            # Ambas escenas vacías = coinciden
            return self.WEIGHT_SCENE, "Ambas escenas vacías — coinciden"

        if not p_objects or not c_objects:
            # Una vacía y otra no
            return 0.0, "Una escena vacía y la otra no"

        # Jaccard similarity: |A ∩ B| / |A ∪ B|
        intersection = p_objects & c_objects
        union = p_objects | c_objects
        jaccard = len(intersection) / len(union) if union else 0.0

        weighted = self.WEIGHT_SCENE * jaccard
        detail = f"Escena Jaccard={jaccard:.2f} ({len(intersection)}/{len(union)} objetos comunes)"

        return round(weighted, 4), detail

    def _compare_adapter(self, pattern_ctx: Dict, current_ctx: Dict) -> Tuple[float, str]:
        """Compara engine_adapter_version."""
        p_adapter = pattern_ctx.get('engine_adapter_version', '')
        c_adapter = current_ctx.get('engine_adapter_version', '')

        if not p_adapter or not c_adapter:
            return self.WEIGHT_ADAPTER * 0.5, "Versión de adapter ausente"

        if p_adapter == c_adapter:
            return self.WEIGHT_ADAPTER, f"Adapter coincide ({p_adapter})"
        else:
            return 0.0, f"Adapter diferente (patrón: {p_adapter} vs actual: {c_adapter})"

    # ═══════════════════════════════════════════════════
    # UTILIDADES
    # ═══════════════════════════════════════════════════

    @staticmethod
    def _both_have_value(ctx_a: Dict, ctx_b: Dict, key: str) -> bool:
        """Verifica si ambos contextos tienen un valor no vacío para la clave dada."""
        return bool(ctx_a.get(key, '')) and bool(ctx_b.get(key, ''))

    @staticmethod
    def _extract_object_names(scene_data: Dict) -> set:
        """
        Extrae nombres de objetos de la data de escena.
        Soporta formatos: {'objects': [{'name': 'X'}, ...]} y {'objects': ['X', ...]}
        """
        objects = scene_data.get('objects', [])
        names = set()
        for obj in objects:
            if isinstance(obj, dict):
                name = obj.get('name', '')
                if name:
                    names.add(name)
            elif isinstance(obj, str):
                names.add(obj)
        return names
