# core/security/identity.py
"""
Módulo de Seguridad e Identidad de Autor para ZULY.
Gestiona la verificación de autoría local y el blindaje de aprendizaje.
"""

import os
import uuid
import hashlib
from core.utils.logging import log_info, log_warning, log_error

KEY_FILE = ".zuly_identity.key"

def generate_local_key() -> str:
    """
    Genera una llave única de autoría en la máquina local si no existe.
    La llave se basa en un UUID4 para garantizar unicidad.
    """
    if os.path.exists(KEY_FILE):
        log_info("La llave de identidad ya existe localmente.")
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    
    # Generar nueva llave
    new_key = str(uuid.uuid4())
    try:
        with open(KEY_FILE, "w") as f:
            f.write(new_key)
        # Ocultar archivo en Windows si es posible (opcional, pero buena práctica)
        if os.name == 'nt':
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(KEY_FILE, 2) # 2 = Hidden
        
        log_info("✓ Nueva llave de identidad local generada exitosamente.")
        return new_key
    except Exception as e:
        log_error(f"Error al generar la llave de identidad: {e}")
        return ""

def is_author_verified() -> bool:
    """
    Comprueba la autoría buscando la llave en la raíz del proyecto
    o en dispositivos externos configurados como 'Bóvedas'.
    """
    # 1. Buscar en raíz local
    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, "r") as f:
                if len(f.read().strip()) > 0:
                    return True
        except:
            pass

    # 2. Buscar en Bóvedas Externas (USB, etc.)
    # Aquí podríamos mapear letras de unidad comunes o buscar un archivo específico
    import string
    if os.name == 'nt':
        # En Windows, buscamos en unidades extraíbles
        available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        for drive in available_drives:
            vault_path = os.path.join(drive, "ZULY_VAULT", KEY_FILE)
            if os.path.exists(vault_path):
                log_info(f"✓ Identidad verificada mediante Bóveda Física en {drive}")
                return True
                
    return False

def decision_learning_allowed(confidence: float = 1.0, coherence: bool = True) -> bool:
    """
    Devuelve True solo si el autor está verificado y se cumplen las condiciones técnicas.
    """
    verified = is_author_verified()
    
    if not verified:
        log_warning("Identidad: Intento de aprendizaje bloqueado. Autor no verificado.")
        return False
    
    if confidence < 0.9:
        log_warning(f"Identidad: Aprendizaje bloqueado por baja confianza ({confidence:.2f}).")
        return False
        
    if not coherence:
        log_warning("Identidad: Aprendizaje bloqueado por falta de coherencia en la orden.")
        return False
        
    return True
