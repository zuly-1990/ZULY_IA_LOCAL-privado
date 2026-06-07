# test_blender_integration.py
"""
Test de integración con Blender para validar mejoras.

Este script prueba la integración completa del sistema mejorado
con Blender en modo headless.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_blender_disponible():
    """Verifica si Blender está disponible."""
    print("Verificando disponibilidad de Blender...")
    
    try:
        import bpy
        print(f"✓ Blender disponible: versión {bpy.app.version_string}")
        return True
    except ImportError:
        print("⚠ Blender no disponible (bpy no importable)")
        print("  Este test debe ejecutarse desde Blender:")
        print("  blender --background --python test_blender_integration.py")
        return False


def test_crear_cubo_con_validacion():
    """Test: Crear cubo usando validadores."""
    print("\n[Test 1] Crear cubo con validación de parámetros")
    print("-" * 70)
    
    from core.utils.validators import validate_location, validate_scale
    from core.utils.exceptions import ValidationError
    
    try:
        # Validar parámetros
        ubicacion = validate_location([0, 0, 0])
        escala = validate_scale(2.0)
        
        print(f"✓ Ubicación validada: {ubicacion}")
        print(f"✓ Escala validada: {escala}")
        
        # Crear cubo con Blender
        import bpy
        bpy.ops.mesh.primitive_cube_add(location=ubicacion)
        obj = bpy.context.active_object
        obj.scale = (escala, escala, escala)
        
        print(f"✓ Cubo creado: {obj.name}")
        print(f"  Ubicación: {obj.location}")
        print(f"  Escala: {obj.scale}")
        
        return True
    
    except ValidationError as e:
        print(f"❌ Error de validación: {e.message}")
        return False
    
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return False


def test_manejo_errores_comando():
    """Test: Manejo de errores en ejecución de comandos."""
    print("\n[Test 2] Manejo de errores en comandos")
    print("-" * 70)
    
    from core.agent import Agent
    from core.utils.exceptions import CommandExecutionError, NLUError
    
    agent = Agent(auto_monitor=False)
    
    # Test 1: Entrada válida
    try:
        print("Ejecutando: 'crear un cubo'")
        resultado = agent.process_natural_request("crear un cubo")
        print(f"✓ Resultado: {resultado.get('success', False)}")
    except Exception as e:
        print(f"⚠ Excepción: {type(e).__name__}")
    
    # Test 2: Entrada inválida
    try:
        print("Ejecutando: None (debería fallar)")
        resultado = agent.process_natural_request(None)
        print(f"❌ No se lanzó excepción (inesperado)")
        return False
    except NLUError as e:
        print(f"✓ NLUError capturada correctamente: {e.message}")
    
    return True


def test_nlu_cache_performance():
    """Test: Rendimiento del caché de NLU."""
    print("\n[Test 3] Rendimiento del caché de NLU")
    print("-" * 70)
    
    from core.agent import Agent
    import time
    
    agent = Agent(auto_monitor=False)
    
    # Limpiar caché
    agent.nlu._calculate_similarity.cache_clear()
    
    # Ejecutar múltiples búsquedas
    comandos = ["crear cubo", "crear esfera", "crear cilindro"] * 3
    
    tiempos = []
    for comando in comandos:
        start = time.perf_counter()
        agent.process_natural_request(comando)
        elapsed = time.perf_counter() - start
        tiempos.append(elapsed)
    
    # Mostrar estadísticas
    cache_info = agent.nlu._calculate_similarity.cache_info()
    print(f"✓ Caché LRU:")
    print(f"  Hits: {cache_info.hits}")
    print(f"  Misses: {cache_info.misses}")
    print(f"  Hit rate: {cache_info.hits / (cache_info.hits + cache_info.misses) * 100:.1f}%")
    
    print(f"✓ Tiempos de ejecución:")
    print(f"  Promedio: {sum(tiempos)/len(tiempos)*1000:.2f}ms")
    print(f"  Mínimo: {min(tiempos)*1000:.2f}ms")
    print(f"  Máximo: {max(tiempos)*1000:.2f}ms")
    
    return cache_info.hits > 0


def test_escena_completa():
    """Test: Crear escena completa con múltiples objetos."""
    print("\n[Test 4] Crear escena completa")
    print("-" * 70)
    
    from core.agent import Agent
    
    agent = Agent(auto_monitor=True)
    
    comandos = [
        "crear un cubo en 0, 0, 0",
        "crear una esfera en 2, 0, 0",
        "crear un cilindro en -2, 0, 0",
        "añadir una luz",
    ]
    
    exitosos = 0
    fallidos = 0
    
    for comando in comandos:
        print(f"\nEjecutando: '{comando}'")
        try:
            resultado = agent.process_natural_request(comando)
            if resultado.get('success'):
                exitosos += 1
                print(f"  ✓ Éxito")
            else:
                fallidos += 1
                print(f"  ⚠ Fallido: {resultado.get('feedback', 'N/A')}")
        except Exception as e:
            fallidos += 1
            print(f"  ❌ Error: {type(e).__name__}")
    
    print(f"\n✓ Resumen:")
    print(f"  Exitosos: {exitosos}/{len(comandos)}")
    print(f"  Fallidos: {fallidos}/{len(comandos)}")
    
    # Verificar escena en Blender
    try:
        import bpy
        objetos = len([obj for obj in bpy.data.objects if obj.type == 'MESH'])
        luces = len([obj for obj in bpy.data.objects if obj.type == 'LIGHT'])
        
        print(f"\n✓ Estado de escena Blender:")
        print(f"  Objetos mesh: {objetos}")
        print(f"  Luces: {luces}")
    except:
        pass
    
    return exitosos > 0


def run_all_tests():
    """Ejecuta todos los tests de integración."""
    print("="*70)
    print("TESTS DE INTEGRACIÓN CON BLENDER")
    print("="*70)
    
    # Verificar Blender
    if not test_blender_disponible():
        print("\n⚠ Tests omitidos: Blender no disponible")
        print("\nPara ejecutar estos tests:")
        print("  blender --background --python test_blender_integration.py")
        return
    
    # Ejecutar tests
    resultados = {
        "Crear cubo con validación": test_crear_cubo_con_validacion(),
        "Manejo de errores": test_manejo_errores_comando(),
        "Caché de NLU": test_nlu_cache_performance(),
        "Escena completa": test_escena_completa(),
    }
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)
    
    pasados = sum(1 for v in resultados.values() if v)
    totales = len(resultados)
    
    for nombre, resultado in resultados.items():
        estado = "✓ PASADO" if resultado else "❌ FALLIDO"
        print(f"{estado}: {nombre}")
    
    print(f"\nTotal: {pasados}/{totales} tests pasados")
    
    if pasados == totales:
        print("\n✅ TODOS LOS TESTS PASARON")
    else:
        print(f"\n⚠ {totales - pasados} test(s) fallaron")


if __name__ == "__main__":
    run_all_tests()
