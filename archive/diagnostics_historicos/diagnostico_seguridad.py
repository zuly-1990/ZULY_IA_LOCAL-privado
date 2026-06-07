#!/usr/bin/env python3
"""
diagnostico_seguridad.py
Verifica la existencia de la llave de identidad y el estado del Protocolo Negro.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.security.black_protocol import BlackProtocol
    from core.utils.logging import log_info, log_success, log_error, log_warning
except ImportError:
    print("❌ Error: No se encontraron los módulos de seguridad de ZULY.")
    sys.exit(1)

def main():
    print("\n" + "="*70)
    print("🔍 DIAGNÓSTICO DE SEGURIDAD - ZULY")
    print("="*70 + "\n")

    key_file = Path(".zuly_identity.key")
    ¿Funciona así?
    user input → agent.py → command_loader.py → blender_handlers/*.py → execute    lock_file = Path(".zuly_black_mode")
    
    if key_file.exists():
        log_success(f"Archivo de identidad encontrado: {key_file}")
        
        if lock_file.exists():
            log_warning("⚠️ PROTOCOLO NEGRO ACTIVO: El sistema está bloqueado.")
            with open(lock_file, 'r', encoding='utf-8') as f:
                log_info(f"Motivo del bloqueo: {f.read().strip()}")
            log_info("Es SEGURO borrar el archivo '.zuly_black_mode' para restaurar el acceso.")
            log_info("ACCIÓN RECOMENDADA: Ejecuta 'python ejecutar_dado_con_desbloq.py'.")
        else:
            log_success("☀️ Sistema desbloqueado y listo para operar.")
    else:
        log_error("CRÍTICO: El archivo '.zuly_identity.key' NO fue encontrado.")
        log_warning("Sin esta llave, ZULY activa el Protocolo Negro para proteger la base de conocimiento.")

if __name__ == "__main__":
    main()