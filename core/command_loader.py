# core/command_loader.py
"""
Cargador dinámico de comandos para el agente Zuly.
"""

import os
import importlib
import inspect
from pathlib import Path
from core.utils.logging import log_info, log_warning, log_error, log_debug
from core.utils.exceptions import CommandLoadError, CommandNotFoundError

class CommandLoader:
    """Carga dinámicamente los comandos disponibles desde el directorio de comandos."""
    
    def __init__(self, commands_dir=None):
        """
        Inicializa el cargador de comandos.
        
        :param commands_dir: Directorio donde se encuentran los comandos
        """
        if commands_dir is None:
            # Directorio por defecto: core/commands/
            self.commands_dir = Path(__file__).parent / "commands"
        else:
            self.commands_dir = Path(commands_dir)
        
        self.commands = {}
    
    def load_commands(self):
        """
        Carga todos los comandos disponibles desde el directorio de comandos.
        
        :return: Diccionario con {nombre_comando: clase_comando}
        """
        log_info(f"Cargando comandos desde: {self.commands_dir}")
        
        # Intentar cargar desde extended_commands.py
        try:
            from core.commands import extended_commands
            self._load_from_module(extended_commands)
        except ImportError as e:
            log_warning(f"No se pudo cargar extended_commands: {e}")
        
        # Intentar cargar desde blender_handlers/
        handlers_dir = self.commands_dir / "blender_handlers"
        if handlers_dir.exists():
            self._load_from_directory(handlers_dir)
        
        log_info(f"Total de comandos cargados: {len(self.commands)}")
        return self.commands
    
    def _load_from_module(self, module):
        """
        Carga comandos desde un módulo específico.
        
        :param module: Módulo Python a inspeccionar
        :raises CommandLoadError: Si hay problemas cargando comandos
        """
        try:
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and self._is_command_class(obj):
                    command_name = self._get_command_name(obj, name)
                    self.commands[command_name.lower()] = obj
                    log_debug(f"  ✓ Comando cargado: {command_name}")
        except Exception as e:
            module_name = getattr(module, '__name__', 'unknown')
            log_error(f"Error inspeccionando módulo {module_name}: {e}")
            raise CommandLoadError(
                f"No se pudo cargar comandos desde módulo",
                details={"module": module_name, "error": str(e), "error_type": type(e).__name__}
            )
    
    def _load_from_directory(self, directory):
        """
        Carga comandos desde un directorio de módulos Python.
        
        :param directory: Path al directorio
        """
        if not directory.exists():
            log_warning(f"Directorio de comandos no existe: {directory}")
            return
        
        loaded_count = 0
        error_count = 0
        
        for file_path in directory.glob("*.py"):
            if file_path.name.startswith("_"):
                continue
            
            try:
                # Construir el nombre del módulo
                module_name = f"core.commands.blender_handlers.{file_path.stem}"
                module = importlib.import_module(module_name)
                self._load_from_module(module)
                loaded_count += 1
            except CommandLoadError:
                # Re-lanzar errores de carga de comandos
                raise
            except ImportError as e:
                error_count += 1
                log_warning(f"No se pudo importar {file_path.name}: {e}")
            except Exception as e:
                error_count += 1
                log_error(f"Error inesperado cargando {file_path.name}: {e}")
        
        log_info(f"Cargados {loaded_count} módulos de comandos ({error_count} errores)")
    
    def _is_command_class(self, obj):
        """Verifica si un objeto es una clase de comando válida."""
        # Debe tener métodos ejecutar() y validar()
        return (hasattr(obj, 'ejecutar') and 
                hasattr(obj, 'validar') and
                not obj.__name__.startswith('_'))
    
    def _get_command_name(self, command_class, default_name):
        """Obtiene el nombre del comando desde la clase."""
        # Intentar obtener desde atributo nombre
        if hasattr(command_class, 'nombre'):
            return command_class.nombre
        
        # Intentar obtener desde el nombre de la clase
        return default_name.lower()
    
    def get_command(self, command_name, raise_if_not_found=False):
        """
        Obtiene una clase de comando por su nombre.
        
        :param command_name: Nombre del comando
        :param raise_if_not_found: Si True, lanza excepción si no se encuentra
        :return: Clase del comando o None
        :raises CommandNotFoundError: Si raise_if_not_found=True y comando no existe
        """
        cmd = self.commands.get(command_name.lower())
        
        if cmd is None and raise_if_not_found:
            raise CommandNotFoundError(
                f"Comando '{command_name}' no encontrado",
                details={
                    "requested_command": command_name,
                    "available_commands": list(self.commands.keys())[:10]  # Primeros 10
                }
            )
        
        return cmd
    
    def list_commands(self):
        """Retorna una lista de nombres de comandos disponibles."""
        return list(self.commands.keys())
