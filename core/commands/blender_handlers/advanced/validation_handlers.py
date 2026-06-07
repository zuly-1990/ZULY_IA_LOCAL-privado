"""
core/commands/blender_handlers/advanced/validation_handlers.py

Handlers para invocar el Validador V3 a través del sistema cognitivo.
"""
from typing import Dict, Any
from core.adapters import get_engine_adapter
from core.utils.logging import log_info, log_error
from core.validation.v3_validator import V3Validator

def validate_topology_handler(params: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Handler para invocar la validación topológica V3 sobre un objeto.
    
    Args:
        params: Diccionario con 'object_name'
        adapter: EngineAdapter (inyectado por IntentRouter)
        
    Returns:
        Diccionario con la clasificación y métricas del validador V3.
    """
    object_name = params.get('object_name')
    if not object_name:
        return {'status': 'failed', 'error': 'Falta el parámetro object_name'}
        
    log_info(f"Iniciando validación V3 para el objeto: {object_name}")
    
    if adapter is None:
        adapter = get_engine_adapter()
        
    validator = V3Validator()
    
    result = validator.validate(object_name, adapter)
    
    return {
        'status': 'success' if result['verified'] else 'failed',
        'result': result
    }
