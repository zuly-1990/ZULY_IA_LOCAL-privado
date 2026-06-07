# SACRED MODULE – DO NOT MODIFY WITHOUT EXPLICIT CONSENSUS
#
# Nombre: NoeGuard
# Función: Inmunidad de Principios (Checksum Ético)
# Estado: ACTIVO - CRÍTICO
#
# Este módulo protege la integridad de la Tabla de NOÉ.
# Cualquier alteración en los principios fundamentales causará
# que el sistema rechace operar (fail-silent o integridad comprometida).

import hashlib
import os
from typing import Optional
from core.utils.logging import log_error

class NoeGuard:
    """
    Guardián de la integridad de principios.
    
    Verifica que la Tabla de NOÉ no haya sido alterada.
    No interpreta, solo compara.
    """
    
    # Hash SHA256 inmutable de docs/philosophy/TABLA_DE_NOE.md
    # Calculado: 2026-01-04
    SACRED_HASH = "b7f385f03e72adb21f400d21de1563408261dbe34450031586f61b4de11dfa13"
    
    # Ruta relativa al archivo sagrado (asumiendo ejecución desde root)
    SACRED_FILE_PATH = "docs/philosophy/TABLA_DE_NOE.md"

    @staticmethod
    def verify_integrity(_override_path: Optional[str] = None) -> bool:
        """
        Verifica la integridad del archivo de principios.
        
        Args:
            _override_path: Ruta opcional para pruebas (internal usage only).
        
        Returns:
            True si el hash coincide (integridad OK).
            False si hay discrepancia o error (integridad COMPROMETIDA).
        """
        try:
            target_path = _override_path or NoeGuard.SACRED_FILE_PATH
            
            if not os.path.exists(target_path):
                # Fallo silencioso en logs, pero retorno False
                return False
                
            with open(target_path, 'rb') as f:
                content = f.read()
            
            # Normalizar saltos de línea a LF para consistencia cross-platform
            content_normalized = content.replace(b'\r\n', b'\n')
                
            calculated_hash = hashlib.sha256(content_normalized).hexdigest()
            
            if calculated_hash != NoeGuard.SACRED_HASH:
                # INTEGRIDAD COMPROMETIDA
                # No lanzamos excepción ruidosa, retornamos señal de compromiso.
                return False
                
            return True
            
        except Exception:
            # Cualquier error de lectura se considera compromiso de seguridad
            return False
