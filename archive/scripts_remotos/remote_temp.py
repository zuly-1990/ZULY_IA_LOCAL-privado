
import sys
import os

sys.path.append('/opt/zuly')
from core.external.multi_api_orchestrator import MultiAPIOrchestrator

print('✅ Inicializando Orquestador Multi-IA...')
api = MultiAPIOrchestrator()

prompt = '''
Eres un experto en Blender 3.6 Python (bpy).
Escribe SOLO EL CÓDIGO PYTHON para generar una CIUDAD PARAMÉTRICA MASIVA.
Reglas:
1. Limpiar todos los objetos existentes primero.
2. Crear un Grid de 20x20 manzanas (400 edificios).
3. Cada edificio debe ser un cubo estirado verticalmente en Z con una altura aleatoria entre 2.0 y 20.0.
4. Usa el módulo random de python.
5. Asignar un material base diferente según la altura (ej: bajo = verde, alto = azul oscuro, muy alto = blanco brillante).
6. Crea una luz tipo SUN con ángulo y energía para que se vean bien las sombras.
7. Sitúa una cámara isométrica o a la distancia correcta para ver toda la ciudad (location=(50, -50, 40), rotation=(math.radians(60), 0, math.radians(45))).
8. Agrupa todo en una colección llamada 'MegaCiudad'. ALERTA: primitive_cube_add ya vincula a la colección activa, asegúrate de desvincular (unlink) de la colección original antes de hacer link a 'MegaCiudad' o simplemente establece 'MegaCiudad' como la colección activa antes de crear los cubos.
10. Al final de tu script, DEBES guardar el archivo con `bpy.ops.wm.save_as_mainfile(filepath="/opt/zuly/mega_ciudad.blend")`.
SOLO CÓDIGO.
'''

print('🚀 Pidiendo código a DeepSeek...')
codigo_ia = api.call_coder_model(prompt)

if '```python' in codigo_ia:
    codigo_ia = codigo_ia.split('```python')[1].split('```')[0].strip()
elif '```' in codigo_ia:
    codigo_ia = codigo_ia.split('```')[1].strip()

# Guardamos el código para que Blender lo ejecute
with open('/opt/zuly/generado_masivo.py', 'w', encoding='utf-8') as f:
    f.write(codigo_ia)

print('✅ Código guardado. Ejecutando en Blender Remoto sin renderizar...')
# Removemos el flag -f 1 para evitar crash en servidores headless sin libEGL
os.system('/opt/blender/blender --background --python /opt/zuly/generado_masivo.py')

print('🎬 Ejecución completada. Archivo .blend guardado.')
