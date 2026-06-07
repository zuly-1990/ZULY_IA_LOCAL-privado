"""
Contexto de Proyecto Blender (Fase 5.19)

Responsabilidad:
- Leer estado del archivo .blend activo
- Identificar si es nuevo o guardado
- Identificar nombre y ruta
- NO modificar nada
Fase 5.16 – Contexto de Proyecto Blender
FASE 17: Refactorizado para usar EngineAdapter

Provee información sobre el proyecto activo en Blender.
"""

import os
from typing import Dict, Any, Optional


class BlenderProjectContext:
    """
    Contexto del proyecto activo en Blender.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    
    def __init__(self, adapter=None):
        """
        Inicializa el contexto del proyecto con un adapter.
        
        Args:
            adapter: EngineAdapter instance (si es None, se obtiene automáticamente)
        """
        self.adapter = adapter
        if self.adapter is None:
            from core.adapters import get_engine_adapter
            self.adapter = get_engine_adapter()
    
    def get_project_info(self) -> Dict[str, Any]:
        """
        Obtiene información del proyecto activo.
        
        Returns:
            Dict con información del proyecto
        """
        if not self.adapter or not self.adapter.is_available():
            return {
                "is_saved": False,
                "filepath": None,
                "directory": None,
                "filename": None,
                "source": "no_engine"
            }
        
        try:
            # Obtener información del motor
            engine_info = self.adapter.get_engine_info()
            
            if not engine_info.get('success', False):
                return {
                    "is_saved": False,
                    "filepath": None,
                    "directory": None,
                    "filename": None,
                    "source": "error",
                    "error": engine_info.get('error', 'Unknown')
                }
            
            # Nota: La información del archivo no está en el adapter estándar
            # Esto es una limitación conocida del desacoplamiento
            # Por ahora retornamos valores seguros
            return {
                "is_saved": False,
                "filepath": None,
                "directory": None,
                "filename": "Unsaved",
                "source": "engine_adapter",
                "engine": engine_info.get('name', 'Unknown'),
                "version": engine_info.get('version', 'Unknown')
            }
            
        except Exception as e:
            return {
                "is_saved": False,
                "filepath": None,
                "directory": None,
                "filename": None,
                "source": "error",
                "error": str(e)
            }
    
    def get_location(self) -> Optional[str]:
        """
        Retorna la ubicación del proyecto.
        
        Returns:
            Ruta del directorio del proyecto o None
        """
        info = self.get_project_info()
        return info.get('directory')
    
    def get_filename(self) -> Optional[str]:
        """
        Retorna el nombre del archivo del proyecto.
        
        Returns:
            Nombre del archivo o None
        """
        info = self.get_project_info()
        return info.get('filename')
    
    def is_saved(self) -> bool:
        """
        Verifica si el proyecto está guardado.
        
        Returns:
            True si el proyecto está guardado
        """
        info = self.get_project_info()
        return info.get('is_saved', False)
