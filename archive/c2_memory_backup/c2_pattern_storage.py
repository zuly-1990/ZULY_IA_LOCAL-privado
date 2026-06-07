"""
C2 - Pattern Storage with Author Signature (WO-002)
=====================================================

Almacenamiento de patrones aprendidos CON FIRMA DEL AUTOR.

Flujo garantizado:
    Entrada → V0 valida → C1 evalúa → AUTOR firma → C2 persiste

REGLAS INAPELABLES:
    1. Sin firma válida → sin guardado, excepción obligatoria
    2. sin _persist() sin validación de identidad
    3. Rechazo del autor se persiste en DISCO (no en C2)
    4. Score final = C1_score * boost (si autor aprobó)
    5. Confianza es numérica (0-100), no string
"""

import json
import sqlite3
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from pathlib import Path
from enum import Enum


# ============================================================================
# Estructura de datos para patrones firmados
# ============================================================================

@dataclass
class AuthorSignature:
    """Firma obligatoria del autor"""
    autor_id: str                    # UUID del autor (debe coincidir con .zuly_identity.key)
    autor_aprueba: bool              # True/False - voto inapelable del autor
    autor_nota: str                  # Texto obligatorio (no vacío) - justificación
    timestamp_firma: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def is_valid(self) -> bool:
        """Valida que la firma sea estructuralmente correcta"""
        return (
            isinstance(self.autor_id, str) and len(self.autor_id) > 0
            and isinstance(self.autor_aprueba, bool)
            and isinstance(self.autor_nota, str) and len(self.autor_nota) > 0
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PatternRecord:
    """Patrón aprendido (estructura final con firma)"""
    pattern_name: str                # Nombre único del patrón
    pattern_type: str                # Type: "interactive_system", "procedural", etc
    origin: str                      # Origen: "real_execution", "synthetic", etc
    intent: str                      # Intención original
    handlers: List[str]              # Handlers usados
    scene_before: Dict[str, Any]     # Snapshot antes
    scene_after: Dict[str, Any]      # Snapshot después
    validation_v0: str               # Estado V0: "OK", "FAIL", "UNKNOWN"
    score_c1: float                  # Score de C1 (0-100)
    
    # Firma obligatoria del autor
    signature: AuthorSignature
    
    # Campos derivados DESPUÉS de firma
    score_final: float = 0.0         # C1_score * boost (si aprobó)
    confianza: int = 0               # 0-100, se calcula en _persist()
    uses_count: int = 0              # Contador de reutilizaciones
    timestamp_stored: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['signature'] = self.signature.to_dict()
        return result


class PatternStorageV2:
    """
    Almacenador de patrones con firma obligatoria de autor.
    
    Características clave:
    - Validación de identidad contra .zuly_identity.key
    - _persist() es privado (solo desde save())
    - Score y confianza se calculan DESPUÉS de validar firma
    - Rechazo del autor se persiste en DISCO
    """
    
    def __init__(self, 
                 db_path: str = 'bitacora/patterns_signed.db',
                 diagnostics_log_path: str = 'bitacora/author_decisions.jsonl'):
        self.db_path = db_path
        self.diagnostics_log_path = Path(diagnostics_log_path)
        self._ensure_storage_exists()
        self._load_author_identity()
    
    def _load_author_identity(self):
        """Carga el UUID del autor desde .zuly_identity.key"""
        try:
            if os.path.exists('.zuly_identity.key'):
                with open('.zuly_identity.key', 'r') as f:
                    self.stored_author_id = f.read().strip()
                    if not self.stored_author_id:
                        raise ValueError("Archivo .zuly_identity.key vacío")
            else:
                raise FileNotFoundError("Archivo .zuly_identity.key no encontrado")
        except Exception as e:
            raise RuntimeError(f"SECURITY: No se pudo cargar identidad del autor: {e}")
    
    def _ensure_storage_exists(self):
        """Crea tablas de almacenamiento si no existen"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            # Tabla para patrones aprobados por autor
            conn.execute('''
                CREATE TABLE IF NOT EXISTS patterns_signed (
                    pattern_id INTEGER PRIMARY KEY,
                    pattern_name TEXT NOT NULL UNIQUE,
                    pattern_type TEXT NOT NULL,
                    origin TEXT NOT NULL,
                    intent TEXT NOT NULL,
                    handlers TEXT NOT NULL,
                    scene_before TEXT NOT NULL,
                    scene_after TEXT NOT NULL,
                    validation_v0 TEXT NOT NULL,
                    score_c1 REAL NOT NULL,
                    
                    autor_id TEXT NOT NULL,
                    autor_aprueba INTEGER NOT NULL,
                    autor_nota TEXT NOT NULL,
                    timestamp_firma TEXT NOT NULL,
                    
                    score_final REAL NOT NULL,
                    confianza INTEGER NOT NULL,
                    uses_count INTEGER DEFAULT 0,
                    timestamp_stored TEXT NOT NULL
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_pattern_name 
                ON patterns_signed(pattern_name)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_confianza 
                ON patterns_signed(confianza)
            ''')
            
            conn.commit()
        
        # Crear log de diagnósticos (JSONL para rechazo del autor)
        self.diagnostics_log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.diagnostics_log_path.exists():
            self.diagnostics_log_path.touch()
    
    # ========================================================================
    # API PÚBLICA: save() — la única puerta a _persist()
    # ========================================================================
    
    def save(self, pattern_dict: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Guarda un patrón SOLO si tiene firma válida del autor.
        
        Args:
            pattern_dict: Diccionario con estructura de patrón
            
        Returns:
            (success: bool, message: str)
            
        Raises:
            ValueError: Si falta firma, identidad no coincide, o autor rechazó
        """
        try:
            # ─────────────────────────────────────────────────────────────
            # VALIDACIÓN 1: Campos de firma obligatorios presentes
            # ─────────────────────────────────────────────────────────────
            required_signature_fields = ["autor_id", "autor_aprueba", "autor_nota"]
            for field in required_signature_fields:
                if field not in pattern_dict:
                    raise ValueError(
                        f"BLOCKED: Campo '{field}' ausente. "
                        "El autor debe firmar antes de guardar. "
                        f"Requeridos: {required_signature_fields}"
                    )
            
            # ─────────────────────────────────────────────────────────────
            # VALIDACIÓN 2: Identidad del autor coincide
            # ─────────────────────────────────────────────────────────────
            submitted_author_id = pattern_dict["autor_id"]
            if submitted_author_id != self.stored_author_id:
                raise ValueError(
                    f"SECURITY: autor_id no coincide con identidad local. "
                    f"Esperado: {self.stored_author_id}, "
                    f"Recibido: {submitted_author_id}. "
                    "Esto puede indicar copia de base de datos de otra máquina."
                )
            
            # ─────────────────────────────────────────────────────────────
            # VALIDACIÓN 3: Estructura de firma es válida
            # ─────────────────────────────────────────────────────────────
            sig = AuthorSignature(
                autor_id=pattern_dict["autor_id"],
                autor_aprueba=pattern_dict["autor_aprueba"],
                autor_nota=pattern_dict["autor_nota"]
            )
            
            if not sig.is_valid():
                raise ValueError(
                    "BLOCKED: Firma del autor inválida estructuralmente. "
                    f"Verificar: {sig}"
                )
            
            # ─────────────────────────────────────────────────────────────
            # CASO 1: Autor RECHAZA el patrón
            # ─────────────────────────────────────────────────────────────
            if sig.autor_aprueba is False:
                self._record_author_rejection(pattern_dict, sig)
                return (False, f"Patrón '{pattern_dict.get('pattern_name', 'UNKNOWN')}' "
                               "rechazado por autor. Evento registrado en diagnósticos.")
            
            # ─────────────────────────────────────────────────────────────
            # VALIDACIÓN 4: Estructura básica del patrón
            # ─────────────────────────────────────────────────────────────
            required_pattern_fields = [
                "pattern_name", "pattern_type", "origin", "intent",
                "handlers", "scene_before", "scene_after",
                "validation_v0", "score_c1"
            ]
            for field in required_pattern_fields:
                if field not in pattern_dict:
                    raise ValueError(
                        f"BLOCKED: Campo patrón '{field}' ausente. "
                        f"Requeridos: {required_pattern_fields}"
                    )
            
            # ─────────────────────────────────────────────────────────────
            # CASO 2: Autor APRUEBA - proceder a _persist()
            # ─────────────────────────────────────────────────────────────
            pattern_record = PatternRecord(
                pattern_name=pattern_dict["pattern_name"],
                pattern_type=pattern_dict["pattern_type"],
                origin=pattern_dict["origin"],
                intent=pattern_dict["intent"],
                handlers=pattern_dict["handlers"],
                scene_before=pattern_dict["scene_before"],
                scene_after=pattern_dict["scene_after"],
                validation_v0=pattern_dict["validation_v0"],
                score_c1=pattern_dict["score_c1"],
                signature=sig
            )
            
            # Aquí SÍ llamamos a _persist() — garantizado que tiene firma válida
            self.__persist(pattern_record)
            
            return (True, f"✓ Patrón '{pattern_record.pattern_name}' "
                          "guardado con firma válida del autor.")
        
        except ValueError as e:
            # Re-raise para que el llamador sepa exactamente qué falló
            raise ValueError(str(e))
        except Exception as e:
            raise RuntimeError(f"Error inesperado en save(): {e}")
    
    # ========================================================================
    # API PRIVADA: __persist() — nombre mangled, SOLO desde save()
    # ========================================================================
    
    def __persist(self, pattern_record: PatternRecord):
        """
        PRIVADO (name mangling). Persiste patrón EN DISCO.
        
        NUNCA debe ser llamado sin:
            1. Firma válida verificada
            2. Identidad del autor validada
            3. Aprobación explícita del autor (autor_aprueba=True)
        
        Calcula score_final y confianza DESPUÉS de validar firma.
        """
        # Calcular score_final: boost si autor aprobó
        if pattern_record.signature.autor_aprueba:
            boost_factor = 1.15  # 15% de boost por aprobación humana
            pattern_record.score_final = min(
                pattern_record.score_c1 * boost_factor,
                100.0  # Cap en 100
            )
            pattern_record.confianza = 95  # Máxima confianza
        else:
            pattern_record.score_final = pattern_record.score_c1
            pattern_record.confianza = 0  # No debería llegar aquí
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO patterns_signed
                    (pattern_name, pattern_type, origin, intent,
                     handlers, scene_before, scene_after,
                     validation_v0, score_c1,
                     autor_id, autor_aprueba, autor_nota, timestamp_firma,
                     score_final, confianza, uses_count, timestamp_stored)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?,
                            ?, ?, ?, ?)
                ''', (
                    pattern_record.pattern_name,
                    pattern_record.pattern_type,
                    pattern_record.origin,
                    pattern_record.intent,
                    json.dumps(pattern_record.handlers),
                    json.dumps(pattern_record.scene_before),
                    json.dumps(pattern_record.scene_after),
                    pattern_record.validation_v0,
                    pattern_record.score_c1,
                    pattern_record.signature.autor_id,
                    int(pattern_record.signature.autor_aprueba),
                    pattern_record.signature.autor_nota,
                    pattern_record.signature.timestamp_firma,
                    pattern_record.score_final,
                    pattern_record.confianza,
                    pattern_record.uses_count,
                    pattern_record.timestamp_stored
                ))
                conn.commit()
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Patrón con este nombre ya existe: {e}")
    
    # ========================================================================
    # Registrar decisiones del autor
    # ========================================================================
    
    def _record_author_rejection(self, pattern_dict: Dict[str, Any], 
                                 sig: AuthorSignature):
        """
        Persiste RECHAZO del autor en DISCO.
        El aprendizaje del "no" es tan valioso como del "sí".
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "patron_rechazado_por_autor",
            "pattern_name": pattern_dict.get("pattern_name", "UNKNOWN"),
            "autor_nota": sig.autor_nota,
            "intent": pattern_dict.get("intent", ""),
            "score_c1": pattern_dict.get("score_c1", 0)
        }
        
        try:
            with open(self.diagnostics_log_path, 'a') as f:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"⚠️  Error registrando rechazo del autor: {e}")
    
    # ========================================================================
    # Lecturas (solo para consulta)
    # ========================================================================
    
    def get_pattern_by_name(self, pattern_name: str) -> Optional[Dict[str, Any]]:
        """Obtiene un patrón por nombre"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM patterns_signed WHERE pattern_name = ?',
                (pattern_name,)
            )
            row = cursor.fetchone()
        
        if not row:
            return None
        
        return self._row_to_dict(row)
    
    def get_patterns_by_confianza(self, min_confianza: int = 80) -> List[Dict[str, Any]]:
        """Obtiene patrones con confianza >= umbral"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM patterns_signed WHERE confianza >= ? ORDER BY confianza DESC',
                (min_confianza,)
            )
            rows = cursor.fetchall()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_all_patterns(self) -> List[Dict[str, Any]]:
        """Obtiene todos los patrones firmados"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM patterns_signed ORDER BY timestamp_stored DESC'
            )
            rows = cursor.fetchall()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_author_decisions(self) -> Dict[str, Any]:
        """Compila estadísticas de decisiones del autor"""
        total_patterns = len(self.get_all_patterns())
        
        rejections = []
        if self.diagnostics_log_path.exists():
            with open(self.diagnostics_log_path, 'r') as f:
                for line in f:
                    if line.strip():
                        rejections.append(json.loads(line))
        
        return {
            "total_patterns_approved": total_patterns,
            "total_patterns_rejected": len(rejections),
            "rejection_rate": len(rejections) / (total_patterns + len(rejections)) 
                            if (total_patterns + len(rejections)) > 0 else 0,
            "recent_rejections": rejections[-5:] if rejections else []
        }
    
    @staticmethod
    def _row_to_dict(row: Tuple) -> Dict[str, Any]:
        """Convierte fila SQLite a diccionario"""
        keys = [
            'pattern_id', 'pattern_name', 'pattern_type', 'origin', 'intent',
            'handlers', 'scene_before', 'scene_after', 'validation_v0', 'score_c1',
            'autor_id', 'autor_aprueba', 'autor_nota', 'timestamp_firma',
            'score_final', 'confianza', 'uses_count', 'timestamp_stored'
        ]
        result = {k: v for k, v in zip(keys, row)}
        
        # Deserializar JSON
        result['handlers'] = json.loads(result['handlers'])
        result['scene_before'] = json.loads(result['scene_before'])
        result['scene_after'] = json.loads(result['scene_after'])
        result['autor_aprueba'] = bool(result['autor_aprueba'])
        
        return result


# ============================================================================
# Ejemplos de uso (documentación)
# ============================================================================

EXAMPLE_USAGE = """
# 1. Crear patrón sin firma → FALLA
pattern_sin_firma = {
    "pattern_name": "cubo_simple",
    "pattern_type": "primitive",
    # ...falta autor_id, autor_aprueba, autor_nota
}

storage = PatternStorageV2()
try:
    storage.save(pattern_sin_firma)
except ValueError as e:
    print(f"❌ {e}")  # BLOCKED: Campo 'autor_id' ausente ...


# 2. Crear patrón CON FIRMA CORRECTA → OK
import os
from core.security.identity import generate_local_key

pattern_firmado = {
    "pattern_name": "cubo_simple_v1",
    "pattern_type": "primitive",
    "origin": "real_execution",
    "intent": "create a simple cube",
    "handlers": ["create_cube"],
    "scene_before": {"objects": 0},
    "scene_after": {"objects": 1},
    "validation_v0": "OK",
    "score_c1": 87.5,
    
    # FIRMA DEL AUTOR
    "autor_id": generate_local_key(),  # Coincide con .zuly_identity.key
    "autor_aprueba": True,              # Voto favorable
    "autor_nota": "Cubo perfecto, listo para reusar"
}

ok, msg = storage.save(pattern_firmado)
print(msg)  # ✓ Patrón 'cubo_simple_v1' guardado con firma válida...


# 3. Autor RECHAZA → Registra rechazo, NO persiste en C2
pattern_rechazado = {
    ...
    "autor_aprueba": False,
    "autor_nota": "Inclinación incorrecta del cubo"
}

ok, msg = storage.save(pattern_rechazado)
print(msg)  # Patrón rechazado por autor. Evento registrado...

# El evento se guardó en bitacora/author_decisions.jsonl, NO en C2


# 4. Consultar patrones de alta confianza
patterns = storage.get_patterns_by_confianza(min_confianza=90)
print(f"Patrones de máxima confianza: {len(patterns)}")


# 5. Ver decisiones del autor
stats = storage.get_author_decisions()
print(f"Aprobados: {stats['total_patterns_approved']}")
print(f"Rechazados: {stats['total_patterns_rejected']}")
"""
