"""
ContextGuard - Validación Activa de ZULY
Fase 12: Autoprotección pasiva.
"""

class ContextGuard:
    """
    Evalúa si una acción es segura y coherente con el contexto actual de Blender.
    """
    
    PERMITIDO = "PERMITIDO"
    BLOQUEADO = "BLOQUEADO"

    @staticmethod
    def evaluate(intention: str, context: dict) -> dict:
        """
        Evalúa la intención contra el contexto.
        
        Args:
            intention (str): Acción solicitada (ej. 'RENDER', 'DELETE', 'CREATE', 'EDIT_MODE').
            context (dict): Diccionario con el estado actual de Blender.
            
        Returns:
            dict: { "status": "PERMITIDO" | "BLOQUEADO", "reason": "Motivo del bloqueo o OK" }
        """
        intention = intention.upper()
        
        # Regla: RENDER
        if intention == "RENDER":
            if context.get("is_dirty", True):
                return {
                    "status": ContextGuard.BLOQUEADO,
                    "reason": "El archivo tiene cambios sin guardar. Guarda el archivo antes de renderizar para asegurar la integridad."
                }
        
        # Regla: DELETE (Borrar)
        if intention == "DELETE":
            selected_count = context.get("selected_objects_count", 0)
            if selected_count == 0:
                return {
                    "status": ContextGuard.BLOQUEADO,
                    "reason": "No hay objetos seleccionados para borrar."
                }
        
        # Regla: CREATE (Crear Objeto)
        if intention == "CREATE":
            mode = context.get("mode", "UNKNOWN")
            if mode != "OBJECT":
                return {
                    "status": ContextGuard.BLOQUEADO,
                    "reason": f"No se pueden crear objetos en modo {mode}. Cambia a modo OBJETO primero."
                }
        
        # Regla: EDIT_MODE (Entrar en modo edición)
        if intention == "EDIT_MODE":
            active_object = context.get("active_object", None)
            if active_object is None:
                return {
                    "status": ContextGuard.BLOQUEADO,
                    "reason": "No hay un objeto activo para entrar en modo edición."
                }
        
        # Si no hay reglas específicas o todas pasan
        return {
            "status": ContextGuard.PERMITIDO,
            "reason": "Contexto validado y coherente."
        }
