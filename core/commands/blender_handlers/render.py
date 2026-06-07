"""
render.py

Handler para renderizar escenas en Blender.
FASE 17: Refactorizado para usar EngineAdapter.
"""

from typing import Dict, Any
from pathlib import Path
from core.utils.logging import log_success, log_warning


def render_scene_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Renderiza la escena actual usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    Parameters:
        parameters: Dict con:
            - output_path: str (path donde guardar render)
            - format: str (PNG, JPEG, etc.) default: PNG
            - resolution: [width, height] default: [1920, 1080]
            - samples: int (render samples) default: 128
        adapter: EngineAdapter instance (si es None, se obtiene automáticamente)
    
    Returns:
        Dict con status y path del archivo
    """
    # Obtener adapter si no se proporciona
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    # Verificar disponibilidad
    if not adapter or not adapter.is_available():
        return {
            'success': False,
            'error': 'Engine adapter not available',
            'hint': 'Blender or compatible 3D engine required'
        }
    
    try:
        output_path = parameters.get('output_path', 'render_output.png')
        format_type = parameters.get('format', 'PNG').upper()
        resolution = parameters.get('resolution', [1920, 1080])
        samples = parameters.get('samples', 128)
        
        # Crear directorio si no existe
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Renderizar usando adapter
        result = adapter.render_scene(
            output_path=str(output_file),
            resolution=resolution,
            samples=samples,
            format=format_type
        )
        
        if not result.get('success', False):
            return result
        
        log_success(f"Render completado: {output_path}")
        
        return {
            'success': True,
            'output_path': str(output_file),
            'resolution': resolution,
            'format': format_type,
            'samples': samples,
            'render_time': result.get('render_time', 0),
            'message': f'Render guardado en {output_file}'
        }
    
    except Exception as e:
        log_warning(f"Error rendering: {e}")
        return {
            'success': False,
            'error': str(e)
        }
