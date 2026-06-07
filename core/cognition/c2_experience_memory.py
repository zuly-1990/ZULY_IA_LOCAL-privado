"""
C2 - Memoria de Experiencias
=============================

Parte del Plan C (Cognición Base) - Fase de Aprendizaje

Responsabilidades:
1. Guardar experiencias (evaluaciones de C1)
2. Extraer aprendizajes automáticamente
3. Buscar patrones en historial
4. Proponer mejoras basadas en datos

Componentes:
- ExperienceStorage: Persistencia de experiencias
- ExperienceExtractor: Extrae patrones y conclusiones
- PatternMatcher: Encuentra casos similares
- HeuristicBuilder: Construye reglas de aprendizaje
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from collections import Counter
import hashlib


class ExperienceType(Enum):
    """Tipos de experiencias que se pueden guardar"""
    SUCCESS = "success"              # Comando exitoso
    PARTIAL = "partial"              # Éxito parcial
    FAILED = "failed"                # Fracaso
    LEARNING = "learning"            # Lección aprendida


class MemoryStrategy(Enum):
    """Estrategias de búsqueda en memoria"""
    EXACT = "exact"                  # Búsqueda exacta
    SIMILAR = "similar"              # Búsqueda por similitud
    PATTERN = "pattern"              # Búsqueda por patrón
    HEURISTIC = "heuristic"          # Aplicar heurística


@dataclass
class Experience:
    """Una experiencia grabada"""
    objective: str                    # Qué se intentó hacer
    evaluation_status: str            # SUCCESS/PARTIAL/FAILED
    evaluation_score: float           # Score numérico
    parameters: Dict[str, Any]        # Parámetros usados
    metrics_passed: int               # Métricas que pasaron
    metrics_total: int                # Total de métricas
    issues: List[str] = field(default_factory=list)      # Problemas encontrados
    recommendations: List[str] = field(default_factory=list)  # Recomendaciones
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def similarity_hash(self) -> str:
        """Hash para buscar experiencias similares (ignora timestamp)"""
        key = f"{self.objective}_{self.evaluation_status}"
        return hashlib.md5(key.encode()).hexdigest()[:8]


@dataclass
class Learning:
    """Una conclusión o regla aprendida"""
    pattern: str                      # Patrón identificado
    rule: str                         # Regla derivada
    confidence: float                 # 0.0 a 1.0
    frequency: int                    # Cuántas veces se vio
    applicable_to: List[str] = field(default_factory=list)  # Casos aplicables
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class ExperienceStorage:
    """Almacena experiencias en SQLite"""
    
    def __init__(self, db_path: str = 'bitacora/memory.db'):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Crea tablas si no existen"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS experiences (
                    id INTEGER PRIMARY KEY,
                    objective TEXT NOT NULL,
                    evaluation_status TEXT NOT NULL,
                    evaluation_score REAL NOT NULL,
                    parameters TEXT NOT NULL,
                    metrics_passed INTEGER NOT NULL,
                    metrics_total INTEGER NOT NULL,
                    issues TEXT,
                    recommendations TEXT,
                    timestamp TEXT NOT NULL,
                    similarity_hash TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS learnings (
                    id INTEGER PRIMARY KEY,
                    pattern TEXT NOT NULL UNIQUE,
                    rule TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    frequency INTEGER NOT NULL,
                    applicable_to TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_status 
                ON experiences(evaluation_status)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_hash 
                ON experiences(similarity_hash)
            ''')
            
            conn.commit()
    
    def save_experience(self, experience: Experience) -> int:
        """Guarda una experiencia y retorna su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO experiences 
                (objective, evaluation_status, evaluation_score, parameters,
                 metrics_passed, metrics_total, issues, recommendations, 
                 timestamp, similarity_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                experience.objective,
                experience.evaluation_status,
                experience.evaluation_score,
                json.dumps(experience.parameters),
                experience.metrics_passed,
                experience.metrics_total,
                json.dumps(experience.issues),
                json.dumps(experience.recommendations),
                experience.timestamp,
                experience.similarity_hash()
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_experiences(self) -> List[Experience]:
        """Obtiene todas las experiencias"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT * FROM experiences ORDER BY timestamp DESC')
            rows = cursor.fetchall()
        
        experiences = []
        for row in rows:
            exp = Experience(
                objective=row[1],
                evaluation_status=row[2],
                evaluation_score=row[3],
                parameters=json.loads(row[4]),
                metrics_passed=row[5],
                metrics_total=row[6],
                issues=json.loads(row[7]) if row[7] else [],
                recommendations=json.loads(row[8]) if row[8] else [],
                timestamp=row[9]
            )
            experiences.append(exp)
        
        return experiences
    
    def get_experiences_by_status(self, status: str) -> List[Experience]:
        """Obtiene experiencias por estado"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM experiences WHERE evaluation_status = ? ORDER BY timestamp DESC',
                (status,)
            )
            rows = cursor.fetchall()
        
        experiences = []
        for row in rows:
            exp = Experience(
                objective=row[1],
                evaluation_status=row[2],
                evaluation_score=row[3],
                parameters=json.loads(row[4]),
                metrics_passed=row[5],
                metrics_total=row[6],
                issues=json.loads(row[7]) if row[7] else [],
                recommendations=json.loads(row[8]) if row[8] else [],
                timestamp=row[9]
            )
            experiences.append(exp)
        
        return experiences
    
    def get_recent_experiences(self, days: int = 7) -> List[Experience]:
        """Obtiene experiencias de los últimos N días"""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM experiences WHERE timestamp > ? ORDER BY timestamp DESC',
                (cutoff,)
            )
            rows = cursor.fetchall()
        
        experiences = []
        for row in rows:
            exp = Experience(
                objective=row[1],
                evaluation_status=row[2],
                evaluation_score=row[3],
                parameters=json.loads(row[4]),
                metrics_passed=row[5],
                metrics_total=row[6],
                issues=json.loads(row[7]) if row[7] else [],
                recommendations=json.loads(row[8]) if row[8] else [],
                timestamp=row[9]
            )
            experiences.append(exp)
        
        return experiences


