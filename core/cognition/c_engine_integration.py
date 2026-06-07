"""
core/cognition/c_engine_integration.py
=======================================

INTEGRACIÓN: TheCubeUniverseEngine v20 ↔ ZULY

Conecta el framework de precisión matemática (TheCubeUniverseEngine)
con los cerebros cognitivos de ZULY:

- C1 (Evaluador): Valida viabilidad física (masa, densidad)
- C3 (Objetivos): Descompone tareas en logística (viajes, toneladas)
- C2 (Patrones): Usa átomo 0.137mm como unidad mínima

Este módulo es el PUENTE que convierte a ZULY de "herramienta de dibujo"
a "sistema de ingeniería preciso".
"""

import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ConstructionViability(Enum):
    """Estados de viabilidad de construcción"""
    VIABLE = "viable"                  # Proyecto realista/posible
    MARGINAL = "marginal"              # Necesita optimización
    UNFEASIBLE = "unfeasible"          # No es viable
    UNKNOWN = "unknown"                # No se puede evaluar


@dataclass
class PhysicalProperties:
    """Propiedades físicas de un objeto en el universo"""
    volume_m3: float                    # Volumen en metros cúbicos
    mass_kg: float                      # Masa en kilogramos
    mass_toneladas: float              # Masa en toneladas
    density_kgm3: float                # Densidad (default 2400 para hormigón)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "volumen_m3": round(self.volume_m3, 4),
            "masa_kg": round(self.mass_kg, 2),
            "masa_ton": round(self.mass_toneladas, 2),
            "densidad_kgm3": self.density_kgm3
        }


@dataclass
class LogisticEstimate:
    """Estimación logística para construcción"""
    volume_m3: float                    # Volumen total
    mass_toneladas: float              # Masa total
    double_truck_capacity: float = 28.0  # Capacidad de dobletroque (toneladas)
    truck_trips: int = 0                # Viajes necesarios
    cost_per_trip_usd: float = 1500.0  # Costo por viaje (USD)
    total_cost_usd: float = 0.0        # Costo total estimado
    
    def __post_init__(self):
        self.truck_trips = math.ceil(self.mass_toneladas / self.double_truck_capacity)
        self.total_cost_usd = self.truck_trips * self.cost_per_trip_usd
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "volumen_m3": round(self.volume_m3, 2),
            "masa_toneladas": round(self.mass_toneladas, 2),
            "viajes_dobletroque": self.truck_trips,
            "costo_estimado_usd": round(self.total_cost_usd, 2),
            "costo_por_viaje": self.cost_per_trip_usd
        }


