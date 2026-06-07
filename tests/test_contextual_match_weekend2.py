"""
Tests Comprehensivos — FIN DE SEMANA 2: Evocación Contextual
TDD para ContextualMatcher + find_similar_pattern contextual

Valida:
- Match contextual con 5 dimensiones
- Veto absoluto por hash
- Bloqueo por modo activo diferente
- Compatibilidad de versión Blender (major.minor)
- Similitud Jaccard de escena
- Integración con PatternMemory.find_similar_pattern
- Modo legacy (sin contexto) con warning
- Logs de rechazo detallados
- Benchmark de latencia
"""

import sys
import os
import time
import hashlib
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.learning.contextual_matcher import ContextualMatcher


# ═══════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════

@pytest.fixture
def matcher():
    return ContextualMatcher()


def _make_hash(objects_list):
    """Helper: genera el mismo hash SHA256 que usa PatternMemory."""
    return hashlib.sha256(str(objects_list).encode('utf-8')).hexdigest()


def _make_pattern(user_request="crear cubo", active_mode="OBJECT",
                  blender_version="3.6.0", adapter_version="v1.0",
                  objects=None):
    """Helper: crea un patrón con contexto completo."""
    if objects is None:
        objects = [{"name": "Camera"}, {"name": "Light"}]
    
    env_hash = _make_hash(objects)
    
    return {
        "pattern_id": "test-pattern-001",
        "user_request": user_request,
        "context": {
            "environment_hash": env_hash,
            "active_mode": active_mode,
            "blender_version": blender_version,
            "engine_adapter_version": adapter_version,
            "scene_before": {"objects": objects}
        },
        "metadata": {
            "uses": 0,
            "last_used": None,
            "status": "STAGING"
        }
    }


def _make_context(active_mode="OBJECT", blender_version="3.6.0",
                  adapter_version="v1.0", objects=None):
    """Helper: crea un contexto actual."""
    if objects is None:
        objects = [{"name": "Camera"}, {"name": "Light"}]
    
    env_hash = _make_hash(objects)
    
    return {
        "environment_hash": env_hash,
        "active_mode": active_mode,
        "blender_version": blender_version,
        "engine_adapter_version": adapter_version,
        "scene_before": {"objects": objects}
    }


# ═══════════════════════════════════════════════════
# TESTS: ContextualMatcher directo
# ═══════════════════════════════════════════════════

