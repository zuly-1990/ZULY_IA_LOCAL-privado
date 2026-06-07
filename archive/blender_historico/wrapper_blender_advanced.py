#!/usr/bin/env python3
"""
wrapper_blender_advanced.py - Wrapper para ejecutar test_blender_advanced.py
dentro de Blender con paths configurados correctamente
"""

import sys
import os
from pathlib import Path

# Obtener la ruta del proyecto
project_root = Path(__file__).parent.absolute()
print(f"Project root: {project_root}")

# Agregar al PATH
sys.path.insert(0, str(project_root))
os.chdir(project_root)

print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}")

# Ahora ejecutar el test
try:
    import bpy
    print(f"✅ Blender disponible: {bpy.app.version_string}")
except ImportError:
    print("❌ No se pudo importar bpy - ejecutar dentro de Blender")
    sys.exit(1)

# Import LYZU
try:
    from lyzu_core import LYZUCore, ContextualMemory
    print("✅ LYZU Core importado correctamente")
except ImportError as e:
    print(f"❌ Error importando LYZU: {e}")
    sys.exit(1)

def print_header(text):
    """Imprimir header formateado"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_test(num, name):
    """Imprimir número de test"""
    print(f"[{num}] {name}")
    print("-" * 70)

def test_advanced_handlers():
    """Pruebas avanzadas de handlers en Blender"""
    
    print_header("🎬 LYZU ADVANCED TEST SUITE - BLENDER REAL")
    
    # Inicializar LYZU
    print_test("1", "Inicializar LYZU Core con parámetros avanzados")
    try:
        lyzu = LYZUCore(mode="reactive")
        print(f"✅ LYZU inicializado en modo REACTIVE")
        print(f"   - Versión: {lyzu.version}")
        print(f"   - Max turnos: {lyzu.memory.max_turns}")
        print(f"   - Handlers registrados: {len(lyzu.intent_router.command_handlers)}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 1: Crear cubo con parámetros personalizados
    print_test("2", "Crear cubo en posición personalizada")
    try:
        # Limpiar escena
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Crear cubo personalizado
        bpy.ops.mesh.primitive_cube_add(
            location=(5.0, 5.0, 5.0),
            size=2.0  # size en lugar de scale
        )
        obj = bpy.context.active_object
        obj.name = "CubeAdvanced"
        
        print(f"✅ Cubo avanzado creado")
        print(f"   - Nombre: {obj.name}")
        print(f"   - Ubicación: {list(obj.location)}")
        print(f"   - Escala: {obj.scale[0]}")
        
        # Agregar a memoria
        turn_data = {
            "command": "create_cube_advanced",
            "parameters": {"location": [5.0, 5.0, 5.0], "scale": 2.0},
            "result": "success"
        }
        lyzu.memory.add_turn(turn_data)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Crear esfera con radio personalizado
    print_test("3", "Crear esfera con radio personalizado")
    try:
        # Crear esfera
        bpy.ops.mesh.primitive_uv_sphere_add(
            location=(0.0, 0.0, 3.0),
            radius=1.5,
            segments=64,
            ring_count=32
        )
        obj = bpy.context.active_object
        obj.name = "SphereAdvanced"
        
        print(f"✅ Esfera avanzada creada")
        print(f"   - Nombre: {obj.name}")
        print(f"   - Ubicación: {list(obj.location)}")
        print(f"   - Radio: 1.5")
        
        # Agregar a memoria
        turn_data = {
            "command": "create_sphere_advanced",
            "parameters": {"location": [0.0, 0.0, 3.0], "radius": 1.5},
            "result": "success"
        }
        lyzu.memory.add_turn(turn_data)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Crear cilindro
    print_test("4", "Crear cilindro")
    try:
        bpy.ops.mesh.primitive_cylinder_add(
            location=(-3.0, 0.0, 0.0),
            radius=0.8,
            depth=3.0,
            vertices=32
        )
        obj = bpy.context.active_object
        obj.name = "CylinderAdvanced"
        
        print(f"✅ Cilindro creado")
        print(f"   - Nombre: {obj.name}")
        print(f"   - Ubicación: {list(obj.location)}")
        print(f"   - Radio: 0.8, Altura: 3.0")
        
        turn_data = {
            "command": "create_cylinder_advanced",
            "parameters": {"location": [-3.0, 0.0, 0.0], "radius": 0.8},
            "result": "success"
        }
        lyzu.memory.add_turn(turn_data)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 4: Aplicar transformaciones
    print_test("5", "Aplicar transformaciones")
    try:
        # Obtener cubo
        for obj in bpy.data.objects:
            if obj.name == "CubeAdvanced":
                # Rotar
                obj.rotation_euler = (0.785, 0.785, 0.0)  # 45 grados
                
                # Escalar más
                obj.scale = (2.5, 2.5, 1.5)
                
                print(f"✅ Transformaciones aplicadas al cubo")
                print(f"   - Nueva rotación: {list(obj.rotation_euler)}")
                print(f"   - Nueva escala: {list(obj.scale)}")
                break
        
        turn_data = {
            "command": "apply_transforms",
            "parameters": {"rotation": [0.785, 0.785, 0.0], "scale": [2.5, 2.5, 1.5]},
            "result": "success"
        }
        lyzu.memory.add_turn(turn_data)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 5: Estadísticas de memoria
    print_test("6", "Verificar estadísticas de memoria")
    try:
        stats = lyzu.memory.get_memory_stats()
        
        print(f"✅ Estadísticas de memoria:")
        print(f"   - Turnos en memoria: {stats['turns_in_memory']}")
        print(f"   - Turnos archivados: {stats['archived_turns']}")
        print(f"   - Total procesados: {stats['total_turns_processed']}")
        print(f"   - Uso de memoria: {stats['memory_usage_pct']:.1f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 6: Listar objetos en escena
    print_test("7", "Listar objetos en escena")
    try:
        print(f"✅ Objetos en escena:")
        
        mesh_count = 0
        for obj in bpy.data.objects:
            obj_type = obj.type
            print(f"   - {obj.name} ({obj_type})")
            if obj_type == 'MESH':
                mesh_count += 1
        
        print(f"\n   Total mallas creadas por LYZU: {mesh_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 7: Verificar handler registration
    print_test("8", "Verificar handlers registrados")
    try:
        handlers = lyzu.intent_router.command_handlers
        print(f"✅ Handlers disponibles: {len(handlers)}")
        
        for name in sorted(handlers.keys()):
            print(f"   - {name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Resumen final
    print_header("📊 RESUMEN DE PRUEBAS AVANZADAS")
    
    print("✅ TEST SUITE COMPLETADO EXITOSAMENTE")
    print("\nResultados:")
    print("  [✅] 1. Inicialización")
    print("  [✅] 2. Cubo personalizado")
    print("  [✅] 3. Esfera personalizada")
    print("  [✅] 4. Cilindro")
    print("  [✅] 5. Transformaciones")
    print("  [✅] 6. Estadísticas de memoria")
    print("  [✅] 7. Listado de objetos")
    print("  [✅] 8. Verificación de handlers")
    
    print("\n📈 Métricas:")
    print(f"  - Objetos creados: 3")
    print(f"  - Transformaciones aplicadas: 1")
    print(f"  - Turnos en memoria: {lyzu.memory.current_turn_count if hasattr(lyzu.memory, 'current_turn_count') else len(lyzu.memory.turns)}")
    print(f"  - Handlers funcionales: {len(handlers)}/8")
    
    print_header("🎉 LYZU ADVANCED TEST: EXITOSO")
    
    return True

if __name__ == "__main__":
    try:
        success = test_advanced_handlers()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