class EngineIntegration:
    """
    Integración de TheCubeUniverseEngine con ZULY
    
    Proporciona:
    - Evaluación C1: ¿Es viable este proyecto?
    - Descomposición C3: ¿Cuántos viajes necesito? ¿Cuál es el costo?
    - Patrón C2: Unidad mínima = Átomo 0.137mm
    """
    
    # Constantes del engine
    ATOM_SIZE_MM = 0.137
    ATOM_SIZE_M = ATOM_SIZE_MM / 1000.0
    DEFAULT_DENSITY = 2400.0  # kg/m³ (hormigón)
    DOUBLE_TRUCK_CAPACITY = 28.0  # toneladas
    
    def __init__(self):
        self.projects: Dict[str, Dict[str, Any]] = {}
        self.evaluation_history: List[Dict[str, Any]] = []
    
    # ========== C1 EVALUADOR: VIABILIDAD FÍSICA ==========
    
    def calculate_physical_properties(
        self,
        volume_m3: float,
        density_kgm3: float = DEFAULT_DENSITY
    ) -> PhysicalProperties:
        """
        Calcula propiedades físicas de un volumen.
        
        Args:
            volume_m3: Volumen en metros cúbicos
            density_kgm3: Densidad del material (default: hormigón 2400)
            
        Returns:
            PhysicalProperties con masa, densidad, etc.
        """
        mass_kg = volume_m3 * density_kgm3
        mass_toneladas = mass_kg / 1000.0
        
        return PhysicalProperties(
            volume_m3=volume_m3,
            mass_kg=mass_kg,
            mass_toneladas=mass_toneladas,
            density_kgm3=density_kgm3
        )
    
    def evaluate_viability(
        self,
        volume_m3: float,
        max_mass_toneladas: Optional[float] = None,
        density_kgm3: float = DEFAULT_DENSITY
    ) -> Dict[str, Any]:
        """
        C1 EVALUADOR: Determina si un proyecto es viable.
        
        Args:
            volume_m3: Volumen a construir
            max_mass_toneladas: Límite máximo de masa (None = sin límite)
            density_kgm3: Densidad del material
            
        Returns:
            Dict con viabilidad, propiedades, recomendaciones
        """
        props = self.calculate_physical_properties(volume_m3, density_kgm3)
        
        viability = ConstructionViability.VIABLE
        warnings = []
        recommendations = []
        
        # Criterios de viabilidad
        if props.mass_toneladas > 100000:
            viability = ConstructionViability.MARGINAL
            warnings.append("Masa muy grande (> 100,000 toneladas) - requiere análisis geotécnico")
        
        if max_mass_toneladas and props.mass_toneladas > max_mass_toneladas:
            viability = ConstructionViability.UNFEASIBLE
            warnings.append(f"Supera masa máxima permitida ({max_mass_toneladas}t)")
            recommendations.append(f"Reducir volumen a {max_mass_toneladas * 1000 / density_kgm3:.2f}m³")
        
        if props.mass_toneladas > 5000:
            recommendations.append("Considerar subestructura de soporte adicional")
        
        evaluation = {
            "viability": viability.value,
            "properties": props.to_dict(),
            "warnings": warnings,
            "recommendations": recommendations,
            "timestamp": self._get_timestamp()
        }
        
        self.evaluation_history.append(evaluation)
        return evaluation
    
    # ========== C3 OBJETIVOS: DESCOMPOSICIÓN LOGÍSTICA ==========
    
    def decompose_construction_task(
        self,
        volume_m3: float,
        task_name: str = "Construcción",
        density_kgm3: float = DEFAULT_DENSITY
    ) -> Dict[str, Any]:
        """
        C3 OBJETIVOS: Descompone un proyecto en subtareas logísticas.
        
        Ejemplo:
            "Construir base en Guayatá de 450m³"
            → 1,080 toneladas
            → 38 viajes de dobletroque
            → 3-4 semanas (estimado)
        
        Args:
            volume_m3: Volumen a construir
            task_name: Nombre del proyecto
            density_kgm3: Densidad del material
            
        Returns:
            Dict con descomposición de tareas logísticas
        """
        props = self.calculate_physical_properties(volume_m3, density_kgm3)
        logistic = LogisticEstimate(
            volume_m3=volume_m3,
            mass_toneladas=props.mass_toneladas
        )
        
        # Estimar duración (basado en viajes)
        days_per_trip = 0.5  # 2 viajes por día típico
        est_days = logistic.truck_trips * days_per_trip
        est_weeks = est_days / 7
        
        subtasks = [
            {
                "id": "logistics_plan",
                "name": "Planificación logística",
                "description": f"Plan de {logistic.truck_trips} viajes de dobletroque",
                "duration_days": 2,
                "cost_usd": 5000
            },
            {
                "id": "site_preparation",
                "name": "Preparación de sitio",
                "description": "Limpieza, nivelación, drenaje",
                "duration_days": 3,
                "cost_usd": 15000
            },
            {
                "id": "material_transport",
                "name": "Transporte de material",
                "description": f"{logistic.truck_trips} viajes ({logistic.mass_toneladas}t total)",
                "duration_days": est_days,
                "cost_usd": logistic.total_cost_usd
            },
            {
                "id": "construction",
                "name": "Construcción",
                "description": f"Colocación de {volume_m3}m³ de material",
                "duration_days": est_days * 1.5,  # Más lento que transporte
                "cost_usd": volume_m3 * 500  # $500 por m³ típico
            },
            {
                "id": "finishing",
                "name": "Acabado",
                "description": "Compactación, acabados finales",
                "duration_days": 5,
                "cost_usd": 25000
            }
        ]
        
        total_cost = sum(t["cost_usd"] for t in subtasks)
        total_days = sum(t["duration_days"] for t in subtasks)
        
        return {
            "task_name": task_name,
            "decomposition": {
                "physical_properties": props.to_dict(),
                "logistics": logistic.to_dict(),
                "estimations": {
                    "duration_days": round(total_days, 1),
                    "duration_weeks": round(total_weeks := total_days/7, 1),
                    "total_cost_usd": round(total_cost, 2),
                    "cost_per_m3": round(total_cost / volume_m3, 2)
                },
                "subtasks": subtasks
            },
            "timestamp": self._get_timestamp()
        }
    
    # ========== C2 PATRONES: UNIDAD MÍNIMA ==========
    
    def get_atom_info(self) -> Dict[str, Any]:
        """
        C2 PATRONES: Información del átomo (unidad mínima).
        
        El átomo de 0.137mm es la unidad de precisión mínima
        en toda la arquitectura de ZULY.
        """
        atom_volume = self.ATOM_SIZE_M ** 3
        atom_mass = atom_volume * self.DEFAULT_DENSITY
        
        return {
            "name": "Átomo Base ZULY",
            "size_mm": self.ATOM_SIZE_MM,
            "size_m": self.ATOM_SIZE_M,
            "size_micrometers": self.ATOM_SIZE_MM * 1000,
            "volume_m3": atom_volume,
            "volume_cm3": atom_volume * 1e6,
            "mass_kg": atom_mass,
            "mass_g": atom_mass * 1000,
            "purpose": "Unidad mínima de precisión para todos los patrones"
        }
    
    def atoms_needed_for_volume(self, volume_m3: float) -> int:
        """Calcula cuántos átomos se necesitan para llenar un volumen"""
        atom_volume = self.ATOM_SIZE_M ** 3
        return int(volume_m3 / atom_volume)
    
    def pattern_from_volume(self, volume_m3: float) -> Dict[str, Any]:
        """
        Convierte un volumen en un patrón con unidades atómicas.
        
        Útil para C2: Ver un diseño en términos del patrón atómico.
        """
        atom_count = self.atoms_needed_for_volume(volume_m3)
        atoms_per_side = round(atom_count ** (1/3))
        
        return {
            "volume_m3": volume_m3,
            "total_atoms": atom_count,
            "atoms_per_side": atoms_per_side,
            "atom_size_mm": self.ATOM_SIZE_MM,
            "equivalent_cube_side_m": atoms_per_side * self.ATOM_SIZE_M,
            "message": f"Volumen = {atom_count:,} átomos de 0.137mm"
        }
    
    # ========== UTILIDADES ==========
    
    def _get_timestamp(self) -> str:
        """Retorna timestamp en formato ISO"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def generate_report(self, project_name: str, volume_m3: float) -> str:
        """Genera reporte completo del proyecto"""
        
        # Evaluación C1
        viability = self.evaluate_viability(volume_m3)
        
        # Descomposición C3
        decomposition = self.decompose_construction_task(volume_m3, project_name)
        
        # Patrón C2
        pattern = self.pattern_from_volume(volume_m3)
        
        report = f"""
{'='*80}
REPORTE INTEGRADO: TheCubeUniverseEngine ↔ ZULY
{'='*80}

