"""
self_assessment.py
==================

AUTO-EVALUACIÓN DE ESCENAS

LYZU mira lo que creó y se pregunta:
"¿Está bien? ¿Qué tan bonito es esto?"

Scoring en múltiples dimensiones:
- Composición (regla de tercios, balance)
- Iluminación (sombras, especulares)
- Contraste (variedad colores/tamaños)
- Simetría (orden vs caos)
- Novedad (qué tan diferente a intentos previos)
- Completitud (escena terminada vs incompleta)

LYZU usa esto para:
1. Evaluar su propio trabajo
2. Comparar estrategias
3. Detectar problemas
4. Auto-mejorar sin esperar feedback
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class SceneQuality(Enum):
    """Nivel de calidad de la escena"""
    POOR = "poor"              # < 40
    FAIR = "fair"              # 40-60
    GOOD = "good"              # 60-75
    VERY_GOOD = "very_good"    # 75-90
    EXCELLENT = "excellent"    # > 90


@dataclass
class AssessmentCriteria:
    """Criterios individuales de evaluación"""
    composition_score: float        # 0-100
    lighting_score: float           # 0-100
    contrast_score: float           # 0-100
    symmetry_score: float           # 0-100
    novelty_score: float            # 0-100
    completeness_score: float       # 0-100
    aesthetic_harmony: float        # 0-100


@dataclass
class SceneAssessment:
    """Evaluación completa de una escena"""
    overall_score: float
    quality_level: SceneQuality
    criteria: AssessmentCriteria
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    confidence: float  # 0-1: qué tan seguro está de la evaluación


class SelfAssessmentEngine:
    """
    Motor de auto-evaluación.
    LYZU evalúa sus propias creaciones.
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.assessment_history: List[Dict] = []
        self.improvement_suggestions: Dict[str, float] = {}  # suggestion -> frequency
    
    def _log(self, message: str):
        if self.verbose:
            print(f"[ASSESSMENT] {message}")
    
    def assess_scenario(
        self,
        num_objects: int,
        has_lights: bool,
        num_lights: int,
        has_materials: bool,
        has_camera: bool,
        num_modifiers: int,
        is_novel: bool,
        previous_scores: Optional[List[float]] = None
    ) -> SceneAssessment:
        """
        Evalúa una escena basada en parámetros.
        
        Args:
            num_objects: Cantidad de objetos en escena
            has_lights: ¿Hay luces?
            num_lights: Cuántas luces
            has_materials: ¿Hay materiales aplicados?
            has_camera: ¿Hay cámara posicionada?
            num_modifiers: Cuántos modificadores aplicados
            is_novel: ¿Es una estrategia nueva/diferente?
            previous_scores: Scores de intentos previos (para comparar)
        """
        self._log(f"🔍 Evaluando escena...")
        
        # Calcular cada criterio
        composition = self._assess_composition(num_objects, num_modifiers)
        lighting = self._assess_lighting(has_lights, num_lights)
        contrast = self._assess_contrast(num_objects, has_materials, num_modifiers)
        symmetry = self._assess_symmetry(num_objects)
        novelty = self._assess_novelty(is_novel, previous_scores)
        completeness = self._assess_completeness(has_lights, has_materials, has_camera)
        harmony = self._assess_aesthetic_harmony(
            composition, lighting, contrast, symmetry
        )
        
        # Crear criteria
        criteria = AssessmentCriteria(
            composition_score=composition,
            lighting_score=lighting,
            contrast_score=contrast,
            symmetry_score=symmetry,
            novelty_score=novelty,
            completeness_score=completeness,
            aesthetic_harmony=harmony
        )
        
        # Score general (ponderado)
        overall = (
            composition * 0.25 +        # 25% composición
            lighting * 0.20 +           # 20% iluminación
            contrast * 0.15 +           # 15% contraste
            symmetry * 0.10 +           # 10% simetría
            novelty * 0.15 +            # 15% novedad
            completeness * 0.10 +       # 10% completitud
            harmony * 0.05              # 5% armonía
        )
        
        # Determinar nivel de calidad
        if overall > 90:
            quality = SceneQuality.EXCELLENT
        elif overall > 75:
            quality = SceneQuality.VERY_GOOD
        elif overall > 60:
            quality = SceneQuality.GOOD
        elif overall > 40:
            quality = SceneQuality.FAIR
        else:
            quality = SceneQuality.POOR
        
        # Identificar fortalezas y debilidades
        strengths, weaknesses = self._identify_strengths_weaknesses(criteria)
        recommendations = self._generate_recommendations(weaknesses, criteria)
        
        # Calcular confianza
        confidence = self._calculate_confidence(criteria)
        
        assessment = SceneAssessment(
            overall_score=overall,
            quality_level=quality,
            criteria=criteria,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            confidence=confidence
        )
        
        # Log
        self._log(f"✓ Score: {overall:.1f}/100 ({quality.value})")
        self._log(f"  Composición: {composition:.0f}  |  Iluminación: {lighting:.0f}")
        self._log(f"  Contraste: {contrast:.0f}  |  Simetría: {symmetry:.0f}")
        
        # Guardar en historial
        self.assessment_history.append({
            'overall_score': overall,
            'quality': quality.value,
            'criteria': {
                'composition': composition,
                'lighting': lighting,
                'contrast': contrast,
                'symmetry': symmetry,
                'novelty': novelty,
                'completeness': completeness
            }
        })
        
        return assessment
    
    def compare_assessments(
        self,
        assessment1: SceneAssessment,
        assessment2: SceneAssessment
    ) -> Dict[str, any]:
        """
        Compara dos evaluaciones.
        LYZU identifica cuál es mejor y por qué.
        """
        score_diff = assessment2.overall_score - assessment1.overall_score
        
        # Identificar dimensiones donde mejoró
        improvements = {}
        criteria1 = assessment1.criteria
        criteria2 = assessment2.criteria
        
        if criteria2.composition_score > criteria1.composition_score:
            improvements['composicion'] = criteria2.composition_score - criteria1.composition_score
        
        if criteria2.lighting_score > criteria1.lighting_score:
            improvements['iluminacion'] = criteria2.lighting_score - criteria1.lighting_score
        
        if criteria2.contrast_score > criteria1.contrast_score:
            improvements['contraste'] = criteria2.contrast_score - criteria1.contrast_score
        
        if criteria2.novelty_score > criteria1.novelty_score:
            improvements['novedad'] = criteria2.novelty_score - criteria1.novelty_score
        
        # Generar resumen
        if score_diff > 10:
            result = "SIGNIFICATIVAMENTE MEJOR"
        elif score_diff > 3:
            result = "MEJOR"
        elif score_diff > -3:
            result = "SIMILAR"
        elif score_diff > -10:
            result = "PEOR"
        else:
            result = "SIGNIFICATIVAMENTE PEOR"
        
        return {
            'assessment1_score': assessment1.overall_score,
            'assessment2_score': assessment2.overall_score,
            'difference': score_diff,
            'verdict': result,
            'improvements': improvements,
            'reason': self._explain_comparison(assessment1, assessment2)
        }
    
    # ========== CRITERIOS DE EVALUACIÓN ==========
    
    def _assess_composition(self, num_objects: int, num_modifiers: int) -> float:
        """
        Evalúa composición (0-100).
        
        Criterios:
        - 1 objeto simple: baja (30)
        - 2-3 objetos: media (60)
        - 4-5 objetos: buena (75)
        - 5+ objetos complejos: excelente (90)
        """
        base_score = min(num_objects * 15, 70)  # Bonus por cantidad
        modifier_bonus = num_modifiers * 5       # Bonus por complejidad
        
        return min(base_score + modifier_bonus, 100.0)
    
    def _assess_lighting(self, has_lights: bool, num_lights: int) -> float:
        """
        Evalúa iluminación (0-100).
        
        Sin luces: 20 (muy oscuro, problema)
        1 luz: 50 (básico)
        2+ luces: 75+ (bueno)
        3+ luces variadas: 90+ (excelente)
        """
        if not has_lights:
            return 20.0  # Crítico: sin iluminación
        
        if num_lights == 1:
            return 50.0
        elif num_lights == 2:
            return 75.0
        elif num_lights >= 3:
            return 90.0
        
        return 50.0
    
    def _assess_contrast(self, num_objects: int, has_materials: bool, num_modifiers: int) -> float:
        """
        Evalúa contraste visual (0-100).
        
        Basado en:
        - Variedad de objetos
        - Materiales diferentes
        - Modificadores (crean variedad visual)
        """
        base_score = 30.0
        
        # Bonus por objetos
        base_score += num_objects * 10
        
        # Bonus por materiales
        if has_materials:
            base_score += 20
        
        # Bonus por complejidad
        base_score += num_modifiers * 5
        
        return min(base_score, 100.0)
    
    def _assess_symmetry(self, num_objects: int) -> float:
        """
        Evalúa simetría (0-100).
        
        Nota: Esto es complejo en realidad,
        aquí es una aproximación simple.
        """
        # Arrays simétricos = buena simetría
        if num_objects % 2 == 0:  # Número par sugiere simetría
            return 65.0
        else:
            return 50.0
    
    def _assess_novelty(self, is_novel: bool, previous_scores: Optional[List[float]] = None) -> float:
        """
        Evalúa novedad (0-100).
        
        ¿Es diferente a intentos previos?
        """
        if not is_novel:
            return 40.0  # No es nuevo
        
        if previous_scores and len(previous_scores) > 0:
            avg_previous = sum(previous_scores) / len(previous_scores)
            if avg_previous > 70:
                return 70.0  # Diferente pero estándar
            else:
                return 85.0  # Diferente y mejor que promedio
        
        return 75.0
    
    def _assess_completeness(self, has_lights: bool, has_materials: bool, has_camera: bool) -> float:
        """
        Evalúa si la escena está "completa" (0-100).
        
        Checklist:
        - ¿Tiene iluminación?
        - ¿Tiene materiales?
        - ¿Tiene cámara?
        """
        score = 30.0  # Base mínima
        
        if has_lights:
            score += 30
        
        if has_materials:
            score += 25
        
        if has_camera:
            score += 15
        
        return min(score, 100.0)
    
    def _assess_aesthetic_harmony(
        self,
        composition: float,
        lighting: float,
        contrast: float,
        symmetry: float
    ) -> float:
        """
        Evalúa armonía estética (0-100).
        
        ¿Los elementos trabajan bien juntos?
        """
        # Si todos los scores son altos y similares = armonía
        scores = [composition, lighting, contrast, symmetry]
        avg = sum(scores) / len(scores)
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        
        # Menos varianza = más armonía
        harmony = max(0, 100 - (variance / 10))
        return harmony
    
    # ========== ANÁLISIS ==========
    
    def _identify_strengths_weaknesses(self, criteria: AssessmentCriteria) -> Tuple[List[str], List[str]]:
        """Identifica fortalezas y debilidades"""
        strengths = []
        weaknesses = []
        
        # Fortalezas
        if criteria.composition_score > 70:
            strengths.append("Composición bien estructurada")
        if criteria.lighting_score > 70:
            strengths.append("Iluminación profesional")
        if criteria.contrast_score > 70:
            strengths.append("Buen contraste visual")
        if criteria.aesthetic_harmony > 70:
            strengths.append("Armonía estética equilibrada")
        if criteria.novelty_score > 70:
            strengths.append("Diseño innovador y diferente")
        
        # Debilidades
        if criteria.composition_score < 50:
            weaknesses.append("Composición simple, agregar variedad")
        if criteria.lighting_score < 50:
            weaknesses.append("Iluminación insuficiente o pobre")
        if criteria.contrast_score < 50:
            weaknesses.append("Poco contraste visual, todo muy similar")
        if criteria.completeness_score < 50:
            weaknesses.append("Escena incompleta, faltan elementos")
        
        return strengths, weaknesses
    
    def _generate_recommendations(self, weaknesses: List[str], criteria: AssessmentCriteria) -> List[str]:
        """Genera recomendaciones basadas en debilidades"""
        recommendations = []
        
        if criteria.lighting_score < 50:
            recommendations.append("💡 Agregar más luces o ajustar energía")
        
        if criteria.composition_score < 50:
            recommendations.append("🎨 Crear composición más interesante (array, múltiples objetos)")
        
        if criteria.contrast_score < 50:
            recommendations.append("🌈 Aplicar materiales con diferentes colores")
        
        if criteria.completeness_score < 60:
            recommendations.append("🎬 Posicionar cámara para mejor presentación")
        
        if not recommendations:
            recommendations.append("✨ Escena evaluada positivamente, considera experimentar variaciones")
        
        return recommendations
    
    def _calculate_confidence(self, criteria: AssessmentCriteria) -> float:
        """
        Calcula confianza de la evaluación (0-1).
        
        Si todos los criterios tienen scores similares = alta confianza.
        Si varían mucho = baja confianza (escena confusa).
        """
        scores = [
            criteria.composition_score,
            criteria.lighting_score,
            criteria.contrast_score,
            criteria.symmetry_score,
            criteria.completeness_score
        ]
        
        avg = sum(scores) / len(scores)
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        
        # Convertir varianza a confianza (0-1)
        confidence = 1.0 - min(variance / 1000, 1.0)
        return confidence
    
    def _explain_comparison(self, a1: SceneAssessment, a2: SceneAssessment) -> str:
        """Explica por qué una escena es mejor que otra"""
        reasons = []
        
        c1, c2 = a1.criteria, a2.criteria
        
        if c2.lighting_score > c1.lighting_score + 15:
            reasons.append("iluminación mejorada")
        
        if c2.composition_score > c1.composition_score + 15:
            reasons.append("mejor composición")
        
        if c2.contrast_score > c1.contrast_score + 15:
            reasons.append("mayor contraste visual")
        
        if c2.completeness_score > c1.completeness_score + 15:
            reasons.append("escena más completa")
        
        return "; ".join(reasons) if reasons else "cambios generales"
    
    def get_history_summary(self) -> Dict:
        """Resumen del historial de evaluaciones"""
        if not self.assessment_history:
            return {'assessments': 0}
        
        scores = [a['overall_score'] for a in self.assessment_history]
        
        return {
            'total_assessments': len(self.assessment_history),
            'average_score': sum(scores) / len(scores),
            'best_score': max(scores),
            'worst_score': min(scores),
            'improvement_trend': scores[-1] - scores[0] if len(scores) > 1 else 0
        }
