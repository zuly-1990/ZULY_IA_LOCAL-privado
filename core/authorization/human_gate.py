"""
HumanGate - Capa de Autorización Humana
Fase 14: Clasificación de riesgo operacional.
"""

class HumanGate:
    """
    Clasifica las acciones según su nivel de riesgo y decide el flujo de autorización.
    """
    
    # Niveles de riesgo
    LOW = "LOW"       # Verde: Ejecución automática
    MEDIUM = "MEDIUM" # Amarillo: Pedir confirmación
    HIGH = "HIGH"     # Rojo: Bloqueado (Protocolo Negro)

    # Comandos clasificados
    RISK_MAP = {
        # BAJO RIESGO (Acciones de lectura o no destructivas simples)
        "LIST_OBJECTS": LOW,
        "GET_CONTEXT": LOW,
        "LIST_COLLECTIONS": LOW,
        
        # RIESGO MEDIO (Acciones destructivas o modificadoras comunes)
        "DELETE": MEDIUM,
        "DELETE_OBJECT": MEDIUM,
        "CREATE": MEDIUM,
        "APPLY_MATERIAL": MEDIUM,
        "TRANSFORM": MEDIUM,
        "RENDER": MEDIUM,
        
        # ALTO RIESGO (Acciones masivas, críticas o estructurales)
        "RESET_SCENE": HIGH,
        "DELETE_ALL": HIGH,
        "OVERWRITE_FILE": HIGH,
        "PURGE_DATA": HIGH
    }

    @staticmethod
    def authorize(intention: str) -> dict:
        """
        Clasifica una intención y decide el nivel de autorización requerido.
        
        Args:
            intention (str): Acción solicitada.
            
        Returns:
            dict: { "risk": str, "action": "EXECUTE" | "ASK" | "BLOCK", "reason": str }
        """
        intention = intention.upper()
        risk_level = HumanGate.RISK_MAP.get(intention, HumanGate.MEDIUM) # Default: MEDIUM por seguridad

        if risk_level == HumanGate.LOW:
            return {
                "risk": HumanGate.LOW,
                "action": "EXECUTE",
                "reason": "Acción de bajo riesgo. No requiere autorización."
            }
        
        elif risk_level == HumanGate.MEDIUM:
            return {
                "risk": HumanGate.MEDIUM,
                "action": "ASK",
                "reason": f"La acción '{intention}' tiene un riesgo moderado. Se requiere confirmación humana."
            }
        
        else: # HIGH
            return {
                "risk": HumanGate.HIGH,
                "action": "BLOCK",
                "reason": f"La acción '{intention}' es de ALTO RIESGO y está bloqueada por seguridad estructural."
            }
