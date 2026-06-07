# core/utils/exceptions.py
"""
Excepciones personalizadas para el sistema ZULY.

Este módulo define una jerarquía de excepciones específicas del dominio
que permiten un manejo de errores más preciso y mensajes más informativos.
"""

from typing import Optional, Dict, Any


class ZulyException(Exception):
    """
    Excepción base para todas las excepciones de ZULY.
    
    Todas las excepciones personalizadas del sistema deben heredar de esta clase.
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """
        Inicializa la excepción.
        
        Args:
            message: Mensaje de error descriptivo
            details: Diccionario opcional con detalles adicionales del error
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class CommandExecutionError(ZulyException):
    """
    Error al ejecutar un comando.
    
    Se lanza cuando un comando falla durante su ejecución,
    ya sea por parámetros inválidos, estado incorrecto de la escena,
    o errores internos del comando.
    
    Example:
        >>> raise CommandExecutionError(
        ...     "No se pudo crear el cubo",
        ...     details={"command": "crearprimitivacubo", "reason": "Blender no disponible"}
        ... )
    """
    pass


class CommandNotFoundError(ZulyException):
    """
    Error cuando no se encuentra un comando solicitado.
    
    Se lanza cuando se intenta ejecutar un comando que no está
    registrado en el sistema.
    
    Example:
        >>> raise CommandNotFoundError(
        ...     "Comando 'creardragon' no encontrado",
        ...     details={"requested_command": "creardragon"}
        ... )
    """
    pass


class CommandLoadError(ZulyException):
    """
    Error al cargar un módulo de comando.
    
    Se lanza cuando hay problemas al importar o inicializar
    un módulo de comando.
    
    Example:
        >>> raise CommandLoadError(
        ...     "No se pudo cargar el módulo de comandos",
        ...     details={"module": "extended_commands", "error": "ImportError"}
        ... )
    """
    pass


class NLUError(ZulyException):
    """
    Error en el procesamiento de lenguaje natural.
    
    Se lanza cuando el sistema NLU no puede procesar correctamente
    una petición del usuario.
    
    Example:
        >>> raise NLUError(
        ...     "No se pudo interpretar la petición",
        ...     details={"user_input": "", "reason": "Entrada vacía"}
        ... )
    """
    pass


class ValidationError(ZulyException):
    """
    Error de validación de parámetros.
    
    Se lanza cuando los parámetros proporcionados no cumplen
    con los requisitos del comando.
    
    Example:
        >>> raise ValidationError(
        ...     "Parámetro 'location' inválido",
        ...     details={"parameter": "location", "value": "abc", "expected": "tuple[float, float, float]"}
        ... )
    """
    pass


class SceneMonitorError(ZulyException):
    """
    Error en el monitoreo de escena.
    
    Se lanza cuando hay problemas al capturar o analizar
    el estado de la escena de Blender.
    
    Example:
        >>> raise SceneMonitorError(
        ...     "No se pudo capturar el estado de la escena",
        ...     details={"reason": "bpy no disponible"}
        ... )
    """
    pass


class FileOperationError(ZulyException):
    """
    Error en operaciones de archivo.
    
    Se lanza cuando hay problemas al leer o escribir archivos.
    
    Example:
        >>> raise FileOperationError(
        ...     "No se pudo escribir el archivo",
        ...     details={"filepath": "/path/to/file.json", "error": "PermissionError"}
        ... )
    """
    pass


class ConfigurationError(ZulyException):
    """
    Error en la configuración del sistema.
    
    Se lanza cuando hay problemas con la configuración
    o cuando falta configuración requerida.
    
    Example:
        >>> raise ConfigurationError(
        ...     "Configuración de Blender inválida",
        ...     details={"key": "BLENDER_VERSION", "value": None}
        ... )
    """
    pass


class LearningEngineError(ZulyException):
    """
    Error en el motor de aprendizaje.
    
    Se lanza cuando hay problemas en el sistema de Learning Freedom
    o en la síntesis de estrategias.
    
    Example:
        >>> raise LearningEngineError(
        ...     "No se pudieron generar estrategias",
        ...     details={"user_request": "...", "reason": "Insuficientes datos de entrenamiento"}
        ... )
    """
    pass


class IntentClassificationError(NLUError):
    """
    Error al clasificar la intención del usuario.
    
    Subclase de NLUError específica para problemas en la
    clasificación de intenciones.
    
    Example:
        >>> raise IntentClassificationError(
        ...     "No se pudo determinar la intención",
        ...     details={"user_input": "haz algo raro", "confidence": 0.2}
        ... )
    """
    pass


class EntityExtractionError(NLUError):
    """
    Error al extraer entidades del texto.
    
    Subclase de NLUError específica para problemas en la
    extracción de entidades.
    
    Example:
        >>> raise EntityExtractionError(
        ...     "No se pudieron extraer las coordenadas",
        ...     details={"text": "mueve a xyz", "expected_entity": "location"}
        ... )
    """
    pass
