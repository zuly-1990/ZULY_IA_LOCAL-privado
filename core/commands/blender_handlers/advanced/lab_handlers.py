"""
core/commands/blender_handlers/advanced/lab_handlers.py

Handlers para invocar el ZULY LAB y el escáner inverso.
Extrae patrones topológicos de modelos 3D y los envía a la memoria.
"""
from typing import Dict, Any
from core.adapters import get_engine_adapter
from core.utils.logging import log_info, log_error, log_success
import os
import json

def scan_and_learn_handler(params: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Handler para invocar la Ingeniería Inversa (Escáner Pasivo).
    
    Args:
        params: Diccionario que puede contener 'output_name' para nombrar el patrón.
        adapter: EngineAdapter (inyectado por IntentRouter)
        
    Returns:
        Diccionario con el patrón extraído.
    """
    log_info("Iniciando Escaneo Pasivo (ZULY LAB)")
    
    if adapter is None:
        adapter = get_engine_adapter()
        
    result = adapter.scan_scene_pattern()
    if not result.get('success', False):
        log_error(f"[LAB] Fallo en el escáner: {result.get('error')}")
        return result
        
    pattern = result.get('pattern', {})
    
    # Guardar en memoria de Zuly (archivo de conocimiento manual por ahora)
    output_name = params.get('output_name', 'learned_pattern_v1')
    save_dir = os.path.join("C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL", "knowledge_base", "patterns", "learned")
    os.makedirs(save_dir, exist_ok=True)
    
    file_path = os.path.join(save_dir, f"{output_name}.json")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(pattern, f, indent=4)
        log_success(f"[LAB] Patrón guardado exitosamente en: {file_path}")
    except Exception as e:
        log_error(f"[LAB] No se pudo guardar el patrón: {e}")
    
    return {
        'success': True,
        'pattern_data': pattern,
        'saved_path': file_path
    }

def validate_topology_handler(params: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Handler para la Auditoría de Malla (V3).
    Analiza si el objeto es estanco (watertight) y otras métricas.
    """
    object_name = params.get('object_name')
    if not object_name:
        return {'success': False, 'error': "Debe especificar 'object_name'"}

    if adapter is None:
        adapter = get_engine_adapter()
        
    log_info(f"[LAB] Iniciando auditoría de topología para: {object_name}")
    result = adapter.validate_mesh_topology(object_name)
    
    if result.get('success'):
        log_success(f"[LAB] Auditoría V3 completada para '{object_name}'")
        return {
            'success': True,
            'is_watertight': result.get('metrics', {}).get('is_watertight', False),
            'metrics': result.get('metrics', {}),
            'feedback': f"Auditoría V3 completa para {object_name}"
        }
    else:
        log_error(f"[LAB] Fallo en la auditoría de {object_name}: {result.get('error')}")
        
    return result
