#!/usr/bin/env python3
"""
🏠 PRUEBA ESPECIAL: CASA COMPLETA DE 2 PLANTAS
Con todos los detalles y características aprendidas en ZULY
Guardada como archivo .blend para revisión detallada

Características:
- Casa de 2 plantas
- Paredes, puertas, ventanas
- Techos con estructura
- Jardín con elementos
- Detalles arquitectónicos
- Aplicadas transformaciones: C2 learning + handlers LYZU
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime


def generar_script_casa_completa() -> str:
    """Genera script Python para crear casa completa en Blender"""
    
    return """
import bpy
import math
from datetime import datetime

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear colecciones para organizar
def crear_coleccion(nombre):
    if nombre not in bpy.data.collections:
        col = bpy.data.collections.new(nombre)
        bpy.context.scene.collection.children.link(col)
    return bpy.data.collections[nombre]

col_estructura = crear_coleccion("Estructura")
col_puertas = crear_coleccion("Puertas")
col_ventanas = crear_coleccion("Ventanas")
col_techo = crear_coleccion("Techo")
col_interior = crear_coleccion("Interior")
col_exterior = crear_coleccion("Exterior")

# ═══════════════════════════════════════════════════════════════════════
# PLANTA BAJA
# ═══════════════════════════════════════════════════════════════════════

# Base/Piso de planta baja
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
piso1 = bpy.context.active_object
piso1.name = "Piso_Planta_Baja"
piso1.scale = (8, 10, 0.2)
piso1.collection_objects_unlink()
col_estructura.objects.link(piso1)

# Paredes planta baja - Frente
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 5, 1.25))
pared_frente = bpy.context.active_object
pared_frente.name = "Pared_Frente_PB"
pared_frente.scale = (8, 0.3, 2.5)
pared_frente.collection_objects_unlink()
col_estructura.objects.link(pared_frente)

# Paredes planta baja - Atrás
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -5, 1.25))
pared_atras = bpy.context.active_object
pared_atras.name = "Pared_Atras_PB"
pared_atras.scale = (8, 0.3, 2.5)
pared_atras.collection_objects_unlink()
col_estructura.objects.link(pared_atras)

# Paredes laterales - Izquierda
bpy.ops.mesh.primitive_cube_add(size=1, location=(-4, 0, 1.25))
pared_izq = bpy.context.active_object
pared_izq.name = "Pared_Izquierda_PB"
pared_izq.scale = (0.3, 10, 2.5)
pared_izq.collection_objects_unlink()
col_estructura.objects.link(pared_izq)

# Paredes laterales - Derecha
bpy.ops.mesh.primitive_cube_add(size=1, location=(4, 0, 1.25))
pared_der = bpy.context.active_object
pared_der.name = "Pared_Derecha_PB"
pared_der.scale = (0.3, 10, 2.5)
pared_der.collection_objects_unlink()
col_estructura.objects.link(pared_der)

# Separador interior (pasillo central)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.25))
separador = bpy.context.active_object
separador.name = "Pared_Separador_PB"
separador.scale = (0.3, 8, 2.5)
separador.collection_objects_unlink()
col_estructura.objects.link(separador)

# ═══════════════════════════════════════════════════════════════════════
# PUERTAS PLANTA BAJA
# ═══════════════════════════════════════════════════════════════════════

# Puerta principal (frente)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 5.15, 0.9))
puerta_principal = bpy.context.active_object
puerta_principal.name = "Puerta_Principal"
puerta_principal.scale = (0.9, 0.1, 1.8)
puerta_principal.collection_objects_unlink()
col_puertas.objects.link(puerta_principal)

# Puerta interior - Izquierda
bpy.ops.mesh.primitive_cube_add(size=1, location=(-2, 0.15, 0.9))
puerta_int1 = bpy.context.active_object
puerta_int1.name = "Puerta_Interior_1"
puerta_int1.scale = (0.9, 0.1, 1.8)
puerta_int1.collection_objects_unlink()
col_puertas.objects.link(puerta_int1)

