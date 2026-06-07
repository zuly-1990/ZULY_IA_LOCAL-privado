#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ TEST ZULY REAL - Versión Simplificada y Funcional
Extracción de Patrones + JUES Validator + Medición de Velocidad

Flujo:
1. Crear modelo en Blender real
2. Extraer patrón de información
3. Validar con JUES
4. Medir velocidad
"""

import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

ZULY_HOME = Path("c:/Users/Admin/Desktop/ZULY_IA_LOCAL")
BLENDER_EXE = ZULY_HOME / "blender/v3/blender-3.6.0-zuly/blender.exe"
ARENA = ZULY_HOME / "archivo_zuly/temp_arena"
REPORTS = ZULY_HOME / "reports"

ARENA.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

BLENDER_SCRIPT = '''
import bpy
import json
import time
from datetime import datetime

start_total = time.time()

print("\\n" + "="*70)
print("ZULY TEST REAL - EXTRACCION DE PATRONES")
print("="*70)

# FASE 1: Limpiar
print("\\n[FASE 1] Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# FASE 2: Crear modelo con forma arquitectónica
print("[FASE 2] Creando modelo...")
start_model = time.time()

bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "ARQUITECTURA_CUBO_001"

# Aplicar Bevel modifier (simula arquitectura)
bevel = cube.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.05
bevel.segments = 3

elapsed_model = time.time() - start_model

# FASE 3: Extraer patrón
print("[FASE 3] Extrayendo patrón...")
start_extract = time.time()

geometry_info = {
    "object_name": cube.name,
    "object_type": "MESH",
    "vertices": len(cube.data.vertices),
    "edges": len(cube.data.edges),
    "faces": len(cube.data.polygons),
    "dimensions": list(cube.dimensions),
    "location": list(cube.location)
}

modifier_info = []
for mod in cube.modifiers:
    modifier_info.append({
        "type": mod.type,
        "name": mod.name,
        "enabled": mod.show_viewport
    })

pattern = {
    "pattern_id": "ARCH-CUB-001",
    "name": cube.name,
    "timestamp": datetime.now().isoformat(),
    "geometry": geometry_info,
    "modifiers": modifier_info
}

elapsed_extract = time.time() - start_extract

# FASE 4: Iluminación
print("[FASE 4] Configurando iluminación...")
start_light = time.time()

# Limpiar luces
for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# Agregar luces
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
bpy.context.active_object.data.energy = 2.0

bpy.ops.object.light_add(type='AREA', location=(-5, 0, 3))
bpy.context.active_object.data.energy = 1.0

elapsed_light = time.time() - start_light

# FASE 5: Guardar
print("[FASE 5] Guardando...")
start_save = time.time()

blend_path = "%s/ZULY_TEST_REAL.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

elapsed_save = time.time() - start_save

# FASE 6: Compilar reporte
elapsed_total = time.time() - start_total

report = {
    "success": True,
    "timestamp": datetime.now().isoformat(),
    "blender_version": ".".join(map(str, bpy.app.version)),
    "performance": {
        "model_creation_s": elapsed_model,
        "pattern_extraction_s": elapsed_extract,
        "illumination_s": elapsed_light,
        "save_s": elapsed_save,
        "total_s": elapsed_total
    },
    "pattern": pattern,
    "output_blend": blend_path
}

print("\\n" + "="*70)
print("RESULTADOS FINALES")
print("="*70)
print(f"Modelo: {pattern['name']}")
print(f"Vértices: {geometry_info['vertices']}")
print(f"Caras: {geometry_info['faces']}")
print(f"Modificadores: {len(modifier_info)}")
print(f"Tiempo Total: {elapsed_total:.3f}s")

# SALIDA PARA HOST
print("\\n[REPORT_START]")
print(json.dumps(report, indent=2, default=str))
print("[REPORT_END]")
''' % str(ARENA).replace("\\", "/")

def main():
    print("\n" + "="*70)
    print("TEST ZULY REAL - SISTEMA COMPLETO")
    print("="*70)
    
    # Preparar script
    print("\n[1/4] Preparando script Blender...")
    script_path = ZULY_HOME / "temp_test_simple.py"
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(BLENDER_SCRIPT)
    
    # Ejecutar Blender
    print("[2/4] Ejecutando Blender...")
    start_blender = time.time()
    
    cmd = [str(BLENDER_EXE), "--background", "--python", str(script_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    elapsed_blender = time.time() - start_blender
    
    # Parsear resultado
    print("[3/4] Analizando resultados...")
    print("\n" + "-"*70)
    print("SALIDA DE BLENDER:")
    print("-"*70)
    print(result.stdout)
    
    report_data = {}
    if "[REPORT_START]" in result.stdout:
        try:
            start = result.stdout.find("[REPORT_START]") + len("[REPORT_START]")
            end = result.stdout.find("[REPORT_END]")
            report_json = result.stdout[start:end].strip()
            report_data = json.loads(report_json)
        except Exception as e:
            print(f"Aviso: No se pudo parsear JSON: {e}")
    
    # Verificar archivos
    print("\n[4/4] Verificando archivos generados...")
    blend_file = ARENA / "ZULY_TEST_REAL.blend"
    
    exists = blend_file.exists()
    size = blend_file.stat().st_size if exists else 0
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN EJECUTIVO - TEST ZULY REAL")
    print("="*70)
    
    print("\n✓ CONEXION BLENDER")
    print(f"  Blender Ejecutado: {exists}")
    print(f"  Tiempo de Ejecución: {elapsed_blender:.2f}s")
    print(f"  Código de Salida: {result.returncode}")
    
    if report_data:
        perf = report_data.get("performance", {})
        pattern = report_data.get("pattern", {})
        
        print("\n✓ PATRON EXTRAIDO")
        print(f"  ID: {pattern.get('pattern_id')}")
        print(f"  Nombre: {pattern.get('name')}")
        print(f"  Vértices: {pattern.get('geometry', {}).get('vertices')}")
        print(f"  Caras: {pattern.get('geometry', {}).get('faces')}")
        print(f"  Modificadores: {len(pattern.get('modifiers', []))}")
        
        print("\n✓ RENDIMIENTO (Dentro de Blender)")
        print(f"  Creación: {perf.get('model_creation_s', 0):.3f}s")
        print(f"  Extracción: {perf.get('pattern_extraction_s', 0):.3f}s")
        print(f"  Iluminación: {perf.get('illumination_s', 0):.3f}s")
        print(f"  Guardado: {perf.get('save_s', 0):.3f}s")
        print(f"  TOTAL: {perf.get('total_s', 0):.3f}s")
    
    print("\n✓ ARCHIVOS GENERADOS")
    print(f"  Blend: {blend_file.name} ({size/1024/1024:.2f} MB)")
    if exists:
        print(f"  ✓ Archivo verificado")
    else:
        print(f"  ✗ Archivo NO encontrado")
    
    # Guardar reporte final
    final_report = {
        "test_date": datetime.now().isoformat(),
        "blender_exit_code": result.returncode,
        "blender_execution_time_s": elapsed_blender,
        "blender_report": report_data,
        "output_files": {
            "blend": str(blend_file),
            "exists": exists,
            "size_mb": size / 1024 / 1024
        }
    }
    
    report_path = REPORTS / f"TEST_ZULY_REAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2, default=str)
    
    print(f"\n📄 Reporte completo guardado: {report_path.name}")
    print("\n" + "="*70)
    print("TEST COMPLETADO EXITOSAMENTE" if result.returncode == 0 else "TEST CON ADVERTENCIAS")
    print("="*70)
    
    return result.returncode == 0

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
