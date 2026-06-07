#!/usr/bin/env python3
"""
ZULY - Generador procedimental de modelos arquitectónicos
Crea geometría detallada directamente con bpy (sin depender de archimesh operators)
"""
import subprocess
import sys
from pathlib import Path

BASE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")
OUTPUT_DIR = BASE / "archivo_zuly" / "temp_arena" / "zuly_generados"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BLENDER = BASE / "blender" / "v3" / "blender-3.6.0-zuly" / "blender.exe"

# Script que se ejecuta dentro de Blender
BLENDER_SCRIPT = r'''
import bpy
import math
from pathlib import Path

OUTPUT_DIR = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\temp_arena\zuly_generados")

def limpiar():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for mesh in bpy.data.meshes:
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)

def setup_camara_luces():
    # Cámara
    cam = bpy.data.cameras.new("Camera")
    cam_obj = bpy.data.objects.new("Camera", cam)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.location = (8, -8, 5)
    cam_obj.rotation_euler = (1.1, 0, 0.785)
    
    # Sol
    sun = bpy.data.lights.new("Sun", type="SUN")
    sun_obj = bpy.data.objects.new("Sun", sun)
    bpy.context.scene.collection.objects.link(sun_obj)
    sun_obj.location = (5, 5, 10)
    sun_obj.rotation_euler = (0.785, 0, 0.785)
    sun.energy = 5.0
    
    # Area
    area = bpy.data.lights.new("Fill", type="AREA")
    area_obj = bpy.data.objects.new("Fill", area)
    bpy.context.scene.collection.objects.link(area_obj)
    area_obj.location = (-5, 3, 4)
    area.energy = 2.0
    area.size = 5

def crear_material(nombre, color, metal=0.0, rough=0.5):
    mat = bpy.data.materials.new(name=nombre)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = metal
    bsdf.inputs['Roughness'].default_value = rough
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def crear_puerta_detallada(nombre, width=0.9, height=2.1, location=(0,0,0), rotation=0):
    """Crea puerta con marco, hoja y picaporte"""
    # Marco
    bpy.ops.mesh.primitive_cube_add(location=location)
    marco = bpy.context.active_object
    marco.scale = (width/2 + 0.05, 0.05, height/2 + 0.05)
    marco.name = f"{nombre}_Marco"
    
    # Hoja
    bpy.ops.mesh.primitive_cube_add(location=(location[0], location[1]+0.02, location[2]+height/2))
    hoja = bpy.context.active_object
    hoja.scale = (width/2 - 0.02, 0.02, height/2 - 0.02)
    hoja.name = f"{nombre}_Hoja"
    
    # Picaporte
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.06, location=(location[0]+width/3, location[1]+0.05, location[2]+height/2))
    pica = bpy.context.active_object
    pica.rotation_euler[0] = 1.5708
    pica.name = f"{nombre}_Pica"
    
    # Rotar todo
    if rotation != 0:
        marco.rotation_euler[2] = math.radians(rotation)
        hoja.rotation_euler[2] = math.radians(rotation)
        pica.rotation_euler[2] = math.radians(rotation)
    
    return hoja

def crear_ventana_detallada(nombre, width=1.2, height=1.0, location=(0,0,0), rotation=0):
    """Crea ventana con marco, vidrio y cruces"""
    # Marco
    bpy.ops.mesh.primitive_cube_add(location=location)
    marco = bpy.context.active_object
    marco.scale = (width/2 + 0.03, 0.03, height/2 + 0.03)
    marco.name = f"{nombre}_Marco"
    
    # Vidrio
    bpy.ops.mesh.primitive_cube_add(location=location)
    vidrio = bpy.context.active_object
    vidrio.scale = (width/2 - 0.01, 0.01, height/2 - 0.01)
    vidrio.name = f"{nombre}_Vidrio"
    
    # Cruces
    bpy.ops.mesh.primitive_cube_add(location=location)
    cruz_h = bpy.context.active_object
    cruz_h.scale = (width/2, 0.015, 0.02)
    cruz_h.name = f"{nombre}_CruzH"
    
    bpy.ops.mesh.primitive_cube_add(location=location)
    cruz_v = bpy.context.active_object
    cruz_v.scale = (0.02, 0.015, height/2)
    cruz_v.name = f"{nombre}_CruzV"
    
    if rotation != 0:
        for obj in [marco, vidrio, cruz_h, cruz_v]:
            obj.rotation_euler[2] = math.radians(rotation)
    
    return vidrio

def crear_columna_detallada(nombre, radius=0.15, height=3.0, location=(0,0,0)):
    """Crea columna con base, fuste y capitel"""
    # Base
    bpy.ops.mesh.primitive_cylinder_add(radius=radius*1.3, depth=0.15, location=(location[0], location[1], location[2]))
    base = bpy.context.active_object
    base.name = f"{nombre}_Base"
    
    # Fuste
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height-0.3, location=(location[0], location[1], location[2]+height/2))
    fuste = bpy.context.active_object
    fuste.name = f"{nombre}_Fuste"
    
    # Capitel
    bpy.ops.mesh.primitive_cylinder_add(radius=radius*1.4, depth=0.15, location=(location[0], location[1], location[2]+height-0.075))
    capitel = bpy.context.active_object
    capitel.name = f"{nombre}_Capitel"
    
    return fuste

def crear_escalera_detallada(nombre, steps=12, width=1.0, total_height=3.0, location=(0,0,0)):
    """Crea escalera con pasos y barandilla"""
    depth = 0.25
    step_height = total_height / steps
    
    for i in range(steps):
        bpy.ops.mesh.primitive_cube_add(location=(
            location[0], 
            location[1] + i * depth, 
            location[2] + i * step_height + step_height/2
        ))
        step = bpy.context.active_object
        step.scale = (width/2, depth/2, step_height/2)
        step.name = f"{nombre}_Step_{i+1}"
    
    # Barandillas
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=total_height+0.5, location=(location[0]-width/2, location[1], location[2]+total_height/2))
    bar1 = bpy.context.active_object
    bar1.name = f"{nombre}_Barandilla_L"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=total_height+0.5, location=(location[0]+width/2, location[1]+(steps-1)*depth, location[2]+total_height/2))
    bar2 = bpy.context.active_object
    bar2.name = f"{nombre}_Barandilla_R"
    
    # Pasamanos
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=steps*depth, location=(location[0], location[1]+(steps-1)*depth/2, location[2]+total_height+0.25))
    pasamanos = bpy.context.active_object
    pasamanos.rotation_euler[1] = 1.5708
    pasamanos.name = f"{nombre}_Pasamanos"
    
    return step

# ============ MODELOS ============

def generar_mod001():
    """MOD-001: Pabellón de Cristal Zen"""
    limpiar()
    setup_camara_luces()
    
    mats = {
        "concreto": crear_material("Concreto", (0.7, 0.7, 0.7)),
        "vidrio": crear_material("Vidrio", (0.85, 0.92, 0.95), rough=0.1),
        "madera": crear_material("Madera", (0.6, 0.4, 0.2))
    }
    
    # Base
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.1))
    base = bpy.context.active_object
    base.scale = (4, 3, 0.1)
    base.data.materials.append(mats["concreto"])
    
    # 4 columnas de cristal
    for x, y in [(-3.5, -2.5), (3.5, -2.5), (-3.5, 2.5), (3.5, 2.5)]:
        col = crear_columna_detallada(f"Col_{x}_{y}", 0.12, 2.8, (x, y, 0.2))
        col.data.materials.append(mats["vidrio"])
    
    # Techo de cristal
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 3.0))
    techo = bpy.context.active_object
    techo.scale = (4, 3, 0.05)
    techo.data.materials.append(mats["vidrio"])
    
    # 2 ventanas frontales
    for x in [-2, 2]:
        vent = crear_ventana_detallada(f"Vent_{x}", 1.5, 1.2, (x, -3, 1.5))
        vent.data.materials.append(mats["vidrio"])
    
    # Puerta
    puerta = crear_puerta_detallada("Puerta", 1.2, 2.2, (0, 3, 0), 180)
    puerta.data.materials.append(mats["madera"])
    
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_DIR / "MOD-001_Pabellon_Cristal_Zen.blend"))
    print("✅ MOD-001_Pabellon_Cristal_Zen")

def generar_mod002():
    """MOD-002: Torre Helix Corporativa"""
    limpiar()
    setup_camara_luces()
    
    mats = {
        "acero": crear_material("Acero", (0.75, 0.78, 0.82), metal=0.3),
        "vidrio": crear_material("Vidrio", (0.7, 0.85, 0.95), rough=0.1)
    }
    
    # 3 pisos
    for floor in range(3):
        z = floor * 3.5
        
        # Piso
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, z))
        piso = bpy.context.active_object
        piso.scale = (3, 3, 0.1)
        piso.data.materials.append(mats["acero"])
        
        # 4 ventanas por piso
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            x = math.cos(rad) * 2.9
            y = math.sin(rad) * 2.9
            vent = crear_ventana_detallada(f"Vent_P{floor}_{angle}", 1.5, 1.0, (x, y, z + 1.5), angle)
            vent.data.materials.append(mats["vidrio"])
    
    # Escalera central
    crear_escalera_detallada("Escalera", 12, 1.2, 10.5, (1.5, 0, 0))
    
    # Puerta entrada
    puerta = crear_puerta_detallada("Puerta", 1.2, 2.2, (0, -3, 0))
    puerta.data.materials.append(mats["acero"])
    
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_DIR / "MOD-002_Torre_Helix_Corporativa.blend"))
    print("✅ MOD-002_Torre_Helix_Corporativa")

def generar_mod003():
    """MOD-003: Casa Nómada Modular"""
    limpiar()
    setup_camara_luces()
    
    mats = {
        "contenedor": crear_material("Contenedor", (0.4, 0.45, 0.5), metal=0.4),
        "vidrio": crear_material("Vidrio", (0.8, 0.9, 1.0), rough=0.1)
    }
    
    # Contenedor principal
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1.25))
    casa = bpy.context.active_object
    casa.scale = (4, 3, 1.25)
    casa.data.materials.append(mats["contenedor"])
    
    # 3 ventanas
    for x, y, rot in [(-3.9, 0, 90), (3.9, 0, -90), (0, 3, 180)]:
        vent = crear_ventana_detallada(f"Vent_{x}", 1.5, 1.0, (x, y, 1.5), rot)
        vent.data.materials.append(mats["vidrio"])
    
    # Puerta
    puerta = crear_puerta_detallada("Puerta", 1.0, 2.0, (0, -3, 0))
    puerta.data.materials.append(mats["contenedor"])
    
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_DIR / "MOD-003_Casa_Nomada_Modular.blend"))
    print("✅ MOD-003_Casa_Nomada_Modular")

def generar_mod004():
    """MOD-004: Galería Lumínica"""
    limpiar()
    setup_camara_luces()
    
    mats = {
        "marmol": crear_material("Marmol", (0.95, 0.95, 0.97), rough=0.2),
        "piedra": crear_material("Piedra", (0.3, 0.3, 0.32)),
        "vidrio": crear_material("Vidrio_Azul", (0.75, 0.85, 0.95), rough=0.05)
    }
    
    # Suelo
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.05))
    suelo = bpy.context.active_object
    suelo.scale = (10, 8, 0.05)
    suelo.data.materials.append(mats["marmol"])
    
    # 10 columnas monumentales
    for x in [-7, -3.5, 0, 3.5, 7]:
        for y in [-7, 7]:
            col = crear_columna_detallada(f"Col_{x}_{y}", 0.4, 4.0, (x, y, 0.1))
            col.data.materials.append(mats["piedra"])
    
    # 3 grandes ventanales
    for x in [-4, 0, 4]:
        vent = crear_ventana_detallada(f"Ventanal_{x}", 2.5, 2.5, (x, -7.9, 2))
        vent.data.materials.append(mats["vidrio"])
    
    # Puerta monumental
    puerta = crear_puerta_detallada("Puerta", 2.0, 3.0, (0, -8, 0))
    puerta.data.materials.append(mats["piedra"])
    
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_DIR / "MOD-004_Galeria_Luminica.blend"))
    print("✅ MOD-004_Galeria_Luminica")

def generar_mod005():
    """MOD-005: Orbitals Habitat Alpha"""
    limpiar()
    setup_camara_luces()
    
    mats = {
        "titanio": crear_material("Titanio", (0.6, 0.62, 0.65), metal=0.6),
        "vidrio": crear_material("Visor", (0.6, 0.85, 0.95), rough=0.1)
    }
    
    # Módulo central
    bpy.ops.mesh.primitive_cylinder_add(radius=2.5, depth=6, location=(0, 0, 2.5))
    central = bpy.context.active_object
    central.rotation_euler[0] = 1.5708
    central.data.materials.append(mats["titanio"])
    
    # 4 módulos laterales
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        x, y = math.cos(rad) * 6, math.sin(rad) * 6
        
        bpy.ops.mesh.primitive_cylinder_add(radius=1.8, depth=4, location=(x, y, 2.5))
        mod = bpy.context.active_object
        mod.rotation_euler[0] = 1.5708
        mod.rotation_euler[2] = rad
        mod.data.materials.append(mats["titanio"])
        
        # Visor
        vent = crear_ventana_detallada(f"Visor_{angle}", 1.0, 0.7, (x*1.3, y*1.3, 2.5), angle)
        vent.data.materials.append(mats["vidrio"])
    
    # 2 Puertas
    for y in [-2.6, 2.6]:
        puerta = crear_puerta_detallada(f"Puerta_{y}", 1.0, 1.8, (0, y, 0.9))
        puerta.data.materials.append(mats["titanio"])
    
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_DIR / "MOD-005_Orbitals_Habitat_Alpha.blend"))
    print("✅ MOD-005_Orbitals_Habitat_Alpha")

# ============ EJECUCIÓN ============
print("=" * 70)
print("ZULY - GENERANDO 5 MODELOS PROCEDIMENTALES")
print("=" * 70)

generar_mod001()
generar_mod002()
generar_mod003()
generar_mod004()
generar_mod005()

print("\n" + "=" * 70)
print(f"✅ 5 MODELOS GENERADOS EN: {OUTPUT_DIR}")
print("=" * 70)
'''

