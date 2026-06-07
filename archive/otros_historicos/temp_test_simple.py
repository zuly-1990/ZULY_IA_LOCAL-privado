
import bpy
import json
import time
from datetime import datetime

start_total = time.time()

print("\n" + "="*70)
print("ZULY TEST REAL - EXTRACCION DE PATRONES")
print("="*70)

# FASE 1: Limpiar
print("\n[FASE 1] Limpiando escena...")
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

blend_path = "c:/Users/Admin/Desktop/ZULY_IA_LOCAL/archivo_zuly/temp_arena/ZULY_TEST_REAL.blend"
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

print("\n" + "="*70)
print("RESULTADOS FINALES")
print("="*70)
print(f"Modelo: {pattern['name']}")
print(f"Vértices: {geometry_info['vertices']}")
print(f"Caras: {geometry_info['faces']}")
print(f"Modificadores: {len(modifier_info)}")
print(f"Tiempo Total: {elapsed_total:.3f}s")

# SALIDA PARA HOST
print("\n[REPORT_START]")
print(json.dumps(report, indent=2, default=str))
print("[REPORT_END]")
