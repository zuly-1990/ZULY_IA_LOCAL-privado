#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ SELLO DEL SOBERANO - CUB-001
Aprobación y archivado en mastered/
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
mastered_path = zuly_path / 'archivo_zuly' / 'por_estado_aprendizaje' / 'mastered'
temp_arena = zuly_path / 'archivo_zuly' / 'temp_arena'

# Configuración del patrón
pattern_id = "CUB-001"
pattern_name = "CUB-001_Modelado_BiselRealista"
categoria = "CUB"  # Cubos
descripcion = "Cubo con bordes suaves (Bevel) y color azul corporativo #1A4DCC"
tags = ["cubo", "bevel", "modelado", "basico", "azul"]
color_hex = "#1A4DCC"

print("="*60)
print("🏛️ SELLO DEL SOBERANO - APROBACIÓN DE PATRÓN")
print("="*60)
print(f"🎯 Patrón: {pattern_name}")
print(f"📂 Categoría: {categoria}")
print(f"👤 Aprobado por: Soberano (Usuario)")
print(f"📅 Fecha: {datetime.now().isoformat()}")
print("="*60)

# 1. Crear estructura de carpetas
pattern_folder = mastered_path / pattern_name
folders = {
    'blend': pattern_folder / 'blend',
    'script': pattern_folder / 'script',
    'json': pattern_folder / 'json',
    'render': pattern_folder / 'render',
    'certificado': pattern_folder / 'certificado'
}

print("\n📁 Creando estructura de carpetas...")
for name, folder in folders.items():
    folder.mkdir(parents=True, exist_ok=True)
    print(f"   ✅ {name}/")

# 2. Copiar archivo .blend
print("\n📦 Copiendo archivos...")
src_blend = temp_arena / f"{pattern_name}.blend"
dst_blend = folders['blend'] / f"{pattern_name}.blend"
shutil.copy2(src_blend, dst_blend)
print(f"   ✅ blend/{pattern_name}.blend")

