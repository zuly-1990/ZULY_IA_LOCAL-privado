#!/usr/bin/env python3
"""Test de configuración de Blender para ZULY."""

import sys
from pathlib import Path

# Agregar raíz al path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("PRUEBA DE CONFIGURACIÓN DE BLENDER PARA ZULY")
print("=" * 70)

try:
    from core.environment.blender_config import BlenderConfig
    print("\n✓ Módulo blender_config cargado correctamente\n")
    
    # Obtener ruta
    blender_path = BlenderConfig.get_blender_path()
    print(f"Ruta de Blender: {blender_path}")
    
    # Verificar existencia
    if blender_path:
        exists = Path(blender_path).exists()
        print(f"Archivo existe: {exists}")
        
        if exists:
            print(f"✅ EXCELENTE: Blender encontrado en la ruta configurada")
        else:
            print(f"⚠️ ADVERTENCIA: Ruta configurada no existe")
    else:
        print(f"❌ ERROR: No se encontró ruta de Blender")
    
    # Mostrar otras configuraciones
    print(f"\nOtras configuraciones:")
    print(f"  • Versión: {BlenderConfig.get_blender_version()}")
    print(f"  • Modo conexión: {BlenderConfig.get_connection_mode()}")
    print(f"  • Modo operación: {BlenderConfig.get_operation_mode()}")
    print(f"  • Timeout: {BlenderConfig.get_timeout()} seg")
    print(f"  • Modo test: {BlenderConfig.is_test_mode()}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
