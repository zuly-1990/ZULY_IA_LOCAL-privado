"""
arq_core.py — ARQ: Arquitecto de Reparación y Calidad
Orquestador principal del sistema de inspección y reparación de mallas 3D.
Se integra con el flujo ZULY → ARQ → JUES.
"""

from __future__ import annotations

import datetime
from typing import Optional, Dict, List, Any

from .mesh_analyzer import analyze_mesh
from .mesh_fixer import fix_mesh


class ARQCore:
    """
    Orquestador de inspección y reparación de mallas 3D.

    Flujo de uso:
        arq = ARQCore(adapter)
        issues = arq.inspect_objects(obj_list)
        if issues['total_issues'] > 0:
            fixes = arq.repair_objects(obj_list)
        report = arq.generate_report(obj_list)  # → JUES
    """

    def __init__(self, adapter: Optional[Any] = None):
        """
        Args:
            adapter: Adaptador de motor de Blender (real o mock).
                     Si es None o mock, todas las operaciones son simuladas.
        """
        self.adapter = adapter
        self._inspection_cache: Dict[str, Dict] = {}
        self._repair_cache: Dict[str, Dict] = {}

    # ------------------------------------------------------------------
    #  PROPIEDADES
    # ------------------------------------------------------------------

    @property
    def is_mock_mode(self) -> bool:
        """Detecta si estamos en modo mock (sin Blender real)."""
        if self.adapter is None:
            return True
        return getattr(self.adapter, 'is_mock', False)

    # ------------------------------------------------------------------
    #  INSPECCIÓN
    # ------------------------------------------------------------------

    def inspect_mesh(self, obj_name: str) -> Dict:
        """
        Inspecciona un único objeto en busca de problemas geométricos.

        Returns:
            {
                'duplicated_verts': int,
                'inverted_normals': bool,
                'non_manifold_edges': int,
                'holes': int,
                'degenerate_faces': int,
                'total_issues': int
            }
        """
        if obj_name in self._inspection_cache:
            return self._inspection_cache[obj_name]

        try:
            result = analyze_mesh(obj_name, self.adapter)
        except Exception as e:
            # Graceful degradation
            result = {
                'duplicated_verts': 0,
                'inverted_normals': False,
                'non_manifold_edges': 0,
                'holes': 0,
                'degenerate_faces': 0,
                'total_issues': 0,
                'error': str(e)
            }

        self._inspection_cache[obj_name] = result
        return result

    def inspect_objects(self, obj_names: List[str]) -> Dict:
        """
        Inspección en lote de múltiples objetos.

        Returns:
            {
                'total_objects': int,
                'total_issues': int,
                'objects': { obj_name: <resultado de inspect_mesh> }
            }
        """
        objects_results: Dict[str, Dict] = {}
        total_issues = 0

        for name in obj_names:
            result = self.inspect_mesh(name)
            objects_results[name] = result
            total_issues += result.get("total_issues", 0)

        return {
            "total_objects": len(obj_names),
            "total_issues": total_issues,
            "objects": objects_results,
        }

    # ------------------------------------------------------------------
    #  REPARACIÓN
    # ------------------------------------------------------------------

    def repair_mesh(self, obj_name: str) -> Dict:
        """
        Repara un único objeto aplicando operaciones estándar de limpieza.

        Operaciones aplicadas:
            - remove_doubles → elimina vértices duplicados
            - normals_make_consistent → corrige normales invertidas
            - fill_holes → rellena agujeros en la malla

        Returns:
            {
                'merged_verts': int,
                'fixed_normals': bool,
                'filled_holes': int,
                'success': bool
            }
        """
        try:
            result = fix_mesh(obj_name, self.adapter)
        except Exception as e:
            result = {
                'merged_verts': 0,
                'fixed_normals': False,
                'filled_holes': 0,
                'success': False,
                'error': str(e)
            }

        self._repair_cache[obj_name] = result

        # Invalidar caché de inspección para reflejar estado post-reparación
        self._inspection_cache.pop(obj_name, None)

        return result

    def repair_objects(self, obj_names: List[str]) -> Dict:
        """
        Reparación en lote de múltiples objetos.

        Returns:
            {
                'total_objects': int,
                'total_repaired': int,
                'total_merged_verts': int,
                'objects': { obj_name: <resultado de repair_mesh> }
            }
        """
        objects_results: Dict[str, Dict] = {}
        total_repaired = 0
        total_merged = 0

        for name in obj_names:
            result = self.repair_mesh(name)
            objects_results[name] = result
            if result.get("success"):
                total_repaired += 1
                total_merged += result.get("merged_verts", 0)

        return {
            "total_objects": len(obj_names),
            "total_repaired": total_repaired,
            "total_merged_verts": total_merged,
            "objects": objects_results,
        }

    # ------------------------------------------------------------------
    #  REPORTE FINAL
    # ------------------------------------------------------------------

    def generate_report(self, obj_names: List[str]) -> Dict:
        """
        Genera el reporte consolidado para JUES.

        Calcula arq_score basado en issues encontrados antes y después
        de las reparaciones aplicadas (si las hubo).

        Returns:
            {
                'arq_score': int,           # 0-100
                'issues_before': dict,
                'fixes_applied': dict,
                'issues_after': dict,
                'dictamen': 'LIMPIO'|'REPARADO'|'CRITICO',
                'timestamp': str
            }
        """
        # Issues antes (o estado actual si no hubo reparación previa)
        issues_before = self.inspect_objects(obj_names)

        # Fixes aplicados (puede estar vacío si no se llamó repair_objects)
        fixes_applied = self._build_fixes_report(obj_names)

        # Re-inspeccionar para issues_after (caché ya invalidado por repair)
        issues_after = self.inspect_objects(obj_names)

        # Calcular score (normalizado por número de objetos)
        arq_score = self._calculate_score(
            issues_after.get("total_issues", 0),
            len(obj_names)
        )

        # Dictamen (usando total_repaired > 0, no solo existencia de caché)
        total_repaired = fixes_applied.get("total_repaired", 0)
        issues_count_after = issues_after.get("total_issues", 0)

        if issues_count_after == 0 and total_repaired == 0:
            dictamen = "LIMPIO"
        elif issues_count_after == 0 and total_repaired > 0:
            dictamen = "REPARADO"
        else:
            dictamen = "CRITICO"

        return {
            "arq_score": arq_score,
            "issues_before": issues_before,
            "fixes_applied": fixes_applied,
            "issues_after": issues_after,
            "dictamen": dictamen,
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        }

    # ------------------------------------------------------------------
    #  HELPERS INTERNOS
    # ------------------------------------------------------------------

    def _build_fixes_report(self, obj_names: List[str]) -> Dict:
        """Construye el reporte de reparaciones aplicadas."""
        if not self._repair_cache:
            return {
                "total_objects": len(obj_names),
                "total_repaired": 0,
                "total_merged_verts": 0,
                "objects": {},
            }

        return {
            "total_objects": len(obj_names),
            "total_repaired": sum(
                1
                for n in obj_names
                if self._repair_cache.get(n, {}).get("success")
            ),
            "total_merged_verts": sum(
                self._repair_cache.get(n, {}).get("merged_verts", 0)
                for n in obj_names
            ),
            "objects": {
                n: self._repair_cache[n]
                for n in obj_names
                if n in self._repair_cache
            },
        }

    def _calculate_score(self, total_issues_after: int, total_objects: int) -> int:
        """
        Scoring normalizado por número de objetos.

        Reglas (issues PROMEDIO por objeto):
            0.0      → 100 pts
            0.1-0.5  →  85 pts
            0.6-1.0  →  70 pts
            1.1-2.0  →  50 pts
            >2.0     →  max(0, 50 - (issues_promedio - 2) * 10)
        """
        if total_objects == 0:
            return 0

        issues_per_object = total_issues_after / total_objects

        if issues_per_object == 0.0:
            return 100
        if issues_per_object <= 0.5:
            return 85
        if issues_per_object <= 1.0:
            return 70
        if issues_per_object <= 2.0:
            return 50

        # Penalización progresiva
        penalty = (issues_per_object - 2.0) * 10
        return max(0, 50 - int(penalty))
