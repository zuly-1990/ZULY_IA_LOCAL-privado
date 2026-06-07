#!/usr/bin/env python3
"""
Lanzador de ZULY con Blender Real
Inicia Blender y carga ZULY para acceso completo a bpy
"""

import subprocess
import sys
import os
from pathlib import Path

ZULY_ROOT = Path(__file__).parent
BLENDER_PATH = ZULY_ROOT / "blender" / "v3" / "blender-3.6.0-zuly" / "blender.exe"

# Script Python que se ejecutará DENTRO de Blender
BLENDER_INIT_SCRIPT = """
import sys
from pathlib import Path

# Setup ZULY en Blender Python
zuly_path = r'""" + str(ZULY_ROOT) + """'
if zuly_path not in sys.path:
    sys.path.insert(0, zuly_path)

import bpy
print("\\n" + "="*70)
print("✅ BLENDER PYTHON API ACTIVA")
print("="*70)
print(f"Blender version: {bpy.app.version_string}")
print(f"Python version: {sys.version}")
print(f"ZULY path: {zuly_path}")
print("="*70 + "\\n")

# Importar ZULY Agent
from core.agent import Agent
from core.utils.logging import log_success, log_info

log_info("Inicializando ZULY con Blender Real...")
agent = Agent(force_mock=False)
log_success("✅ ZULY conectado a Blender Real (bpy disponible)")

# Ejecutar comando de prueba
log_info("\\nEjecutando: Crear un cubo...")
result = agent.process_natural_request("Crear un cubo de 2 metros")
if result.get('success'):
    log_success(f"✅ Cubo creado: {result.get('message')}")
    # Renderizar la escena
    log_info("\\nActivando renderizado...")
    result = agent.process_natural_request("Renderiza la escena")
    if result.get('success'):
        log_success(f"✅ Renderizado: {result.get('message')}")
else:
    log_info(f"⚠️ Resultado: {result.get('message')}")

print("\\n" + "="*70)
print("🎊 SESIÓN COMPLETADA")
print("="*70 + "\\n")
"""

def main():
    print("\n" + "="*70)
    print("🚀 LANZADOR DE ZULY CON BLENDER REAL")
    print("="*70 + "\n")
    
    # Verificar que Blender existe
    if not BLENDER_PATH.exists():
        print(f"❌ Blender no encontrado en: {BLENDER_PATH}")
        return False
    
    print(f"✅ Ejecutable: {BLENDER_PATH}")
    print(f"   Modo: BACKGROUND (sin interfaz gráfica)")
    print(f"   Propósito: Acceso completo a Python API (bpy)")
    
    # Crear archivo temporal con el script
    temp_script = ZULY_ROOT / "_zuly_blender_init.py"
    try:
        with open(temp_script, "w", encoding="utf-8") as f:
            f.write(BLENDER_INIT_SCRIPT)
        
        print(f"\n▶️  Iniciando Blender...")
        
        # Ejecutar Blender con el script
        cmd = [
            str(BLENDER_PATH),
            "--background",
            "--python", str(temp_script)
        ]
        
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        print("\n" + "="*70)
        if result.returncode == 0:
            print("✅ Ejecución completada exitosamente")
        else:
            print(f"⚠️ Ejecución terminó con código: {result.returncode}")
        print("="*70 + "\n")
        
        return result.returncode == 0
        
    finally:
        # Limpiar archivo temporal
        if temp_script.exists():
            temp_script.unlink()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