class ExperienceExtractor:
    """Extrae aprendizajes de experiencias"""
    
    @staticmethod
    def extract_common_issues(experiences: List[Experience]) -> Dict[str, int]:
        """Identifica los problemas más comunes"""
        issues = []
        for exp in experiences:
            issues.extend(exp.issues)
        
        return dict(Counter(issues).most_common(10))
    
    @staticmethod
    def extract_successful_patterns(experiences: List[Experience]) -> List[Dict[str, Any]]:
        """Extrae patrones de casos exitosos"""
        successful = [e for e in experiences if e.evaluation_status == 'success']
        
        patterns = []
        for exp in successful:
            patterns.append({
                'objective': exp.objective,
                'parameters': exp.parameters,
                'score': exp.evaluation_score,
                'recommendations': exp.recommendations
            })
        
        return sorted(patterns, key=lambda x: x['score'], reverse=True)[:5]
    
    @staticmethod
    def extract_failure_reasons(experiences: List[Experience]) -> Dict[str, int]:
        """Analiza por qué fallaron los comandos"""
        failures = [e for e in experiences if e.evaluation_status == 'failed']
        
        reasons = {}
        for exp in failures:
            if exp.issues:
                reason = exp.issues[0]  # Primera razón
                reasons[reason] = reasons.get(reason, 0) + 1
        
        return dict(sorted(reasons.items(), key=lambda x: x[1], reverse=True))
    
    @staticmethod
    def calculate_success_rate(experiences: List[Experience]) -> float:
        """Calcula tasa de éxito"""
        if not experiences:
            return 0.0
        
        successes = sum(1 for e in experiences if e.evaluation_status in ['success', 'partial'])
        return successes / len(experiences)
    
    @staticmethod
    def calculate_average_score(experiences: List[Experience]) -> float:
        """Calcula score promedio"""
        if not experiences:
            return 0.0
        
        return sum(e.evaluation_score for e in experiences) / len(experiences)


