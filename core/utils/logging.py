"""
Módulo de logging para LYZU Core
Proporciona funciones de registro simplificadas
"""

import sys
from datetime import datetime
from pathlib import Path

# Configurar encoding UTF-8 para evitar errores con emojis en Windows
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    # Python < 3.7 no tiene reconfigure
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def log(message: str, level: str = "INFO", module: str = "LYZU") -> None:
    """
    Registra un mensaje con timestamp y nivel.
    
    Args:
        message: Mensaje a registrar
        level: Nivel de log (INFO, WARNING, ERROR, SUCCESS)
        module: Nombre del módulo que genera el log
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {level:8} [{module}] {message}"
    print(formatted)


def log_info(message: str, module: str = "LYZU") -> None:
    """Log nivel INFO"""
    log(message, "INFO", module)


def log_warning(message: str, module: str = "LYZU") -> None:
    """Log nivel WARNING"""
    log(message, "WARNING", module)


def log_error(message: str, module: str = "LYZU") -> None:
    """Log nivel ERROR"""
    log(message, "ERROR", module)


def log_success(message: str, module: str = "LYZU") -> None:
    """Log nivel SUCCESS"""
    log(message, "SUCCESS", module)


def log_debug(message: str, module: str = "LYZU") -> None:
    """Log nivel DEBUG"""
    log(message, "DEBUG", module)