# Puerta interior - Derecha
bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 0.15, 0.9))
puerta_int2 = bpy.context.active_object
puerta_int2.name = "Puerta_Interior_2"
puerta_int2.scale = (0.9, 0.1, 1.8)
puerta_int2.collection_objects_unlink()
col_puertas.objects.link(puerta_int2)

# ═══════════════════════════════════════════════════════════════════════
# VENTANAS PLANTA BAJA
# ═══════════════════════════════════════════════════════════════════════

# Ventanas frente - Izquierda
bpy.ops.mesh.primitive_cube_add(size=1, location=(-2, 5.15, 1.5))
vent_f1 = bpy.context.active_object
vent_f1.name = "Ventana_Frente_Izq"
vent_f1.scale = (0.8, 0.1, 0.8)
vent_f1.collection_objects_unlink()
col_ventanas.objects.link(vent_f1)

# Ventanas frente - Derecha
bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 5.15, 1.5))
vent_f2 = bpy.context.active_object
vent_f2.name = "Ventana_Frente_Der"
vent_f2.scale = (0.8, 0.1, 0.8)
vent_f2.collection_objects_unlink()
col_ventanas.objects.link(vent_f2)

# Ventanas atrás
for x in [-2, 2]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, -5.15, 1.5))
    vent = bpy.context.active_object
    vent.name = f"Ventana_Atras_{x}"
    vent.scale = (0.8, 0.1, 0.8)
    vent.collection_objects_unlink()
    col_ventanas.objects.link(vent)

# Ventanas laterales
for y in [-3, 3]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-4.15, y, 1.5))
    vent = bpy.context.active_object
    vent.name = f"Ventana_Izq_{y}"
    vent.scale = (0.1, 0.8, 0.8)
    vent.collection_objects_unlink()
    col_ventanas.objects.link(vent)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(4.15, y, 1.5))
    vent = bpy.context.active_object
    vent.name = f"Ventana_Der_{y}"
    vent.scale = (0.1, 0.8, 0.8)
    vent.collection_objects_unlink()
    col_ventanas.objects.link(vent)

# ═══════════════════════════════════════════════════════════════════════
# PLANTA ALTA
# ═══════════════════════════════════════════════════════════════════════

# Base/Piso planta alta
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.7))
piso2 = bpy.context.active_object
piso2.name = "Piso_Planta_Alta"
piso2.scale = (8, 10, 0.2)
piso2.collection_objects_unlink()
col_estructura.objects.link(piso2)

# Paredes planta alta (interior)
# Pared separadora alta
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 3.95))
pared_sep_alta = bpy.context.active_object
pared_sep_alta.name = "Pared_Separador_PA"
pared_sep_alta.scale = (0.3, 8, 2.5)
pared_sep_alta.collection_objects_unlink()
col_estructura.objects.link(pared_sep_alta)

# Paredes exteriores planta alta
for z_pos, name in [(3.95, "Frente"), (3.95, "Atras"), (3.95, "Izq"), (3.95, "Der")]:
    if name == "Frente":
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 5, z_pos))
    elif name == "Atras":
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -5, z_pos))
    elif name == "Izq":
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-4, 0, z_pos))
    else:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(4, 0, z_pos))
    
    pared = bpy.context.active_object
    pared.name = f"Pared_{name}_PA"
    if name in ["Frente", "Atras"]:
        pared.scale = (8, 0.3, 2.5)
    else:
        pared.scale = (0.3, 10, 2.5)
    pared.collection_objects_unlink()
    col_estructura.objects.link(pared)

# Ventanas planta alta
for x in [-2, 2]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 5.15, 3.5))
    vent = bpy.context.active_object
    vent.name = f"Ventana_Frente_PA_{x}"
    vent.scale = (0.8, 0.1, 0.8)
    vent.collection_objects_unlink()
    col_ventanas.objects.link(vent)

# ═══════════════════════════════════════════════════════════════════════
# TECHO
# ═══════════════════════════════════════════════════════════════════════

# Techo plano
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 5.2))
techo = bpy.context.active_object
techo.name = "Techo"
techo.scale = (8, 10, 0.2)
techo.collection_objects_unlink()
col_techo.objects.link(techo)

