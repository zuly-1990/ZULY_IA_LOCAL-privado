"""
core/intents/entity_extractor.py
================================

Extractor de entidades. Transforma órdenes en lenguaje natural 
a parámetros estructurados listos para comandos.

Ejemplo:
    "Crea un cubo de 5 metros en posición 2,3,4"
    
    ↓ (Extractor)
    
    {
        'objeto': 'cubo',
        'tamaño': 5,
        'unidad': 'metros',
        'posición': (2, 3, 4)
    }
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Entity:
    """Representa una entidad extraída de una orden."""
    name: str
    value: Any
    confidence: float
    entity_type: str  # 'object', 'number', 'position', 'color', etc.


class EntityExtractor:
    """
    Extrae entidades (parámetros) de órdenes en lenguaje natural.
    
    Utiliza reglas semánticas y patrones regex para detectar:
    - Objetos: cubo, esfera, cilindro, etc.
    - Números: tamaños, cantidades, posiciones
    - Colores: rojo, azul, verde, etc.
    - Posiciones: coordenadas (x,y,z)
    - Modificadores: grande, pequeño, alto, etc.
    """
    
    # Diccionario de objetos reconocibles
    OBJECTS = {
        'cubo': {'alternatives': ['cubo', 'box', 'cube'], 'blender_type': 'Cube'},
        'esfera': {'alternatives': ['esfera', 'bola', 'sphere'], 'blender_type': 'UV Sphere'},
        'cilindro': {'alternatives': ['cilindro', 'cylinder'], 'blender_type': 'Cylinder'},
        'cono': {'alternatives': ['cono', 'cone'], 'blender_type': 'Cone'},
        'toroide': {'alternatives': ['toroide', 'torus'], 'blender_type': 'Torus'},
        'plano': {'alternatives': ['plano', 'plane'], 'blender_type': 'Plane'},
        'luz': {'alternatives': ['luz', 'light'], 'blender_type': 'Light'},
    }
    
    # Diccionario de colores
    COLORS = {
        'rojo': (1.0, 0.0, 0.0),
        'verde': (0.0, 1.0, 0.0),
        'azul': (0.0, 0.0, 1.0),
        'amarillo': (1.0, 1.0, 0.0),
        'blanco': (1.0, 1.0, 1.0),
        'negro': (0.0, 0.0, 0.0),
        'gris': (0.5, 0.5, 0.5),
        'naranja': (1.0, 0.5, 0.0),
        'violeta': (0.5, 0.0, 1.0),
    }
    
    # Patrones regex
    PATTERNS = {
        'posicion': r'posición?\s*[:=]?\s*(\d+\.?\d*)[,\s]+(\d+\.?\d*)[,\s]+(\d+\.?\d*)',
        'tamaño': r'(tamaño|tamaño|size)\s*[:=]?\s*(\d+\.?\d*)\s*(metros|m|cm|mm)?',
        'escala': r'escala\s*[:=]?\s*(\d+\.?\d*)',
        'rotacion': r'(rotación|rotacion|rotation)\s*[:=]?\s*(\d+\.?\d*)[,\s]+(\d+\.?\d*)[,\s]+(\d+\.?\d*)',
        'cantidad': r'(crear|duplicar|hacer|add)\s*(\d+)\s*(cubos|esferas|objetos)?',
        'filepath': r'(?:filepath|archivo|ruta|en|in)\s*[:=]?\s*("(?:[^"]+)"|\'(?:[^\']+)\'|([a-zA-Z]:\\(?:[^\s,]+)|/(?:[^\s,]+)))',
        'output_name': r'(?:nombre|name|como|as|como|llamado)\s*[:=]?\s*([a-zA-Z0-9_\-]+)',
        # NUEVO: Patrones arquitectónicos para dimensiones
        'dimensiones_2d': r'(\d+\.?\d*)\s*[xX\*]\s*(\d+\.?\d*)\s*(m|metros|m²)?',  # "4x5" o "4 x 5 metros"
        'dimensiones_2d_por': r'(\d+\.?\d*)\s*(?:por|by)\s*(\d+\.?\d*)\s*(m|metros|m²)?',  # "4 por 5" o "4 by 5"
        'dimensiones_3d': r'(\d+\.?\d*)\s*[xX\*]\s*(\d+\.?\d*)\s*[xX\*]\s*(\d+\.?\d*)\s*(m|metros|m³)?',  # "4x5x2.5"
        'altura_explicita': r'(altura|alto|height)\s*(?:de)?\s*(\d+\.?\d*)\s*(m|metros)?',  # "altura de 2.5m"
        'ancho_explicito': r'(ancho|anchura|width)\s*(?:de)?\s*(\d+\.?\d*)\s*(m|metros)?',  # "ancho de 4m"
        'largo_explicito': r'(largo|profundidad|length|deep)\s*(?:de)?\s*(\d+\.?\d*)\s*(m|metros)?',  # "largo de 5m"
    }
    
    def __init__(self):
        """Inicializa el extractor de entidades."""
        self.confidence_threshold = 0.5
    
    def extract(self, command: str) -> Dict[str, Entity]:
        """
        Extrae todas las entidades de un comando.
        
        Args:
            command: Orden en lenguaje natural
            
        Returns:
            Diccionario con entidades extraídas {nombre: Entity}
        """
        entities = {}
        
        # Normalizar entrada
        command_lower = command.lower().strip()
        
        # Extraer objeto
        obj = self._extract_object(command_lower)
        if obj:
            entities['objeto'] = obj
        
        # Extraer color
        color = self._extract_color(command_lower)
        if color:
            entities['color'] = color
        
        # Extraer posición
        position = self._extract_position(command_lower)
        if position:
            entities['posicion'] = position
        
        # Extraer tamaño
        size = self._extract_size(command_lower)
        if size:
            entities['tamaño'] = size
        
        # Extraer rotación
        rotation = self._extract_rotation(command_lower)
        if rotation:
            entities['rotacion'] = rotation
        
        # Extraer cantidad
        quantity = self._extract_quantity(command_lower)
        if quantity:
            entities['cantidad'] = quantity

        # Extraer filepath (case sensitive para rutas de Windows!)
        filepath = self._extract_filepath(command)
        if filepath:
            entities['filepath'] = filepath

        # Extraer output_name
        output_name = self._extract_output_name(command_lower)
        if output_name:
            entities['output_name'] = output_name
        
        # NUEVO: Extraer dimensiones arquitectónicas
        dimensions = self._extract_architectural_dimensions(command_lower)
        if dimensions:
            entities['dimensiones'] = dimensions
            
        return entities

    def _extract_architectural_dimensions(self, command: str) -> Optional[Entity]:
        """
        Extrae dimensiones arquitectónicas (ancho x profundidad x altura).
        
        Soporta formatos:
        - "4x5" → ancho=4, profundidad=5
        - "4x5x2.5" → ancho=4, profundidad=5, altura=2.5
        - "4 x 5 metros" → ancho=4, profundidad=5
        - "ancho de 4m, largo 5m, alto 2.5m" → ancho=4, profundidad=5, altura=2.5
        - "habitación 4 por 5" → ancho=4, profundidad=5
        
        Returns:
            Entity con value={'ancho': float, 'profundidad': float, 'altura': float}
        """
        dimensions = {'ancho': None, 'profundidad': None, 'altura': None}
        confidence = 0.0
        
        # 1. Intentar extraer dimensiones 3D completas (4x5x2.5)
        match_3d = re.search(self.PATTERNS['dimensiones_3d'], command)
        if match_3d:
            dimensions['ancho'] = float(match_3d.group(1))
            dimensions['profundidad'] = float(match_3d.group(2))
            dimensions['altura'] = float(match_3d.group(3))
            confidence = 0.95
            return Entity(
                name='dimensiones',
                value=dimensions,
                confidence=confidence,
                entity_type='architectural_dimensions'
            )
        
        # 2. Intentar extraer dimensiones 2D (4x5 o 4 por 5) - ancho x profundidad
        match_2d = re.search(self.PATTERNS['dimensiones_2d'], command)
        if not match_2d:
            # Intentar con "por" como separador
            match_2d = re.search(self.PATTERNS['dimensiones_2d_por'], command)
        if match_2d:
            dimensions['ancho'] = float(match_2d.group(1))
            dimensions['profundidad'] = float(match_2d.group(2))
            confidence = 0.90
        
        # 3. Extraer dimensiones explícitas (sobrescriben las implícitas)
        # Altura/alto
        match_altura = re.search(self.PATTERNS['altura_explicita'], command)
        if match_altura:
            dimensions['altura'] = float(match_altura.group(2))
            confidence = max(confidence, 0.90)
        
        # Ancho
        match_ancho = re.search(self.PATTERNS['ancho_explicito'], command)
        if match_ancho:
            dimensions['ancho'] = float(match_ancho.group(2))
            confidence = max(confidence, 0.90)
        
        # Largo/profundidad
        match_largo = re.search(self.PATTERNS['largo_explicito'], command)
        if match_largo:
            dimensions['profundidad'] = float(match_largo.group(2))
            confidence = max(confidence, 0.90)
        
        # 4. Inferir altura por contexto si no se especificó
        if dimensions['altura'] is None and (dimensions['ancho'] or dimensions['profundidad']):
            # Para habitaciones, altura estándar es 2.5m
            if any(word in command for word in ['habitación', 'cuarto', 'room', 'casa', 'edificio']):
                dimensions['altura'] = 2.5
                confidence = max(confidence * 0.8, 0.7)  # Menor confianza por inferencia
        
        # Si tenemos al menos ancho o profundidad, retornar entidad
        if dimensions['ancho'] is not None or dimensions['profundidad'] is not None:
            return Entity(
                name='dimensiones',
                value=dimensions,
                confidence=confidence,
                entity_type='architectural_dimensions'
            )
        
        return None

    def _extract_filepath(self, command: str) -> Optional[Entity]:
        """Extrae rutas de archivos."""
        match = re.search(self.PATTERNS['filepath'], command, re.IGNORECASE)
        if match:
            path = match.group(2) if len(match.groups()) > 1 else match.group(1)
            # Limpiar posibles comillas o espacios residuales
            path = path.strip().strip('"').strip("'")
            return Entity(
                name='filepath',
                value=path,
                confidence=0.95,
                entity_type='path'
            )
        return None
    
    def _extract_output_name(self, command: str) -> Optional[Entity]:
        """Extrae el nombre de salida para patrones."""
        match = re.search(self.PATTERNS['output_name'], command)
        if match:
            return Entity(
                name='output_name',
                value=match.group(1),
                confidence=0.95,
                entity_type='string'
            )
        return None

    def _extract_object(self, command: str) -> Optional[Entity]:
        """Extrae el tipo de objeto de la orden."""
        for obj_name, obj_data in self.OBJECTS.items():
            for alt in obj_data['alternatives']:
                if alt in command:
                    return Entity(
                        name='objeto',
                        value=obj_data['blender_type'],
                        confidence=0.95,
                        entity_type='object'
                    )
        return None
    
    def _extract_color(self, command: str) -> Optional[Entity]:
        """Extrae el color de la orden."""
        for color_name, color_rgb in self.COLORS.items():
            if color_name in command:
                return Entity(
                    name='color',
                    value=color_rgb,
                    confidence=0.90,
                    entity_type='color'
                )
        return None
    
    def _extract_position(self, command: str) -> Optional[Entity]:
        """Extrae la posición (x, y, z) de la orden."""
        match = re.search(self.PATTERNS['posicion'], command)
        if match:
            x, y, z = float(match.group(1)), float(match.group(2)), float(match.group(3))
            return Entity(
                name='posicion',
                value=(x, y, z),
                confidence=0.95,
                entity_type='position'
            )
        return None
    
    def _extract_size(self, command: str) -> Optional[Entity]:
        """Extrae el tamaño de la orden."""
        match = re.search(self.PATTERNS['tamaño'], command)
        if match:
            size = float(match.group(2))
            unit = match.group(3) or 'm'
            return Entity(
                name='tamaño',
                value=size,
                confidence=0.90,
                entity_type='number'
            )
        return None
    
    def _extract_rotation(self, command: str) -> Optional[Entity]:
        """Extrae la rotación (x, y, z) de la orden."""
        match = re.search(self.PATTERNS['rotacion'], command)
        if match:
            rx, ry, rz = float(match.group(2)), float(match.group(3)), float(match.group(4))
            return Entity(
                name='rotacion',
                value=(rx, ry, rz),
                confidence=0.85,
                entity_type='position'
            )
        return None
    
    def _extract_quantity(self, command: str) -> Optional[Entity]:
        """Extrae la cantidad de objetos a crear."""
        match = re.search(self.PATTERNS['cantidad'], command)
        if match:
            qty = int(match.group(2))
            return Entity(
                name='cantidad',
                value=qty,
                confidence=0.85,
                entity_type='number'
            )
        return None
    
    def validate_entities(self, entities: Dict[str, Entity]) -> Tuple[bool, List[str]]:
        """
        Valida que las entidades extraídas sean coherentes.
        
        Args:
            entities: Diccionario de entidades
            
        Returns:
            (válido, lista_de_errores)
        """
        errors = []
        
        # Si hay tamaño pero es negativo o muy grande
        if 'tamaño' in entities:
            size = entities['tamaño'].value
            if size <= 0 or size > 1000:
                errors.append(f"Tamaño inválido: {size}")
        
        # Si hay posición fuera de rango
        if 'posicion' in entities:
            x, y, z = entities['posicion'].value
            if any(abs(v) > 500 for v in [x, y, z]):
                errors.append(f"Posición fuera de rango: ({x}, {y}, {z})")
        
        # Validar confianza mínima
        low_confidence = [name for name, entity in entities.items() 
                         if entity.confidence < self.confidence_threshold]
        if low_confidence:
            errors.append(f"Baja confianza en: {low_confidence}")
        
        return len(errors) == 0, errors
