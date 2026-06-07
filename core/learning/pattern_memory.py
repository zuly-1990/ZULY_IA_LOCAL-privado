# core/learning/pattern_memory.py
"""
Stub minimo para desbloquear import en agent.py.
Fase 5.13 - Memoria de patrones aprendidos.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
import uuid
from datetime import datetime


class PatternMemory:
    """
    Almacena y recupera patrones de ejecución válidos.
    """

    def __init__(self, db_path: str = None, storage_dir: str = None):
        self.patterns: List[Dict[str, Any]] = []
        self.db_path = Path(db_path) if db_path else Path(storage_dir or "memory") / "pattern_db.json"
        self._load()

    def _load(self):
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.patterns = json.load(f)
            except Exception:
                self.patterns = []

    def save(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, indent=2, ensure_ascii=False, default=str)

    def _normalize_text(self, text: str) -> str:
        return text.lower().strip()

    def _find_existing_pattern(self, user_request: str) -> Optional[Dict[str, Any]]:
        normalized = self._normalize_text(user_request)
        for pattern in self.patterns:
            if self._normalize_text(pattern.get('user_request', '')) == normalized:
                return pattern
        return None

    def _can_store(self, execution_result: Dict[str, Any]) -> bool:
        if not execution_result.get('success', False):
            return False
        if execution_result.get('confidence', 0) < 0.85:
            return False
        validation = execution_result.get('validation', {})
        if not validation.get('verified', False):
            return False
        if execution_result.get('mode', 'REACTIVE') == 'HYBRID':
            return False
        if execution_result.get('attempts', 1) > 1:
            return False
        scene_before = execution_result.get('scene_state_pre', {})
        scene_after = execution_result.get('scene_state', {})
        if not scene_before and not scene_after:
            return False
        return True

    def store_pattern(self, user_request: str, execution_result: Dict[str, Any]) -> Optional[str]:
        """Almacena un patrón si cumple las condiciones mínimas."""
        if not self._can_store(execution_result):
            return None

        existing = self._find_existing_pattern(user_request)
        if existing:
            return existing.get('pattern_id')

        pattern_id = str(uuid.uuid4())
        pattern = {
            'pattern_id': pattern_id,
            'timestamp': datetime.now().isoformat(),
            'user_request': user_request,
            'command_executed': execution_result.get('command_executed'),
            'confidence': execution_result.get('confidence'),
            'parameters': execution_result.get('parameters', {}),
            'validation': execution_result.get('validation', {}),
            'scene_state_pre': execution_result.get('scene_state_pre', {}),
            'scene_state': execution_result.get('scene_state', {}),
            'mode': execution_result.get('mode', 'REACTIVE'),
            'metadata': {
                'uses': 0,
                'successes': 0,
                'fails': 0,
                'consecutive_successes': 0,
                'last_used': None,
                'status': 'STAGING'
            }
        }
        self.patterns.append(pattern)
        self.save()
        return pattern_id

    def register_execution_result(self, pattern_id: str, success: bool):
        """Registra resultado de ejecución para un patrón memorizado."""
        for pattern in self.patterns:
            if pattern.get('pattern_id') == pattern_id:
                meta = pattern.setdefault('metadata', {})
                meta['uses'] = meta.get('uses', 0) + 1
                meta['last_used'] = datetime.now().isoformat()
                if success:
                    meta['successes'] = meta.get('successes', 0) + 1
                    meta['consecutive_successes'] = meta.get('consecutive_successes', 0) + 1
                else:
                    meta['fails'] = meta.get('fails', 0) + 1
                    meta['consecutive_successes'] = 0
                self.save()
                return True
        return False

    def recall(self, command_name: str) -> Optional[Dict[str, Any]]:
        """Recupera un patrón previo por nombre de comando."""
        for pattern in self.patterns:
            if pattern.get('command_executed') == command_name:
                return pattern
        return None

    def get_stats(self, command_name: str = None) -> Dict[str, Any]:
        """Estadísticas de memoria o de un comando específico."""
        if command_name:
            matches = [p for p in self.patterns if p.get('command_executed') == command_name]
            total = len(matches)
            return {
                'command': command_name,
                'total_patterns': total,
                'total_attempts': sum(p.get('metadata', {}).get('uses', 0) for p in matches),
                'average_confidence': sum(p.get('confidence', 0) for p in matches) / max(total, 1)
            }

        return {
            'total_patterns': len(self.patterns),
            'total_uses': sum(p.get('metadata', {}).get('uses', 0) for p in self.patterns),
            'patterns': [p.get('pattern_id') for p in self.patterns]
        }
