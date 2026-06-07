"""
cognition_core.py

Orquestador de la capa cognitiva de ZULY.
Permite evaluar los resultados de las acciones para asegurar calidad y éxito real.
"""

from collections import deque
from typing import Dict, List, Any, Optional
from datetime import datetime
from core.utils.logging import log_info, log_warning, log_success, log_error

from core.cognition.memory.heuristic_memory import HeuristicMemory
from core.cognition.jues_logic import JUESAggregator

class CognitionCore:
    """Sistema de evaluación y diagnóstico de resultados"""
    
    def __init__(self, max_history: int = 100):
        """
        Inicializa CognitionCore.
        
        Args:
            max_history: Máximo de diagnósticos a mantener en memoria.
        """
        self.evaluators = {}
        # Historial limitado para evitar fugas de memoria (Fase 4 - Estabilidad)
        self.diagnoses = deque(maxlen=max_history)
        self.memory = HeuristicMemory()
        self.jues_aggregator = JUESAggregator()
        log_info(f"CognitionCore inicializado (Historial: {max_history})", module="COGNITION")

    def register_evaluator(self, name: str, evaluator_instance):
        """Registra un evaluador especializado"""
        self.evaluators[name] = evaluator_instance
        log_info(f"Evaluador registrado: {name}", module="COGNITION")

    def evaluate(self, result: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analiza un resultado y genera un diagnóstico cognitivo.
        """
        diagnosis = {
            'timestamp': datetime.now().isoformat(),
            'status': 'UNKNOWN',
            'score': 0.0,
            'findings': [],
            'recommendations': []
        }
        
        # Determinar qué evaluadores usar basado en el comando o resultado
        command = result.get('command_executed', 'unknown')
        parameters = result.get('parameters', {})
        output_path = result.get('output_path') or parameters.get('output_path')
        
        # Caso: Renderizado
        if 'render_scene' in command or (output_path and output_path.endswith('.png')):
            if 'render' in self.evaluators:
                eval_result = self.evaluators['render'].evaluate(output_path, context)
                diagnosis['findings'].extend(eval_result.get('findings', []))
                diagnosis['score'] = eval_result.get('score', 0.0)
                diagnosis['status'] = eval_result.get('status', 'FAILED')
        
        # Diagnóstico por defecto si no hay evaluadores específicos
        if diagnosis['status'] == 'UNKNOWN':
            if result.get('success'):
                diagnosis['status'] = 'PROBABLY_OK'
                diagnosis['score'] = 0.5
            else:
                diagnosis['status'] = 'ACTION_FAILED'
                diagnosis['score'] = 0.0

        # FASE 4: Almacenar experiencia si es exitosa (Sustituye C2 por HeuristicMemory funcional)
        if diagnosis['score'] >= 0.7:
            self.memory.store_experience(
                command=command,
                parameters=parameters,
                score=diagnosis['score'],
                diagnosis=diagnosis
            )

        self.diagnoses.append(diagnosis)
        return diagnosis

    def get_last_diagnosis(self) -> Optional[Dict[str, Any]]:
        """Retorna el último diagnóstico generado"""
        return self.diagnoses[-1] if self.diagnoses else None

    def get_suggested_parameters(self, command: str) -> Optional[Dict[str, Any]]:
        """Recupera los mejores parámetros conocidos para un comando"""
        return self.memory.get_best_parameters(command)

    def evaluate_with_jues(
        self,
        pattern_id: str,
        v0_result: Dict[str, Any],
        v1_result: Dict[str, Any],
        v2_result: Dict[str, Any],
        v3_result: Dict[str, Any],
        chromatic_sync_result: Dict[str, Any],
        optimization_instinct_result: Dict[str, Any],
        immutability_seal_result: Dict[str, Any],
        save_to_bitacora: bool = True
    ) -> Dict[str, Any]:
        """
        Paso 2: Evaluación final usando JUESAggregator.
        
        Genera un reporte JUES completo con ponderación de validaciones,
        dictamen automático de 5 tipos, y persistencia en bitácora JSON.
        
        Args:
            pattern_id: ID del patrón evaluado (ej: "CUB-001")
            v0_result: Resultado validación V0 (Física) - CRÍTICO
            v1_result: Resultado validación V1 (Estructural) - CRÍTICO
            v2_result: Resultado validación V2 (Contextual)
            v3_result: Resultado validación V3 (Topológica)
            chromatic_sync_result: Resultado sincronía cromática
            optimization_instinct_result: Resultado optimización
            immutability_seal_result: Resultado sello inmutabilidad
            save_to_bitacora: Si guardar en bitácora JSON con timestamp
            
        Returns:
            Reporte JUES completo con puntuación 0-100, dictamen y dashboard
        """
        log_info(f"Iniciando evaluación JUES para: {pattern_id}", module="COGNITION")
        
        report = self.jues_aggregator.generate_jues_report(
            v0_result=v0_result,
            v1_result=v1_result,
            v2_result=v2_result,
            v3_result=v3_result,
            chromatic_sync_result=chromatic_sync_result,
            optimization_instinct_result=optimization_instinct_result,
            immutability_seal_result=immutability_seal_result,
            pattern_id=pattern_id,
            save_to_bitacora=save_to_bitacora
        )
        
        # Almacenar en memoria heurística si es apto
        if report['puntuacion_jues'] >= 70 and len(report['errors']) == 0:
            self.memory.store_experience(
                command=pattern_id,
                parameters={"jues_report": report},
                score=report['puntuacion_jues'] / 100,
                diagnosis={"dictamen": report['dictamen'], "findings": report['findings']}
            )
            log_success(f"Experiencia JUES almacenada: {pattern_id} ({report['puntuacion_jues']}pts)", module="COGNITION")
        
        return report

    def get_jues_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Obtiene resumen histórico de reportes JUES para análisis de tendencias.
        
        Args:
            days: Número de días a considerar (default: 7)
            
        Returns:
            Estadísticas: total reportes, promedio puntuación, distribución dictámenes
        """
        return self.jues_aggregator.get_bitacora_summary(days=days)

    def prepare_for_soberano_seal(self, jues_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Paso 3: Preparar datos para SoberanoSealSystem.
        
        Transforma el reporte JUES en formato compatible con el sistema de sellado,
        incluyendo el dashboard visual y metadata necesaria.
        
        Args:
            jues_report: Reporte generado por evaluate_with_jues()
            
        Returns:
            Datos formateados para SoberanoSealSystem con toda la información validada
        """
        dashboard = jues_report.get('dashboard', {})
        
        seal_data = {
            "candidato_id": jues_report.get('pattern_id'),
            "status": "LISTO_PARA_SELLO" if jues_report.get('dictamen') == "APTO_PARA_SELLO" else "REVISION_REQUERIDA",
            "puntuacion_jues": jues_report.get('puntuacion_jues'),
            "dictamen": jues_report.get('dictamen'),
            "metricas_visuales": {
                "estado_malla": dashboard.get('estado_malla', 'DESCONOCIDO'),
                "estado_malla_icon": dashboard.get('estado_malla_icon', '❓'),
                "concordancia_color": dashboard.get('concordancia_color', 'DESCONOCIDO'),
                "concordancia_icon": dashboard.get('concordancia_icon', '❓'),
                "peso_kb": dashboard.get('peso_patron_kb', 'N/A'),
                "hash_corto": dashboard.get('hash_corto', 'N/A')
            },
            "validaciones": {
                "errores": len(jues_report.get('errors', [])),
                "advertencias": len(jues_report.get('warnings', [])),
                "hallazgos": len(jues_report.get('findings', []))
            },
            "raw_jues_report": jues_report  # Referencia completa para auditoría
        }
        
        log_info(f"Datos preparados para SoberanoSeal: {seal_data['candidato_id']} - {seal_data['status']}", module="COGNITION")
        return seal_data

    def quick_jues_evaluate(
        self,
        pattern_id: str,
        v0_verified: bool,
        v1_verified: bool,
        v3_verified: bool = True,
        color_match: bool = True,
        save_to_bitacora: bool = True
    ) -> Dict[str, Any]:
        """
        Evaluación JUES rápida para casos simples (modo compatibilidad).
        
        Usa valores por defecto para resultados no críticos, enfocándose
        en V0 y V1 que son los validadores críticos.
        
        Args:
            pattern_id: ID del patrón
            v0_verified: Resultado crítico V0 (física)
            v1_verified: Resultado crítico V1 (estructural)
            v3_verified: Resultado V3 (topológica, default True)
            color_match: Coincidencia de color, default True
            save_to_bitacora: Persistir en bitácora
            
        Returns:
            Reporte JUES simplificado
        """
        v0_result = {"verified": v0_verified, "details": "V0 checked" if v0_verified else "V0 FAILED"}
        v1_result = {"verified": v1_verified, "details": "V1 checked" if v1_verified else "V1 FAILED"}
        v2_result = {"verified": True, "details": "Context OK"}
        v3_result = {"verified": v3_verified, "metrics": {"is_watertight": v3_verified, "non_manifold_edges_count": 0}}
        chromatic = {"match": color_match, "details": "Color OK" if color_match else "Color mismatch"}
        optimization = {"optimized": True, "details": "Optimized", "final_size_kb": 100.0}
        immutability = {"verified": True, "hash_short": "quick"}
        
        return self.evaluate_with_jues(
            pattern_id=pattern_id,
            v0_result=v0_result,
            v1_result=v1_result,
            v2_result=v2_result,
            v3_result=v3_result,
            chromatic_sync_result=chromatic,
            optimization_instinct_result=optimization,
            immutability_seal_result=immutability,
            save_to_bitacora=save_to_bitacora
        )
