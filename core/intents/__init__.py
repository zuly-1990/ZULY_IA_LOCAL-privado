"""
core/intents/
==============

Módulo de gestión de intenciones para el agente ZULY/LYZU.

Este paquete contiene toda la lógica para:
1. Procesar lenguaje natural (NLU)
2. Extraer entidades de las órdenes
3. Mapear intenciones a comandos
4. Enrutar hacia la ejecución

Componentes:
- entity_extractor: Extrae parámetros y valores de órdenes
- intent_manager: Gestor central de intenciones
- intent_router: Conecta intenciones con comandos ejecutables
"""

from .entity_extractor import EntityExtractor
from .intent_manager import IntentManager
from .intent_router import IntentRouter

__all__ = ['EntityExtractor', 'IntentManager', 'IntentRouter']
