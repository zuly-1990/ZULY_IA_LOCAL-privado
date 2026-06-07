# core/utils/parser_interface.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BaseSemanticParser(ABC):
    """
    Interfaz abstracta para futuros parsers semánticos basados en IA.
    Define el contrato que cualquier implementación debe seguir para integrarse con Zuly.
    """

    @abstractmethod
    def parse_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Toma una cadena de texto y devuelve una lista de componentes estructurales.
        
        Entrada: "Un cubo sobre una esfera"
        Salida esperada: [
            {"type": "cube", "context": "..."},
            {"type": "sphere", "context": "..."}
        ]
        """
        pass

    @abstractmethod
    def detect_relations(self, elements: List[Dict[str, Any]], text: str) -> List[Dict[str, Any]]:
        """
        Detecta relaciones entre elementos previamente identificados.
        
        Salida esperada: [
            {"type": "encima_de", "source": "element_id_1", "target": "element_id_2"}
        ]
        """
        pass