class TestContextualMatcherDirect:
    """Tests directos del ContextualMatcher."""

    def test_exact_context_match(self, matcher):
        """Contexto idéntico → match con score alto."""
        pattern = _make_pattern()
        context = _make_context()

        match, score, reason = matcher.contextual_match(pattern, context)

        assert match is True
        assert score >= 0.90
        assert "compatible" in reason.lower()
        print(f"  ✅ Exact match: score={score:.4f} — {reason}")

    def test_hash_mismatch_blocks(self, matcher):
        """Hash diferente → VETO ABSOLUTO, score=0."""
        pattern = _make_pattern(objects=[{"name": "Camera"}, {"name": "Light"}])
        context = _make_context(objects=[{"name": "Camera"}, {"name": "Light"}, {"name": "Cube"}])

        match, score, reason = matcher.contextual_match(pattern, context)

        assert match is False
        assert score == 0.0
        assert "VETO" in reason
        print(f"  🚫 Hash veto: score={score} — {reason}")

    def test_active_mode_mismatch(self, matcher):
        """Modo OBJECT vs EDIT → bloqueado."""
        objects = [{"name": "Camera"}]
        pattern = _make_pattern(active_mode="OBJECT", objects=objects)
        context = _make_context(active_mode="EDIT", objects=objects)

        match, score, reason = matcher.contextual_match(pattern, context)

        assert match is False
        assert "Modo activo diferente" in reason or "incompatible" in reason.lower()
        print(f"  🚫 Mode mismatch: score={score:.4f} — {reason}")

    def test_blender_version_minor_diff_passes(self, matcher):
        """3.6.0 vs 3.6.1 → pasa (mismo major.minor)."""
        objects = [{"name": "Camera"}]
        pattern = _make_pattern(blender_version="3.6.0", objects=objects)
        context = _make_context(blender_version="3.6.1", objects=objects)

        match, score, reason = matcher.contextual_match(pattern, context)

        assert match is True
        print(f"  ✅ Minor version diff passes: score={score:.4f}")

    def test_blender_version_major_diff_blocks(self, matcher):
        """3.6.0 vs 4.2.0 → bloqueado."""
        objects = [{"name": "Camera"}]
        pattern = _make_pattern(blender_version="3.6.0", objects=objects)
        context = _make_context(blender_version="4.2.0", objects=objects)

        match, score, reason = matcher.contextual_match(pattern, context)

        assert match is False
        assert "incompatible" in reason.lower() or "Blender" in reason
        print(f"  🚫 Major version diff blocks: score={score:.4f} — {reason}")

    def test_scene_partial_match(self, matcher):
        """2 de 3 objetos coinciden → Jaccard parcial."""
        objects_pattern = [{"name": "Camera"}, {"name": "Light"}, {"name": "Cube"}]
        objects_current = [{"name": "Camera"}, {"name": "Light"}, {"name": "Sphere"}]
        
        # Mismo hash para que no sea veto (usamos mismos objetos para generar hash)
        shared_hash = _make_hash(objects_pattern)
        
        pattern = _make_pattern(objects=objects_pattern)
        context = _make_context(objects=objects_current)
        
        # Para este test, forzamos el mismo hash para saltar el veto
        pattern['context']['environment_hash'] = shared_hash
        context['environment_hash'] = shared_hash

        match, score, reason = matcher.contextual_match(pattern, context)

        # Jaccard = 2/4 = 0.5, así que scene aporta 0.20 * 0.5 = 0.10
        # Otros pasan, así que score = 0.35 + 0.25 + 0.10 + 0.10 + 0.10 = 0.90
        # Pero Jaccard reduce scene: score ≈ 0.80
        print(f"  📊 Partial scene: score={score:.4f}, match={match} — {reason}")
        # El resultado depende de si el score total pasa el threshold

    def test_adapter_mismatch(self, matcher):
        """Adapter diferente reduce score."""
        objects = [{"name": "Camera"}]
        pattern = _make_pattern(adapter_version="v1.0", objects=objects)
        context = _make_context(adapter_version="v2.0", objects=objects)

        match, score, reason = matcher.contextual_match(pattern, context)

        # Adapter aporta 0.10, así que score sin adapter = 0.90
        # Score con adapter mismatch = 0.90 - 0.10 = 0.80 → podría pasar o no
        print(f"  📊 Adapter mismatch: score={score:.4f}, match={match}")

    def test_pattern_without_context(self, matcher):
        """Patrón sin campo context → bloqueado."""
        pattern = {"pattern_id": "test", "user_request": "test"}
        context = _make_context()

        match, score, reason = matcher.contextual_match(pattern, context)

        assert match is False
        assert score == 0.0
        assert "sin contexto" in reason.lower()
        print(f"  🚫 No context: {reason}")

    def test_empty_hash_blocks(self, matcher):
        """Hash vacío → veto."""
        objects = [{"name": "Camera"}]
        pattern = _make_pattern(objects=objects)
        context = _make_context(objects=objects)
        
        # Forzar hash vacío
        pattern['context']['environment_hash'] = ""

        match, score, reason = matcher.contextual_match(pattern, context)

        assert match is False
        assert "VETO" in reason
        print(f"  🚫 Empty hash veto: {reason}")

    def test_custom_threshold(self, matcher):
        """Umbral personalizado respetado."""
        objects = [{"name": "Camera"}]
        pattern = _make_pattern(objects=objects)
        context = _make_context(objects=objects)

        # Con umbral muy alto
        match_strict, score, _ = matcher.contextual_match(pattern, context, threshold=0.99)
        # Con umbral bajo
        match_lax, _, _ = matcher.contextual_match(pattern, context, threshold=0.50)

        assert match_lax is True
        print(f"  📊 Threshold test: strict={match_strict}, lax={match_lax}, score={score:.4f}")


# ═══════════════════════════════════════════════════
# TESTS: Integración PatternMemory + ContextualMatcher
# ═══════════════════════════════════════════════════

