# test_render_cubo.py
"""
Script para probar las mejoras con Blender y generar un render de un cubo.
"""

import bpy
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

print("="*70)
print("PRUEBA CON BLENDER REAL - CREAR Y RENDERIZAR CUBO")
print("="*70)

# Limpiar escena
print("\n[1] Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Importar mejoras
print("\n[2] Importando mejoras de ZULY...")
try:
    from core.utils.validators import validate_location, validate_scale
    from core.utils.exceptions import ValidationError
    print("✓ Validadores importados")
    print("✓ Excepciones importadas")
except Exception as e:
    print(f"❌ Error importando: {e}")
    sys.exit(1)

# Validar parámetros
print("\n[3] Validando parámetros...")
try:
    ubicacion = validate_location([0, 0, 0])
    escala = validate_scale(2.0)
    print(f"✓ Ubicación validada: {ubicacion}")
    print(f"✓ Escala validada: {escala}")
except ValidationError as e:
    print(f"❌ Error de validación: {e.message}")
    sys.exit(1)

# Crear cubo
print("\n[4] Creando cubo...")
bpy.ops.mesh.primitive_cube_add(location=ubicacion)
cubo = bpy.context.active_object
cubo.scale = (escala, escala, escala)
cubo.name = "Cubo_Mejorado"
print(f"✓ Cubo creado: {cubo.name}")
print(f"  Ubicación: {cubo.location}")
print(f"  Escala: {cubo.scale}")

# Agregar material
print("\n[5] Agregando material dorado...")
material = bpy.data.materials.new(name="Oro")
material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)  # Color oro
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.2

cubo.data.materials.append(material)
print("✓ Material oro aplicado")

# Agregar luz
print("\n[6] Agregando iluminación...")
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
luz = bpy.context.active_object
luz.data.energy = 3.0
print(f"✓ Luz agregada: {luz.name}")

# Configurar cámara
print("\n[7] Configurando cámara...")
bpy.ops.object.camera_add(location=(7, -7, 5))
camara = bpy.context.active_object
camara.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = camara
print(f"✓ Cámara configurada: {camara.name}")

# Configurar render
print("\n[8] Configurando render...")
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.image_settings.file_format = 'PNG'

# Definir ruta de salida
output_dir = project_dir / "export"
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "cubo_render.png"
scene.render.filepath = str(output_path)

print(f"✓ Motor: {scene.render.engine}")
print(f"✓ Samples: {scene.cycles.samples}")
print(f"✓ Resolución: {scene.render.resolution_x}x{scene.render.resolution_y}")
print(f"✓ Salida: {output_path}")

# Renderizar
print("\n[9] Renderizando...")
print("⏳ Esto puede tomar unos segundos...")
bpy.ops.render.render(write_still=True)
print(f"✓ Render completado!")
print(f"✓ Imagen guardada en: {output_path}")

# Guardar archivo .blend
blend_path = output_dir / "cubo_mejorado.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
print(f"✓ Archivo Blender guardado: {blend_path}")

# Resumen
print("\n" + "="*70)
print("RESUMEN DE PRUEBA")
print("="*70)
print(f"✅ Validadores funcionando correctamente")
print(f"✅ Cubo creado con parámetros validados")
print(f"✅ Material oro aplicado")
print(f"✅ Iluminación configurada")
print(f"✅ Render generado exitosamente")
print(f"\nArchivos generados:")
print(f"  • Render: {output_path}")
print(f"  • Blender: {blend_path}")
print("="*70)
