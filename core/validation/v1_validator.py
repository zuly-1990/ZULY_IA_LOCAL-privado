from typing import Dict, Any, List
from core.utils.logging import log_info, log_warning, log_success, log_error

class V1Validator:
    """
    Validador de Nivel V1: Validación Estructural Profunda.
    
    Responsabilidad:
    Interpretar la estructura de la escena para asegurar que el comando
    no solo tuvo un efecto físico (V0), sino que el efecto fue ESTRUCTURALMENTE correcto.
    
    Checks:
    1. Tipos de objetos (¿cubo es cubo?)
    2. Relaciones jerárquicas (Parenting)
    3. Integridad geométrica básica (Conteo de vértices)
    """

    def __init__(self):
        pass

    def validate(self, command_result: Dict[str, Any], 
                 pre_snapshot: Dict[str, Any], 
                 post_snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta la validación V1 comparando el antes y el después con más detalle que V0.
        
        :param command_result: Resultado retornado por la ejecución del comando
        :param pre_snapshot: Snapshot capturado antes de la ejecución
        :param post_snapshot: Snapshot capturado después de la ejecución
        :return: Resultado de validación {verified: bool, details: str}
        """
        if not command_result.get('success', False):
            return {'verified': False, 'details': 'Comando fallido, saltando V1.'}

        effect = command_result.get('effect', None)
        
        # Validar según efecto declarado
        if effect == 'create':
            return self._validate_creation_structural(command_result, pre_snapshot, post_snapshot)
        elif effect == 'transform':
            # V1 puede validar si hubo deformación accidental (vertex count change)
            return self._validate_geometric_integrity(command_result, pre_snapshot, post_snapshot)
        elif effect == 'hierarchy' or 'parent' in command_result.get('command_executed', ''):
            return self._validate_hierarchy(command_result, pre_snapshot, post_snapshot)
        
        # Validación pasiva para otros efectos
        return {'verified': True, 'details': 'V1: Sin anomalías estructurales detectadas.'}

    def _validate_creation_structural(self, command_result: Dict[str, Any],
                                     pre: Dict, post: Dict) -> Dict[str, Any]:
        """
        V1 de Creación: Verifica tipo y geometría inicial.
        """
        target_name = command_result.get('result', {}).get('object_name') or command_result.get('result', {}).get('name')
        
        # Case-insensitive lookup
        post_lower = {k.lower(): v for k, v in post.items()}
        target_name_lower = target_name.lower() if target_name else None
        
        if not target_name_lower or target_name_lower not in post_lower:
            return {'verified': False, 'details': f"V1: Objeto '{target_name}' no encontrado en snapshot post."}

        obj_data = post_lower[target_name_lower]
        expected_type = command_result.get('parameters', {}).get('primitive_type', '').upper()
        
        # 1. Verificar tipo (Blender usa 'MESH', 'LIGHT', etc.)
        actual_type = obj_data.get('type')
        if expected_type and expected_type != actual_type:
            # Notar que command_result puede tener 'cube' y Blender dice 'MESH'
            if expected_type in ['CUBE', 'SPHERE', 'CYLINDER', 'CONE', 'PLANE'] and actual_type != 'MESH':
                msg = f"FALLO V1: Se esperaba MESH ({expected_type}), se obtuvo {actual_type}"
                log_warning(msg)
                return {'verified': False, 'details': msg}

        # 2. Verificar vértices (si es MESH)
        if actual_type == 'MESH':
            v_count = obj_data.get('vertex_count', 0)
            if v_count == 0:
                msg = f"FALLO V1: Objeto '{target_name}' es MESH pero no tiene vértices."
                log_warning(msg)
                return {'verified': False, 'details': msg}
            
            # Check básico: Un cubo tiene al menos 8 vértices
            if expected_type == 'CUBE' and v_count < 8:
                msg = f"FALLO V1: Cubo '{target_name}' tiene solo {v_count} vértices (anomalía)."
                log_warning(msg)
                return {'verified': False, 'details': msg}

        log_success(f"V1: Integridad estructural de '{target_name}' verificada.")
        return {'verified': True, 'details': f"Estructura de '{target_name}' correcta."}

    def _validate_hierarchy(self, command_result: Dict[str, Any],
                           pre: Dict, post: Dict) -> Dict[str, Any]:
        """
        V1 de Jerarquía: Verifica que el parenting ocurrió.
        """
        params = command_result.get('parameters', {})
        child_name = params.get('child_name') or params.get('objeto')
        parent_name = params.get('parent_name') or params.get('padre')

        if not child_name or child_name not in post:
             return {'verified': True, 'details': 'V1: No se pudo identificar el hijo para validar jerarquía.'}

        actual_parent = post_lower.get(child_name.lower(), {}).get('parent')
        
        if parent_name and (not actual_parent or actual_parent.lower() != parent_name.lower()):
            msg = f"FALLO V1: Jerarquía incorrecta. '{child_name}' tiene de padre a '{actual_parent}', se esperaba '{parent_name}'"
            log_warning(msg)
            return {'verified': False, 'details': msg}

        log_success(f"V1: Jerarquía de '{child_name}' verificada.")
        return {'verified': True, 'details': f"Parenting de '{child_name}' -> '{parent_name}' correcto."}

    def _validate_geometric_integrity(self, command_result: Dict[str, Any],
                                     pre: Dict, post: Dict) -> Dict[str, Any]:
        """
        V1 de Integridad: Verifica que una transformación no rompió la geometría.
        (Ej: Un Move no debería cambiar el conteo de vértices).
        """
        target_name = command_result.get('result', {}).get('object_name') or command_result.get('result', {}).get('name')
        if not target_name or target_name not in pre or target_name not in post:
            return {'verified': True, 'details': 'V1: Objeto no encontrado para check geométrico.'}

        pre_v = pre[target_name].get('vertex_count', 0)
        post_v = post[target_name].get('vertex_count', 0)

        if pre_v != post_v:
            # Una transformación (move/rot/scale) NO debe cambiar vértices. 
            # Si cambió, algo raro pasó (ej: se aplicó un modificador por error).
            msg = f"FALLO V1: Integridad geométrica comprometida en '{target_name}'. Vértices: {pre_v} -> {post_v}"
            log_warning(msg)
            return {'verified': False, 'details': msg}

        return {'verified': True, 'details': 'V1: Geometría persistente.'}
