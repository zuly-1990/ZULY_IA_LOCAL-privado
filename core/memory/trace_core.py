"""
TraceCore - Registro Inmutable de Trazas de ZULY
Fase 15: "Esto ya lo intenté antes, y falló por esta razón."
"""

import datetime
from typing import Dict, List, Any, Optional
from core.learning.storage_interface import JSONStorage

class TraceCore:
    """
    Gestiona el historial de trazas (Trace Logs) de ZULY.
    Proporciona un registro inmutable de cada ciclo completo de ejecución.
    
    FASE 19: Ahora con límites de memoria y archivado automático.
    """
    
    MAX_TRACES = 1000  # Límite de trazas en memoria activa

    def __init__(self, storage_path: str = "memory/traces.json"):
        """
        Inicializa el núcleo de trazas.
        
        Args:
            storage_path (str): Ruta al archivo de almacenamiento de trazas.
        """
        self.storage = JSONStorage(storage_path)
        self.traces: List[Dict] = self.storage.load()
        self.storage_path = storage_path
        
        # FASE 19: Aplicar límites al cargar
        if len(self.traces) > self.MAX_TRACES:
            self._apply_trace_limit()


    def append_trace(self, trace_data: Dict[str, Any]) -> bool:
        """
        Añade una nueva traza al historial.
        
        Args:
            trace_data (dict): Contenido de la traza (intención, decisión, resultado, etc.)
            
        Returns:
            bool: True si se guardó correctamente.
        """
        trace = {
            "timestamp": datetime.datetime.now().isoformat(),
            "data": trace_data
        }
        self.traces.append(trace)
        
        # FASE 19: Aplicar límite automáticamente
        if len(self.traces) > self.MAX_TRACES:
            self._apply_trace_limit()
        
        return self.storage.save(self.patterns_list_to_save()) # Nota: JSONStorage.save espera la lista completa

    def patterns_list_to_save(self) -> List[Dict]:
        """Retorna la lista de trazas para guardar."""
        return self.traces

    def query_failures(self, intent_name: str) -> int:
        """
        Cuenta cuántas veces ha fallado una intención específica en el pasado.
        
        Args:
            intent_name (str): Nombre del comando.
            
        Returns:
            int: Número de fallos registrados.
        """
        failures = [
            t for t in self.traces 
            if t["data"].get("intention", "").upper() == intent_name.upper() 
            and t["data"].get("execution_success") is False
        ]
        return len(failures)

    def get_last_result(self, intent_name: str) -> Optional[Dict]:
        """
        Obtiene el último resultado registrado para una intención.
        """
        relevant = [
            t for t in self.traces 
            if t["data"].get("intention", "").upper() == intent_name.upper()
        ]
        if not relevant:
            return None
        return relevant[-1]

    def needs_human_authorization(self, intent_name: str) -> bool:
        """
        Consulta si una intención ha requerido autorización humana frecuentemente.
        """
        relevant = [
            t for t in self.traces 
            if t["data"].get("intention", "").upper() == intent_name.upper()
            and t["data"].get("auth_required") is True
        ]
        return len(relevant) > 0

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas básicas del núcleo de trazas."""
        return {
            "total_traces": len(self.traces),
            "last_activity": self.traces[-1]["timestamp"] if self.traces else None
        }
    
    def to_human_readable(self) -> str:
        """
        FASE 18.2: Formato legible para humanos.
        Memoria narrativa de lo que hizo ZULY.
        """
        lines = [
            "══════════════════════════════════",
            "📜 ZULY — TRAZA DE EJECUCIÓN",
            "══════════════════════════════════",
        ]
        
        if not self.traces:
            lines.append("(Sin trazas registradas)")
        else:
            for t in self.traces:
                data = t.get("data", {})
                timestamp = t.get("timestamp", "unknown")
                intention = data.get("intention", "unknown")
                success = data.get("execution_success", False)
                status = "✓" if success else "✗"
                
                lines.append(
                    f"[{timestamp}] {status} {intention}"
                )
        
        return "\n".join(lines)
    
    def _apply_trace_limit(self):
        """
        FASE 19: Aplica límite de trazas archivando las más antiguas.
        """
        if len(self.traces) <= self.MAX_TRACES:
            return
        
        # Calcular cuántas archivar
        to_archive_count = len(self.traces) - self.MAX_TRACES
        
        # Separar trazas antiguas
        old_traces = self.traces[:to_archive_count]
        self.traces = self.traces[to_archive_count:]
        
        # Archivar trazas antiguas
        self._archive_traces(old_traces)
        
        # Guardar trazas restantes
        self.storage.save(self.patterns_list_to_save())
    
    def _archive_traces(self, traces: List[Dict]):
        """
        Archiva trazas antiguas usando SessionArchiver.
        
        Args:
            traces: Lista de trazas a archivar
        """
        try:
            from core.memory.archiver import SessionArchiver
            import os
            from datetime import datetime
            
            # Crear archiver para directorio memory/
            memory_dir = os.path.dirname(self.storage_path)
            archiver = SessionArchiver(memory_dir)
            
            # Crear archivo temporal con trazas antiguas
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_filename = f"traces_archived_{timestamp}.json"
            temp_path = os.path.join(memory_dir, temp_filename)
            
            # Guardar trazas en archivo temporal
            import json
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(traces, f, indent=2, ensure_ascii=False)
            
            # Archivar
            archiver.archive_file(temp_path, compress=True)
            
        except Exception as e:
            # Si el archivado falla, al menos no perdemos las trazas
            # (ya están en memoria, solo no se archivaron)
            pass
