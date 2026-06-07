"""
core/commands/blender_handlers/advanced/universe_engine_handler.py

Handler para generar entornos espaciales y cosmicos.
Parte del modulo advanced de ZULY.
"""
from typing import Dict, Any
from core.adapters import get_engine_adapter
from core.utils.logging import log_info, log_error, log_success
import os
import json
import random

def create_space_environment_handler(params: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Handler para crear un entorno espacial basico.
    
    Args:
        params: Diccionario con 'star_count', 'nebula_color', 'output_name'.
        adapter: EngineAdapter inyectado por IntentRouter.
        
    Returns:
        Dict con resultado de la creacion.
    """
    log_info("[UNIVERSE] Iniciando creacion de entorno espacial")
    
    if adapter is None:
        adapter = get_engine_adapter()
    
    star_count = params.get('star_count', 200)
    nebula_color = params.get('nebula_color', [0.1, 0.0, 0.3])
    output_name = params.get('output_name', 'space_env_default')
    
    result = adapter.create_space_environment(
        star_count=star_count,
        nebula_color=nebula_color,
        output_name=output_name
    )
    
    if result.get('success', False):
        log_success(f"[UNIVERSE] Entorno espacial creado: {output_name}")
    else:
        log_error(f"[UNIVERSE] Fallo al crear entorno: {result.get('error')}")
    
    return result

def create_planet_handler(params: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Handler para crear un planeta con atmosfera.
    
    Args:
        params: Diccionario con 'radius', 'atmosphere', 'rings', 'output_name'.
        adapter: EngineAdapter inyectado por IntentRouter.
    """
    log_info("[UNIVERSE] Iniciando creacion de planeta")
    
    if adapter is None:
        adapter = get_engine_adapter()
    
    radius = params.get('radius', 2.0)
    atmosphere = params.get('atmosphere', True)
    rings = params.get('rings', False)
    output_name = params.get('output_name', 'planet_default')
    
    result = adapter.create_planet(
        radius=radius,
        atmosphere=atmosphere,
        rings=rings,
        output_name=output_name
    )
    
    if result.get('success', False):
        log_success(f"[UNIVERSE] Planeta creado: {output_name}")
    else:
        log_error(f"[UNIVERSE] Fallo al crear planeta: {result.get('error')}")
    
    return result

def create_asteroid_belt_handler(params: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Handler para crear un cinturon de asteroides.
    
    Args:
        params: Diccionario con 'count', 'radius_min', 'radius_max', 'output_name'.
        adapter: EngineAdapter inyectado por IntentRouter.
    """
    log_info("[UNIVERSE] Iniciando creacion de cinturon de asteroides")
    
    if adapter is None:
        adapter = get_engine_adapter()
    
    count = params.get('count', 50)
    radius_min = params.get('radius_min', 5.0)
    radius_max = params.get('radius_max', 8.0)
    output_name = params.get('output_name', 'asteroid_belt_default')
    
    result = adapter.create_asteroid_belt(
        count=count,
        radius_min=radius_min,
        radius_max=radius_max,
        output_name=output_name
    )
    
    if result.get('success', False):
        log_success(f"[UNIVERSE] Cinturon de asteroides creado: {output_name}")
    else:
        log_error(f"[UNIVERSE] Fallo al crear asteroides: {result.get('error')}")
    
    return result
