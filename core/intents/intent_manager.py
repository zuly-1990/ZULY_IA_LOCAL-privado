"""
core/intents/intent_manager.py
==============================

Gestor central de intenciones. Clasifica órdenes en lenguaje natural
en intenciones reconocibles (crear_objeto, mover, renderizar, etc.)
y mapea cada intención al comando Blender correspondiente.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass
class Intent:
    """Representa una intención extraída de una orden."""
    name: str
    command: str  # Comando Blender a ejecutar
    confidence: float
    raw_input: str
    parameters: Dict


class IntentManager:
    """
    Gestor de intenciones. Mapea órdenes en lenguaje natural 
    a intenciones y comandos ejecutables.
    """
    
    # Catálogo de intenciones disponibles (expandido)
    INTENT_CATALOG = {
        # Primitivas
        'crear_objeto': {
            'keywords': ['crear', 'add', 'nuevo', 'make', 'crea', 'agregar'],
            'command': 'blender.create_primitive',
            'description': 'Crear un objeto primitivo en la escena'
        },
        'crear_cubo': {
            'keywords': ['cubo', 'cube', 'box', 'caja'],
            'command': 'blender.create_cube',
            'description': 'Crear un cubo'
        },
        'crear_dado': {
            'keywords': ['dado', 'dice', 'parqués'],
            'command': 'blender.create_parques_dice',
            'description': 'Crear un dado de parqués funcional'
        },
        'crear_esfera': {
            'keywords': ['esfera', 'sphere', 'bola', 'orbe'],
            'command': 'blender.create_sphere',
            'description': 'Crear una esfera'
        },
        'crear_cilindro': {
            'keywords': ['cilindro', 'cylinder', 'tubo'],
            'command': 'blender.create_cylinder',
            'description': 'Crear un cilindro'
        },
        # Transformaciones
        'mover_objeto': {
            'keywords': ['mover', 'move', 'desplazar', 'cambiar posición', 'ir a', 'mueve', 'pon', 'ubica', 'coloca'],
            'command': 'blender.move_object',
            'description': 'Mover un objeto a una posición específica'
        },
        'rotar_objeto': {
            'keywords': ['rotar', 'rotate', 'girar', 'rotation', 'rota', 'gira'],
            'command': 'blender.rotate_object',
            'description': 'Rotar un objeto'
        },
        'escalar_objeto': {
            'keywords': ['escalar', 'scale', 'agrandar', 'reducir', 'tamano', 'escala', 'amplía'],
            'command': 'blender.scale_object',
            'description': 'Escalar un objeto'
        },
        'duplicar_objeto': {
            'keywords': ['duplicar', 'duplicate', 'copiar', 'clone', 'duplica', 'copia'],
            'command': 'blender.duplicate_object',
            'description': 'Duplicar un objeto'
        },
        # Materiales
        'aplicar_material': {
            'keywords': ['material', 'color', 'pintar', 'paint', 'colorear'],
            'command': 'blender.apply_material',
            'description': 'Aplicar un material o color a un objeto'
        },
        'aplicar_textura': {
            'keywords': ['textura', 'texture', 'mapa', 'texture map'],
            'command': 'blender.apply_texture',
            'description': 'Aplicar una textura a un objeto'
        },
        # Render
        'renderizar': {
            'keywords': ['render', 'renderizar', 'renderize', 'captura', 'imagen'],
            'command': 'blender.render_scene',
            'description': 'Renderizar la escena actual'
        },
        'render_rapido': {
            'keywords': ['render rápido', 'quick render', 'preview'],
            'command': 'blender.render_quick',
            'description': 'Renderizar rápido para preview'
        },
        # Cámara
        'mover_camara': {
            'keywords': ['cámara', 'camera', 'vista', 'view'],
            'command': 'blender.move_camera',
            'description': 'Mover la cámara'
        },
        'zoom_camara': {
            'keywords': ['zoom', 'acercar', 'alejar'],
            'command': 'blender.zoom_camera',
            'description': 'Hacer zoom en la cámara'
        },
        # Escena
        'limpiar_escena': {
            'keywords': ['limpiar', 'clear', 'borrar todo', 'reset'],
            'command': 'blender.clear_scene',
            'description': 'Limpiar toda la escena'
        },
        'cambiar_fondo': {
            'keywords': ['fondo', 'background', 'cielo', 'sky'],
            'command': 'blender.set_background',
            'description': 'Cambiar el fondo de la escena'
        },
        # Luces
        'crear_luz': {
            'keywords': ['luz', 'light', 'iluminación', 'lamp'],
            'command': 'blender.create_light',
            'description': 'Crear una fuente de luz'
        },
        'ajustar_luz': {
            'keywords': ['brillo', 'intensidad', 'light intensity'],
            'command': 'blender.adjust_light',
            'description': 'Ajustar parámetros de iluminación'
        },
        # Modifiers
        'aplicar_modifier': {
            'keywords': ['modifier', 'efecto', 'deform', 'smooth'],
            'command': 'blender.apply_modifier',
            'description': 'Aplicar un modificador a un objeto'
        },
        'subdivision_surface': {
            'keywords': ['subdivision', 'suave', 'smooth', 'subdiv'],
            'command': 'blender.subdivision_surface',
            'description': 'Aplicar Subdivision Surface'
        },
        # Sistema
        'ejecutar_script': {
            'keywords': ['script', 'ejecutar', 'run', 'lanzar'],
            'command': 'system.execute_script',
            'description': 'Ejecutar un script externo'
        },
        'info_sistema': {
            'keywords': ['info', 'estado', 'status', 'diagnostico', 'información'],
            'command': 'system.get_info',
            'description': 'Obtener información del sistema'
        },
        'abrir_blender': {
            'keywords': ['abrir blender', 'launch blender', 'start', 'iniciar'],
            'command': 'blender.launch',
            'description': 'Abrir Blender'
        },
        # Guardado
        'guardar_escena': {
            'keywords': ['guardar', 'save', 'almacenar', 'guarda', 'salva'],
            'command': 'blender.save_scene',
            'description': 'Guardar la escena'
        },
        'exportar': {
            'keywords': ['exportar', 'export', 'salida', 'output'],
            'command': 'blender.export_scene',
            'description': 'Exportar la escena en formato'
        },
        # Selección
        'seleccionar_objeto': {
            'keywords': ['seleccionar', 'select', 'elegir', 'choose'],
            'command': 'blender.select_object',
            'description': 'Seleccionar un objeto'
        },
        'seleccionar_todo': {
            'keywords': ['seleccionar todo', 'select all', 'todos'],
            'command': 'blender.select_all',
            'description': 'Seleccionar todos los objetos'
        },
        
        # ===== NUEVAS INTENCIONES - HANDLERS AVANZADOS =====
        
        # Materiales
        'crear_material': {
            'keywords': ['crear material', 'new material', 'material nuevo'],
            'command': 'blender.create_material',
            'description': 'Crear un nuevo material'
        },
        'aplicar_material_a_objeto': {
            'keywords': ['aplicar material', 'poner material', 'asignar material'],
            'command': 'blender.apply_material',
            'description': 'Aplicar un material a un objeto'
        },
        'cambiar_color_material': {
            'keywords': ['cambiar color', 'color material', 'set color'],
            'command': 'blender.set_material_color',
            'description': 'Cambiar el color de un material'
        },
        
        # Luces
        'crear_luz': {
            'keywords': ['crear luz', 'add light', 'nueva luz', 'luz'],
            'command': 'blender.create_light',
            'description': 'Crear una nueva luz'
        },
        'luz_punto': {
            'keywords': ['luz punto', 'point light', 'luz puntual'],
            'command': 'blender.create_light',
            'description': 'Crear una luz punto'
        },
        'luz_area': {
            'keywords': ['luz area', 'area light', 'luz de área'],
            'command': 'blender.create_light',
            'description': 'Crear una luz de área'
        },
        'luz_sol': {
            'keywords': ['luz sol', 'sun light', 'luz del sol'],
            'command': 'blender.create_light',
            'description': 'Crear una luz del sol'
        },
        'cambiar_intensidad_luz': {
            'keywords': ['intensidad luz', 'energía luz', 'light energy', 'brightness'],
            'command': 'blender.set_light_energy',
            'description': 'Cambiar la intensidad de una luz'
        },
        'cambiar_color_luz': {
            'keywords': ['color luz', 'light color', 'color de luz'],
            'command': 'blender.set_light_color',
            'description': 'Cambiar el color de una luz'
        },
        
        # Cámaras
        'crear_camara': {
            'keywords': ['crear cámara', 'new camera', 'cámara nueva', 'agregar cámara'],
            'command': 'blender.create_camera',
            'description': 'Crear una nueva cámara'
        },
        'activar_camara': {
            'keywords': ['activar cámara', 'set camera', 'usar cámara', 'cámara activa'],
            'command': 'blender.set_active_camera',
            'description': 'Establecer una cámara como activa'
        },
        'posicionar_camara': {
            'keywords': ['posicionar cámara', 'mover cámara', 'camera position', 'ver desde'],
            'command': 'blender.position_camera',
            'description': 'Posicionar una cámara en un punto específico'
        },
        
        # Modificadores
        'subdivision_surface': {
            'keywords': ['subdivision', 'subdiv', 'suavizar', 'smooth', 'suavizar objeto'],
            'command': 'blender.add_subdivision_surface',
            'description': 'Agregar modificador Subdivision Surface'
        },
        'array_modifier': {
            'keywords': ['array', 'arreglo', 'copias', 'repetir', 'multiplic'],
            'command': 'blender.add_array',
            'description': 'Agregar modificador Array'
        },
        'bevel_modifier': {
            'keywords': ['bevel', 'bisel', 'edges', 'bordes'],
            'command': 'blender.add_bevel',
            'description': 'Agregar modificador Bevel'
        },
        
        # Exportación
        'exportar_fbx': {
            'keywords': ['exportar fbx', 'export fbx', 'save fbx'],
            'command': 'blender.export_fbx',
            'description': 'Exportar escena a FBX'
        },
        'exportar_obj': {
            'keywords': ['exportar obj', 'export obj', 'save obj'],
            'command': 'blender.export_obj',
            'description': 'Exportar escena a OBJ'
        },
        'exportar_gltf': {
            'keywords': ['exportar gltf', 'export gltf', 'save gltf', 'glb'],
            'command': 'blender.export_gltf',
            'description': 'Exportar escena a glTF'
        },
        # ZULY LAB / Ingeniería Inversa
        'scan_and_learn': {
            'keywords': ['escanear escena', 'aprender escena', 'ingeniería inversa', 'scan and learn', 'extraer adn'],
            'command': 'blender.scan_and_learn',
            'description': 'Escanear la escena actual para extraer patrones de ADN'
        },
        
        # ===== ARQUITECTURA (Assembly Patterns) =====
        'crear_columna': {
            'keywords': ['columna', 'pillar', 'pilar', 'columnata'],
            'command': 'blender.create_column',
            'description': 'Crear una columna arquitectónica (base + fuste + capitel)'
        },
        'crear_muro': {
            'keywords': ['muro', 'pared', 'wall', 'tabique', 'divisorio'],
            'command': 'blender.create_wall',
            'description': 'Crear un muro/pared con medidas arquitectónicas'
        },
        'crear_piso': {
            'keywords': ['piso', 'suelo', 'floor', 'pavimento', 'losa'],
            'command': 'blender.create_floor',
            'description': 'Crear un piso/suelo arquitectónico'
        },
        'crear_techo': {
            'keywords': ['techo', 'cubierta', 'ceiling', 'roof', 'azotea'],
            'command': 'blender.create_ceiling',
            'description': 'Crear un techo arquitectónico'
        },
        'crear_habitacion': {
            'keywords': ['habitación', 'cuarto', 'room', 'sala', 'espacio', 'recinto', 'ambiente'],
            'command': 'blender.create_room',
            'description': 'Crear una habitación completa (4 paredes + piso + techo)'
        },
        'listar_patrones': {
            'keywords': ['patrones', 'patterns', 'plantillas', 'templates', 'ver patrones'],
            'command': 'blender.list_patterns',
            'description': 'Listar patrones arquitectónicos disponibles'
        },
    }

    
    def __init__(self):
        """Inicializa el gestor de intenciones."""
        self.confidence_threshold = 0.6
        self.last_intent: Optional[Intent] = None
    
    def classify(self, raw_input: str, entities: Dict = None) -> Intent:
        """
        Clasifica una orden en una intención.
        
        Args:
            raw_input: Orden en lenguaje natural
            entities: Diccionario de entidades extraídas (opcional)
            
        Returns:
            Intent con la clasificación y confianza
        """
        if entities is None:
            entities = {}
        
        raw_lower = raw_input.lower().strip()
        best_intent = None
        best_confidence = 0.0
        
        # Buscar la mejor coincidencia en el catálogo
        for intent_name, intent_data in self.INTENT_CATALOG.items():
            for keyword in intent_data['keywords']:
                similarity = self._calculate_similarity(raw_lower, keyword)
                
                # Bonus de especificidad: si no es una intención genérica de alto nivel, 
                # le damos un pequeño empujón para que gane a 'crear_objeto' en caso de empate.
                generic_intents = ['crear_objeto', 'info_sistema']
                if intent_name not in generic_intents and similarity > 0.8:
                    similarity += 0.05
                
                # Bonus para verbos de acción (CRÍTICO: Evita confusión con nombres de archivos)
                action_verbs = ['mover', 'mueve', 'rota', 'gira', 'escala', 'agrandar', 'guarda', 'guardar', 'save']
                if any(v in raw_lower for v in action_verbs) and intent_name in ['mover_objeto', 'rotar_objeto', 'escalar_objeto', 'guardar_escena']:
                    similarity += 0.4
                
                if similarity >= best_confidence:
                    best_confidence = min(1.0, similarity)
                    best_intent = (intent_name, intent_data)
        
        # Si no hay buena coincidencia, usar heurística
        if best_confidence < self.confidence_threshold:
            best_intent = self._fallback_intent(raw_lower)
            # Re-verificar si el fallback es más específico
            if best_intent[0] == 'crear_objeto':
                # Si el input contiene palabras de objeto específicas, forzamos esa intención
                for specific in ['cubo', 'esfera', 'cilindro', 'cono', 'plano', 'luz', 'columna', 'muro', 'pared', 'piso', 'suelo', 'techo', 'habitación', 'cuarto', 'room']:
                    if specific in raw_lower:
                        # Mapear a intent correcto
                        intent_map = {
                            'muro': 'crear_muro', 'pared': 'crear_muro',
                            'columna': 'crear_columna',
                            'piso': 'crear_piso', 'suelo': 'crear_piso',
                            'techo': 'crear_techo',
                            'habitación': 'crear_habitacion', 'cuarto': 'crear_habitacion', 'room': 'crear_habitacion',
                        }
                        specific_intent_name = intent_map.get(specific, f"crear_{specific}")
                        if specific_intent_name in self.INTENT_CATALOG:
                            best_intent = (specific_intent_name, self.INTENT_CATALOG[specific_intent_name])
                            best_confidence = 0.95
                            break
            best_confidence = max(best_confidence, (0.85 if best_intent[0] != 'info_sistema' else 0.5))
        
        # Crear objeto Intent
        intent = Intent(
            name=best_intent[0] if best_intent else 'unknown',
            command=best_intent[1]['command'] if best_intent else 'system.noop',
            confidence=best_confidence,
            raw_input=raw_input,
            parameters=entities
        )
        
        self.last_intent = intent
        return intent
    
    def _calculate_similarity(self, input_str: str, keyword: str) -> float:
        """Calcula similitud entre entrada y keyword."""
        # Normalizar para comparación
        input_words = input_str.split()
        
        # Si el keyword es una palabra exacta en el input, confianza alta
        if keyword in input_words:
            return 0.95
            
        # Si el keyword está contenido en alguna palabra o el input completo
        if keyword in input_str:
            # Penalización SOLO si la palabra exacta NO está en la lista de palabras (es decir, es parte de otra cosa como una ruta)
            if keyword not in input_words and ("/" in input_str or "\\" in input_str):
                return max(0.4, SequenceMatcher(None, input_str, keyword).ratio())
            # Si es una palabra exacta o está claramente separada, confianza alta
            return max(0.9, SequenceMatcher(None, input_str, keyword).ratio())
        
        return SequenceMatcher(None, input_str, keyword).ratio()
    
    def _fallback_intent(self, input_str: str) -> Tuple[str, Dict]:
        """Intención fallback basada en análisis básico."""
        if any(word in input_str for word in ['crear', 'crea', 'add', 'nuevo', 'agregar', 'pón', 'añade']):
            return 'crear_objeto', self.INTENT_CATALOG['crear_objeto']
        elif any(word in input_str for word in ['mover', 'mueve', 'move', 'posiciona', 'ubica']):
            return 'mover_objeto', self.INTENT_CATALOG['mover_objeto']
        elif any(word in input_str for word in ['escalar', 'escala', 'scale', 'tamaño', 'agrandar']):
            return 'escalar_objeto', self.INTENT_CATALOG['escalar_objeto']
        elif any(word in input_str for word in ['rotar', 'rota', 'girar', 'gira', 'rotate']):
            return 'rotar_objeto', self.INTENT_CATALOG['rotar_objeto']
        elif any(word in input_str for word in ['material', 'color', 'pintar', 'pinta', 'textura']):
            return 'aplicar_material', self.INTENT_CATALOG['aplicar_material']
        elif any(word in input_str for word in ['render', 'renderizar', 'renderiza', 'captura', 'imagen']):
            return 'renderizar', self.INTENT_CATALOG['renderizar']
        elif any(word in input_str for word in ['limpiar', 'clear', 'borrar', 'reset']):
            return 'limpiar_escena', self.INTENT_CATALOG['limpiar_escena']
        else:
            return 'unknown', {'command': 'system.noop', 'description': 'Intención no reconocida'}
    
    def get_intent_description(self, intent_name: str) -> Optional[str]:
        """Obtiene descripción de una intención."""
        return self.INTENT_CATALOG.get(intent_name, {}).get('description')
    
    def list_intents(self) -> Dict[str, str]:
        """Lista todas las intenciones disponibles con descripciones."""
        return {
            name: data['description'] 
            for name, data in self.INTENT_CATALOG.items()
        }
