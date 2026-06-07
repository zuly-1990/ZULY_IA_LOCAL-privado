"""
core/utils/units.py

Utilidades para el manejo de unidades reales (mm, cm, m).
Centraliza la conversión a metros (unidad base de Blender).
"""

import re
from typing import Dict, Any, Tuple, Optional

# Conversión a metros
UNIT_FACTORS = {
    'mm': 0.001,
    'millimeter': 0.001,
    'milimetro': 0.001,
    'cm': 0.01,
    'centimeter': 0.01,
    'centimetro': 0.01,
    'm': 1.0,
    'meter': 1.0,
    'metro': 1.0
}

def parse_dimension(text: str) -> Tuple[Optional[float], Optional[str]]:
    """
    Busca una medida y su unidad en un texto.
    Ejemplo: "40mm" -> (40.0, "mm")
    """
    # Regex para buscar [numero][espacio]?[unidad]
    pattern = r'(\d+\.?\d*)\s*(mm|cm|m|millimeter|milimetro|centimetro|centimeter|metro|meter)\b'
    match = re.search(pattern, text.lower())
    
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        return value, unit
    
    return None, None

def to_meters(value: float, unit: str) -> float:
    """Convierte un valor de una unidad a metros."""
    unit = unit.lower()
    factor = UNIT_FACTORS.get(unit, 1.0)
    return value * factor

def format_real_unit(meters: float) -> str:
    """Formatea un valor en metros a la unidad más legible."""
    if meters < 0.01:
        return f"{meters * 1000:.1f} mm"
    if meters < 1.0:
        return f"{meters * 100:.1f} cm"
    return f"{meters:.1f} m"

class DimensionIntent:
    """Encapsula la intención dimensional de un objeto."""
    
    def __init__(self, value: float, unit: str):
        self.original_value = value
        self.original_unit = unit
        self.value_m = to_meters(value, unit)
        
    def __repr__(self):
        return f"DimensionIntent({self.original_value}{self.original_unit} -> {self.value_m}m)"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'value': self.original_value,
            'unit': self.original_unit,
            'meters': self.value_m
        }

if __name__ == "__main__":
    # Test simple
    test_texts = ["cubo de 40mm", "cilindro de 5 cm", "1.5 metros de largo"]
    for t in test_texts:
        v, u = parse_dimension(t)
        if v:
            print(f"Texto: '{t}' -> {v} {u} ({to_meters(v, u)}m)")
