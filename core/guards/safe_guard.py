from typing import Dict, Any

class SafeGuard:
    """
    Sistema de Guardia de Zuly (SafeGuard)
    Evalúa comandos antes de su ejecución para prevenir acciones destructivas no intencionadas.
    """
    
    def __init__(self):
        # Lista de comandos que SIEMPRE requieren confirmación humana
        self.dangerous_commands = {
            'blender.delete_object': 'Peligro de pérdida de geometría.',
            'blender.clear_scene': 'Peligro de borrar todo el proyecto.',
            'blender.run_python_script': 'Peligro de ejecución de código arbitrario.',
            'blender.save_project': 'Peligro de sobreescribir archivos existentes sin respaldo.',
            'system.delete_file': 'Peligro de borrado a nivel sistema operativo.'
        }
        
    def evaluate(self, command_name: str, parameters: Dict[str, Any], force_execute: bool = False) -> Dict[str, Any]:
        """
        Evalúa si un comando es seguro para ejecutarse.
        
        Retorna un diccionario:
        {
            'is_safe': bool,
            'requires_confirmation': bool,
            'reason': str
        }
        """
        
        if force_execute:
            return {
                'is_safe': True,
                'requires_confirmation': False,
                'reason': 'Confirmación forzada por el usuario (override).'
            }
            
        command_lower = command_name.lower()
        
        # 1. Chequeo de Lista Negra / Comandos Peligrosos
        if command_lower in self.dangerous_commands:
            return {
                'is_safe': False,
                'requires_confirmation': True,
                'reason': self.dangerous_commands[command_lower]
            }
            
        # 2. Validaciones Específicas de Parámetros
        if command_lower == 'blender.scale_object':
            scale_val = parameters.get('scale', [1.0, 1.0, 1.0])
            if isinstance(scale_val, (list, tuple)) and any(s <= 0 for s in scale_val):
                return {
                    'is_safe': False,
                    'requires_confirmation': True,
                    'reason': 'Peligro de colapsar la malla escalando a cero o usando valores negativos.'
                }
        
        if command_lower == 'blender.add_subdivision_surface':
            levels = parameters.get('levels', 1)
            if isinstance(levels, (int, float)) and levels > 4:
                return {
                    'is_safe': False,
                    'requires_confirmation': True,
                    'reason': 'Peligro de sobrecargar la memoria con más de 4 niveles de subdivisión.'
                }
                
        # Si pasa todo, es seguro
        return {
            'is_safe': True,
            'requires_confirmation': False,
            'reason': 'Comando verificado por SafeGuard.'
        }
