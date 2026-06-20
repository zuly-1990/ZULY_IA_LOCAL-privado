"""
geonodes.py

Handler para ejecutar scripts de Geometry Nodes procedurales de forma dinámica.
"""
from typing import Dict, Any
from core.commands.handler_registry_utils import blender_handler
from core.adapters.engine_adapter import EngineAdapter, EngineError

@blender_handler("blender.generate_geometry_nodes")
def generate_geometry_nodes_handler(adapter: EngineAdapter, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejecuta un script de Python de IA para aplicar Geometry Nodes.
    
    Expected params:
        - target_object: Nombre del objeto destino.
        - script_code: Código python puro para generar los nodos.
    """
    if not hasattr(adapter, 'execute_geometry_nodes_script'):
        return {'success': False, 'error': 'El adapter no soporta Geometry Nodes scripting.'}
        
    target_object = params.get('target_object', params.get('name', params.get('object')))
    script_code = params.get('script_code', params.get('script', ''))
    
    if not target_object or not script_code:
        return {'success': False, 'error': 'Faltan parámetros: target_object o script_code'}
        
    return adapter.execute_geometry_nodes_script(target_object, script_code)
