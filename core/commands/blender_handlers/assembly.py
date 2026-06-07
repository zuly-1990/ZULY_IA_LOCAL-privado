"""
assembly.py

FASE 20: Handlers para comandos de construcción y ensamblaje.

Conecta AssemblyCore con el sistema de comandos del Agent.
"""

from typing import Dict, Any
from core.assembly.assembly_core import AssemblyCore
from core.assembly.pattern_storage import PatternStorage
from core.validation.v3_validator import V3Validator
from core.utils.logging import log_info, log_warning, log_error, log_success


def build_structure_handler(parameters: Dict[str, Any], adapter) -> Dict[str, Any]:
    """
    Handler para construir estructuras compuestas.
    
    Args:
        parameters: {
            'structure_def': Dict (definición de estructura),
            'validate': bool (ejecutar validación V3, default True)
        }
        adapter: EngineAdapter
    
    Returns:
        {
            'success': bool,
            'structure_name': str,
            'created_objects': [str],
            'validation': Dict (si validate=True),
            'message': str
        }
    """
    log_info("🏗️ Handler: build_structure")
    
    structure_def = parameters.get('structure_def')
    should_validate = parameters.get('validate', True)
    
    if not structure_def:
        return {
            'success': False,
            'effect': 'none',
            'message': 'No se proporcionó definición de estructura'
        }
    
    # Crear estructura
    assembly = AssemblyCore(adapter=adapter)
    result = assembly.create_structure(structure_def)
    
    if not result.get('success'):
        return {
            'success': False,
            'effect': 'none',
            'message': f"Error construyendo estructura: {result.get('error')}"
        }
    
    # Validación V3 (opcional)
    validation_result = None
    if should_validate:
        validator = V3Validator(adapter=adapter)
        mapping = result.get('component_mapping', {})
        validation_result = validator.validate_structure(mapping)
        
        if not validation_result.get('valid'):
            log_warning(f"⚠️ Estructura creada pero con errores de validación V3")
        elif validation_result.get('warnings'):
            log_warning(f"⚠️ Estructura válida con {len(validation_result['warnings'])} advertencias")
    
    # Preparar respuesta
    created_count = len(result.get('created_objects', []))
    structure_name = result.get('structure_name', 'estructura')
    
    log_success(f"✅ Estructura '{structure_name}' creada: {created_count} objetos")
    
    return {
        'success': True,
        'effect': 'create',
        'result': {
            'name': structure_name,
            'created_objects': result.get('created_objects'),
            'stats': result.get('stats'),
            'component_mapping': result.get('component_mapping')
        },
        'validation': validation_result,
        'message': f"Estructura '{structure_name}' creada con {created_count} objetos"
    }


def save_pattern_handler(parameters: Dict[str, Any], adapter) -> Dict[str, Any]:
    """
    Handler para guardar un patrón de construcción.
    
    Args:
        parameters: {
            'name': str,
            'description': str,
            'components': List[Dict]
        }
        adapter: EngineAdapter (no usado, pero mantenido por consistencia)
    
    Returns:
        {
            'success': bool,
            'pattern_name': str,
            'message': str
        }
    """
    log_info("💾 Handler: save_pattern")
    
    name = parameters.get('name')
    description = parameters.get('description', '')
    components = parameters.get('components', [])
    
    if not name:
        return {
            'success': False,
            'effect': 'none',
            'message': 'No se proporcionó nombre de patrón'
        }
    
    if not components:
        return {
            'success': False,
            'effect': 'none',
            'message': 'No se proporcionaron componentes'
        }
    
    # Validar patrón antes de guardar
    validator = V3Validator(adapter=adapter)
    pattern_def = {
        'name': name,
        'description': description,
        'components': components
    }
    validation = validator.validate_pattern(pattern_def)
    
    if not validation.get('valid'):
        log_warning(f"⚠️ Patrón '{name}' tiene errores de validación")
        return {
            'success': False,
            'effect': 'none',
            'message': f"Patrón inválido: {validation.get('errors')}",
            'validation_errors': validation.get('errors')
        }
    
    # Guardar patrón
    storage = PatternStorage()
    success = storage.save_pattern(name, description, components)
    
    if success:
        log_success(f"✅ Patrón '{name}' guardado ({len(components)} componentes)")
        return {
            'success': True,
            'effect': 'property',
            'result': {
                'name': name,
                'component_count': len(components)
            },
            'message': f"Patrón '{name}' guardado correctamente"
        }
    else:
        log_error(f"❌ Error guardando patrón '{name}'")
        return {
            'success': False,
            'effect': 'none',
            'message': f"Error al guardar patrón '{name}'"
        }


def load_pattern_handler(parameters: Dict[str, Any], adapter) -> Dict[str, Any]:
    """
    Handler para cargar y construir un patrón guardado.
    
    Args:
        parameters: {
            'name': str,
            'location': [x, y, z] (opcional, offset para toda la estructura),
            'validate': bool (ejecutar validación V3, default True)
        }
        adapter: EngineAdapter
    
    Returns:
        {
            'success': bool,
            'pattern_name': str,
            'created_objects': [str],
            'validation': Dict,
            'message': str
        }
    """
    log_info("📂 Handler: load_pattern")
    
    name = parameters.get('name')
    location_offset = parameters.get('location', [0, 0, 0])
    should_validate = parameters.get('validate', True)
    
    if not name:
        return {
            'success': False,
            'effect': 'none',
            'message': 'No se proporcionó nombre de patrón'
        }
    
    # Cargar patrón
    storage = PatternStorage()
    pattern = storage.get_pattern(name)
    
    if not pattern:
        log_warning(f"⚠️ Patrón '{name}' no encontrado")
        return {
            'success': False,
            'effect': 'none',
            'message': f"Patrón '{name}' no existe"
        }
    
    # Aplicar offset a todos los componentes (si se especificó)
    components = pattern.get('components', [])
    if location_offset != [0, 0, 0]:
        for comp in components:
            original_loc = comp.get('location', [0, 0, 0])
            comp['location'] = [
                original_loc[0] + location_offset[0],
                original_loc[1] + location_offset[1],
                original_loc[2] + location_offset[2]
            ]
    
    # Construir estructura desde patrón
    structure_def = {
        'name': pattern.get('name'),
        'components': components
    }
    
    return build_structure_handler(
        {'structure_def': structure_def, 'validate': should_validate},
        adapter
    )


def list_patterns_handler(parameters: Dict[str, Any], adapter) -> Dict[str, Any]:
    """
    Handler para listar patrones disponibles.
    
    Args:
        parameters: {} (vacío)
        adapter: EngineAdapter (no usado)
    
    Returns:
        {
            'success': bool,
            'patterns': List[Dict],
            'count': int,
            'message': str
        }
    """
    log_info("📋 Handler: list_patterns")
    
    storage = PatternStorage()
    patterns = storage.list_patterns()
    
    log_info(f"📋 {len(patterns)} patrones disponibles")
    
    return {
        'success': True,
        'effect': 'none',
        'result': {
            'patterns': patterns,
            'count': len(patterns)
        },
        'message': f"{len(patterns)} patrones disponibles"
    }
