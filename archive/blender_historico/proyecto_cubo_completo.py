"""
proyecto_cubo_completo.py

PROYECTO: EXPLORACIÓN COMPLETA DEL CUBO PRIMITIVO
==================================================

Este script explora TODAS las variaciones posibles del cubo en Blender:
- Diferentes posiciones
- Diferentes escalas
- Diferentes rotaciones
- Diferentes materiales
- Combinaciones de transformaciones
- Renders profesionales de cada variación

Ejecutar en Blender:
1. Abrir Blender 3.6
2. Ir a Scripting
3. Copiar este código
4. Ejecutar con Alt+P
"""

import sys
from pathlib import Path
import math

# Agregar ZULY al path
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy
from lyzu_core import LYZUCore

# ============================================================================
# CONFIGURACIÓN DEL PROYECTO
# ============================================================================

PROJECT_NAME = "Cubo_Exploracion_Completa"
OUTPUT_DIR = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/cubos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RENDER_RESOLUTION = (1920, 1080)
RENDER_SAMPLES = 32
RENDER_ENGINE = 'CYCLES'

print("=" * 80)
print(f"PROYECTO: {PROJECT_NAME}")
print("=" * 80)
print(f"Directorio de salida: {OUTPUT_DIR}")
print(f"Resolución: {RENDER_RESOLUTION[0]}x{RENDER_RESOLUTION[1]}")
print(f"Samples: {RENDER_SAMPLES}")
print("=" * 80)

# ============================================================================
# INICIALIZAR LYZU
# ============================================================================

print("\n[1/10] Inicializando LYZU Core...")
lyzu = LYZUCore(mode='reactive')
print("✅ LYZU inicializado")

# ============================================================================
# LIMPIAR ESCENA
# ============================================================================