class PatternMatcher:
    """Busca patrones y experiencias similares"""
    
    @staticmethod
    def find_similar_experiences(objective: str, 
                                experiences: List[Experience],
                                threshold: float = 0.7) -> List[Tuple[Experience, float]]:
        """Encuentra experiencias similares por objetivo"""
        similar = []
        
        obj_lower = objective.lower()
        
        for exp in experiences:
            exp_lower = exp.objective.lower()
            
            # Similitud simple: palabras en común
            obj_words = set(obj_lower.split())
            exp_words = set(exp_lower.split())
            
            if not obj_words or not exp_words:
                continue
            
            intersection = len(obj_words & exp_words)
            union = len(obj_words | exp_words)
            similarity = intersection / union if union > 0 else 0
            
            if similarity >= threshold:
                similar.append((exp, similarity))
        
        return sorted(similar, key=lambda x: x[1], reverse=True)
    
    @staticmethod
    def find_failed_cases_for_objective(objective: str,
                                       experiences: List[Experience]) -> List[Experience]:
        """Encuentra casos donde este objetivo falló"""
        failed = []
        obj_lower = objective.lower()
        
        for exp in experiences:
            if exp.evaluation_status == 'failed':
                exp_lower = exp.objective.lower()
                if obj_lower in exp_lower or exp_lower in obj_lower:
                    failed.append(exp)
        
        return failed


class HeuristicBuilder:
    """Construye heurísticas/reglas a partir de experiencias"""
    
    @staticmethod
    def build_parameter_heuristics(experiences: List[Experience]) -> Dict[str, Any]:
        """Construye heurísticas sobre parámetros que funcionan"""
        successful = [e for e in experiences if e.evaluation_status == 'success']
        
        if not successful:
            return {}
        
        heuristics = {}
        
        # Analizar parámetros más frecuentes en casos exitosos
        for exp in successful:
            for key, value in exp.parameters.items():
                if key not in heuristics:
                    heuristics[key] = Counter()
                heuristics[key][value] += 1
        
        # Convertir a recomendaciones
        recommendations = {}
        for key, counter in heuristics.items():
            if counter:
                most_common = counter.most_common(1)[0][0]
                recommendations[key] = most_common
        
        return recommendations
    
    @staticmethod
    def build_improvement_suggestions(objective: str,
                                     experiences: List[Experience]) -> List[str]:
        """Sugiere mejoras basadas en intentos previos"""
        suggestions = []
        
        # Buscar casos similares
        similar = PatternMatcher.find_similar_experiences(objective, experiences)
        
        for similar_exp, similarity in similar[:3]:  # Top 3
            if similar_exp.recommendations:
                for rec in similar_exp.recommendations[:2]:  # Top 2 recomendaciones
                    if rec not in suggestions:
                        suggestions.append(f"({similarity:.0%}) {rec}")
        
        return suggestions


