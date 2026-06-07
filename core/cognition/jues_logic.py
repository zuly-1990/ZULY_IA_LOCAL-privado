# core/cognition/jues_logic.py
"""
JUES Logic - Agregador de Puntuaciones de Validación.

Este módulo centraliza el cálculo del 'reporte_jues'
a partir de los resultados de las diferentes capas de validación (V0, V1, V2, V3)
y evaluaciones cognitivas (Sincronía Cromática, Instinto de Optimización, etc.).

Define los pesos de cada validación para generar una puntuación consolidada
que refleje la calidad y la integridad del patrón o resultado.
"""

from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import json
from core.utils.logging import log_info, log_warning, log_error

class JUESAggregator:
    """
    Agrega y pondera los resultados de las validaciones para generar un reporte JUES.
    """

    # Pesos de las validaciones para el cálculo de la puntuación JUES (total 100)
    # AJUSTADO 2026-05-02: Más exigente. No todo puede ser 100/100.
    WEIGHTS = {
        "v0_physical_integrity": 15,  # CRÍTICO: ¿Se creó el objeto?
        "v1_structural_integrity": 15, # CRÍTICO: ¿Estructura del archivo OK?
        "v2_contextual_relevance": 10, # ¿Tiene cámara + luz? Requiere ambos.
        "v3_topological_quality": 25,  # CRÍTICO: Malla perfecta (0 non-manifold)
        "chromatic_sync": 10,          # ¿Color exacto o coherente?
        "optimization_instinct": 15,   # ¿Eficiente? Penaliza vértices/tamaño alto.
        "immutability_seal": 10,       # SEGURIDAD: Hash consistente + reproducible.
    }

    def __init__(self):
        """Inicializa el agregador con directorio de bitácora."""
        self.bitacora_dir = Path("bitacora/jues_reports")
        self.bitacora_dir.mkdir(parents=True, exist_ok=True)
        log_info(f"✓ JUESAggregator inicializado. Bitácora en: {self.bitacora_dir}")

    def generate_jues_report(
        self,
        v0_result: Dict[str, Any],
        v1_result: Dict[str, Any],
        v2_result: Dict[str, Any],
        v3_result: Dict[str, Any],
        chromatic_sync_result: Dict[str, Any],
        optimization_instinct_result: Dict[str, Any],
        immutability_seal_result: Dict[str, Any],
        pattern_id: str = "N/A",
        save_to_bitacora: bool = True
    ) -> Dict[str, Any]:
        """
        Genera el reporte consolidado de JUES con una puntuación final.

        Args:
            v0_result: Resultado de la validación V0 (Física).
            v1_result: Resultado de la validación V1 (Estructural).
            v2_result: Resultado de la validación V2 (Contextual).
            v3_result: Resultado de la validación V3 (Topológica).
            chromatic_sync_result: Resultado de la sincronía cromática.
            optimization_instinct_result: Resultado del instinto de optimización.
            immutability_seal_result: Resultado del sello de inmutabilidad.
            pattern_id: ID del patrón que se está evaluando.

        Returns:
            Un diccionario con el reporte JUES consolidado.
        """
        total_score = 0.0
        findings: List[str] = []
        errors: List[str] = []
        warnings: List[str] = []
        dictamen = "PENDIENTE" # Default, se actualizará

        # --- Evaluación de V0 (Física) ---
        v0_verified = v0_result.get('verified', False)
        if v0_verified:
            total_score += self.WEIGHTS["v0_physical_integrity"]
            findings.append(f"V0 (Física): OK - {v0_result.get('details', 'Objeto creado y válido.')}")
        else:
            errors.append(f"V0 (Física): FALLO - {v0_result.get('details', 'Fallo en la creación o integridad física.')}")
            # Si V0 falla, el patrón es fundamentalmente defectuoso.
            # No tiene sentido sumar otros puntos si la base es incorrecta.
            return self._create_failed_report(pattern_id, errors, warnings, findings, "FALLO_CRITICO_V0")

        # --- Evaluación de V1 (Estructural) ---
        v1_verified = v1_result.get('verified', False)
        if v1_verified:
            total_score += self.WEIGHTS["v1_structural_integrity"]
            findings.append(f"V1 (Estructural): OK - {v1_result.get('details', 'Estructura del archivo correcta.')}")
        else:
            errors.append(f"V1 (Estructural): FALLO - {v1_result.get('details', 'Fallo en la estructura del archivo Blender.')}")
            # Si V1 falla, el patrón es fundamentalmente defectuoso.
            return self._create_failed_report(pattern_id, errors, warnings, findings, "FALLO_CRITICO_V1")

        # --- Evaluación de V2 (Contextual) ---
        v2_verified = v2_result.get('verified', False)
        if v2_verified:
            total_score += self.WEIGHTS["v2_contextual_relevance"]
            findings.append(f"V2 (Contextual): OK - {v2_result.get('details', 'Contexto de escena válido.')}")
        else:
            # Penalización parcial: media puntuación si tiene al menos cámara O luz
            has_cam = v2_result.get('has_camera', False)
            has_light = v2_result.get('has_light', False)
            if has_cam or has_light:
                total_score += self.WEIGHTS["v2_contextual_relevance"] * 0.5
                warnings.append(f"V2 (Contextual): PARCIAL - Solo {'cámara' if has_cam else 'luz'} presente.")
            else:
                warnings.append(f"V2 (Contextual): ADVERTENCIA - {v2_result.get('reason', 'Contexto de escena no óptimo.')}")

        # --- Evaluación de V3 (Topológica) ---
        v3_verified = v3_result.get('verified', False)
        nm_count = v3_result.get('metrics', {}).get('non_manifold_edges_count', 0)
        if v3_verified and nm_count == 0:
            total_score += self.WEIGHTS["v3_topological_quality"]
            findings.append("V3 (Topológica): OK - Malla perfecta (0 non-manifold)")
        else:
            # Penalización proporcional por cada non-manifold edge
            penalty = min(nm_count * 2.0, self.WEIGHTS["v3_topological_quality"])
            earned = self.WEIGHTS["v3_topological_quality"] - penalty
            total_score += max(earned, 0)
            if nm_count > 0:
                warnings.append(f"V3 (Topológica): {nm_count} non-manifold edges (-{penalty:.1f} pts)")
            else:
                errors.append("V3 (Topológica): FALLO - Malla no verificada.")

        # --- Evaluación de Sincronía Cromática ---
        chromatic_match = chromatic_sync_result.get('match', False)
        if chromatic_match:
            total_score += self.WEIGHTS["chromatic_sync"]
            findings.append(f"Sincronía Cromática: OK - {chromatic_sync_result.get('details', 'Color exacto.')}")
        else:
            warnings.append(f"Sincronía Cromática: ADVERTENCIA - {chromatic_sync_result.get('details', 'Color no coincide exactamente.')}")

        # --- Evaluación de Instinto de Optimización ---
        optimized = optimization_instinct_result.get('optimized', False)
        verts = optimization_instinct_result.get('vertex_count', 0)
        size_kb = optimization_instinct_result.get('final_size_kb', 9999)
        # Score basado en densidad: vertices por KB. Ideal < 15 verts/KB.
        density = verts / max(size_kb, 1)
        if optimized and density < 15:
            total_score += self.WEIGHTS["optimization_instinct"]
            findings.append(f"Optimización: OK - {verts} verts / {size_kb} KB ({density:.1f} v/KB)")
        elif optimized:
            # Parcial: modelo funciona pero es denso
            partial = self.WEIGHTS["optimization_instinct"] * 0.6
            total_score += partial
            warnings.append(f"Optimización: DENSO - {verts} verts / {size_kb} KB ({density:.1f} v/KB, -{self.WEIGHTS['optimization_instinct']-partial:.1f} pts)")
        else:
            # No optimizado = 0 pts
            warnings.append(f"Optimización: NO OPTIMIZADO - {optimization_instinct_result.get('details', 'Patrón no optimizado.')}")

        # --- Evaluación de Sello de Inmutabilidad ---
        immutability_ok = immutability_seal_result.get('verified', False)
        hash_val = immutability_seal_result.get('hash_short', 'N/A')
        if immutability_ok and hash_val != 'N/A' and hash_val != 'fallback':
            total_score += self.WEIGHTS["immutability_seal"]
            findings.append(f"Inmutabilidad: OK - Hash {hash_val}")
        elif immutability_ok and hash_val == 'fallback':
            # Hash fallback = penalización parcial
            partial = self.WEIGHTS["immutability_seal"] * 0.5
            total_score += partial
            warnings.append(f"Inmutabilidad: HASH FALLBACK (-{self.WEIGHTS['immutability_seal']-partial:.1f} pts)")
        else:
            errors.append("Inmutabilidad: FALLO - Hash inconsistente o no generado.")

        # --- Determinar Dictamen Final ---
        if len(errors) > 0:
            dictamen = "FALLO_TECNICO"
        elif total_score >= 90:
            dictamen = "APTO_PARA_SELLO"
        elif total_score >= 70:
            dictamen = "APTO_CON_ADVERTENCIAS"
        else:
            dictamen = "RECHAZADO_POR_CALIDAD"

        log_info(f"JUES Reporte para {pattern_id}: Puntuación {total_score:.2f}, Dictamen: {dictamen}")

        report = {
            "pattern_id": pattern_id,
            "puntuacion_jues": round(total_score, 2),
            "dictamen": dictamen,
            "findings": findings,
            "errors": errors,
            "warnings": warnings,
            "dashboard": { # Para el SoberanoSealSystem
                "estado_malla": "LIMPIA" if v3_verified else "CON_ERRORES",
                "estado_malla_icon": "✅" if v3_verified else "❌",
                "concordancia_color": "MATCH" if chromatic_match else "NO_MATCH",
                "concordancia_icon": "🎨" if chromatic_match else "⚠️",
                "peso_patron_kb": optimization_instinct_result.get('final_size_kb', 'N/A'),
                "hash_corto": immutability_seal_result.get('hash_short', 'N/A')
            },
            "raw_results": { # Para auditoría detallada
                "v0": v0_result,
                "v1": v1_result,
                "v2": v2_result,
                "v3": v3_result,
                "chromatic_sync": chromatic_sync_result,
                "optimization_instinct": optimization_instinct_result,
                "immutability_seal": immutability_seal_result,
            }
        }

        # Guardar en bitácora si se solicita
        if save_to_bitacora:
            self.save_report_to_bitacora(report)

        return report

    def _create_failed_report(self, pattern_id: str, errors: List[str], warnings: List[str], findings: List[str], dictamen: str) -> Dict[str, Any]:
        """Crea un reporte de fallo crítico temprano."""
        log_error(f"JUES Reporte para {pattern_id}: FALLO CRÍTICO - {dictamen}")
        return {
            "pattern_id": pattern_id,
            "puntuacion_jues": 0.0,
            "dictamen": dictamen,
            "findings": findings,
            "errors": errors,
            "warnings": warnings,
            "dashboard": {
                "estado_malla": "FALLO_CRITICO",
                "estado_malla_icon": "❌",
                "concordancia_color": "N/A",
                "concordancia_icon": "❌",
                "peso_patron_kb": "N/A",
                "hash_corto": "N/A"
            },
            "raw_results": {}
        }

    def save_report_to_bitacora(self, report: Dict[str, Any]) -> str:
        """
        Guarda el reporte JUES en la bitácora con fecha y hora.
        
        Args:
            report: El reporte JUES generado.
            
        Returns:
            La ruta del archivo guardado en la bitácora.
        """
        timestamp = datetime.now()
        date_folder = self.bitacora_dir / timestamp.strftime("%Y-%m-%d")
        date_folder.mkdir(parents=True, exist_ok=True)
        
        # Nombre archivo: HHMMSS_pattern_id.json
        filename = f"{timestamp.strftime('%H%M%S')}_{report.get('pattern_id', 'unknown')}.json"
        file_path = date_folder / filename
        
        # Agregar timestamp al reporte
        report_with_metadata = {
            "timestamp": timestamp.isoformat(),
            "fecha": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            **report
        }
        
        # Guardar JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report_with_metadata, f, indent=2, ensure_ascii=False)
        
        log_info(f"✅ Reporte JUES guardado en bitácora: {file_path}")
        return str(file_path)

    def get_bitacora_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Obtiene un resumen de los reportes en la bitácora de los últimos N días.
        
        Args:
            days: Número de días a considerar (default: 7).
            
        Returns:
            Un diccionario con estadísticas de los reportes.
        """
        from collections import defaultdict
        
        stats = {
            "total_reportes": 0,
            "por_dictamen": defaultdict(int),
            "promedio_puntuacion": 0.0,
            "reportes_criticos": [],
        }
        
        puntuaciones = []
        fecha_inicio = (datetime.now() - __import__('datetime').timedelta(days=days)).date()
        
        if not self.bitacora_dir.exists():
            return stats
        
        for date_folder in self.bitacora_dir.iterdir():
            if not date_folder.is_dir():
                continue
            
            try:
                folder_date = datetime.strptime(date_folder.name, "%Y-%m-%d").date()
                if folder_date < fecha_inicio:
                    continue
            except ValueError:
                continue
            
            for json_file in date_folder.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        report = json.load(f)
                    
                    stats["total_reportes"] += 1
                    dictamen = report.get("dictamen", "DESCONOCIDO")
                    stats["por_dictamen"][dictamen] += 1
                    
                    puntuacion = report.get("puntuacion_jues", 0)
                    puntuaciones.append(puntuacion)
                    
                    if dictamen.startswith("FALLO"):
                        stats["reportes_criticos"].append({
                            "pattern_id": report.get("pattern_id"),
                            "fecha": report.get("fecha"),
                            "dictamen": dictamen
                        })
                except Exception as e:
                    log_warning(f"Error leyendo {json_file}: {e}")
        
        if puntuaciones:
            stats["promedio_puntuacion"] = round(sum(puntuaciones) / len(puntuaciones), 2)
        
        stats["por_dictamen"] = dict(stats["por_dictamen"])
        
        return stats
