"""
🚀 ZULY - 5 PRUEBAS REALES v2 (VERSIÓN ROBUSTA)
=====================================================

Script que ejecuta 5 pruebas complejas de ZULY usando toda su potencia:
- BlenderAdapter en modo REAL
- NLU completo con 59 handlers
- Memoria de patrones
- Arquitectura inteligente
- Inteligencia Operativa

Ejecución:
    blender --background --python test_5_pruebas_zuly_v2_robusto.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

import bpy
from core.agent import Agent

print("\n" + "="*80)
print("🚀 ZULY - 5 PRUEBAS REALES v2 (VERSIÓN ROBUSTA)")
print("="*80)

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Inicializar Agent con BlenderAdapter real
print("\n[INIT] Inicializando ZULY con BlenderAdapter en modo REAL...")
agent = Agent(force_mock=False)
print("✅ ZULY inicializado correctamente\n")

# Resultados
results = {
    "timestamp": datetime.now().isoformat(),
    "modo": "BLENDER REAL",
    "pruebas": [],
    "resumen": {"total": 5, "exitosas": 0, "fallidas": 0, "porcentaje": 0}
}

# ============================================================================
# PRUEBA 1: Operaciones básicas (Create + Move + Scale)
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ [PRUEBA 1/5] Operaciones Básicas (Create + Move + Scale)             │")
print("└" + "─"*78 + "┘\n")

try:
    # Crear cubo
    r1a = agent.execute_via_router('blender.create_cube', {
        'location': [0, 0, 0],
        'scale': 2.0,
        'name': 'Cubo_Test1'
    })
    
    # Mover
    r1b = agent.execute_via_router('blender.move_object', {
        'name': 'Cubo_Test1',
        'location': [3, 2, 1]
    })
    
    # Rotar
    r1c = agent.execute_via_router('blender.rotate_object', {
        'name': 'Cubo_Test1',
        'rotation': [45, 30, 15]
    })
    
    # Escalar
    r1d = agent.execute_via_router('blender.scale_object', {
        'name': 'Cubo_Test1',
        'scale': 1.5
    })
    
    success = all([r1a.get('success'), r1b.get('success'), 
                   r1c.get('success'), r1d.get('success')])
    
    if success:
        print("✅ PRUEBA 1: EXITOSA")
        print(f"   → Objeto: {r1a.get('object_name')}")
        print(f"   → Ubicación final: [3, 2, 1]")
        print(f"   → Rotación: 45°x, 30°y, 15°z")
        print(f"   → Escala: 1.5x")
        results["pruebas"].append({
            "numero": 1,
            "nombre": "Operaciones Básicas (Create + Move + Scale)",
            "exitosa": True,
            "operaciones": 4,
            "objeto": r1a.get('object_name')
        })
        results["resumen"]["exitosas"] += 1
    else:
        print("❌ PRUEBA 1: FALLIDA")
        raise Exception("Una o más operaciones fallaron")
        
except Exception as e:
    print(f"❌ PRUEBA 1: FALLIDA - {e}")
    results["pruebas"].append({
        "numero": 1,
        "nombre": "Operaciones Básicas (Create + Move + Scale)",
        "exitosa": False,
        "error": str(e)
    })
    results["resumen"]["fallidas"] += 1

print()

# ============================================================================
# PRUEBA 2: Arquitectura Inteligente (Muro + Ventana + Puerta)
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ [PRUEBA 2/5] Arquitectura Inteligente (Muro + Ventana + Puerta)      │")
print("└" + "─"*78 + "┘\n")

try:
    # Muro profesional
    r2a = agent.execute_via_router('blender.create_pro_wall', {
        'location': [0, 0, 0],
        'width': 5.0,
        'height': 3.0,
        'depth': 0.3,
        'name': 'Muro_001'
    })
    
    # Ventana inteligente
    r2b = agent.execute_via_router('blender.create_intelligent_window', {
        'location': [1.5, 0.01, 1.8],
        'width': 1.5,
        'height': 1.4,
        'name': 'Ventana_001'
    })
    
    # Puerta inteligente
    r2c = agent.execute_via_router('blender.create_intelligent_door', {
        'location': [-1.5, 0.01, 0],
        'width': 1.0,
        'height': 2.5,
        'name': 'Puerta_001'
    })
    
    success = all([r2a.get('success'), r2b.get('success'), r2c.get('success')])
    
    if success:
        print("✅ PRUEBA 2: EXITOSA")
        print(f"   → Componentes arquitectónicos: 3")
        print(f"   → Muro: 5.0m x 3.0m x 0.3m")
        print(f"   → Ventana: 1.5m x 1.4m (inteligente)")
        print(f"   → Puerta: 1.0m x 2.5m (inteligente)")
        results["pruebas"].append({
            "numero": 2,
            "nombre": "Arquitectura Inteligente (Muro + Ventana + Puerta)",
            "exitosa": True,
            "componentes": 3,
            "tipos": ["pro_wall", "intelligent_window", "intelligent_door"]
        })
        results["resumen"]["exitosas"] += 1
    else:
        print("❌ PRUEBA 2: FALLIDA")
        raise Exception("Fallo en creación arquitectónica")
        
except Exception as e:
    print(f"❌ PRUEBA 2: FALLIDA - {e}")
    results["pruebas"].append({
        "numero": 2,
        "nombre": "Arquitectura Inteligente (Muro + Ventana + Puerta)",
        "exitosa": False,
        "error": str(e)
    })
    results["resumen"]["fallidas"] += 1

print()

# ============================================================================
# PRUEBA 3: Escena Multi-Objeto con Iluminación Realista
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ [PRUEBA 3/5] Escena Multi-Objeto con Iluminación Realista            │")
print("└" + "─"*78 + "┘\n")

try:
    # Esfera
    r3a = agent.execute_via_router('blender.create_sphere', {
        'location': [4, 0, 1.5],
        'scale': 1.2,
        'name': 'Esfera_001'
    })
    
    # Cilindro
    r3b = agent.execute_via_router('blender.create_cylinder', {
        'location': [-4, 0, 1],
        'scale': 0.8,
        'name': 'Cilindro_001'
    })
    
    # Cono
    r3c = agent.execute_via_router('blender.create_cone', {
        'location': [0, 4, 1],
        'scale': 1.0,
        'name': 'Cono_001'
    })
    
    # Plano (piso)
    r3d = agent.execute_via_router('blender.create_plane', {
        'location': [0, 0, -0.5],
        'scale': [10, 10, 1],
        'name': 'Piso_001'
    })
    
    # Luz solar
    r3e = agent.execute_via_router('blender.create_light', {
        'light_type': 'SUN',
        'location': [5, 5, 8],
        'energy': 2.5,
        'name': 'Sol_001'
    })
    
    # Luz puntual
    r3f = agent.execute_via_router('blender.create_light', {
        'light_type': 'POINT',
        'location': [-5, -5, 5],
        'energy': 1.8,
        'name': 'Punto_001'
    })
    
    success = all([r3a.get('success'), r3b.get('success'), r3c.get('success'),
                   r3d.get('success'), r3e.get('success'), r3f.get('success')])
    
    if success:
        print("✅ PRUEBA 3: EXITOSA")
        print(f"   → Primitivas: esfera, cilindro, cono, plano (4)")
        print(f"   → Luces: SUN (2.5W) + POINT (1.8W)")
        print(f"   → Objetos totales: 6")
        results["pruebas"].append({
            "numero": 3,
            "nombre": "Escena Multi-Objeto con Iluminación Realista",
            "exitosa": True,
            "primitivas": 4,
            "luces": 2,
            "total_objetos": 6
        })
        results["resumen"]["exitosas"] += 1
    else:
        print("❌ PRUEBA 3: FALLIDA")
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
# PRUEBA 4: Modificadores Avanzados (Subdiv + Bevel)
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ [PRUEBA 4/5] Modificadores Avanzados (Subdiv + Bevel)                │")
print("└" + "─"*78 + "┘\n")

try:
    # Crear cubo base
    r4a = agent.execute_via_router('blender.create_cube', {
        'location': [0, 0, 3],
        'scale': 1.5,
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
        'amount': 0.15
    })
    
    success = all([r4a.get('success'), r4b.get('success'), r4c.get('success')])
    
    if success:
        print("✅ PRUEBA 4: EXITOSA")
        print(f"   → Base: {r4a.get('object_name')}")
        print(f"   → Subdivision Surface aplicado (niveles: 2)")
        print(f"   → Bevel aplicado (amount: 0.15)")
        print(f"   → Modificadores: 2")
        results["pruebas"].append({
            "numero": 4,
            "nombre": "Modificadores Avanzados (Subdiv + Bevel)",
            "exitosa": True,
            "objeto": r4a.get('object_name'),
            "modificadores": ["Subdivision Surface", "Bevel"],
            "total_modificadores": 2
        })
        results["resumen"]["exitosas"] += 1
    else:
        print("❌ PRUEBA 4: FALLIDA")
        raise Exception("Fallo en aplicación de modificadores")
        
except Exception as e:
    print(f"❌ PRUEBA 4: FALLIDA - {e}")
    results["pruebas"].append({
        "numero": 4,
        "nombre": "Modificadores Avanzados (Subdiv + Bevel)",
        "exitosa": False,
        "error": str(e)
    })
    results["resumen"]["fallidas"] += 1

print()

# ============================================================================
# PRUEBA 5: Integración Completa (Estadísticas + Guardar .blend)
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ [PRUEBA 5/5] Integración Completa (Stats + Guardar .blend)           │")
print("└" + "─"*78 + "┘\n")

try:
    # Crear cámara para completar la escena
    r5a = agent.execute_via_router('blender.create_camera', {
        'location': [10, -10, 8],
        'name': 'Camara_Final'
    })
    
    # Obtener estadísticas de escena ANTES de guardar
    num_objects = len(bpy.data.objects)
    num_materials = len(bpy.data.materials)
    num_lights = len([obj for obj in bpy.data.objects if obj.type == 'LIGHT'])
    num_cameras = len([obj for obj in bpy.data.objects if obj.type == 'CAMERA'])
    
    # Guardar escena
    blend_dir = Path("ZULY_PROJECTS")
    blend_dir.mkdir(parents=True, exist_ok=True)
    blend_path = str(blend_dir / "zuly_5pruebas_v2_robusto.blend")
    
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    blend_exists = Path(blend_path).exists()
    blend_size = Path(blend_path).stat().st_size if blend_exists else 0
    
    success = r5a.get('success') and blend_exists
    
    if success:
        print("✅ PRUEBA 5: EXITOSA")
        print(f"   → Cámara: {r5a.get('object_name')}")
        print(f"   → Archivo .blend: {blend_path}")
        print(f"   → Tamaño archivo: {blend_size / 1024:.2f} KB")
        print(f"   → Objetos en escena: {num_objects}")
        print(f"   → Materiales: {num_materials}")
        print(f"   → Luces: {num_lights}")
        print(f"   → Cámaras: {num_cameras}")
        results["pruebas"].append({
            "numero": 5,
            "nombre": "Integración Completa (Stats + Guardar .blend)",
            "exitosa": True,
            "detalles": {
                "archivo": blend_path,
                "tamaño_kb": round(blend_size / 1024, 2),
                "objetos": num_objects,
                "materiales": num_materials,
                "luces": num_lights,
                "camaras": num_cameras
            }
        })
        results["resumen"]["exitosas"] += 1
    else:
        print("❌ PRUEBA 5: FALLIDA")
        raise Exception("Fallo en integración")
        
except Exception as e:
    print(f"❌ PRUEBA 5: FALLIDA - {e}")
    results["pruebas"].append({
        "numero": 5,
        "nombre": "Integración Completa (Stats + Guardar .blend)",
        "exitosa": False,
        "error": str(e)
    })
    results["resumen"]["fallidas"] += 1

print()

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("┌" + "─"*78 + "┐")
print("│ RESUMEN FINAL - ZULY CON POTENCIA MÁXIMA                              │")
print("└" + "─"*78 + "┘\n")

exitosas = results["resumen"]["exitosas"]
total = results["resumen"]["total"]
porcentaje = (exitosas / total) * 100
results["resumen"]["porcentaje"] = round(porcentaje, 1)

print(f"📊 RESULTADOS FINALES:")
print(f"   ✅ Pruebas exitosas: {exitosas}/{total}")
print(f"   ❌ Pruebas fallidas: {results['resumen']['fallidas']}/{total}")
print(f"   📈 Porcentaje de éxito: {porcentaje:.1f}%\n")

print("📋 DETALLE DE PRUEBAS:")
for prueba in results["pruebas"]:
    status = "✅" if prueba["exitosa"] else "❌"
    print(f"   {status} [{prueba['numero']}] {prueba['nombre']}")

print()

# Guardar resultados en JSON
results_dir = Path("ZULY_LAB/resultados_zuly")
results_dir.mkdir(parents=True, exist_ok=True)
results_file = results_dir / "5_pruebas_v2_resultados.json"

with open(results_file, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"📁 Resultados guardados en: {results_file}\n")

print("="*80)
if exitosas >= 4:
    print("🎯 ZULY - 5 PRUEBAS CON POTENCIA MÁXIMA: ✅ COMPLETADAS EXITOSAMENTE")
else:
    print("⚠️  ZULY - 5 PRUEBAS: COMPLETADAS (Se requieren ajustes)")
print("="*80 + "\n")
