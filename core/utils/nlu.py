# core/utils/nlu.py
"""
Procesador de Lenguaje Natural (NLU) para el agente Zuly.
Interpreta peticiones en lenguaje natural y las convierte en intenciones de comandos.
"""

import re
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher
from functools import lru_cache
from core.utils.logging import log_info, log_warning, log_error, log_debug
from core.utils.exceptions import NLUError, ValidationError
from core.intents.entity_extractor import EntityExtractor

class CommandIntent:
    """Representa una intención de comando extraída del lenguaje natural."""
    
    def __init__(self, command_name: str, confidence: float = 1.0, parameters: Dict = None):
        """
        Inicializa una intención de comando.
        
        :param command_name: Nombre del comando a ejecutar
        :param confidence: Nivel de confianza (0.0 a 1.0)
        :param parameters: Parámetros extraídos para el comando
        """
        self.command_name = command_name
        self.confidence = confidence
        self.parameters = parameters or {}
    
    def __repr__(self):
        return f"CommandIntent({self.command_name}, conf={self.confidence:.2f}, params={self.parameters})"
    
    def __str__(self):
        return f"{self.command_name} ({self.confidence:.0%})"


class NaturalLanguageProcessor:
    """Procesador de lenguaje natural para interpretar peticiones del usuario."""
    
    def __init__(self, available_commands: Dict):
        """
        Inicializa el procesador NLU.
        
        :param available_commands: Diccionario de comandos disponibles
        """
        self.commands = available_commands
        self.command_names = list(available_commands.keys())
        
        # Palabras clave para detectar intenciones
        self.keywords = {
            'crear': ['crear', 'crea', 'añade', 'añadir', 'agrega', 'agregar', 'haz', 'hacer', 'genera', 'generar'],
            'cubo': ['cubo', 'cubos', 'box', 'cube'],
            'esfera': ['esfera', 'esferas', 'sphere', 'bola', 'bolas'],
            'cilindro': ['cilindro', 'cilindros', 'cylinder'],
            'cono': ['cono', 'conos', 'cone'],
            'plano': ['plano', 'planos', 'plane', 'suelo', 'piso'],
            'luz': ['luz', 'luces', 'light', 'iluminacion', 'iluminación', 'lampara', 'lámpara'],
            'material': ['material', 'materiales', 'textura', 'aspecto', 'apariencia'],
            'oro': ['oro', 'dorado', 'dorada', 'gold', 'golden'],
            'plata': ['plata', 'plateado', 'plateada', 'silver'],
            'vidrio': ['vidrio', 'cristal', 'glass', 'transparente'],
            'mover': ['mover', 'mueve', 'move', 'posicion', 'posición', 'ubicar'],
            'rotar': ['rotar', 'rota', 'rotate', 'girar', 'gira', 'rotacion', 'rotación'],
            'escalar': ['escalar', 'escala', 'scale', 'tamaño', 'tamano', 'redimensionar'],
            'guardar': ['guardar', 'guarda', 'save', 'salvar', 'grabar', 'exportar_blend'],
            'parent': ['parent', 'hijo', 'padre', 'jerarquia', 'jerarquía', 'emparentar', 'dentro de'],
            'camara': ['camara', 'camera', 'vista'],
            'rename': ['renombra', 'rename', 'llámalo', 'llamalo', 'nombre'],
            'invisible': ['invisible', 'ocultar', 'ver', 'mostrar'],
            'limpiar': ['limpiar', 'vaciar', 'borrar todo', 'resetear escena'],
            'modificador': ['modificador', 'modifier', 'aplica', 'subdivision', 'array', 'bevel'],
            # Arquitectura
            'habitacion': ['habitación', 'cuarto', 'room', 'recámara', 'dormitorio'],
            'muro': ['muro', 'pared', 'wall'],
            'columna': ['columna', 'pilar', 'pilastra', 'column'],
            'piso': ['piso', 'suelo', 'floor'],
            'techo': ['techo', 'cielo', 'roof', 'ceiling'],
            'ventana': ['ventana', 'ventanas', 'window', 'cristalera', 'lucernario'],
            'puerta': ['puerta', 'puertas', 'door', 'entrada'],
        }
        
        # Mapeo de palabras clave a comandos
        self.keyword_to_command = {
            # Crear primitivas
            'crear_cubo': 'blender.create_cube',
            'crear_esfera': 'blender.create_sphere',
            'crear_cilindro': 'blender.create_cylinder',
            'crear_cono': 'blender.create_cone',
            'crear_plano': 'blender.create_plane',
            'crear_ventana': 'blender.create_window',
            # Mover
            'mover_cubo': 'blender.move_object',
            'mover_esfera': 'blender.move_object',
            'mover_cilindro': 'blender.move_object',
            # Material
            'material_cubo': 'blender.apply_material',
            'material_esfera': 'blender.apply_material',
            'material_cilindro': 'blender.apply_material',
            # Otros
            'luz': 'blender.create_light',
            'material': 'blender.apply_material',
            'guardar': 'blender.save_project',
            'parent': 'blender.set_parent',
            'render': 'blender.render_scene',
            'camara': 'blender.create_camera',
            'rename': 'blender.rename_object',
            'invisible': 'blender.set_object_visibility',
            'limpiar': 'blender.clear_scene',
            'subdivision': 'blender.add_subdivision_surface',
            'array': 'blender.add_array',
            'bevel': 'blender.add_bevel',
            'parent': 'blender.move_object', # Usado para emparentar en este sistema
            # Arquitectura
            'habitacion': 'blender.create_room',
            'muro': 'blender.create_pro_wall',
            'columna': 'blender.create_column',
            'piso': 'blender.create_floor',
            'techo': 'blender.create_ceiling',
            'ventana': 'blender.create_intelligent_window',
            'puerta': 'blender.create_intelligent_door',
        }
        
        # Entity extractor para parámetros avanzados
        self.entity_extractor = EntityExtractor()
        
        log_info(f"NLU inicializado con {len(self.commands)} comandos")
    
    def process(self, user_request: str) -> List[CommandIntent]:
        """
        Procesa una petición en lenguaje natural y extrae intenciones.
        
        :param user_request: Petición del usuario en texto libre
        :return: Lista de intenciones ordenadas por confianza
        :raises NLUError: Si hay un error crítico en el procesamiento
        """
        # Validación mejorada de entrada
        if user_request is None:
            log_warning("Petición None recibida en NLU")
            raise NLUError(
                "La petición no puede ser None",
                details={"user_request": None}
            )
        
        if not isinstance(user_request, str):
            log_error(f"Tipo de petición inválido: {type(user_request)}")
            raise NLUError(
                "La petición debe ser un string",
                details={"type": type(user_request).__name__}
            )
        
        if not user_request.strip():
            log_warning("Petición vacía recibida en NLU")
            return []
        
        # Preservar el original para extracción de parámetros (case sensitive)
        original_request = user_request.strip()
        user_request = original_request.lower()
        intents = []
        
        # 1. Intentar coincidencia directa con nombres de comandos
        for cmd_name in self.command_names:
            if cmd_name in user_request:
                params = self._extract_parameters(original_request)
                intents.append(CommandIntent(cmd_name, confidence=0.95, parameters=params))
                return intents  # Retornar inmediatamente si hay coincidencia directa
        
        # 2. Buscar palabras clave
        detected_keywords = self._detect_keywords(user_request)
        # 3. Mapear combinaciones de palabras clave a comandos
        # Ejemplo: "crear cubo" => crearprimitivacubo
        for obj in ['cubo', 'esfera', 'cilindro', 'cono', 'plano']:
            if 'crear' in detected_keywords and obj in detected_keywords:
                key = f'crear_{obj}'
                if key in self.keyword_to_command:
                    params = self._extract_parameters(original_request)
                    intents.append(CommandIntent(self.keyword_to_command[key], confidence=0.85, parameters=params))
            if 'material' in detected_keywords and obj in detected_keywords:
                key = f'material_{obj}'
                if key in self.keyword_to_command:
                    params = self._extract_parameters(original_request)
                    intents.append(CommandIntent(self.keyword_to_command[key], confidence=0.8, parameters=params))
        
        # 3.1 NUEVO: Comandos arquitectónicos
        # "crear habitación", "nueva habitación", "crea muro", etc.
        for arch_obj in ['habitacion', 'muro', 'columna', 'piso', 'techo', 'ventana', 'puerta']:
            if ('crear' in detected_keywords or 'nuevo' in user_request or 'nueva' in user_request or 'añadir' in user_request) \
               and arch_obj in detected_keywords:
                key = arch_obj
                if key in self.keyword_to_command:
                    params = self._extract_parameters(original_request)
                    intents.append(CommandIntent(self.keyword_to_command[key], confidence=0.92, parameters=params))
                    log_debug(f"NLU: Comando arquitectónico AADD detectado: {key} -> {self.keyword_to_command[key]}")
        
        # 3.1 Soporte genérico para transformat (Mueve/Escala/Rota CUALQUER COSA)
        if 'mover' in detected_keywords:
            params = self._extract_parameters(original_request)
            intents.append(CommandIntent('blender.move_object', confidence=0.75, parameters=params))
        if 'escalar' in detected_keywords:
            params = self._extract_parameters(original_request)
            intents.append(CommandIntent('blender.scale_object', confidence=0.75, parameters=params))
        if 'rotar' in detected_keywords:
            params = self._extract_parameters(original_request)
            intents.append(CommandIntent('blender.rotate_object', confidence=0.75, parameters=params))
        if 'invisible' in user_request or 'ocultar' in user_request:
            params = self._extract_parameters(original_request)
            intents.append(CommandIntent('blender.set_object_visibility', confidence=0.8, parameters=params))
        
        if any(kw in user_request for kw in ['informacion', 'sistema', 'info', 'status']):
            params = self._extract_parameters(original_request)
            intents.append(CommandIntent('system.get_info', confidence=0.85, parameters=params))

        if 'renombra' in user_request or 'rename' in user_request:
            params = self._extract_parameters(original_request)
            intents.append(CommandIntent('blender.rename_object', confidence=0.9, parameters=params))

        # 3.2 Otros comandos simples (Luz, Cámara, Render, Guardar, etc.)
        for keyword, cmd_name in self.keyword_to_command.items():
            if keyword in detected_keywords and '_' not in keyword:
                params = self._extract_parameters(original_request)
                intents.append(CommandIntent(cmd_name, confidence=0.7, parameters=params))

        if 'render' in user_request:
             intents.append(CommandIntent('blender.render_scene', confidence=0.8, parameters=self._extract_parameters(original_request)))


        # 4. Si no se encontró nada, buscar comando similar
        if not intents:
            similar = self.find_similar_command(user_request)
            if similar:
                cmd_name, ratio = similar
                if ratio > 0.6:
                    params = self._extract_parameters(original_request)
                    intents.append(CommandIntent(cmd_name, confidence=ratio, parameters=params))
        
        # Ordenar por confianza
        intents.sort(key=lambda x: x.confidence, reverse=True)
        
        return intents
    
    def _detect_keywords(self, text: str) -> List[str]:
        """Detecta palabras clave en el texto."""
        detected = []
        for category, words in self.keywords.items():
            for word in words:
                if word in text:
                    detected.append(category)
                    break
        return detected
    
    def _extract_parameters(self, text: str) -> Dict:
        """Extrae parámetros numéricos y de texto del texto, con soporte contextual."""
        params = {}
        
        # NUEVO: Extraer entidades avanzadas (dimensiones arquitectónicas, etc.)
        entities = self.entity_extractor.extract(text)
        if entities:
            # Guardar entidades para que los handlers las usen
            params['_nlu_entities'] = {name: {'value': ent.value, 'confidence': ent.confidence, 'type': ent.entity_type} 
                                       for name, ent in entities.items()}
            
            # Si hay dimensiones arquitectónicas, agregarlas como parámetros directos
            if 'dimensiones' in entities:
                dims = entities['dimensiones'].value
                if dims.get('ancho') is not None:
                    params['ancho'] = dims['ancho']
                if dims.get('profundidad') is not None:
                    params['profundidad'] = dims['profundidad']
                if dims.get('altura') is not None:
                    params['altura'] = dims['altura']
                log_debug(f"NLU: Dimensiones arquitectónicas detectadas: {dims}")
        
        # 1. Extraer nombres (entre comillas) PRIMERO para evitar que sus números
        # contaminen la extracción de coordenadas (ej: 'Orbital_0')
        names = re.findall(r'["\'](.*?)["\']', text)
        
        # Crear una versión del texto sin nombres para extraer números de forma segura
        text_no_names = re.sub(r'["\'].*?["\']', '', text)
        text_lower = text_no_names.lower()
        
        # 2. EXTRACCIÓN CONTEXTUAL: Buscar patrones específicos primero
        # A. Búsqueda de TAMAÑO/ESCALA explícito
        scale_match = re.search(r'(?:tamaño|escala|scale)\s+([+-]?\d+\.?\d*)', text_lower, re.IGNORECASE)
        if scale_match:
            params['scale'] = float(scale_match.group(1))
        
        # B. Búsqueda de POSICIÓN/UBICACIÓN explícita
        pos_match = re.search(r'(?:posición|ubicación|en:?|location:?)\s*[\(\s]?([+-]?\d+\.?\d*)\s*[,\s]+([+-]?\d+\.?\d*)\s*[,\s]+([+-]?\d+\.?\d*)[\)\s]?', text_lower, re.IGNORECASE)
        if pos_match:
            params['location'] = [float(pos_match.group(1)), float(pos_match.group(2)), float(pos_match.group(3))]
        
        # C. Búsqueda de ROTACIÓN explícita
        rot_match = re.search(r'(?:rotar|rotation|gira|giro)\s*[\(\s]?([+-]?\d+\.?\d*)\s*[,\s]+([+-]?\d+\.?\d*)\s*[,\s]+([+-]?\d+\.?\d*)[\)\s]?', text_lower, re.IGNORECASE)
        if rot_match:
            params['rotation'] = [float(rot_match.group(1)), float(rot_match.group(2)), float(rot_match.group(3))]
        
        # 3. Si no se encontró nada explícitamente, usar lógica de números generales
        if not params or (not all(k in params for k in ['location', 'scale', 'rotation'])):
            numbers = re.findall(r'-?\d+\.?\d*', text_no_names)
            
            if len(numbers) >= 6:
                # Caso avanzado: Ubicación y Escala ambos como tripletas
                if 'location' not in params:
                    params['location'] = [float(numbers[0]), float(numbers[1]), float(numbers[2])]
                if 'scale' not in params:
                    params['scale'] = [float(numbers[3]), float(numbers[4]), float(numbers[5])]
            elif len(numbers) >= 3:
                coords = [float(numbers[-3]), float(numbers[-2]), float(numbers[-1])]
                # Si solo hay una tripleta, determinar su función por keywords
                is_loc = any(k in text_lower for k in ['mover', 'posicion', 'ubicación', 'en', 'location'])
                is_rot = any(k in text_lower for k in ['rotar', 'gira', 'rota', 'grados', 'rotation'])
                is_scale = any(k in text_lower for k in ['escala', 'tamaño', 'dimension', 'scale'])
                
                if 'location' not in params and is_loc: 
                    params['location'] = coords
                if 'rotation' not in params and is_rot: 
                    params['rotation'] = coords
                if 'scale' not in params and is_scale: 
                    params['scale'] = coords
                
                # Fallback a location si no hay nada claro
                if 'location' not in params and not (is_loc or is_rot or is_scale):
                    params['location'] = coords
            elif len(numbers) == 1:
                # Posible escala uniforme, radio o parámetros de modificadores
                val = float(numbers[0])
                if 'scale' not in params and any(k in text_lower for k in ['radio', 'escala', 'tamaño', 'scale']):
                    params['scale'] = val
                    if 'radio' in text_lower or 'radius' in text_lower:
                        params['radius'] = val
                if 'levels' not in params and any(k in text_lower for k in ['nivel', 'subdivision', 'segmento']):
                    params['levels'] = int(val)
                    params['segments'] = int(val)
                if 'count' not in params and any(k in text_lower for k in ['cantidad', 'count', 'copia']):
                    params['count'] = int(val)
                if 'width' not in params and any(k in text_lower for k in ['ancho', 'width', 'grosor']):
                    params['width'] = val

        # 3. Lógica inteligente para nombres basados en contexto usando lower para búsqueda
        parent_match = re.search(r'(?:emparenta|dentro de|padre|hijo de|al)\s+["\'](.*?)["\']', text, re.IGNORECASE)
        
        # B. Renombrado (Rename 'A' to 'B')
        rename_match = re.search(r'(?:renombra|rename|camia el nombre de)\s+["\'](.*?)["\']\s+(?:a|to|por)\s+["\'](.*?)["\']', text)
        
        if rename_match:
            params['name'] = rename_match.group(1)
            params['object_name'] = rename_match.group(1)
            params['new_name'] = rename_match.group(2)
        elif parent_match and any(kw in text_lower for kw in ['emparenta', 'padre', 'hijo', 'jerarquia', 'jerarquía']):
            params['parent'] = parent_match.group(1)
            # Si hay otros nombres, el que NO es el padre es el name del objeto (hijo)
            other_names = [n for n in names if n != params['parent']]
            if other_names:
                params['name'] = other_names[0]
                params['object_name'] = other_names[0]
        # 4. Extraer materiales (Lógica inteligente: si un nombre citado es material, el otro es el objeto)
        materials_list = ['oro', 'plata', 'vidrio', 'cobre', 'madera', 'metal', 'concreto', 'hojas', 'tronco']
        colors_list = ['negro', 'rojo', 'azul', 'verde', 'amarillo', 'blanco', 'gris', 'naranja', 'violeta', 'rosa', 'marron', 'marrón']
        
        detected_material = None
        detected_color = None
        
        # Buscar colores primero
        for color in colors_list:
            if color in text_lower:
                detected_color = color
                params['color'] = color
                break
        
        # Luego buscar materiales
        if not detected_color:
            for material in materials_list:
                if material in text_lower:
                    detected_material = material
                    params['material'] = material
                    params['material_name'] = material
                    params['color'] = material
                    break
        
        # Si detectamos un material y este estaba en las comillas, el OTRO nombre citado es el objeto
        if detected_material and names:
            actual_objects = [n for n in names if n.lower() != detected_material]
            if actual_objects:
                params['name'] = actual_objects[0]
                params['object_name'] = actual_objects[0]
            elif len(names) > 0:
                # Failsafe: Si solo hay un nombre y coincide con material, el objeto es el ACTIVO o el NLU falló
                pass
        elif names and 'name' not in params:
            params['name'] = names[0]
            params['object_name'] = names[0]

        # 5. Extraer FILEPATH (Crítico para Semana 6)
        # Soporta rutas con espacios y comillas
        path_match = re.search(r'(?:filepath|archivo|ruta|en|in)\s*[:=]?\s*("(?:[^"]+)"|\'(?:[^\']+)\'|([a-zA-Z]:\\(?:[^\s,]+)|/(?:[^\s,]+)))', text, re.IGNORECASE)
        if path_match:
            # Capturar el grupo adecuado (con o sin comillas)
            path = path_match.group(2) if path_match.group(2) else path_match.group(1)
            params['filepath'] = path.strip().strip('"').strip("'")
            params['path'] = params['filepath']
            log_debug(f"NLU: Filepath detectado -> {params['filepath']}")
                
        # 6. Traducción de nombres comunes (Español -> Inglés Blender)
        # Esto asegura que "cilindro" se busque como "Cylinder" en el adapter
        name_translations = {
            'cubo': 'Cube',
            'esfera': 'Sphere',
            'cilindro': 'Cylinder',
            'cono': 'Cone',
            'plano': 'Plane',
            'camara': 'Camera',
            'camera': 'Camera',
            'luz': 'Light',
            'sol': 'Sun',
            'padre': 'Padre', # Mantener nombres propios si no son primitivas
            'mona': 'Suzanne'
        }
        
        for es, en in name_translations.items():
            # Traducir nombre del objeto actual
            if params.get('name') and params.get('name').lower() == es:
                params['name'] = en
            if params.get('object_name') and params.get('object_name').lower() == es:
                params['object_name'] = en
            
            # Traducir nombre del padre
            if params.get('parent') and params.get('parent').lower() == es:
                params['parent'] = en
            
            # Traducir materiales comunes
            if params.get('material_name') and params.get('material_name').lower() == es:
                 # Note: Oro/Plata etc se manejan en el handler de materiales
                 pass

        return params
    
    @lru_cache(maxsize=256)
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud entre dos textos (con caché).
        
        :param text1: Primer texto
        :param text2: Segundo texto
        :return: Ratio de similitud [0.0 - 1.0]
        """
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def find_similar_command(self, text: str) -> Optional[Tuple[str, float]]:
        """
        Encuentra el comando más similar al texto dado.
        
        :param text: Texto a comparar
        :return: Tupla (nombre_comando, ratio_similitud) o None
        """
        best_match = None
        best_ratio = 0.0
        
        text_lower = text.lower()
        
        for cmd_name in self.command_names:
            # Usar función cacheada para mejor rendimiento
            ratio = self._calculate_similarity(text_lower, cmd_name.lower())
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = cmd_name
        
        if best_match and best_ratio > 0.4:
            log_debug(f"Comando similar encontrado: {best_match} (similitud: {best_ratio:.2f})")
            return (best_match, best_ratio)
        
        log_debug(f"No se encontró comando similar para: {text}")
        return None
    
    def get_command_suggestions(self, partial_text: str, max_suggestions: int = 5) -> List[str]:
        """
        Obtiene sugerencias de comandos basadas en texto parcial.
        
        :param partial_text: Texto parcial del usuario
        :param max_suggestions: Número máximo de sugerencias
        :return: Lista de nombres de comandos sugeridos
        """
        suggestions = []
        partial_lower = partial_text.lower()
        
        for cmd_name in self.command_names:
            if partial_lower in cmd_name.lower():
                suggestions.append(cmd_name)
        
        return suggestions[:max_suggestions]