print("\n[2/10] Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
print("✅ Escena limpia")

# ============================================================================
# CONFIGURAR ILUMINACIÓN PROFESIONAL (3-POINT LIGHTING)
# ============================================================================

print("\n[3/10] Configurando iluminación profesional...")

# Key Light (Luz principal)
bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
key_light = bpy.context.active_object
key_light.name = "Key_Light"
key_light.data.energy = 500
key_light.data.size = 3
key_light.rotation_euler = (math.radians(45), 0, math.radians(45))
print("  ✓ Key Light creada")

# Fill Light (Luz de relleno)
bpy.ops.object.light_add(type='AREA', location=(-5, -3, 5))
fill_light = bpy.context.active_object
fill_light.name = "Fill_Light"
fill_light.data.energy = 200
fill_light.data.size = 2
fill_light.rotation_euler = (math.radians(60), 0, math.radians(-45))
print("  ✓ Fill Light creada")

# Back Light (Luz trasera/rim)
bpy.ops.object.light_add(type='SPOT', location=(0, 5, 6))
back_light = bpy.context.active_object
back_light.name = "Back_Light"
back_light.data.energy = 300
back_light.data.spot_size = math.radians(60)
back_light.rotation_euler = (math.radians(135), 0, 0)
print("  ✓ Back Light creada")

print("✅ Iluminación profesional configurada (3-point lighting)")

# ============================================================================
# CONFIGURAR CÁMARA
# ============================================================================

print("\n[4/10] Configurando cámara...")
bpy.ops.object.camera_add(location=(8, -8, 6))
camera = bpy.context.active_object
camera.name = "Camera_Main"
camera.rotation_euler = (math.radians(63), 0, math.radians(45))
camera.data.lens = 50
bpy.context.scene.camera = camera
print("✅ Cámara configurada")

# ============================================================================
# CONFIGURAR RENDER
# ============================================================================

print("\n[5/10] Configurando motor de render...")
scene = bpy.context.scene
scene.render.engine = RENDER_ENGINE
scene.cycles.samples = RENDER_SAMPLES
scene.render.resolution_x = RENDER_RESOLUTION[0]
scene.render.resolution_y = RENDER_RESOLUTION[1]
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False

# Configurar mundo (fondo)
world = bpy.data.worlds.get("World")
if world:
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value = (0.05, 0.05, 0.05, 1.0)  # Fondo gris oscuro
    bg.inputs[1].default_value = 0.5

print("✅ Motor de render configurado")

# ============================================================================
# DEFINIR MATERIALES
# ============================================================================

print("\n[6/10] Creando materiales...")

def create_material(name, base_color, metallic=0.0, roughness=0.5, emission=0.0):
    """Crea un material PBR personalizado"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Emission Strength'].default_value = emission
    
    return mat

# Crear paleta de materiales
materiales = {
    'oro': create_material('Oro', (1.0, 0.766, 0.336), metallic=1.0, roughness=0.2),
    'plata': create_material('Plata', (0.972, 0.960, 0.915), metallic=1.0, roughness=0.1),
    'cobre': create_material('Cobre', (0.955, 0.637, 0.538), metallic=1.0, roughness=0.3),
    'vidrio': create_material('Vidrio', (0.8, 0.9, 1.0), metallic=0.0, roughness=0.0),
    'plastico_rojo': create_material('Plastico_Rojo', (0.8, 0.1, 0.1), metallic=0.0, roughness=0.3),
    'plastico_azul': create_material('Plastico_Azul', (0.1, 0.3, 0.8), metallic=0.0, roughness=0.3),
    'plastico_verde': create_material('Plastico_Verde', (0.1, 0.8, 0.3), metallic=0.0, roughness=0.3),
    'mate_negro': create_material('Mate_Negro', (0.02, 0.02, 0.02), metallic=0.0, roughness=0.9),
    'mate_blanco': create_material('Mate_Blanco', (0.9, 0.9, 0.9), metallic=0.0, roughness=0.8),
    'emision_azul': create_material('Emision_Azul', (0.2, 0.5, 1.0), metallic=0.0, roughness=0.5, emission=3.0),
}

print(f"✅ {len(materiales)} materiales creados")

# ============================================================================
# DEFINIR VARIACIONES DE CUBO
# ============================================================================

print("\n[7/10] Definiendo variaciones de cubo...")

variaciones = []

# Variación 1: Cubos con diferentes escalas
print("  • Variaciones de escala...")
for i, escala in enumerate([0.5, 1.0, 1.5, 2.0, 2.5]):
    variaciones.append({
        'nombre': f'Cubo_Escala_{escala}',
        'location': (i * 3 - 6, 0, 0),
        'scale': (escala, escala, escala),
        'rotation': (0, 0, 0),
        'material': 'oro'
    })

# Variación 2: Cubos con diferentes rotaciones
print("  • Variaciones de rotación...")
for i, angulo in enumerate([0, 45, 90, 135, 180]):
    variaciones.append({
        'nombre': f'Cubo_Rotacion_{angulo}',
        'location': (i * 3 - 6, 3, 0),
        'scale': (1.5, 1.5, 1.5),
        'rotation': (0, 0, math.radians(angulo)),
        'material': 'plata'
    })

# Variación 3: Cubos con diferentes materiales
print("  • Variaciones de material...")
materiales_lista = ['oro', 'plata', 'cobre', 'plastico_rojo', 'plastico_azul']
for i, mat_name in enumerate(materiales_lista):
    variaciones.append({
        'nombre': f'Cubo_Material_{mat_name}',
        'location': (i * 3 - 6, 6, 0),
        'scale': (1.5, 1.5, 1.5),
        'rotation': (math.radians(30), math.radians(30), 0),
        'material': mat_name
    })

# Variación 4: Cubos con escalas no uniformes
print("  • Variaciones de escala no uniforme...")
escalas_no_uniformes = [
    (2.0, 0.5, 0.5),  # Barra horizontal
    (0.5, 2.0, 0.5),  # Barra vertical
    (0.5, 0.5, 2.0),  # Barra profundidad
    (2.0, 1.0, 0.5),  # Placa
    (1.5, 1.5, 0.3),  # Disco
]
for i, escala in enumerate(escalas_no_uniformes):
    variaciones.append({
        'nombre': f'Cubo_NoUniforme_{i+1}',
        'location': (i * 3 - 6, 9, 0),
        'scale': escala,
        'rotation': (0, 0, 0),
        'material': 'plastico_verde'
    })

# Variación 5: Cubos con rotaciones complejas
print("  • Variaciones de rotación compleja...")
rotaciones_complejas = [
    (45, 0, 0),
    (0, 45, 0),
    (0, 0, 45),
    (45, 45, 0),
    (45, 45, 45),
]
for i, rot in enumerate(rotaciones_complejas):
    variaciones.append({
        'nombre': f'Cubo_RotCompleja_{i+1}',
        'location': (i * 3 - 6, 12, 0),
        'scale': (1.5, 1.5, 1.5),
        'rotation': (math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2])),
        'material': 'cobre'
    })

print(f"✅ {len(variaciones)} variaciones definidas")

# ============================================================================
# CREAR TODOS LOS CUBOS
# ============================================================================

print(f"\n[8/10] Creando {len(variaciones)} cubos...")

cubos_creados = []

for i, var in enumerate(variaciones, 1):
    # Crear cubo
    bpy.ops.mesh.primitive_cube_add(
        location=var['location'],
        scale=var['scale']
    )
    
    cubo = bpy.context.active_object
    cubo.name = var['nombre']
    cubo.rotation_euler = var['rotation']
    
    # Aplicar material
    if var['material'] in materiales:
        cubo.data.materials.clear()
        cubo.data.materials.append(materiales[var['material']])
    
    cubos_creados.append(cubo)
    
    if i % 5 == 0:
        print(f"  ✓ {i}/{len(variaciones)} cubos creados...")

print(f"✅ {len(cubos_creados)} cubos creados exitosamente")

# ============================================================================
# GUARDAR ARCHIVO .BLEND
# ============================================================================

print("\n[9/10] Guardando archivo .blend...")
blend_path = OUTPUT_DIR / f"{PROJECT_NAME}.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
print(f"✅ Archivo guardado: {blend_path}")

# ============================================================================
# RENDERIZAR ESCENA COMPLETA
# ============================================================================

print("\n[10/10] Renderizando escena completa...")
print("⏳ Esto puede tomar varios minutos...")

# Render de vista general
scene.render.filepath = str(OUTPUT_DIR / f"{PROJECT_NAME}_Vista_General.png")
bpy.ops.render.render(write_still=True)
print(f"✅ Render general guardado")

# Opcional: Renderizar cubos individuales (comentado por defecto para ahorrar tiempo)
RENDER_INDIVIDUAL = False  # Cambiar a True para renderizar cada cubo

if RENDER_INDIVIDUAL:
    print("\n[BONUS] Renderizando cubos individuales...")
    
    # Ocultar todos los cubos
    for cubo in cubos_creados:
        cubo.hide_render = True
    
    # Renderizar cada cubo individualmente
    for i, cubo in enumerate(cubos_creados, 1):
        cubo.hide_render = False
        
        # Ajustar cámara para enfocar el cubo
        camera.location = (
            cubo.location.x + 4,
            cubo.location.y - 4,
            cubo.location.z + 3
        )
        
        # Renderizar
        scene.render.filepath = str(OUTPUT_DIR / f"{cubo.name}.png")
        bpy.ops.render.render(write_still=True)
        
        cubo.hide_render = True
        
        if i % 5 == 0:
            print(f"  ✓ {i}/{len(cubos_creados)} renders individuales...")
    
    # Mostrar todos los cubos de nuevo
    for cubo in cubos_creados:
        cubo.hide_render = False
    
    print(f"✅ {len(cubos_creados)} renders individuales completados")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 80)
print("PROYECTO COMPLETADO EXITOSAMENTE")
print("=" * 80)
print(f"\n📊 ESTADÍSTICAS:")
print(f"  • Cubos creados: {len(cubos_creados)}")
print(f"  • Materiales usados: {len(set(v['material'] for v in variaciones))}")
print(f"  • Luces configuradas: 3 (3-point lighting)")
print(f"  • Renders generados: 1 (vista general)")
print(f"\n📁 ARCHIVOS GENERADOS:")
print(f"  • Blender: {blend_path}")
print(f"  • Render: {OUTPUT_DIR / f'{PROJECT_NAME}_Vista_General.png'}")
print(f"\n📂 Directorio de salida: {OUTPUT_DIR}")
print("\n" + "=" * 80)

# ============================================================================
# INFORMACIÓN DE VARIACIONES
# ============================================================================

print("\n📋 VARIACIONES CREADAS:")
print("-" * 80)

categorias = {
    'Escala': [v for v in variaciones if 'Escala' in v['nombre']],
    'Rotación': [v for v in variaciones if 'Rotacion' in v['nombre']],
    'Material': [v for v in variaciones if 'Material' in v['nombre']],
    'Escala No Uniforme': [v for v in variaciones if 'NoUniforme' in v['nombre']],
    'Rotación Compleja': [v for v in variaciones if 'RotCompleja' in v['nombre']],
}

for categoria, vars_cat in categorias.items():
    print(f"\n{categoria}: {len(vars_cat)} variaciones")
    for var in vars_cat:
        print(f"  • {var['nombre']}")

print("\n" + "=" * 80)
print("¡LISTO PARA EXPLORAR! 🎨🚀")
print("=" * 80)