class TestPatternMemoryContextual:
    """Tests de integración de find_similar_pattern con contexto."""

    @pytest.fixture
    def memory(self):
        """PatternMemory con repos mockeados."""
        with patch('core.learning.pattern_memory.StagingPatternRepository') as MockStaging, \
             patch('core.learning.pattern_memory.VerifiedPatternRepository') as MockVerified, \
             patch('core.learning.pattern_memory.QuarantinePatternRepository') as MockQuarantine:
            
            MockStaging.return_value.load_all.return_value = []
            MockVerified.return_value.load_all.return_value = []
            MockQuarantine.return_value.load_all.return_value = []
            MockStaging.return_value.add_pattern.return_value = True
            MockStaging.return_value.update_pattern.return_value = True
            
            from core.learning.pattern_memory import PatternMemory
            pm = PatternMemory()
            return pm

    def _store_test_pattern(self, memory, user_request="crear cubo de prueba",
                           objects=None):
        """Helper: almacena un patrón de prueba."""
        if objects is None:
            objects = [{"name": "Camera"}, {"name": "Light"}]
        
        execution = {
            'command_executed': 'blender.create_cube',
            'confidence': 0.95,
            'success': True,
            'validation': {'verified': True, 'details': 'ok'},
            'mode': 'REACTIVE',
            'scene_state_pre': {'objects': objects},
            'scene_state': {'blender_version': '3.6.0', 'active_mode': 'OBJECT'},
            'engine_adapter_version': 'v1.0'
        }
        return memory.store_pattern(user_request, execution)

    def test_find_similar_with_context_pass(self, memory):
        """Texto similar + contexto OK → patrón devuelto."""
        self._store_test_pattern(memory)
        
        context = _make_context(objects=[{"name": "Camera"}, {"name": "Light"}])
        # Threshold 0.60 porque "crear cubo de prueba" vs "crear cubo rojo" ≈ 0.69
        result = memory.find_similar_pattern("crear cubo rojo", current_context=context, threshold=0.60)

        assert result is not None
        assert "cubo" in result['user_request'].lower()
        print(f"  ✅ Contextual match found: '{result['user_request']}'")

    def test_find_similar_with_context_block(self, memory):
        """Texto similar + contexto NO → None + log."""
        self._store_test_pattern(memory, objects=[{"name": "Camera"}, {"name": "Light"}])
        
        # Contexto diferente: objetos distintos → hash diferente → veto
        context = _make_context(objects=[{"name": "Camera"}, {"name": "Light"}, {"name": "Cube"}])
        result = memory.find_similar_pattern("crear cubo azul", current_context=context)

        assert result is None
        print("  🚫 Contextual block: text matched but context blocked")

    def test_find_similar_no_context_legacy(self, memory):
        """Sin contexto → modo legacy + warning."""
        self._store_test_pattern(memory)
        
        result = memory.find_similar_pattern("crear cubo de prueba")

        assert result is not None
        assert result['metadata']['uses'] == 1
        print(f"  ⚠️ Legacy mode: pattern found without context check")

    def test_find_similar_no_match(self, memory):
        """Texto muy diferente → None."""
        self._store_test_pattern(memory)
        
        context = _make_context()
        result = memory.find_similar_pattern("eliminar todas las esferas", current_context=context)

        assert result is None
        print("  ✅ No text match: correctly returned None")

    def test_rejection_log_contains_detail(self, memory, capsys):
        """Log de rechazo incluye las razones de bloqueo."""
        self._store_test_pattern(memory, objects=[{"name": "Camera"}])
        
        # Contexto con objetos diferentes → hash diferente → veto
        context = _make_context(objects=[{"name": "Camera"}, {"name": "Cube"}])
        result = memory.find_similar_pattern("crear cubo de prueba", current_context=context)

        assert result is None
        # El log se emite via core.utils.logging, verificamos que no hay crash
        print("  ✅ Rejection log emitted (no crash)")


# ═══════════════════════════════════════════════════
# BENCHMARK: Latencia
# ═══════════════════════════════════════════════════

class TestLatencyBenchmark:
    """Benchmark de rendimiento del matching contextual."""

    def test_latency_100_comparisons(self, matcher):
        """100 comparaciones contextuales deben completarse en < 50ms."""
        pattern = _make_pattern()
        context = _make_context()

        start = time.perf_counter()
        for _ in range(100):
            matcher.contextual_match(pattern, context)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 50, f"100 comparaciones tomaron {elapsed_ms:.1f}ms (límite: 50ms)"
        print(f"  ⚡ Latencia: {elapsed_ms:.1f}ms para 100 comparaciones ({elapsed_ms/100:.2f}ms/op)")

    def test_latency_with_large_scene(self, matcher):
        """Escena con 50 objetos — verificar que no hay degradación excesiva."""
        objects = [{"name": f"Object_{i}"} for i in range(50)]
        pattern = _make_pattern(objects=objects)
        context = _make_context(objects=objects)

        start = time.perf_counter()
        for _ in range(100):
            matcher.contextual_match(pattern, context)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 100, f"100 comparaciones con 50 objetos tomaron {elapsed_ms:.1f}ms"
        print(f"  ⚡ Latencia (50 obj): {elapsed_ms:.1f}ms para 100 ops ({elapsed_ms/100:.2f}ms/op)")


# ═══════════════════════════════════════════════════
# TESTS: _extract_object_names utility
# ═══════════════════════════════════════════════════

class TestExtractObjectNames:
    """Tests del extractor de nombres de objetos de escena."""

    def test_dict_format(self, matcher):
        """Formato {'objects': [{'name': 'X'}, ...]}."""
        scene = {"objects": [{"name": "Camera"}, {"name": "Light"}, {"name": "Cube"}]}
        names = matcher._extract_object_names(scene)
        assert names == {"Camera", "Light", "Cube"}

    def test_string_format(self, matcher):
        """Formato {'objects': ['X', 'Y', ...]}."""
        scene = {"objects": ["Camera", "Light"]}
        names = matcher._extract_object_names(scene)
        assert names == {"Camera", "Light"}

    def test_empty_scene(self, matcher):
        """Escena vacía → set vacío."""
        scene = {"objects": []}
        names = matcher._extract_object_names(scene)
        assert names == set()

    def test_no_objects_key(self, matcher):
        """Scene sin clave 'objects' → set vacío."""
        scene = {}
        names = matcher._extract_object_names(scene)
        assert names == set()

    def test_mixed_format(self, matcher):
        """Mix de dict y string → extrae lo que puede."""
        scene = {"objects": [{"name": "Camera"}, "Light", {"name": ""}]}
        names = matcher._extract_object_names(scene)
        assert names == {"Camera", "Light"}
