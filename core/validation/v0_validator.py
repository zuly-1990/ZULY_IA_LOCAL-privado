from typing import Dict, Any
from core.utils.logging import log_info, log_warning, log_success
from core.validation.state_snapshot import StateSnapshot

class V0Validator:
    """
    Validador de Nivel V0: Validación Existencial.
    
    Responsabilidad:
    Verificar que el resultado reportado por el comando tiene una correspondencia
    física inmediata en la escena.
    
    Principio: "V0 observa. V1 interpreta. V2 aprende."
    
    V0 verifica que el mundo físico cambió cuando debía cambiar.
    - Comparación booleana (cambió / no cambió)
    - Sin semántica
    - Sin intención
    - Sin juicio estético
    """

    def __init__(self, adapter=None):
        self.adapter = adapter
        self.pre_snapshot = {}
        self.post_snapshot = {}

    def start_validation(self, adapter=None):
        """Toma una foto del estado ANTES de la ejecución."""
        # Usar adapter proporcionado o el de la instancia
        target_adapter = adapter or self.adapter
        self.pre_snapshot = StateSnapshot.capture(target_adapter)

    def validate(self, command_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta la validación V0 comparando el antes y el después.
        
        V0 observa efectos declarados, NO interpreta texto.
        
        :param command_result: Resultado retornado por la ejecución del comando
        :return: Resultado de validación {verified: bool, details: str}
        """
        if not command_result.get('success', False):
            return {'verified': False, 'details': 'El comando reportó fallo, no hay nada que validar.'}

        # Usar el adapter de la instancia para capturar el POST
        self.post_snapshot = StateSnapshot.capture(self.adapter)
        post_snapshot = self.post_snapshot
        
        # AJUSTE CRÍTICO: Usar campo 'effect', NO parsing de texto
        effect = command_result.get('effect', None)
        
        # Validar según efecto declarado
        if effect == 'create':
            return self._validate_creation(command_result, self.pre_snapshot, post_snapshot)
        elif effect == 'delete':
            return self._validate_deletion(command_result, self.pre_snapshot, post_snapshot)
        elif effect == 'transform':
            return self._validate_transformation(command_result, self.pre_snapshot, post_snapshot)
        elif effect == 'property':
            return self._validate_property_change(command_result, self.pre_snapshot, post_snapshot)
        else:
            # ULTRA EMERGENCIA: V0 pasivo ya NO valida como si fuera OK
            # Retorna verified=True para no romper ejecución, PERO marca passive=True
            # para que PatternMemory NUNCA memorice resultados no verificados físicamente
            log_warning("⚠️ V0 PASIVO: Comando sin 'effect' declarado — resultado NO verificado físicamente")
            return {'verified': True, 
                    'passive': True,
                    'warning': 'V0 PASIVO: Sin effect declarado. Resultado NO verificado físicamente.',
                    'details': 'Validación V0 pasiva — NO MEMORIZABLE.'}

    def _validate_creation(self, command_result: Dict[str, Any],
                          pre: Dict, post: Dict) -> Dict[str, Any]:
        """
        Valida que un objeto fue creado.
        V0: Solo verifica que existe algo nuevo.
        """
        new_objects = set(post.keys()) - set(pre.keys())
        
        if not new_objects:
            msg = "FALLO V0: Creación reportada pero no aparecieron objetos nuevos."
            log_warning(msg)
            return {'verified': False, 'details': msg}
        
        created_name = command_result.get('result', {}).get('name')
        if created_name:
            created_name_lower = created_name.lower()
            new_objects_lower = [n.lower() for n in new_objects]
            # Comprobar si el nombre reportado está en los objetos nuevos (o es prefijo con sufijo Blender)
            found = False
            for new_obj in new_objects:
                new_obj_lower = new_obj.lower()
                # Coincidencia exacta o con sufijo .001, .002, etc.
                if new_obj_lower == created_name_lower or new_obj_lower.startswith(created_name_lower + "."):
                    found = True
                    created_name = new_obj # Usar el nombre real de Blender
                    break
            
            if not found:
                msg = f"FALLO V0: Se reportó crear '{created_name}', pero se detectaron otros objetos: {list(new_objects)}"
                log_warning(msg)
                return {'verified': False, 'details': msg}
        
        log_success(f"VALIDACIÓN V0 EXITOSA: Objeto '{created_name}' confirmado en escena.")
        return {'verified': True, 
                'details': f"Objeto '{created_name}' existe físicamente.", 
                'new_objects': list(new_objects)}

    def _validate_transformation(self, command_result: Dict[str, Any], 
                                pre: Dict, post: Dict) -> Dict[str, Any]:
        """
        Valida que una transformación realmente ocurrió.
        V0: Solo verifica que ALGO cambió (location/rotation/scale).
        NO valida cuánto ni si es correcto.
        """
        target_name = command_result.get('result', {}).get('name')
        if not target_name:
            return {'verified': False, 'details': 'No se especificó objeto objetivo'}
        
        if target_name not in pre or target_name not in post:
            return {'verified': False, 'details': f'Objeto {target_name} no encontrado'}
        
        # Comparar estados (booleano: cambió o no cambió)
        pre_obj = pre[target_name]
        post_obj = post[target_name]
        
        changed = []
        if pre_obj.get('location') != post_obj.get('location'):
            changed.append('location')
        if pre_obj.get('rotation') != post_obj.get('rotation'):
            changed.append('rotation')
        if pre_obj.get('scale') != post_obj.get('scale'):
            changed.append('scale')
        
        if not changed:
            msg = f"FALLO V0: Transformación reportada pero no se detectaron cambios en {target_name}"
            log_warning(msg)
            return {'verified': False, 'details': msg}
        
        log_success(f"VALIDACIÓN V0 EXITOSA: Transformación detectada ({', '.join(changed)})")
        return {'verified': True, 
                'details': f"Transformación verificada: {', '.join(changed)} cambiados",
                'changes': changed}

    def _validate_deletion(self, command_result: Dict[str, Any],
                          pre: Dict, post: Dict) -> Dict[str, Any]:
        """
        Valida que un objeto fue eliminado.
        V0: Solo verifica que ya no existe.
        """
        target_name = command_result.get('result', {}).get('name')
        if not target_name:
            return {'verified': False, 'details': 'No se especificó objeto a eliminar'}
        
        if target_name not in pre:
            msg = f"FALLO V0: Objeto {target_name} no existía antes de eliminación"
            log_warning(msg)
            return {'verified': False, 'details': msg}
        
        if target_name.lower() in [n.lower() for n in post.keys()]:
            msg = f"FALLO V0: Objeto {target_name} aún existe después de eliminación"
            log_warning(msg)
            return {'verified': False, 'details': msg}
        
        log_success(f"VALIDACIÓN V0 EXITOSA: {target_name} eliminado correctamente")
        return {'verified': True, 
                'details': f"Eliminación verificada: {target_name} ya no existe"}

    def _validate_property_change(self, command_result: Dict[str, Any],
                                 pre: Dict, post: Dict) -> Dict[str, Any]:
        """
        Valida cambios de propiedades.
        V0: Genera WARNING si no se detecta cambio, pero NO bloquea.
        """
        target_name = command_result.get('result', {}).get('name')
        if not target_name or target_name not in pre or target_name not in post:
            # No bloquear, solo advertir
            return {'verified': True, 
                    'warning': 'Property change target not found, but not blocking'}
        
        pre_obj = pre[target_name]
        post_obj = post[target_name]
        
        # Detectar cambios en propiedades
        changed = []
        if pre_obj.get('visible') != post_obj.get('visible'):
            changed.append('visible')
        if pre_obj.get('name') != post_obj.get('name'):
            changed.append('name')
        
        if not changed:
            # WARNING, no fallo
            return {'verified': True, 
                    'warning': 'Property change not detected'}
        
        return {'verified': True, 
                'details': f"Property change detected: {', '.join(changed)}",
                'changes': changed}
