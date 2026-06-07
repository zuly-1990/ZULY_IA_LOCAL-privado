# core/utils/file_manager.py
"""
Gestor de archivos para el agente Zuly.
Maneja lectura/escritura de archivos JSON, reportes y exportaciones.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from core.utils.logging import log
from core.utils.exceptions import FileOperationError

class FileManager:
    """Gestor de archivos para operaciones de I/O."""
    
    @staticmethod
    def write_json(filepath: str, data: Dict, indent: int = 2) -> bool:
        """
        Escribe datos a un archivo JSON.
        
        :param filepath: Ruta del archivo
        :param data: Datos a escribir
        :param indent: Nivel de indentación
        :return: True si fue exitoso, False en caso contrario
        """
        try:
            # Crear directorio si no existe
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            
            log.info(f"Archivo JSON escrito: {filepath}")
            return True
        
        except (IOError, OSError, PermissionError) as e:
            log.error(f"Error de I/O escribiendo JSON a {filepath}: {e}")
            raise FileOperationError(
                f"No se pudo escribir archivo JSON",
                details={"filepath": filepath, "error": str(e), "error_type": type(e).__name__}
            )
        except (TypeError, ValueError) as e:
            log.error(f"Error serializando datos a JSON: {e}")
            raise FileOperationError(
                f"Datos no serializables a JSON",
                details={"filepath": filepath, "error": str(e)}
            )
    
    @staticmethod
    def read_json(filepath: str) -> Optional[Dict]:
        """
        Lee datos desde un archivo JSON.
        
        :param filepath: Ruta del archivo
        :return: Datos leídos o None si hay error
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            log.info(f"Archivo JSON leído: {filepath}")
            return data
        
        except FileNotFoundError:
            log.warning(f"Archivo no encontrado: {filepath}")
            return None
        
        except Exception as e:
            log.error(f"Error leyendo JSON desde {filepath}: {e}")
            return None
    
    @staticmethod
    def write_text(filepath: str, content: str) -> bool:
        """
        Escribe contenido de texto a un archivo.
        
        :param filepath: Ruta del archivo
        :param content: Contenido a escribir
        :return: True si fue exitoso, False en caso contrario
        """
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            log.info(f"Archivo de texto escrito: {filepath}")
            return True
        
        except Exception as e:
            log.error(f"Error escribiendo texto a {filepath}: {e}")
            return False
    
    @staticmethod
    def read_text(filepath: str) -> Optional[str]:
        """
        Lee contenido de texto desde un archivo.
        
        :param filepath: Ruta del archivo
        :return: Contenido leído o None si hay error
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            log.info(f"Archivo de texto leído: {filepath}")
            return content
        
        except FileNotFoundError:
            log.warning(f"Archivo no encontrado: {filepath}")
            return None
        
        except Exception as e:
            log.error(f"Error leyendo texto desde {filepath}: {e}")
            return None
    
    @staticmethod
    def ensure_directory(dirpath: str) -> bool:
        """
        Asegura que un directorio exista, creándolo si es necesario.
        
        :param dirpath: Ruta del directorio
        :return: True si el directorio existe o fue creado
        """
        try:
            Path(dirpath).mkdir(parents=True, exist_ok=True)
            return True
        
        except Exception as e:
            log.error(f"Error creando directorio {dirpath}: {e}")
            return False
    
    @staticmethod
    def generate_timestamped_filename(prefix: str, extension: str = 'json') -> str:
        """
        Genera un nombre de archivo con timestamp.
        
        :param prefix: Prefijo del nombre de archivo
        :param extension: Extensión del archivo
        :return: Nombre de archivo generado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
    
    @staticmethod
    def list_files(directory: str, pattern: str = '*') -> list:
        """
        Lista archivos en un directorio que coincidan con un patrón.
        
        :param directory: Directorio a listar
        :param pattern: Patrón de archivos (glob)
        :return: Lista de rutas de archivos
        """
        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                return []
            
            files = [str(f) for f in dir_path.glob(pattern) if f.is_file()]
            return files
        
        except Exception as e:
            log.error(f"Error listando archivos en {directory}: {e}")
            return []
