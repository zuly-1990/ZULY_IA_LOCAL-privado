"""
blender_real_tests_18_5.py
Script de pruebas reales para ejecutar DENTRO de Blender.
Fase 18.5: Verificación de precisión dimensional.

MODO: DESCARTE - Solo validar, no modificar nada.
"""

import bpy
import sys
import os
from datetime import datetime

# Agregar path de ZULY al sys.path
ZULY_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
if ZULY_PATH not in sys.path:
    sys.path.insert(0, ZULY_PATH)

# Importar módulos de ZULY
from core.utils.units import parse_dimension, to_meters


# ============================================================================
# UTILIDADES DE PRUEBA
# ============================================================================

def clear_scene():
    """Limpia la escena completamente."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def get_object_real_dimensions(obj_name):
    """Obtiene las dimensiones reales de un objeto."""
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return None
    return {
        'name': obj.name,
        'dimensions': list(obj.dimensions),
        'scale': list(obj.scale),
        'location': list(obj.location),
        'custom_props': {k: obj.get(k) for k in obj.keys() if k.startswith('zuly')}
    }

def log_result(test_name, mock_result, blender_result, observations=""):
    """Registra resultado de prueba."""
    return f"""
## PRUEBA: {test_name}
- **MockAdapter:** {mock_result}
- **Blender real:** {blender_result}
- **Observaciones:** {observations if observations else "—"}
"""


# ============================================================================
# PRUEBAS
# ============================================================================

results = []
results.append(f"# Verificación Blender Real - Fase 18.5\n")
results.append(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
results.append(f"**Blender version:** {bpy.app.version_string}\n")
results.append("---\n")


# ---------------------------------------------------------------------------
# PRUEBA 1: Cilindro 20mm diámetro, 50mm altura
# ---------------------------------------------------------------------------
print("\n=== PRUEBA 1: Cilindro 20mm x 50mm ===")
clear_scene()

try:
    # Parsear dimensiones (como lo haría ZULY)
    diameter_val, diameter_unit = parse_dimension("20mm")
    height_val, height_unit = parse_dimension("50mm")
    
    diameter_m = to_meters(diameter_val, diameter_unit)  # 0.02m
    height_m = to_meters(height_val, height_unit)  # 0.05m
    radius_m = diameter_m / 2  # 0.01m
    
    # Crear cilindro en Blender
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius_m,
        depth=height_m,
        location=(0, 0, height_m/2)
    )
    
    obj = bpy.context.active_object
    obj.name = "Cylinder_20mm_50mm"
    
    # Agregar custom properties (como lo haría ZULY)
    obj["zuly_intended_diameter"] = "20mm"
    obj["zuly_intended_height"] = "50mm"
    obj["zuly_intended_value"] = 20.0
    obj["zuly_intended_unit"] = "mm"
    
    # Verificar
    dims = obj.dimensions
    expected_diameter = 0.02  # 20mm en metros
    expected_height = 0.05  # 50mm en metros
    
    # Blender reporta dimensions como [diámetro_x, diámetro_y, altura]
    diameter_ok = abs(dims[0] - expected_diameter) < 0.0001
    height_ok = abs(dims[2] - expected_height) < 0.0001
    props_ok = obj.get("zuly_intended_unit") == "mm"
    
    if diameter_ok and height_ok and props_ok:
        result = "OK"
        obs = f"Dims: {dims[0]*1000:.1f}mm x {dims[2]*1000:.1f}mm, Props: ✓"
    else:
        result = "FAIL"
        obs = f"Dims: {dims[0]*1000:.1f}mm x {dims[2]*1000:.1f}mm (esperado 20x50)"
    
    results.append(log_result("Cilindro 20mm x 50mm", "OK", result, obs))
    print(f"Resultado: {result} - {obs}")

except Exception as e:
    results.append(log_result("Cilindro 20mm x 50mm", "OK", "FAIL", str(e)))
    print(f"ERROR: {e}")


# ---------------------------------------------------------------------------
# PRUEBA 2: Cubo 40cm
# ---------------------------------------------------------------------------
print("\n=== PRUEBA 2: Cubo 40cm ===")
clear_scene()

try:
    size_val, size_unit = parse_dimension("40cm")
    size_m = to_meters(size_val, size_unit)  # 0.4m
    
    bpy.ops.mesh.primitive_cube_add(size=size_m, location=(0, 0, size_m/2))
    
    obj = bpy.context.active_object
    obj.name = "Cube_40cm"
    obj["zuly_intended_value"] = 40.0
    obj["zuly_intended_unit"] = "cm"
    
    dims = obj.dimensions
    expected = 0.4  # 40cm en metros
    
    all_dims_ok = all(abs(d - expected) < 0.0001 for d in dims)
    props_ok = obj.get("zuly_intended_unit") == "cm"
    
    if all_dims_ok and props_ok:
        result = "OK"
        obs = f"Dims: {dims[0]*100:.1f}cm x {dims[1]*100:.1f}cm x {dims[2]*100:.1f}cm"
    else:
        result = "FAIL"
        obs = f"Dims: {dims[0]*100:.1f}cm (esperado 40cm)"
    
    results.append(log_result("Cubo 40cm", "OK", result, obs))
    print(f"Resultado: {result} - {obs}")

except Exception as e:
    results.append(log_result("Cubo 40cm", "OK", "FAIL", str(e)))
    print(f"ERROR: {e}")


# ---------------------------------------------------------------------------
# PRUEBA 3: Cilindro 10mm escalado al doble
# ---------------------------------------------------------------------------
print("\n=== PRUEBA 3: Cilindro 10mm escalado x2 ===")
clear_scene()

try:
    size_val, size_unit = parse_dimension("10mm")
    size_m = to_meters(size_val, size_unit)  # 0.01m
    
    bpy.ops.mesh.primitive_cylinder_add(radius=size_m/2, depth=size_m, location=(0, 0, 0))
    
    obj = bpy.context.active_object
    obj.name = "Cylinder_10mm_scaled"
    obj["zuly_intended_value"] = 10.0
    obj["zuly_intended_unit"] = "mm"
    obj["zuly_original_scale"] = 1.0
    
    # Escalar al doble
    obj.scale = (2, 2, 2)
    
    # Las dimensiones en Blender se actualizan automáticamente
    dims = obj.dimensions
    expected = 0.02  # 10mm * 2 = 20mm = 0.02m
    
    # Verificar que la intención original se preserva
    original_preserved = obj.get("zuly_intended_value") == 10.0
    scale_correct = abs(dims[0] - expected) < 0.0001
    
    if scale_correct and original_preserved:
        result = "OK"
        obs = f"Dims finales: {dims[0]*1000:.1f}mm, Original preservado: 10mm"
    else:
        result = "FAIL"
        obs = f"Dims: {dims[0]*1000:.1f}mm, Original: {obj.get('zuly_intended_value')}"
    
    results.append(log_result("Cilindro 10mm escalado x2", "OK", result, obs))
    print(f"Resultado: {result} - {obs}")

except Exception as e:
    results.append(log_result("Cilindro 10mm escalado x2", "OK", "FAIL", str(e)))
    print(f"ERROR: {e}")


# ---------------------------------------------------------------------------
# PRUEBA 4: Parent/Child
# ---------------------------------------------------------------------------
print("\n=== PRUEBA 4: Parent/Child (30mm → 60mm) ===")
clear_scene()

try:
    # Cubo padre 60mm
    size_parent = to_meters(60, "mm")
    bpy.ops.mesh.primitive_cube_add(size=size_parent, location=(0, 0, 0))
    parent_obj = bpy.context.active_object
    parent_obj.name = "Parent_60mm"
    parent_obj["zuly_intended_value"] = 60.0
    parent_obj["zuly_intended_unit"] = "mm"
    
    # Cubo hijo 30mm
    size_child = to_meters(30, "mm")
    bpy.ops.mesh.primitive_cube_add(size=size_child, location=(0.1, 0, 0))
    child_obj = bpy.context.active_object
    child_obj.name = "Child_30mm"
    child_obj["zuly_intended_value"] = 30.0
    child_obj["zuly_intended_unit"] = "mm"
    
    # Establecer parent
    child_obj.parent = parent_obj
    
    # Verificar
    hierarchy_ok = child_obj.parent == parent_obj
    parent_dims_ok = abs(parent_obj.dimensions[0] - 0.06) < 0.0001
    child_dims_ok = abs(child_obj.dimensions[0] - 0.03) < 0.0001
    
    if hierarchy_ok and parent_dims_ok and child_dims_ok:
        result = "OK"
        obs = f"Jerarquía correcta, Parent: {parent_obj.dimensions[0]*1000:.1f}mm, Child: {child_obj.dimensions[0]*1000:.1f}mm"
    else:
        result = "FAIL"
        obs = f"Hierarchy: {hierarchy_ok}, Dims: P={parent_obj.dimensions[0]*1000:.1f}mm C={child_obj.dimensions[0]*1000:.1f}mm"
    
    results.append(log_result("Parent/Child 30mm → 60mm", "OK", result, obs))
    print(f"Resultado: {result} - {obs}")

except Exception as e:
    results.append(log_result("Parent/Child 30mm → 60mm", "OK", "FAIL", str(e)))
    print(f"ERROR: {e}")


# ---------------------------------------------------------------------------
# PRUEBA 5: Exportación STL
# ---------------------------------------------------------------------------
print("\n=== PRUEBA 5: Exportación STL ===")
clear_scene()

try:
    # Crear objeto simple
    size_m = to_meters(25, "mm")
    bpy.ops.mesh.primitive_cube_add(size=size_m, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = "Export_Test_25mm"
    
    # Seleccionar objeto
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # Exportar a STL
    export_path = os.path.join(ZULY_PATH, "logs", "test_export_25mm.stl")
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    
    bpy.ops.export_mesh.stl(
        filepath=export_path,
        use_selection=True,
        global_scale=1.0
    )
    
    # Verificar que se creó el archivo
    file_exists = os.path.exists(export_path)
    file_size = os.path.getsize(export_path) if file_exists else 0
    
    if file_exists and file_size > 0:
        result = "OK"
        obs = f"Archivo creado: {file_size} bytes, Path: {export_path}"
    else:
        result = "FAIL"
        obs = f"Archivo no creado o vacío"
    
    results.append(log_result("Exportación STL 25mm", "OK", result, obs))
    print(f"Resultado: {result} - {obs}")

except Exception as e:
    results.append(log_result("Exportación STL 25mm", "OK", "FAIL", str(e)))
    print(f"ERROR: {e}")


# ============================================================================
# GUARDAR RESULTADOS
# ============================================================================

results.append("\n---\n")
results.append("## RESUMEN\n")

# Contar resultados
ok_count = sum(1 for r in results if "Blender real:** OK" in r)
fail_count = sum(1 for r in results if "Blender real:** FAIL" in r)

results.append(f"- **OK:** {ok_count}/5\n")
results.append(f"- **FAIL:** {fail_count}/5\n")

if ok_count >= 4:
    results.append("\n✅ **CRITERIO DE ÉXITO CUMPLIDO** (≥4/5 OK)\n")
    results.append("👉 Fase 18.5 VALIDADA EN MUNDO REAL\n")
else:
    results.append("\n❌ **CRITERIO DE ÉXITO NO CUMPLIDO**\n")
    results.append("⚠️ Revisar fallos antes de continuar\n")

# Guardar archivo de log
log_path = os.path.join(ZULY_PATH, "logs", "blender_real_verification_18_5.md")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

with open(log_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print(f"\n✅ Resultados guardados en: {log_path}")
print(f"Total: {ok_count}/5 OK")
