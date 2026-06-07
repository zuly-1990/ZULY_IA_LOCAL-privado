# core/utils/validators.py
"""
Validadores centralizados para el sistema ZULY.

Este módulo proporciona funciones de validación reutilizables
para parámetros comunes de comandos y datos del sistema.
"""

from typing import Any, Dict, List, Tuple, Optional, Union
import re
from .exceptions import ValidationError


def validate_location(location: Any) -> Tuple[float, float, float]:
    """
    Valida y convierte un parámetro de ubicación a tupla de 3 floats.
    
    Args:
        location: Puede ser tupla, lista, o string con formato "x,y,z"
        
    Returns:
        Tupla de 3 floats (x, y, z)
        
    Raises:
        ValidationError: Si el formato es inválido
        
    Example:
        >>> validate_location([1, 2, 3])
        (1.0, 2.0, 3.0)
        >>> validate_location("1.5, 2.0, 3.5")
        (1.5, 2.0, 3.5)
    """
    try:
        # Si es string, parsear
        if isinstance(location, str):
            parts = [float(x.strip()) for x in location.split(',')]
            if len(parts) != 3:
                raise ValueError("Se esperan 3 coordenadas")
            return tuple(parts)
        
        # Si es lista o tupla
        if isinstance(location, (list, tuple)):
            if len(location) != 3:
                raise ValueError("Se esperan 3 coordenadas")
            return tuple(float(x) for x in location)
        
        raise TypeError(f"Tipo no soportado: {type(location)}")
        
    except (ValueError, TypeError) as e:
        raise ValidationError(
            f"Ubicación inválida: {location}",
            details={
                "value": str(location),
                "expected": "tuple[float, float, float] o 'x,y,z'",
                "error": str(e)
            }
        )


def validate_rotation(rotation: Any) -> Tuple[float, float, float]:
    """
    Valida y convierte un parámetro de rotación a tupla de 3 floats (en grados).
    
    Args:
        rotation: Puede ser tupla, lista, o string con formato "x,y,z"
        
    Returns:
        Tupla de 3 floats (rx, ry, rz) en grados
        
    Raises:
        ValidationError: Si el formato es inválido
    """
    try:
        # Reutilizar lógica de validate_location
        result = validate_location(rotation)
        
        # Normalizar ángulos a rango [0, 360)
        normalized = tuple(angle % 360.0 for angle in result)
        return normalized
        
    except ValidationError as e:
        # Re-lanzar con mensaje específico de rotación
        raise ValidationError(
            f"Rotación inválida: {rotation}",
            details={
                "value": str(rotation),
                "expected": "tuple[float, float, float] en grados",
                "error": str(e.details.get('error', ''))
            }
        )


def validate_scale(scale: Any) -> Union[float, Tuple[float, float, float]]:
    """
    Valida y convierte un parámetro de escala.
    
    Args:
        scale: Puede ser float (escala uniforme) o tupla de 3 floats
        
    Returns:
        Float para escala uniforme o tupla de 3 floats
        
    Raises:
        ValidationError: Si el formato es inválido
        
    Example:
        >>> validate_scale(2.0)
        2.0
        >>> validate_scale([1, 2, 3])
        (1.0, 2.0, 3.0)
    """
    try:
        # Si es número, escala uniforme
        if isinstance(scale, (int, float)):
            if scale <= 0:
                raise ValueError("La escala debe ser positiva")
            return float(scale)
        
        # Si es tupla/lista, escala no uniforme
        if isinstance(scale, (list, tuple)):
            if len(scale) != 3:
                raise ValueError("Se esperan 3 valores de escala")
            result = tuple(float(x) for x in scale)
            if any(x <= 0 for x in result):
                raise ValueError("Todos los valores de escala deben ser positivos")
            return result
        
        # Si es string, intentar parsear
        if isinstance(scale, str):
            # Intentar como número único
            try:
                value = float(scale.strip())
                if value <= 0:
                    raise ValueError("La escala debe ser positiva")
                return value
            except ValueError:
                # Intentar como tupla
                return validate_location(scale)
        
        raise TypeError(f"Tipo no soportado: {type(scale)}")
        
    except (ValueError, TypeError) as e:
        raise ValidationError(
            f"Escala inválida: {scale}",
            details={
                "value": str(scale),
                "expected": "float > 0 o tuple[float, float, float]",
                "error": str(e)
            }
        )


def validate_material_name(material: str, valid_materials: List[str]) -> str:
    """
    Valida que un nombre de material sea válido.
    
    Args:
        material: Nombre del material
        valid_materials: Lista de materiales válidos
        
    Returns:
        Nombre del material validado (lowercase)
        
    Raises:
        ValidationError: Si el material no es válido
    """
    if not isinstance(material, str):
        raise ValidationError(
            "El material debe ser un string",
            details={"value": str(material), "type": type(material).__name__}
        )
    
    material_lower = material.lower().strip()
    
    if material_lower not in [m.lower() for m in valid_materials]:
        raise ValidationError(
            f"Material '{material}' no válido",
            details={
                "value": material,
                "valid_options": valid_materials
            }
        )
    
    return material_lower


