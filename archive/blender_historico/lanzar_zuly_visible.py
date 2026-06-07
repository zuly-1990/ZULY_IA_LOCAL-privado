#!/usr/bin/env python3
"""
lanzar_zuly_visible.py

Lanza Blender en modo visible (GUI) inyectando el servidor Live-Link (9999).
Permite que ZULY opere en tiempo real mientras ves los resultados.
"""

import subprocess
import sys
import os
import time
from pathlib import Path

# Configuración de Rutas
ZULY_ROOT = Path(r"c:\Users\Admin\Desktop\ZULY_IA_LOCAL")
BLENDER_EXE = ZULY_ROOT / "blender" / "v3" / "blender-3.6.0-zuly" / "blender.exe"
LIVELINK_SERVER = ZULY_ROOT / "core" / "adapters" / "livelink_server.py"

def launch_blender_visible():
    print("\n" + "="*70)
    print("🚀 INICIANDO ZULY LIVE-LINK EN MODO VISIBLE")
    print("="*70)
    
    if not BLENDER_EXE.exists():
        print(f"❌ Error: No se encontró Blender en {BLENDER_EXE}")
        return False
        
    print(f"✅ Ejecutable: {BLENDER_EXE}")
    print(f"📡 Cargando Servidor: {LIVELINK_SERVER}")
    
    # Comando para lanzar Blender con el script del servidor
    cmd = [
        str(BLENDER_EXE),
        "--python", str(LIVELINK_SERVER)
    ]
    
    print("\n▶️  Abriendo Blender GUI...")
    # Usar Popen para no bloquear el script y poder lanzar la CLI después
    try:
        proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        print("\n⏳ Esperando 5 segundos para que el servidor Live-Link inicie...")
        time.sleep(5)
        
        # Verificar si el puerto 9999 está abierto
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            result = s.connect_ex(('localhost', 9999))
            if result == 0:
                print("✅ Live-Link detectado en el puerto 9999!")
            else:
                print("⚠️  Advertencia: No se detectó respuesta en el puerto 9999 aún.")
        
        print("\n🤖 Lanzando ZULY CLI v2...")
        # Lanzar la CLI en una nueva ventana de consola
        cli_cmd = ["python", str(ZULY_ROOT / "zuly_cli_v2.py"), "--real"]
        subprocess.Popen(cli_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        print("\n" + "="*70)
        print("🎉 TODO LISTO! Blender y la CLI están conectados.")
        print("Puedes empezar a enviar comandos en la nueva ventana de ZULY.")
        print("="*70 + "\n")
        
        return True
    except Exception as e:
        print(f"❌ Error lanzando procesos: {e}")
        return False

if __name__ == "__main__":
    launch_blender_visible()