class C2ExperienceMemory:
    """
    Memory Principal (C2)
    
    Orquesta almacenamiento, extracción y búsqueda de experiencias.
    """
    
    def __init__(self, db_path: str = 'bitacora/memory.db'):
        self.storage = ExperienceStorage(db_path)
        self.extractor = ExperienceExtractor()
        self.matcher = PatternMatcher()
        self.heuristic_builder = HeuristicBuilder()
    
    def record_experience(self, objective: str, evaluation: Dict[str, Any]) -> int:
        """
        Registra una experiencia de C1.
        
        Args:
            objective: Qué se intentó hacer
            evaluation: Resultado de C1 (status, score, metrics, etc)
            
        Returns:
            ID de la experiencia guardada
        """
        experience = Experience(
            objective=objective,
            evaluation_status=evaluation.get('status', 'unknown'),
            evaluation_score=evaluation.get('score', 0.0),
            parameters=evaluation.get('parameters', {}),
            metrics_passed=evaluation.get('metrics_passed', 0),
            metrics_total=evaluation.get('metrics_total', 0),
            issues=evaluation.get('issues', []),
            recommendations=evaluation.get('recommendations', [])
        )
        
        return self.storage.save_experience(experience)
    
    def get_insights(self, limit_days: int = 7) -> Dict[str, Any]:
        """
        Obtiene insights del historial reciente.
        
        Returns:
            Diccionario con análisis de experiencias
        """
        experiences = self.storage.get_recent_experiences(limit_days)
        
        if not experiences:
            return {
                'total_experiences': 0,
                'message': 'No hay experiencias en el período'
            }
        
        return {
            'total_experiences': len(experiences),
            'success_rate': self.extractor.calculate_success_rate(experiences),
            'average_score': self.extractor.calculate_average_score(experiences),
            'successes': len([e for e in experiences if e.evaluation_status == 'success']),
            'failures': len([e for e in experiences if e.evaluation_status == 'failed']),
            'common_issues': self.extractor.extract_common_issues(experiences),
            'failure_reasons': self.extractor.extract_failure_reasons(experiences),
            'top_patterns': self.extractor.extract_successful_patterns(experiences)
        }
    
    def get_suggestions_for(self, objective: str) -> Dict[str, Any]:
        """
        Obtiene sugerencias basadas en experiencias previas.
        
        Args:
            objective: El objetivo para el cual se quieren sugerencias
            
        Returns:
            Diccionario con sugerencias y experiencias similares
        """
        all_experiences = self.storage.get_all_experiences()
        
        # Buscar casos similares
        similar = self.matcher.find_similar_experiences(objective, all_experiences)
        
        # Buscar casos que fallaron
        failed = self.matcher.find_failed_cases_for_objective(objective, all_experiences)
        
        # Construir sugerencias
        improvements = self.heuristic_builder.build_improvement_suggestions(objective, all_experiences)
        parameters = self.heuristic_builder.build_parameter_heuristics(all_experiences)
        
        return {
            'objective': objective,
            'similar_experiences': len(similar),
            'failed_attempts': len(failed),
            'suggested_parameters': parameters,
            'improvement_suggestions': improvements[:5],
            'failed_reasons': [f.issues[0] if f.issues else 'Unknown' for f in failed[:3]]
        }
    
    def get_all_learnings(self) -> List[Dict[str, Any]]:
        """Obtiene todas las lecciones aprendidas"""
        experiences = self.storage.get_all_experiences()
        
        learnings = []
        
        # Lecciones sobre éxito
        if self.extractor.calculate_success_rate(experiences) > 0.7:
            learnings.append({
                'type': 'positive',
                'learning': 'Alta tasa de éxito detectada',
                'confidence': self.extractor.calculate_success_rate(experiences)
            })
        
        # Lecciones sobre problemas comunes
        common_issues = self.extractor.extract_common_issues(experiences)
        if common_issues:
            top_issue = list(common_issues.items())[0]
            learnings.append({
                'type': 'problem',
                'learning': f'Problema frecuente: {top_issue[0]}',
                'frequency': top_issue[1],
                'confidence': top_issue[1] / len(experiences)
            })
        
        return learnings
    
    def export_memory(self, filepath: Path) -> bool:
        """Exporta memoria a JSON"""
        try:
            experiences = self.storage.get_all_experiences()
            insights = self.get_insights(limit_days=30)
            
            data = {
                'exported_at': datetime.now().isoformat(),
                'total_experiences': len(experiences),
                'insights': insights,
                'learnings': self.get_all_learnings(),
                'recent_experiences': [e.to_dict() for e in experiences[:10]]
            }
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exportando memoria: {e}")
            return False
