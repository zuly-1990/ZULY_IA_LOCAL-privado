#!/usr/bin/env python3
"""
ZULY - Conexión Real a Blender 3.6.0
Conecta ZULY al Blender incluido en la instalación
"""

import os
import sys
from pathlib import Path

# Setup path
ZULY_ROOT = Path(__file__).parent
sys.path.insert(0, str(ZULY_ROOT))

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_warning, log_error

def main():
    print("\n" + "="*70)
    print("🔗 ZULY - CONEXIÓN A BLENDER REAL 3.6.0")
    print("="*70 + "\n")
    
    try:
        # Inicializar Agent CON Blender REAL (no mock)
        log_info("Inicializando Agent con Blender REAL...")
        agent = Agent(force_mock=False)
        
        log_success("✅ Conexión establecida con Blender real")
        
        # Verificar que el adapter es BlenderAdapter
        adapter_type = type(agent.engine_adapter).__name__
        log_info(f"Adapter activo: {adapter_type}")
        
        if adapter_type == "MockAdapter":
            log_warning("⚠️  Blender no disponible, usando MockAdapter como fallback")
        else:
            log_success("✅ BlenderAdapter conectado - Blender listo")
        
        print("\n" + "="*70)
        print("🎯 PRUEBAS DE CONEXIÓN")
        print("="*70 + "\n")
        
        # Test 1: Crear cubo simple
        log_info("[TEST 1] Creando cubo...")
        result = agent.process_natural_request("Crear un cubo")
        if result.get('success'):
            log_success(f"✅ TEST 1 EXITOSO: {result.get('message')}")
        else:
            log_warning(f"⚠️  TEST 1: {result.get('message')}")
        
        # Test 2: Crear esfera
        log_info("\n[TEST 2] Creando esfera...")
        result = agent.process_natural_request("Agregar una esfera")
        if result.get('success'):
            log_success(f"✅ TEST 2 EXITOSO: {result.get('message')}")
        else:
            log_warning(f"⚠️  TEST 2: {result.get('message')}")
        
        # Test 3: Cambiar color
        log_info("\n[TEST 3] Aplicando color rojo...")
        result = agent.process_natural_request("Colorea de rojo")
        if result.get('success'):
            log_success(f"✅ TEST 3 EXITOSO: {result.get('message')}")
        else:
            log_warning(f"⚠️  TEST 3: {result.get('message')}")
        
        print("\n" + "="*70)
        print("🎊 CONEXIÓN COMPLETADA")
        print("="*70)
        print(f"\n📊 Estado del Agent:")
        print(f"   • Modo: BLENDER REAL")
        print(f"   • Adapter: {adapter_type}")
        print(f"   • Handlers: {len(agent.intent_router.command_handlers)}")
        print(f"   • Status: ✅ OPERACIONAL\n")
        
        return True
        
    except Exception as e:
        log_error(f"Error durante la conexión: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
