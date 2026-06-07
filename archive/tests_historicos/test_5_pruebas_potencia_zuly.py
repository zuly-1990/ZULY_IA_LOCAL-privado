"""
🚀 ZULY - 5 PRUEBAS REALES CON POTENCIA MÁXIMA
=====================================================

Script que ejecuta 5 pruebas complejas de ZULY usando:
- BlenderAdapter en modo REAL
- NLU completo
- Handlers arquitectónicos
- Memoria de patrones
- Renderizado real

Ejecución:
    blender --background --python test_5_pruebas_potencia_zuly.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

import bpy
from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

print("\n" + "="*80)
print("🚀 ZULY - 5 PRUEBAS REALES CON POTENCIA MÁXIMA")
print("="*80)

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Inicializar Agent con BlenderAdapter real
print("\n[INIT] Inicializando ZULY con BlenderAdapter...")
agent = Agent(force_mock=False)
print("✅ ZULY inicializado\n")

# Resultados
results = {
    "timestamp": datetime.now().isoformat(),
    "pruebas": [],
    "resumen": {"total": 5, "exitosas": 0, "fallidas": 0}
}

# ============================================================================
# PRUEBA 1: Crear primitiva compleja con material y transformación
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ [PRUEBA 1/5] Primitiva Compleja + Material + Transformación          │")
print("└" + "─"*78 + "┘\n")

try:
    # Crear cubo
    r1a = agent.execute_via_router('blender.create_cube', {
        'location': [0, 0, 0],
        'scale': 2.0,
        'name': 'Cubo_Premium'
    })
    
    # Transformar (rotar + escalar)
    r1b = agent.execute_via_router('blender.rotate_object', {
        'name': 'Cubo_Premium',
        'rotation': [45, 30, 15]
    })
    
    # Escalar
    r1c = agent.execute_via_router('blender.scale_object', {
        'name': 'Cubo_Premium',
        'scale': [1.5, 1.2, 0.8]
    })
    
    success = r1a.get('success') and r1b.get('success') and r1c.get('success')
    
    if success:
        print("✅ PRUEBA 1: EXITOSA")
        print(f"   → Cubo creado: {r1a.get('object_name')}")
        print(f"   → Rotación: 45°x, 30°y, 15°z")
        print(f"   → Escala: 1.5x, 1.2y, 0.8z")
        results["pruebas"].append({
            "numero": 1,
            "nombre": "Primitiva Compleja + Material + Transformación",
            "exitosa": True,
            "detalles": {
                "objeto": r1a.get('object_name'),
                "transformaciones": ["rotación", "escala"],
                "rotacion": [45, 30, 15],
                "escala": [1.5, 1.2, 0.8]
            }
        })
        results["resumen"]["exitosas"] += 1
    else:
        raise Exception("Fallo en creación o transformación")
        
except Exception as e:
    print(f"❌ PRUEBA 1: FALLIDA - {e}")
    results["pruebas"].append({
        "numero": 1,
        "nombre": "Primitiva Compleja + Material + Transformación",
        "exitosa": False,
        "error": str(e)
    })
    results["resumen"]["fallidas"] += 1

print()

# ============================================================================
# PRUEBA 2: Crear escena arquitectónica básica
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ [PRUEBA 2/5] Escena Arquitectónica (Muro + Ventana + Puerta)        │")
print("└" + "─"*78 + "┘\n")

try:
    # Muro
    r2a = agent.execute_via_router('blender.create_pro_wall', {
        'location': [0, 0, 0],
        'width': 4.0,
        'height': 3.0,
        'depth': 0.2,
        'name': 'Muro_Principal'
    })
    
    # Ventana
    r2b = agent.execute_via_router('blender.create_intelligent_window', {
        'location': [1.5, 0, 1.5],
        'width': 1.5,
        'height': 1.5,
        'name': 'Ventana_001'
    })
    
    # Puerta
    r2c = agent.execute_via_router('blender.create_intelligent_door', {
        'location': [-1.0, 0, 0],
        'width': 1.0,
        'height': 2.5,
        'name': 'Puerta_001'
    })
    
    success = r2a.get('success') and r2b.get('success') and r2c.get('success')
    
    if success:
        print("✅ PRUEBA 2: EXITOSA")
        print(f"   → Muro: {r2a.get('object_name')} (4.0 x 3.0 x 0.2)")
        print(f"   → Ventana: {r2b.get('object_name')} (1.5 x 1.5)")
        print(f"   → Puerta: {r2c.get('object_name')} (1.0 x 2.5)")
        results["pruebas"].append({
            "numero": 2,
            "nombre": "Escena Arquitectónica (Muro + Ventana + Puerta)",
            "exitosa": True,
            "detalles": {
                "muro": r2a.get('object_name'),
                "ventana": r2b.get('object_name'),
                "puerta": r2c.get('object_name'),
                "componentes": 3
            }
        })
        results["resumen"]["exitosas"] += 1
    else:
        raise Exception("Fallo en creación arquitectónica")
        
except Exception as e:
    print(f"❌ PRUEBA 2: FALLIDA - {e}")
    results["pruebas"].append({
        "numero": 2,
        "nombre": "Escena Arquitectónica (Muro + Ventana + Puerta)",
        "exitosa": False,
        "error": str(e)
    })
    results["resumen"]["fallidas"] += 1

print()

# ============================================================================
# PRUEBA 3: Crear escena con múltiples primitivas y luces
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ [PRUEBA 3/5] Escena Multi-Objeto con Iluminación Realista            │")
print("└" + "─"*78 + "┘\n")

try:
    # Esfera
    r3a = agent.execute_via_router('blender.create_sphere', {
        'location': [3, 0, 1],
        'scale': 1.0,
        'name': 'Esfera_Dorada'
    })
    
    # Cilindro
    r3b = agent.execute_via_router('blender.create_cylinder', {
        'location': [0, 3, 0.5],
        'scale': 0.8,
        'name': 'Cilindro_Azul'
    })
    
    # Plano (piso)
    r3c = agent.execute_via_router('blender.create_plane', {
        'location': [0, 0, -1],
        'scale': [5, 5, 1],
        'name': 'Piso'
    })
    
    # Luz solar
    r3d = agent.execute_via_router('blender.create_light', {
        'light_type': 'SUN',
        'location': [5, 5, 5],
        'energy': 3.0,
        'name': 'Sol'
    })
    
    # Luz puntual
    r3e = agent.execute_via_router('blender.create_light', {
        'light_type': 'POINT',
        'location': [-3, -3, 3],
        'energy': 2.0,
        'name': 'Punto'
    })
    
    success = all([r3a.get('success'), r3b.get('success'), r3c.get('success'),
                   r3d.get('success'), r3e.get('success')])
    
    if success:
        print("✅ PRUEBA 3: EXITOSA")
        print(f"   → Esfera: {r3a.get('object_name')}")
        print(f"   → Cilindro: {r3b.get('object_name')}")
        print(f"   → Piso: {r3c.get('object_name')}")
        print(f"   → Luz solar: {r3d.get('object_name')} (3.0 W)")
        print(f"   → Luz punto: {r3e.get('object_name')} (2.0 W)")
        results["pruebas"].append({
            "numero": 3,
            "nombre": "Escena Multi-Objeto con Iluminación Realista",
            "exitosa": True,
            "detalles": {
                "primitivas": 3,
                "luces": 2,
                "total_objetos": 5
            }
        })
        results["resumen"]["exitosas"] += 1
    else:
        raise Exception("Fallo en creación multi-objeto")
        
except Exception as e:
    print(f"❌ PRUEBA 3: FALLIDA - {e}")
    results["pruebas"].append({
        "numero": 3,
        "nombre": "Escena Multi-Objeto con Iluminación Realista",
        "exitosa": False,
        "error": str(e)
    })
    results["resumen"]["fallidas"] += 1

print()

# ============================================================================
# PRUEBA 4: Aplicar modificadores complejos
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ [PRUEBA 4/5] Modificadores Avanzados (Subdiv + Bevel + Array)        │")
print("└" + "─"*78 + "┘\n")

try:
    # Crear base para modificadores
    r4a = agent.execute_via_router('blender.create_cube', {
        'location': [-4, 0, 0],
        'scale': 1.0,
        'name': 'Cubo_Modificado'
    })
    
    # Subdivision surface
    r4b = agent.execute_via_router('blender.add_subdivision_surface', {
        'object_name': 'Cubo_Modificado',
        'levels': 2
    })
    
    # Bevel
    r4c = agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Cubo_Modificado',
        'amount': 0.1
    })
    
    # Array (copia repetida)
    r4d = agent.execute_via_router('blender.add_array', {
        'object_name': 'Cubo_Modificado',
        'count': 3,
        'offset': [2, 0, 0]
    })
    
    success = all([r4a.get('success'), r4b.get('success'), 
                   r4c.get('success'), r4d.get('success')])
    
    if success:
        print("✅ PRUEBA 4: EXITOSA")
        print(f"   → Base: {r4a.get('object_name')}")
        print(f"   → Subdivision Surface: niveles 2")
        print(f"   → Bevel: 0.1 unidades")
        print(f"   → Array: 3 copias en eje X")
        results["pruebas"].append({
            "numero": 4,
            "nombre": "Modificadores Avanzados (Subdiv + Bevel + Array)",
            "exitosa": True,
            "detalles": {
                "objeto": r4a.get('object_name'),
                "modificadores": ["Subdivision Surface", "Bevel", "Array"],
                "total_modificadores": 3
            }
        })
        results["resumen"]["exitosas"] += 1
    else:
        raise Exception("Fallo en aplicación de modificadores")
        
except Exception as e:
    print(f"❌ PRUEBA 4: FALLIDA - {e}")
    results["pruebas"].append({
        "numero": 4,
        "nombre": "Modificadores Avanzados (Subdiv + Bevel + Array)",
        "exitosa": False,
        "error": str(e)
    })
    results["resumen"]["fallidas"] += 1

print()

# ============================================================================
# PRUEBA 5: Integración completa (Crear + Render + Guardar)
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ [PRUEBA 5/5] Integración Completa (Crear + Render + Guardar .blend)  │")
print("└" + "─"*78 + "┘\n")

try:
    # Crear cámara
    r5a = agent.execute_via_router('blender.create_camera', {
        'location': [8, -8, 6],
        'name': 'Camara_Principal'
    })
    
    # Establecer como activa
    r5b = agent.execute_via_router('blender.set_active_camera', {
        'name': 'Camara_Principal'
    })
    
    # Renderizar
    render_path = str(Path("ZULY_LAB/resultados_zuly/render_pruebas_potencia.png").absolute())
    Path("ZULY_LAB/resultados_zuly").mkdir(parents=True, exist_ok=True)
    
    r5c = agent.execute_via_router('blender.render_scene', {
        'output_path': render_path,
        'resolution': [800, 600],
        'samples': 32
    })
    
    # Guardar escena
    blend_path = str(Path("ZULY_PROJECTS/zuly_5pruebas_potencia.blend").absolute())
    Path("ZULY_PROJECTS").mkdir(parents=True, exist_ok=True)
    
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    render_exists = Path(render_path).exists()
    blend_exists = Path(blend_path).exists()
    
    success = r5a.get('success') and r5b.get('success') and render_exists and blend_exists
    
    if success:
        print("✅ PRUEBA 5: EXITOSA")
        print(f"   → Cámara: {r5a.get('object_name')}")
        print(f"   → Render: {render_path}")
        print(f"   → Archivo .blend: {blend_path}")
        results["pruebas"].append({
            "numero": 5,
            "nombre": "Integración Completa (Crear + Render + Guardar)",
            "exitosa": True,
            "detalles": {
                "camara": r5a.get('object_name'),
                "render_path": render_path,
                "blend_path": blend_path,
                "resolucion": "800x600",
                "samples": 32
            }
        })
        results["resumen"]["exitosas"] += 1
    else:
        raise Exception("Fallo en integración completa")
        
except Exception as e:
    print(f"❌ PRUEBA 5: FALLIDA - {e}")
    results["pruebas"].append({
        "numero": 5,
        "nombre": "Integración Completa (Crear + Render + Guardar)",
        "exitosa": False,
        "error": str(e)
    })
    results["resumen"]["fallidas"] += 1

print()

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ RESUMEN FINAL                                                        │")
print("└" + "─"*78 + "┘\n")

print(f"📊 Pruebas Exitosas: {results['resumen']['exitosas']}/5")
print(f"📊 Pruebas Fallidas: {results['resumen']['fallidas']}/5")
print(f"📊 Porcentaje de éxito: {(results['resumen']['exitosas']/5)*100:.1f}%\n")

for prueba in results['pruebas']:
    status = "✅" if prueba['exitosa'] else "❌"
    print(f"{status} [{prueba['numero']}] {prueba['nombre']}")

# Guardar resultados en JSON
results_path = Path("ZULY_LAB/resultados_zuly/5_pruebas_potencia_resultados.json")
results_path.parent.mkdir(parents=True, exist_ok=True)
with open(results_path, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n📁 Resultados guardados en: {results_path}")
print("\n" + "="*80)
print("🎯 ZULY - 5 PRUEBAS CON POTENCIA MÁXIMA: COMPLETADAS")
print("="*80 + "\n")
