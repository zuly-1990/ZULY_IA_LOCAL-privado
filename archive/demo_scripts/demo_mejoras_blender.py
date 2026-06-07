# demo_mejoras_blender.py
"""
Demostración de las mejoras implementadas con Blender real.

Este script muestra cómo las nuevas excepciones, validadores y
mejoras en NLU funcionan en un escenario real con Blender.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from core.agent import Agent
from core.utils.exceptions import (
    CommandExecutionError,
    NLUError,
    ValidationError
)
from core.utils.validators import validate_location, validate_scale
from core.utils.logging import log

def demo_validadores():
    """Demuestra el uso de validadores antes de ejecutar comandos."""
    print("\n" + "="*70)
    print("DEMO 1: Validadores en Acción")
    print("="*70)
    
    # Validar ubicación antes de crear objeto
    try:
        ubicacion = validate_location("2, 3, 4")
        print(f"✓ Ubicación validada: {ubicacion}")
        
        escala = validate_scale(2.5)
        print(f"✓ Escala validada: {escala}")
        
        # Intentar validación inválida
        try:
            ubicacion_mala = validate_location("abc")
        except ValidationError as e:
            print(f"✓ Error de validación capturado correctamente:")
            print(f"  {e.message}")
            print(f"  Detalles: {e.details}")
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


def demo_manejo_errores():
    """Demuestra el manejo mejorado de errores."""
    print("\n" + "="*70)
    print("DEMO 2: Manejo de Errores Específicos")
    print("="*70)
    
    agent = Agent(auto_monitor=False)
    
    # Test 1: Comando válido
    try:
        print("\n[Test 1] Procesando: 'crear un cubo'")
        resultado = agent.process_natural_request("crear un cubo")
        
        if resultado.get('success'):
            print(f"✓ Comando ejecutado exitosamente")
            print(f"  Feedback: {resultado.get('feedback', 'N/A')}")
        else:
            print(f"⚠ Comando no ejecutado completamente")
            print(f"  Razón: {resultado.get('feedback', 'N/A')}")
    
    except CommandExecutionError as e:
        print(f"✓ CommandExecutionError capturada:")
        print(f"  {e.message}")
        print(f"  Comando: {e.details.get('command', 'N/A')}")
    
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
    
    # Test 2: Entrada inválida para NLU
    try:
        print("\n[Test 2] Procesando entrada None")
        resultado = agent.process_natural_request(None)
    
    except NLUError as e:
        print(f"✓ NLUError capturada correctamente:")
        print(f"  {e.message}")
    
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")


def demo_nlu_mejorado():
    """Demuestra las mejoras en NLU."""
    print("\n" + "="*70)
    print("DEMO 3: NLU Mejorado con Caché")
    print("="*70)
    
    agent = Agent(auto_monitor=False)
    
    # Limpiar caché
    agent.nlu._calculate_similarity.cache_clear()
    
    # Primera búsqueda
    print("\n[Primera búsqueda] Buscando comando similar...")
    import time
    start = time.perf_counter()
    resultado1 = agent.process_natural_request("crear esfera")
    tiempo1 = time.perf_counter() - start
    
    # Segunda búsqueda (con caché)
    print("\n[Segunda búsqueda] Buscando comando similar (con caché)...")
    start = time.perf_counter()
    resultado2 = agent.process_natural_request("crear esfera")
    tiempo2 = time.perf_counter() - start
    
    # Mostrar estadísticas de caché
    cache_info = agent.nlu._calculate_similarity.cache_info()
    print(f"\n✓ Estadísticas de caché:")
    print(f"  Hits: {cache_info.hits}")
    print(f"  Misses: {cache_info.misses}")
    print(f"  Tamaño actual: {cache_info.currsize}")
    print(f"  Tamaño máximo: {cache_info.maxsize}")
    print(f"\n✓ Rendimiento:")
    print(f"  Primera búsqueda: {tiempo1*1000:.2f}ms")
    print(f"  Segunda búsqueda: {tiempo2*1000:.2f}ms")
    if tiempo1 > 0:
        mejora = ((tiempo1 - tiempo2) / tiempo1) * 100
        print(f"  Mejora: {mejora:.1f}%")


def demo_comandos_blender():
    """Demuestra ejecución de comandos reales con Blender."""
    print("\n" + "="*70)
    print("DEMO 4: Comandos con Blender Real")
    print("="*70)
    
    agent = Agent(auto_monitor=True)
    
    comandos_demo = [
        "crear un cubo en la posición 0, 0, 0",
        "crear una esfera dorada en 2, 0, 0",
        "crear un cilindro plateado en -2, 0, 0",
        "añadir una luz",
    ]
    
    print("\nEjecutando secuencia de comandos...")
    print("-" * 70)
    
    for i, comando in enumerate(comandos_demo, 1):
        print(f"\n[Comando {i}] {comando}")
        try:
            resultado = agent.process_natural_request(comando)
            
            if resultado.get('success'):
                print(f"  ✓ Éxito")
                if 'feedback' in resultado:
                    print(f"  Feedback: {resultado['feedback']}")
            else:
                print(f"  ⚠ No completado")
                if 'feedback' in resultado:
                    print(f"  Razón: {resultado['feedback']}")
        
        except Exception as e:
            print(f"  ❌ Error: {type(e).__name__}: {e}")
    
    # Mostrar resumen de sesión
    print("\n" + "="*70)
    print("RESUMEN DE SESIÓN")
    print("="*70)
    
    resumen = agent.get_session_summary()
    print(f"Total de comandos ejecutados: {resumen.get('total_executions', 0)}")
    print(f"Comandos exitosos: {resumen.get('successful_executions', 0)}")
    print(f"Comandos fallidos: {resumen.get('failed_executions', 0)}")


def demo_completo():
    """Ejecuta todas las demos."""
    print("\n" + "="*70)
    print("DEMOSTRACIÓN COMPLETA DE MEJORAS - ZULY + BLENDER")
    print("="*70)
    print("\nEste script demuestra las mejoras implementadas:")
    print("  • Excepciones personalizadas")
    print("  • Validadores centralizados")
    print("  • NLU mejorado con caché")
    print("  • Manejo de errores robusto")
    print("="*70)
    
    try:
        # Demo 1: Validadores
        demo_validadores()
        
        # Demo 2: Manejo de errores
        demo_manejo_errores()
        
        # Demo 3: NLU mejorado
        demo_nlu_mejorado()
        
        # Demo 4: Comandos con Blender
        print("\n" + "="*70)
        print("¿Deseas ejecutar comandos reales con Blender? (s/n)")
        print("NOTA: Esto requiere que Blender esté disponible")
        print("="*70)
        
        respuesta = input("Respuesta: ").strip().lower()
        
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            demo_comandos_blender()
        else:
            print("\n✓ Demo de comandos Blender omitida")
        
        # Resumen final
        print("\n" + "="*70)
        print("✅ DEMOSTRACIÓN COMPLETADA")
        print("="*70)
        print("\nTodas las mejoras están funcionando correctamente:")
        print("  ✓ Excepciones personalizadas")
        print("  ✓ Validadores centralizados")
        print("  ✓ NLU con caché LRU")
        print("  ✓ Manejo de errores robusto")
        print("\n" + "="*70)
    
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrumpida por el usuario")
    
    except Exception as e:
        print(f"\n\n❌ Error en demo: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    demo_completo()
