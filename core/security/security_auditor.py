"""
AUDITOR DE SEGURIDAD PROACTIVO (Bloque 4 - Refuerzo)
Analiza la intención maliciosa antes de que llegue al NLU.
"""
import re
from core.security.black_protocol import BlackProtocol
from core.utils.logging import log_warning, log_error

class SecurityAuditor:
    # Patrones de inyección más avanzados (Prompt Injection)
    DANGEROUS_PATTERNS = [
        r"(?i)ignore.*instructions",
        r"(?i)system.*prompt",
        r"(?i)acting.*as",
        r"(?i)developer.*mode",
        r"(?i)sudo.*rm",
        r"\{\{.*\}\}",  # Intento de template injection
    ]

    @staticmethod
    def audit_request(request_text: str) -> bool:
        """
        Analiza el texto buscando anomalías.
        Retorna True si es SEGURO, False si detecta riesgo.
        """
        # 1. Verificar longitud inusual (típico de payloads de inyección)
        if len(request_text) > 500:
            log_warning(f"Petición sospechosamente larga detectada ({len(request_text)} chars)")
            # No bloqueamos solo por longitud, pero subimos guardia
            
        # 2. Match de patrones peligrosos
        for pattern in SecurityAuditor.DANGEROUS_PATTERNS:
            if re.search(pattern, request_text):
                log_error(f"¡AMENAZA DETECTADA! Patrón: {pattern}")
                BlackProtocol.activate_lock(f"Intento de inyección: {pattern}")
                return False
                
        # 3. Verificación de caracteres no ASCII (ofuscación)
        non_ascii = len(re.findall(r'[^\x00-\x7F]', request_text))
        if non_ascii > len(request_text) * 0.3:
            log_warning("Posible intento de ofuscación detectado")
            
        return True