PROYECTO: {project_name}
Volumen: {volume_m3}m³

{'─'*80}
C1 EVALUADOR - VIABILIDAD FÍSICA
{'─'*80}
Estado: {viability['viability'].upper()}
Propiedades:
  Masa: {viability['properties']['masa_ton']}t ({viability['properties']['masa_kg']}kg)
  Densidad: {viability['properties']['densidad_kgm3']}kg/m³

Recomendaciones:
{chr(10).join('  • ' + r for r in viability['recommendations'])}

{'─'*80}
C3 OBJETIVOS - DESCOMPOSICIÓN LOGÍSTICA
{'─'*80}
Logística:
  Viajes dobletroque: {decomposition['decomposition']['logistics']['viajes_dobletroque']}
  Costo estimado: ${decomposition['decomposition']['logistics']['costo_estimado_usd']:,}
  Duración: {decomposition['decomposition']['estimations']['duration_weeks']} semanas

Subtareas:
{chr(10).join(f"  {i+1}. {t['name']}: {t['duration_days']} días, ${t['cost_usd']:,}" for i, t in enumerate(decomposition['decomposition']['subtasks']))}

{'─'*80}
C2 PATRONES - UNIDAD MÍNIMA
{'─'*80}
Patrón Atómico:
  Átomos necesarios: {pattern['total_atoms']:,}
  Cubo equivalente: {pattern['equivalent_cube_side_m']:.3f}m por lado

{'='*80}
"""
        return report


# Instancia global para ZULY
engine_integration = EngineIntegration()