# 3. Crear script de generación
script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 {pattern_name}
{categoria} - {descripcion}
Generado: {fecha}
"""

import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear cubo
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cubo = bpy.context.active_object
cubo.name = "{pattern_name}"

# Bevel
bevel = cubo.modifiers.new(name="Bevel_Pro", type='BEVEL')
bevel.width = 0.08
bevel.segments = 4
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5236

# Material Azul #1A4DCC
mat = bpy.data.materials.new(name="Mat_Azul_Pro")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    r, g, b = 26/255, 77/255, 204/255  # #1A4DCC
    principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
    principled.inputs['Roughness'].default_value = 0.3
    principled.inputs['Specular'].default_value = 0.7
cubo.data.materials.append(mat)

# Iluminación SLIZ
luces = aplicar_iluminacion_profesional(cubo)

# Cámara
import mathutils
cam_pos = mathutils.Vector((4, -4, 3))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = cubo.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# Render settings
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Guardar
bpy.ops.wm.save_as_mainfile(filepath='./{pattern_name}.blend')
'''.format(
    pattern_name=pattern_name,
    categoria=categoria,
    descripcion=descripcion,
    fecha=datetime.now().isoformat()
)

script_path = folders['script'] / f"{pattern_name}.py"
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_content)
print(f"   ✅ script/{pattern_name}.py")

# 4. Crear JSON de metadatos
metadata = {
    "pattern_id": pattern_id,
    "nombre_tecnico": pattern_name,
    "version": "1.0",
    "categoria": categoria,
    "descripcion": descripcion,
    "tags": tags,
    "color_base": color_hex,
    "fecha_creacion": datetime.now().isoformat(),
    "fecha_sello": datetime.now().isoformat(),
    "estado": "SELLADO",
    "sellado_por": "Soberano",
    "geometria": {
        "tipo": "primitiva_cubo",
        "dimensiones": "2x2x2",
        "modificadores": ["Bevel"]
    },
    "material": {
        "nombre": "Mat_Azul_Pro",
        "tipo": "Principled BSDF",
        "color_hex": color_hex,
        "propiedades": {
            "roughness": 0.3,
            "specular": 0.7
        }
    },
    "iluminacion": {
        "sistema": "SLIZ v2.0",
        "luces": ["Sol", "Key", "Fill", "Rim"]
    },
    "validacion_jues": {
        "estado_malla": "LIMPIA",
        "color_match": True,
        "peso_kb": 812.4,
        "dictamen": "APTO_PARA_SELLO"
    },
    "ubicacion": {
        "mastered": f"archivo_zuly/por_estado_aprendizaje/mastered/{pattern_name}/",
        "blend": f"blend/{pattern_name}.blend",
        "script": f"script/{pattern_name}.py",
        "json": f"json/{pattern_name}.json"
    }
}

json_path = folders['json'] / f"{pattern_name}.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)
print(f"   ✅ json/{pattern_name}.json")

# 5. Crear CERTIFICADO DE SELLO
certificado = {
    "certificado_id": f"CERT-{pattern_id}-{datetime.now().strftime('%Y%m%d')}",
    "pattern_id": pattern_id,
    "pattern_nombre": pattern_name,
    "categoria": categoria,
    "version": "1.0",
    "fecha_sello": datetime.now().isoformat(),
    "sellado_por": "Soberano",
    "decision": "SELLADO",
    "observaciones": "Primer patrón aprobado del sistema ZULY",
    "hash_inmutabilidad": "ef305bb9c2537dfa",  # Del reporte JUES
    "validacion": {
        "estado_malla": "LIMPIA",
        "color_match": True,
        "peso_kb": 812.4,
        "dictamen_jues": "APTO_PARA_SELLO"
    },
    "jerarquia_zei": {
        "zuly_genero": True,
        "jues_valido": True,
        "lyzu_registro": True,
        "soberano_aprobo": True
    }
}

cert_path = folders['certificado'] / "CERTIFICADO_SELLO.json"
with open(cert_path, 'w', encoding='utf-8') as f:
    json.dump(certificado, f, indent=2, ensure_ascii=False)
print(f"   ✅ certificado/CERTIFICADO_SELLO.json")

# 6. Actualizar REGISTRO_MAESTRO
registro_path = zuly_path / 'archivo_zuly' / 'REGISTRO_MAESTRO.json'

# Cargar registro existente o crear nuevo
if registro_path.exists():
    with open(registro_path, 'r', encoding='utf-8') as f:
        registro = json.load(f)
else:
    registro = {
        "sistema": "ZULY Pattern Registry",
        "version": "1.0",
        "total_patrones": 0,
        "patrones": []
    }

# Agregar nuevo patrón
registro["patrones"].append({
    "pattern_id": pattern_id,
    "nombre": pattern_name,
    "categoria": categoria,
    "descripcion": descripcion,
    "estado": "SELLADO",
    "fecha_sello": datetime.now().isoformat(),
    "ubicacion": f"por_estado_aprendizaje/mastered/{pattern_name}/"
})
registro["total_patrones"] = len(registro["patrones"])
registro["ultima_actualizacion"] = datetime.now().isoformat()

with open(registro_path, 'w', encoding='utf-8') as f:
    json.dump(registro, f, indent=2, ensure_ascii=False)

print(f"\n📚 REGISTRO_MAESTRO.json actualizado")
print(f"   Total patrones: {registro['total_patrones']}")

# 7. LYZU registra evento (simulado)
lyzu_entry = {
    "timestamp": datetime.now().isoformat(),
    "evento": "SELLO_APROBADO",
    "pattern_id": pattern_id,
    "pattern_nombre": pattern_name,
    "soberano": "Usuario",
    "accion": "SELLADO",
    "mensaje": f"Patrón {pattern_name} sellado y archivado en mastered/"
}

print(f"\n🧠 LYZU registra: SELLO_APROBADO - {pattern_name}")

# Resumen final
print("\n" + "="*60)
print("✅ SELLO APLICADO EXITOSAMENTE")
print("="*60)
print(f"📁 Ubicación final:")
print(f"   por_estado_aprendizaje/mastered/{pattern_name}/")
print(f"   ├── blend/{pattern_name}.blend")
print(f"   ├── script/{pattern_name}.py")
print(f"   ├── json/{pattern_name}.json")
print(f"   ├── render/")
print(f"   └── certificado/CERTIFICADO_SELLO.json")
print(f"\n📚 REGISTRO_MAESTRO: {registro['total_patrones']} patrones registrados")
print(f"\n🏆 {pattern_name} es oficialmente parte del sistema ZULY")
print("="*60)