def validate_object_type(obj_type: str, valid_types: List[str]) -> str:
    """
    Valida que un tipo de objeto 3D sea válido.
    
    Args:
        obj_type: Tipo de objeto (cubo, esfera, etc.)
        valid_types: Lista de tipos válidos
        
    Returns:
        Tipo de objeto validado (lowercase)
        
    Raises:
        ValidationError: Si el tipo no es válido
    """
    if not isinstance(obj_type, str):
        raise ValidationError(
            "El tipo de objeto debe ser un string",
            details={"value": str(obj_type), "type": type(obj_type).__name__}
        )
    
    obj_type_lower = obj_type.lower().strip()
    
    if obj_type_lower not in [t.lower() for t in valid_types]:
        raise ValidationError(
            f"Tipo de objeto '{obj_type}' no válido",
            details={
                "value": obj_type,
                "valid_options": valid_types
            }
        )
    
    return obj_type_lower


def validate_positive_number(value: Any, name: str = "valor") -> float:
    """
    Valida que un valor sea un número positivo.
    
    Args:
        value: Valor a validar
        name: Nombre del parámetro (para mensajes de error)
        
    Returns:
        Valor como float
        
    Raises:
        ValidationError: Si no es un número positivo
    """
    try:
        num = float(value)
        if num <= 0:
            raise ValueError("Debe ser positivo")
        return num
    except (ValueError, TypeError) as e:
        raise ValidationError(
            f"{name} debe ser un número positivo",
            details={"value": str(value), "error": str(e)}
        )


def validate_color_rgb(color: Any) -> Tuple[float, float, float]:
    """
    Valida un color RGB.
    
    Args:
        color: Puede ser tupla de 3 floats [0-1] o string hex "#RRGGBB"
        
    Returns:
        Tupla de 3 floats en rango [0, 1]
        
    Raises:
        ValidationError: Si el formato es inválido
        
    Example:
        >>> validate_color_rgb([1.0, 0.5, 0.0])
        (1.0, 0.5, 0.0)
        >>> validate_color_rgb("#FF8000")
        (1.0, 0.5019607843137255, 0.0)
    """
    try:
        # Si es string hex
        if isinstance(color, str):
            color = color.strip()
            if color.startswith('#'):
                color = color[1:]
            if len(color) != 6:
                raise ValueError("Formato hex debe ser #RRGGBB")
            
            r = int(color[0:2], 16) / 255.0
            g = int(color[2:4], 16) / 255.0
            b = int(color[4:6], 16) / 255.0
            return (r, g, b)
        
        # Si es tupla/lista
        if isinstance(color, (list, tuple)):
            if len(color) != 3:
                raise ValueError("Se esperan 3 valores RGB")
            
            rgb = tuple(float(x) for x in color)
            
            # Validar rango [0, 1]
            if not all(0.0 <= x <= 1.0 for x in rgb):
                raise ValueError("Valores RGB deben estar en rango [0, 1]")
            
            return rgb
        
        raise TypeError(f"Tipo no soportado: {type(color)}")
        
    except (ValueError, TypeError) as e:
        raise ValidationError(
            f"Color RGB inválido: {color}",
            details={
                "value": str(color),
                "expected": "tuple[float, float, float] [0-1] o '#RRGGBB'",
                "error": str(e)
            }
        )


def validate_command_parameters(
    command_class: type,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Valida parámetros para un comando específico.
    
    Esta función verifica que los parámetros proporcionados sean
    compatibles con los requeridos por el comando.
    
    Args:
        command_class: Clase del comando
        parameters: Diccionario de parámetros
        
    Returns:
        Diccionario de parámetros validados y convertidos
        
    Raises:
        ValidationError: Si hay parámetros inválidos o faltantes
    """
    import inspect
    
    # Obtener signature del método ejecutar
    if not hasattr(command_class, 'ejecutar'):
        raise ValidationError(
            f"Comando {command_class.__name__} no tiene método 'ejecutar'",
            details={"command_class": command_class.__name__}
        )
    
    sig = inspect.signature(command_class.ejecutar)
    required_params = []
    optional_params = []
    
    for param_name, param in sig.parameters.items():
        if param_name == 'self':
            continue
        
        if param.default == inspect.Parameter.empty:
            required_params.append(param_name)
        else:
            optional_params.append(param_name)
    
    # Verificar parámetros requeridos
    missing = [p for p in required_params if p not in parameters]
    if missing:
        raise ValidationError(
            f"Faltan parámetros requeridos: {', '.join(missing)}",
            details={
                "command": command_class.__name__,
                "missing_params": missing,
                "provided_params": list(parameters.keys())
            }
        )
    
    # TODO: Validar tipos específicos según anotaciones
    
    return parameters
