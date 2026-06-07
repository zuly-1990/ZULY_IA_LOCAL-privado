"""
export.py - Handlers para exportación en Blender
FASE 17: Refactorizado para usar EngineAdapter.
"""

from typing import Dict, Any
from pathlib import Path
from core.utils.logging import log_success, log_warning, log_info


def export_fbx_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Exporta la escena a FBX usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    Parameters:
        parameters: Dict con:
            - filepath: str (ruta del archivo)
            - selected_only: bool (solo objetos seleccionados)
        adapter: EngineAdapter instance
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        filepath = parameters.get('filepath')
        selected_only = parameters.get('selected_only', False)
        
        if not filepath:
            return {'success': False, 'error': 'Missing filepath'}
        
        # Validar ruta
        export_path = Path(filepath)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Exportar usando adapter
        result = adapter.export_scene(
            format='FBX',
            output_path=str(export_path),
            use_selection=selected_only
        )
        
        if not result.get('success', False):
            return result
        
        log_success(f"Escena exportada a FBX: {filepath}")
        
        return {
            'success': True,
            'filepath': str(export_path),
            'format': 'FBX',
            'file_size': export_path.stat().st_size if export_path.exists() else 0,
            'message': f'Exportado exitosamente'
        }
    
    except Exception as e:
        log_warning(f"Error exporting FBX: {e}")
        return {'success': False, 'error': str(e)}


def export_obj_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Exporta la escena a OBJ usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        filepath = parameters.get('filepath')
        selected_only = parameters.get('selected_only', False)
        
        if not filepath:
            return {'success': False, 'error': 'Missing filepath'}
        
        export_path = Path(filepath)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        result = adapter.export_scene(
            format='OBJ',
            output_path=str(export_path),
            use_selection=selected_only
        )
        
        if not result.get('success', False):
            return result
        
        log_success(f"Escena exportada a OBJ: {filepath}")
        
        return {
            'success': True,
            'filepath': str(export_path),
            'format': 'OBJ',
            'file_size': export_path.stat().st_size if export_path.exists() else 0,
            'message': f'Exportado exitosamente'
        }
    
    except Exception as e:
        log_warning(f"Error exporting OBJ: {e}")
        return {'success': False, 'error': str(e)}


def export_gltf_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Exporta la escena a glTF usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        filepath = parameters.get('filepath')
        export_format = parameters.get('export_format', 'GLTF_SEPARATE')
        
        if not filepath:
            return {'success': False, 'error': 'Missing filepath'}
        
        if export_format not in ['GLTF_SEPARATE', 'GLTF_EMBEDDED']:
            return {'success': False, 'error': 'Invalid export_format'}
        
        export_path = Path(filepath)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        result = adapter.export_scene(
            format='GLTF',
            output_path=str(export_path),
            export_format=export_format
        )
        
        if not result.get('success', False):
            return result
        
        log_success(f"Escena exportada a glTF: {filepath}")
        
        return {
            'success': True,
            'filepath': str(export_path),
            'format': 'glTF',
            'export_format': export_format,
            'file_size': export_path.stat().st_size if export_path.exists() else 0,
            'message': f'Exportado exitosamente'
        }
    
    except Exception as e:
        log_warning(f"Error exporting glTF: {e}")
        return {'success': False, 'error': str(e)}