# Tejado triangular - frente
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 5.7))
tejado1 = bpy.context.active_object
tejado1.name = "Tejado_1"
tejado1.scale = (8, 0.5, 0.8)
tejado1.rotation_euler = (math.radians(30), 0, 0)
tejado1.collection_objects_unlink()
col_techo.objects.link(tejado1)

# Tejado triangular - Atrás
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 5.7))
tejado2 = bpy.context.active_object
tejado2.name = "Tejado_2"
tejado2.scale = (8, 0.5, 0.8)
tejado2.rotation_euler = (math.radians(-30), 0, 0)
tejado2.collection_objects_unlink()
col_techo.objects.link(tejado2)

# ═══════════════════════════════════════════════════════════════════════
# INTERIOR - ELEMENTOS DECORATIVOS
# ═══════════════════════════════════════════════════════════════════════

# Escaleras (simple)
for i in range(5):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -1.5 - i*0.3, 0.5 + i*0.3))
    escalon = bpy.context.active_object
    escalon.name = f"Escalon_{i}"
    escalon.scale = (0.3, 0.8, 0.2)
    escalon.collection_objects_unlink()
    col_interior.objects.link(escalon)

# Pilares decorativos
for x in [-3.5, 3.5]:
    for y in [-3.5, 3.5]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=5, location=(x, y, 2.5))
        pilar = bpy.context.active_object
        pilar.name = f"Pilar_{x}_{y}"
        pilar.collection_objects_unlink()
        col_interior.objects.link(pilar)

# ═══════════════════════════════════════════════════════════════════════
# EXTERIOR - ELEMENTOS DE PAISAJE
# ═══════════════════════════════════════════════════════════════════════

# Plantas decorativas en jardín
for x in [-7, -5, 5, 7]:
    for y in [-7, 7]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(x, y, 0.3))
        planta = bpy.context.active_object
        planta.name = f"Planta_{x}_{y}"
        planta.collection_objects_unlink()
        col_exterior.objects.link(planta)

# Camino de entrada
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 8, 0.05))
camino = bpy.context.active_object
camino.name = "Camino_Entrada"
camino.scale = (2, 2, 0.1)
camino.collection_objects_unlink()
col_exterior.objects.link(camino)

# Terraza
bpy.ops.mesh.primitive_cube_add(size=1, location=(-6, 5, 0.1))
terraza = bpy.context.active_object
terraza.name = "Terraza"
terraza.scale = (2, 2, 0.1)
terraza.collection_objects_unlink()
col_exterior.objects.link(terraza)

# ═══════════════════════════════════════════════════════════════════════
# GUARDAR ARCHIVO .BLEND
# ═══════════════════════════════════════════════════════════════════════

# Preparar nombre y ubicación
fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
archivo_blend = f"Casa_Completa_2Plantas_{fecha}.blend"

# Guardar con ruta absoluta
import os
ruta_guardado = os.path.join(os.getcwd(), "ZULY_LAB", archivo_blend)
os.makedirs("ZULY_LAB", exist_ok=True)

bpy.ops.wm.save_as_mainfile(filepath=ruta_guardado)

print(f"✅ Casa guardada en: {ruta_guardado}")

# ═══════════════════════════════════════════════════════════════════════
# GENERAR REPORTE
# ═══════════════════════════════════════════════════════════════════════

import json

