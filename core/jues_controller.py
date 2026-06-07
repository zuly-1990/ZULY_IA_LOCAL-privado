"""
core/jues_controller.py

JUES Controller - Sistema Único de Validación y Sellado

Consolida:
- JUESAggregator (evaluación ponderada)
- SoberanoSealSystem (sellado físico)
- Controlador ZULY-JUES (orquestación)

ÚNICO punto de entrada para validación JUES en ZULY.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from core.cognition.jues_logic import JUESAggregator
from core.utils.logging import log_info, log_success, log_error, log_warning


class JUESController:
    """
    Controlador único JUES.
    
    Flujo: Validar → Evaluar JUES → Decidir → Ejecutar acción
    """
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Inicializa el controlador JUES.
        
        Args:
            base_path: Ruta base del proyecto ZULY (default: auto-detect)
        """
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent
        self.aggregator = JUESAggregator()
        
        # Directorios
        self.sellos_dir = self.base_path / "archivo_zuly" / "sellos"
        self.rechazados_dir = self.base_path / "archivo_zuly" / "rechazados"
        self.temp_arena = self.base_path / "archivo_zuly" / "temp_arena"
        
        # Crear directorios si no existen
        self.sellos_dir.mkdir(parents=True, exist_ok=True)
        self.rechazados_dir.mkdir(parents=True, exist_ok=True)
        self.temp_arena.mkdir(parents=True, exist_ok=True)
        
        log_info("JUESController inicializado", module="JUES")
    
    def validar_y_decidir(
        self,
        candidato_id: str,
        resultados_validacion: Dict[str, Any],
        blend_path: Optional[str] = None,
        target_color: Optional[str] = None,
        auto_aprobar: bool = False
    ) -> Dict[str, Any]:
        """
        Flujo completo: validar → evaluar JUES → decidir acción.
        
        Args:
            candidato_id: ID del patrón (ej: "CUB-001")
            resultados_validacion: Dict con V0, V1, V2, V3, etc.
            blend_path: Ruta al archivo .blend (opcional)
            target_color: Color objetivo para validación (opcional)
            auto_aprobar: Si True, sella automáticamente si pasa validación
            
        Returns:
            Dict con status, dictamen, y datos de la acción ejecutada
        """
        log_info(f"Iniciando validación JUES: {candidato_id}", module="JUES")
        
        # 1. EVALUAR con JUESAggregator
        reporte = self.aggregator.generate_jues_report(
            pattern_id=candidato_id,
            save_to_bitacora=True,
            **resultados_validacion
        )
        
        log_info(f"Reporte JUES: {reporte['puntuacion_jues']}pts - {reporte['dictamen']}", module="JUES")
        
        # 2. DECIDIR acción basada en dictamen
        dictamen = reporte['dictamen']
        
        if dictamen.startswith('FALLO_CRITICO'):
            # Fallo en V0 o V1 - rechazo inmediato
            return self._rechazar(candidato_id, reporte, blend_path)
            
        elif dictamen == 'APTO_PARA_SELLO' or (auto_aprobar and dictamen == 'APTO_CON_ADVERTENCIAS'):
            # Apto para sellado
            if blend_path and Path(blend_path).exists():
                return self._ejecutar_sello(blend_path, candidato_id, target_color, reporte)
            else:
                return self._pendiente_revision(candidato_id, reporte, "Archivo .blend no disponible")
                
        elif dictamen == 'APTO_CON_ADVERTENCIAS':
            # Apto pero con advertencias - requiere revisión manual
            return self._pendiente_revision(candidato_id, reporte, "Revisar advertencias antes de sellar")
            
        else:  # RECHAZADO_POR_CALIDAD o FALLO_TECNICO
            return self._rechazar(candidato_id, reporte, blend_path)
    
    def _ejecutar_sello(
        self,
        blend_path: str,
        candidato_id: str,
        target_color: Optional[str],
        reporte: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ejecuta sellado físico del archivo .blend"""
        
        blend_src = Path(blend_path)
        if not blend_src.exists():
            log_error(f"Archivo no encontrado: {blend_path}", module="JUES")
            return {
                'status': 'ERROR',
                'candidato_id': candidato_id,
                'error': 'Archivo no encontrado'
            }
        
        # Crear ruta de destino
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sello_filename = f"{candidato_id}_SELLADO_{timestamp}.blend"
        sello_path = self.sellos_dir / sello_filename
        
        try:
            # Copiar archivo al directorio de sellos
            shutil.copy2(blend_src, sello_path)
            
            # Guardar metadata del sello
            metadata = {
                'candidato_id': candidato_id,
                'timestamp': datetime.now().isoformat(),
                'puntuacion_jues': reporte['puntuacion_jues'],
                'dictamen': reporte['dictamen'],
                'target_color': target_color,
                'archivo_original': str(blend_src),
                'archivo_sellado': str(sello_path),
                'dashboard': reporte.get('dashboard', {}),
                'validaciones': {
                    'errores': len(reporte.get('errors', [])),
                    'advertencias': len(reporte.get('warnings', [])),
                    'hallazgos': len(reporte.get('findings', []))
                }
            }
            
            metadata_path = sello_path.with_suffix('.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            log_success(f"SELLADO: {candidato_id} → {sello_path}", module="JUES")
            
            return {
                'status': 'SELLADO',
                'candidato_id': candidato_id,
                'puntuacion_jues': reporte['puntuacion_jues'],
                'dictamen': reporte['dictamen'],
                'ubicacion': str(sello_path),
                'metadata': str(metadata_path)
            }
            
        except Exception as e:
            log_error(f"Error al sellar: {e}", module="JUES")
            return {
                'status': 'ERROR_SELLO',
                'candidato_id': candidato_id,
                'error': str(e)
            }
    
    def _rechazar(
        self,
        candidato_id: str,
        reporte: Dict[str, Any],
        blend_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Rechaza patrón con fallos críticos"""
        
        # Mover archivo a rechazados si existe
        if blend_path and Path(blend_path).exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            rechazo_filename = f"{candidato_id}_RECHAZADO_{timestamp}.blend"
            rechazo_path = self.rechazados_dir / rechazo_filename
            
            try:
                shutil.move(blend_path, rechazo_path)
                log_warning(f"RECHAZADO: {candidato_id} → {rechazo_path}", module="JUES")
                ubicacion = str(rechazo_path)
            except Exception as e:
                log_error(f"Error al mover archivo rechazado: {e}", module="JUES")
                ubicacion = None
        else:
            ubicacion = None
        
        return {
            'status': 'RECHAZADO',
            'candidato_id': candidato_id,
            'puntuacion_jues': reporte['puntuacion_jues'],
            'dictamen': reporte['dictamen'],
            'razon': reporte.get('errors', ['Fallo crítico']),
            'ubicacion': ubicacion
        }
    
    def _pendiente_revision(
        self,
        candidato_id: str,
        reporte: Dict[str, Any],
        motivo: str
    ) -> Dict[str, Any]:
        """Pone en cola de revisión manual"""
        
        log_warning(f"PENDIENTE: {candidato_id} - {motivo}", module="JUES")
        
        return {
            'status': 'PENDIENTE_REVISION',
            'candidato_id': candidato_id,
            'puntuacion_jues': reporte['puntuacion_jues'],
            'dictamen': reporte['dictamen'],
            'advertencias': reporte.get('warnings', []),
            'motivo_revision': motivo
        }
    
    def get_estadisticas(self, dias: int = 7) -> Dict[str, Any]:
        """
        Obtiene resumen de bitácora JUES.
        
        Args:
            dias: Número de días a considerar
            
        Returns:
            Estadísticas de reportes JUES
        """
        return self.aggregator.get_bitacora_summary(days=dias)
    
    def get_ultimos_sellados(self, n: int = 5) -> list:
        """
        Obtiene los últimos N sellados.
        
        Args:
            n: Cantidad de sellados a retornar
            
        Returns:
            Lista de metadata de sellados
        """
        sellados = []
        
        for json_file in sorted(self.sellos_dir.glob("*.json"), reverse=True):
            if len(sellados) >= n:
                break
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    sellados.append(metadata)
            except Exception as e:
                log_warning(f"Error leyendo metadata: {e}", module="JUES")
        
        return sellados


# Singleton global
_jues_controller: Optional[JUESController] = None


def get_jues_controller(base_path: Optional[str] = None) -> JUESController:
    """
    Obtiene instancia singleton del JUESController.
    
    Args:
        base_path: Ruta base (opcional, solo usado en primera llamada)
        
    Returns:
        Instancia de JUESController
    """
    global _jues_controller
    if _jues_controller is None:
        _jues_controller = JUESController(base_path)
    return _jues_controller


def reset_jues_controller():
    """Resetea el singleton (útil para tests)."""
    global _jues_controller
    _jues_controller = None
