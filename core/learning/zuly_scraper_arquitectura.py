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
    
    # Crear un script de Blender para normalizar y extraer metadata
    blender_script = os.path.join(TEMP_DIR, "normalize_model.py")
    with open(blender_script, "w", encoding="utf-8") as f:
        f.write("""import bpy
import sys
import os
import json

# Argumentos: script.py <input_glb> <output_blend> <output_json>
input_glb = sys.argv[-3]
output_blend = sys.argv[-2]
output_json = sys.argv[-1]

# Limpiar escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Importar GLB
try:
    bpy.ops.import_scene.gltf(filepath=input_glb)
except Exception as e:
    print(f"Error importando GLB: {e}")
    sys.exit(1)

# Seleccionar mallas
bpy.ops.object.select_all(action='DESELECT')
mallas = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
if not mallas:
    print("No se encontraron mallas.")
    sys.exit(1)

for obj in mallas:
    obj.select_set(True)

bpy.context.view_layer.objects.active = mallas[0]
bpy.ops.object.join()

obj = bpy.context.active_object
obj.location = (0,0,0)

# Calcular metricas matematicas antes de escalar
verts = len(obj.data.vertices)
faces = len(obj.data.polygons)
dims = obj.dimensions
materiales = len(obj.data.materials)

metadata = {
    "dimensiones_crudas_metros": {
        "ancho_x": round(dims.x, 2),
        "largo_y": round(dims.y, 2),
        "alto_z": round(dims.z, 2)
    },
    "geometria": {
        "vertices": verts,
        "caras_poligonos": faces,
        "cantidad_materiales": materiales
    }
}

# Escalar para que encaje en una caja de 10x10x10 metros (tamaño edificio base)
max_dim = max(obj.dimensions)
if max_dim > 0:
    scale_factor = 10.0 / max_dim
    obj.scale = (scale_factor, scale_factor, scale_factor)

bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Guardar BLEND y JSON
bpy.ops.wm.save_as_mainfile(filepath=output_blend)
with open(output_json, "w", encoding="utf-8") as jf:
    json.dump(metadata, jf, indent=4)

print(f"Guardado exitosamente: {output_blend}")
sys.exit(0)
""")

    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not deepseek_key:
        print("⚠️ No se encontro DEEPSEEK_API_KEY. Se saltara la validacion de aprendizaje.")

    import requests

    def evaluar_modelo_deepseek(uid, metadata):
        if not deepseek_key: return True # Si no hay key, aprueba por defecto
        
        prompt = f'''Actúa como un arquitecto experto evaluando topología 3D extraída matemáticamente.
Acabamos de descargar un modelo 3D con etiqueta de "arquitectura". Estos son sus datos puros:
{json.dumps(metadata, indent=2)}

Analiza si estas proporciones y geometría tienen sentido para ser considerado arquitectura (una casa, edificio, rascacielos o ruina).
Si tiene muy pocos polígonos (ej. < 10) podría ser un cubo basura. 
Si sus dimensiones son 0x0x0 es basura.

Responde ÚNICAMENTE con la palabra "APROBADO" si los datos sugieren que es un modelo arquitectónico válido del que Zuly puede aprender.
Responde "RECHAZADO" si parece basura geométrica. Justifica brevemente en 1 linea después de la palabra.'''

        try:
            url = "https://api.deepseek.com/chat/completions"
            headers = {"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"}
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }
            resp = requests.post(url, headers=headers, json=data, timeout=20)
            if resp.status_code == 200:
                respuesta = resp.json()['choices'][0]['message']['content'].strip()
                print(f"[DeepSeek] Veredicto para {uid}: {respuesta}")
                return "APROBADO" in respuesta.upper()
        except Exception as e:
            print(f"[DeepSeek] Error evaluando: {e}")
        return False

    # Ejecutar blender para cada objeto
    for uid, filepath in objects.items():
        if not filepath: continue
        
        # SEGURO DE VIDA PARA SERVIDOR DE 4GB RAM: Saltar modelos mayores a 30 MB
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
        if file_size_mb > 30.0:
            print(f"⚠️ Saltando {uid} porque pesa demasiado ({file_size_mb:.2f} MB). Podría crashear el servidor.")
            os.remove(filepath) # Limpiar espacio en disco
            continue
            
        temp_blend = os.path.join(TEMP_DIR, f"temp_{uid}.blend")
        temp_json = os.path.join(TEMP_DIR, f"temp_{uid}.json")
        
        print(f"Procesando en Blender y Extrayendo Matemáticas: {filepath} ({file_size_mb:.2f} MB)")
        
        # Ejecutar blender en modo oculto (-b)
        cmd = ["blender", "-b", "-P", blender_script, "--", filepath, temp_blend, temp_json]
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        if os.path.exists(temp_blend) and os.path.exists(temp_json):
            # Fase de Aprendizaje Activo
            with open(temp_json, "r") as jf:
                metadata = json.load(jf)
            
            aprobado = evaluar_modelo_deepseek(uid, metadata)
            
            if aprobado:
                # Mover a la memoria permanente
                final_blend = os.path.join(LIBRERIA_DIR, f"arquitectura_{uid}.blend")
                final_json = os.path.join(LIBRERIA_DIR, f"arquitectura_{uid}.json")
                os.rename(temp_blend, final_blend)
                os.rename(temp_json, final_json)
                print(f"✅ APRENDIZAJE COMPLETADO. Guardado en memoria permanente: {final_blend}")
            else:
                print(f"❌ RECHAZADO por DeepSeek. Borrando basura geométrica.")
                os.remove(temp_blend)
                os.remove(temp_json)
                
            os.remove(filepath) # Borrar el GLB crudo
        else:
            print(f"❌ Falló la normalización para {uid}.")
            if os.path.exists(filepath): os.remove(filepath)
            
    print("PROCESO MASIVO DE INGESTA Y APRENDIZAJE TERMINADO.")

if __name__ == "__main__":
    main()