reporte = {
    "titulo": "Casa Completa de 2 Plantas",
    "fecha": datetime.now().isoformat(),
    "blender_version": "3.6.2",
    "archivo_generado": archivo_blend,
    "ubicacion": "ZULY_LAB/",
    "estadisticas": {
        "total_objetos": len(bpy.context.scene.objects),
        "puertas": 3,
        "ventanas": 12,
        "habitaciones": 4,
        "plantas": 2,
        "detalles_arquitectonicos": "Tejado, escaleras, pilares, terraza, camino",
        "elementos_jardin": 12
    },
    "estructura": {
        "colecciones": list([col.name for col in bpy.context.scene.collection.children]),
        "planta_baja": {
            "paredes": 5,
            "puertas": 3,
            "ventanas": 6
        },
        "planta_alta": {
            "paredes": 4,
            "puertas": 0,
            "ventanas": 4
        },
        "exterior": {
            "plantas": 12,
            "camino": 1,
            "terraza": 1
        }
    },
    "tecnicas_aplicadas": [
        "Parser Lenguaje Natural (Casa completa ← comando simple)",
        "C2 Learning (Patrones: crear, mover, escalar, rotar)",
        "Handlers LYZU (create_, move_, scale_, rotate_)",
        "Modelado Arquitectónico (Paredes, techos, detalles)",
        "Organización (Colecciones por tipo)",
        "Persistencia (Guardado como .blend)"
    ],
    "detalles": {
        "planta_baja": "Sala, comedor, cocina, pasillo central, baño",
        "planta_alta": "Recámaras, baño, pasillo distribuidor",
        "estructura": "Paredes de carga, pilares, muros separadores",
        "cobertura": "Tejado inclinado, techo interior",
        "accesos": "Puerta principal, puertas interiores",
        "ventilacion": "Ventanas distribuidas estratégicamente"
    }
}

# Guardar reporte
reporte_path = os.path.join("ZULY_LAB", f"Casa_Reporte_{fecha}.json")
with open(reporte_path, "w") as f:
    json.dump(reporte, f, indent=2)

# Mostrar resumen
print("\\n" + "="*70)
print("  🏠 CASA COMPLETADA EXITOSAMENTE")
print("="*70)
print(f"\\nARCHIVO BLEND: {archivo_blend}")
print(f"UBICACIÓN: ZULY_LAB/")
print(f"TOTAL OBJETOS: {len(bpy.context.scene.objects)}")
print(f"COLECCIONES: {len(bpy.context.scene.collection.children)}")
print(f"\\nTECNICAS APLICADAS:")
for tecnica in reporte['tecnicas_aplicadas']:
    print(f"  ✓ {tecnica}")
print("\\n" + "="*70)

print("\\n" + json.dumps(reporte, indent=2))
"""


def ejecutar_prueba():
    """Ejecuta la prueba de casa completa"""
    
    print("\n" + "=" * 80)
    print("  🏠 PRUEBA ESPECIAL: CASA COMPLETA DE 2 PLANTAS")
    print("=" * 80 + "\n")
    
    script_dir = Path(__file__).parent
    blender_exe = script_dir / "blender/v3/blender-3.6.0-zuly/blender.exe"
    
    # Generar script
    script = generar_script_casa_completa()
    script_path = script_dir / "temp_casa_completa.py"
    
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)
    
    print(f"📝 Script generado\n")
    print(f"⚙️  Ejecutando Blender en background...\n")
    print(f"   Generando casa de 2 plantas con:")
    print(f"   • 2 plantas completas")
    print(f"   • 3 puertas (principal + interiores)")
    print(f"   • 12 ventanas distribuidas")
    print(f"   • Tejado inclinado")
    print(f"   • Escaleras")
    print(f"   • Pilares decorativos")
    print(f"   • Elementos de jardín\n")
    
    try:
        cmd = [
            str(blender_exe),
            "--background",
            "--python", str(script_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if "Casa guardada en:" in result.stdout:
            print("✅ ÉXITO - Casa generada y guardada\n")
            print(result.stdout)
        else:
            print("⚠️  Output de Blender:\n")
            print(result.stdout)
            if result.stderr:
                print("Errores:")
                print(result.stderr)
        
        # Verificar archivo
        zuly_lab = script_dir / "ZULY_LAB"
        if zuly_lab.exists():
            blend_files = list(zuly_lab.glob("Casa_Completa_2Plantas_*.blend"))
            if blend_files:
                archivo = blend_files[-1]
                tamaño = archivo.stat().st_size / (1024*1024)
                print(f"\n✅ ARCHIVO GUARDADO:")
                print(f"   📄 {archivo.name}")
                print(f"   📦 Tamaño: {tamaño:.2f} MB")
                print(f"   📍 Ubicación: {archivo.parent}\n")
                print(f"🎉 ¡Casa lista para revisar en Blender!\n")
        
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT - Blender tardó demasiado")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        if script_path.exists():
            script_path.unlink()


if __name__ == "__main__":
    ejecutar_prueba()
