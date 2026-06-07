"""
scripting.py

Handlers para ejecución de scripts y lógica procedural en Blender.
FASE B: Automatización.
"""

from typing import Dict, Any
from core.utils.logging import log_success, log_warning, log_info

def run_python_script_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Ejecuta un script de Python arbitrario dentro del contexto de Blender (o Mock).
    
    Parameters:
        parameters: Dict con:
            - script_content: str (Código Python a ejecutar)
            - variables: Dict opcional (Variables a inyectar en el contexto global)
    
    Returns:
        Dict con resultado de la ejecución.
    """
    # Obtener adapter si no se proporciona (para verificar disponibilidad)
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}

    script_content = parameters.get('script_content')
    script_path = parameters.get('script_path')
    
    if script_path:
        try:
            import os
            # Resolver ruta relativa a la raíz del proyecto
            # Asumimos que ZULY se ejecuta desde la raíz
            full_path = os.path.abspath(script_path)
            if not os.path.exists(full_path):
                 return {'success': False, 'error': f"Script file not found: {full_path}"}
            
            with open(full_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
                
            log_info(f"Cargado script externo: {script_path}")
        except Exception as e:
            return {'success': False, 'error': f"Error loading script file: {e}"}

    if not script_content:
        return {'success': False, 'error': 'No script_content or script_path provided'}
    
    injected_vars = parameters.get('variables', {})
    
    try:
        # Preparar contexto de ejecución seguro
        # FASE 17: NO importamos bpy directamente - usamos adapter.run_python_script()
        import math
        import random

        # El adapter proporcionará bpy si está disponible
        # No importamos directamente para respetar la arquitectura
        bpy = None
        mathutils = None
        
        # Intentar obtener bpy del adapter si es posible
        try:
            # Algunos adapters pueden proporcionar acceso a bpy
            if hasattr(adapter, 'bpy_module'):
                bpy = adapter.bpy_module
        except:
            pass
        
        # Preparar espacio de nombres unificado
        exec_scope = globals().copy()
        exec_scope.update({
            'bpy': bpy,
            'math': math,
            'random': random,
            'mathutils': mathutils,
            'adapter': adapter,
            **injected_vars
        })
        
        # Ejecutar
        log_info(f"Ejecutando script procedural de {len(script_content)} bytes...")
        exec(script_content, exec_scope)
        
        # Verificar si el script definió un resultado
        script_result = exec_scope.get('result', 'Script executed successfully')
        
        log_success("Script procedural ejecutado correctamente")
        
        return {
            'success': True,
            'message': 'Script executed',
            'script_result': str(script_result),
            'context_keys': list(exec_scope.keys())
        }

    except Exception as e:
        log_warning(f"Error executing procedural script: {e}")
        return {
            'success': False,
            'error': str(e),
            'traceback': str(e) # Simplificado
        }