# Guardar script temporal
script_path = BASE / "_temp_zuly_script.py"
with open(script_path, "w", encoding="utf-8") as f:
    f.write(BLENDER_SCRIPT)

print("=" * 70)
print("ZULY - EJECUTANDO GENERADOR EN BLENDER")
print("=" * 70)
print(f"Script: {script_path}")
print(f"Output: {OUTPUT_DIR}")
print("=" * 70)

# Ejecutar con Blender
cmd = [str(BLENDER), "--background", "--python", str(script_path)]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    # Mostrar salida
    if result.stdout:
        lines = result.stdout.strip().split('\n')
        for line in lines[-50:]:  # Últimas 50 líneas
            if '✅' in line or '═' in line or 'ZULY' in line or 'MOD-' in line:
                print(line)
    
    if result.stderr and 'TBBmalloc' not in result.stderr:
        print(f"\n⚠️  Errores: {result.stderr[:500]}")
    
    # Verificar archivos creados
    archivos = list(OUTPUT_DIR.glob("MOD-*.blend"))
    print(f"\n📁 Archivos generados: {len(archivos)}")
    for f in sorted(archivos):
        size = f.stat().st_size / 1024
        print(f"   {f.name} ({size:.1f} KB)")
    
    if len(archivos) == 5:
        print("\n🎉 ¡Todos los modelos generados exitosamente!")
    else:
        print(f"\n⚠️  Se generaron {len(archivos)}/5 modelos")
        
except Exception as e:
    print(f"\n❌ Error: {e}")

finally:
    # Limpiar script temporal
    if script_path.exists():
        script_path.unlink()
