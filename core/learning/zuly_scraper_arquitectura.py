import os
import sys
import json
import urllib.request
import subprocess
from pathlib import Path

# Configuracion de carpetas en el servidor Linux
LIBRERIA_DIR = "/opt/zuly/libreria_3d/arquitectura"
TEMP_DIR = "/opt/zuly/libreria_3d/temp"

os.makedirs(LIBRERIA_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Instalar objaverse si no esta
try:
    import objaverse
except ImportError:
    print("Instalando objaverse...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "objaverse"])
    import objaverse

def main():
    print("1. Cargando metadatos de Objaverse (esto puede tomar unos minutos la primera vez)...")
    # Cargar anotaciones
    # Nota: para evitar cargar los 800k, objaverse provee un buscador.
    # Pero usaremos load_uids para traer la lista.
    uids = objaverse.load_uids()
    print(f"Total de modelos en Objaverse: {len(uids)}")
    
    # Objaverse es inmenso. Para hacer un test rapido, tomaremos 5 modelos arquitectonicos conocidos
    # O haremos una busqueda en las anotaciones.
    # Como buscar requiere descargar todo el json de anotaciones, 
    # descargaremos las anotaciones completas y buscaremos "architecture" o "building"
    print("Buscando modelos con la etiqueta 'building' o 'architecture'...")
    annotations = objaverse.load_annotations(uids[:10000]) # Solo revisamos los primeros 10,000 para no agotar la RAM
    
    selected_uids = []
    for uid, data in annotations.items():
        name = str(data.get("name", "")).lower()
        tags = [tag.get("name", "").lower() for tag in data.get("tags", [])]
        categories = [c.get("name", "").lower() for c in data.get("categories", [])]
        
        # Filtros de busqueda
        search_terms = ["architecture", "building", "house", "villa", "skyscraper"]
        
        if any(term in name for term in search_terms) or \
           any(term in tags for term in search_terms) or \
           any(term in categories for term in search_terms):
            selected_uids.append(uid)
            
        if len(selected_uids) >= 5:
            break
            
    print(f"Se encontraron {len(selected_uids)} modelos. Descargando...")
    
    # Descargar modelos (se guardan por defecto en ~/.objaverse)
    objects = objaverse.load_objects(
        uids=selected_uids
    )
    
    print("Descarga completada. Preparando conversiones en Blender...")
    
    # Crear un script de Blender para normalizar
    blender_script = os.path.join(TEMP_DIR, "normalize_model.py")
    with open(blender_script, "w", encoding="utf-8") as f:
        f.write("""import bpy
import sys
import os

# Argumentos: script.py <input_glb> <output_blend>
input_glb = sys.argv[-2]
output_blend = sys.argv[-1]

# Limpiar escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Importar GLB
try:
    bpy.ops.import_scene.gltf(filepath=input_glb)
except Exception as e:
    print(f"Error importando GLB: {e}")
    sys.exit(1)

# Normalizar y Escalar
# Seleccionar todo
bpy.ops.object.select_all(action='SELECT')
if len(bpy.context.selected_objects) == 0:
    print("No se encontraron objetos.")
    sys.exit(1)

# Asignar un objeto activo (el mas grande o el primero)
bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

# Agrupar todo en un parent vacio o unirlos
bpy.ops.object.join()

obj = bpy.context.active_object
obj.location = (0,0,0)

# Escalar para que encaje en una caja de 10x10x10 metros (tamaño edificio base)
max_dim = max(obj.dimensions)
if max_dim > 0:
    scale_factor = 10.0 / max_dim
    obj.scale = (scale_factor, scale_factor, scale_factor)

bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Guardar como BLEND
bpy.ops.wm.save_as_mainfile(filepath=output_blend)
print(f"Guardado exitosamente: {output_blend}")
sys.exit(0)
""")

    # Ejecutar blender para cada objeto
    for uid, filepath in objects.items():
        if not filepath: continue
        
        output_blend = os.path.join(LIBRERIA_DIR, f"arquitectura_{uid}.blend")
        print(f"Procesando en Blender: {filepath} -> {output_blend}")
        
        # Ejecutar blender en modo oculto (-b) con el script de normalizacion
        cmd = ["blender", "-b", "-P", blender_script, "--", filepath, output_blend]
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        if os.path.exists(output_blend):
            print(f"✅ ¡Normalización completada! {output_blend}")
        else:
            print(f"❌ Falló la normalización para {uid}.")
            print(res.stderr[-200:])
            
    print("PROCESO MASIVO DE INGESTA TERMINADO.")

if __name__ == "__main__":
    main()
