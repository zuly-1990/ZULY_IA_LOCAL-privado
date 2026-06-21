import paramiko
import os

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

remote_test_script = """
import sys
import os

sys.path.append('/opt/zuly')
from core.external.multi_api_orchestrator import MultiAPIOrchestrator

print('✅ Inicializando Orquestador Multi-IA...')
api = MultiAPIOrchestrator()

prompt = '''
Eres un maestro absoluto de Python y la API de Geometry Nodes de Blender 3.6.
Escribe un script en Python que construya un árbol de Geometry Nodes desde cero para crear un edificio detallado.
Instrucciones obligatorias:
1. Limpia todos los objetos existentes.
2. Crea un cubo base y agrégale un modificador "GeometryNodes".
3. Crea un nuevo NodeGroup para el modificador.
4. En el NodeGroup, usando la API de Python (`group.nodes.new`, `group.links.new`), debes tomar la geometría base y subdividirla o instanciar pequeñas ventanas (como cubos estirados) en las caras. ¡Solo haz algo que use nodos geométricos como Instance on Points o Extrude Mesh!
5. Crea una cámara y apuntala al objeto.
6. Al final, DEBES incluir exactamente la línea: `bpy.ops.wm.save_as_mainfile(filepath="/opt/zuly/geonodes_edificio.blend")`
RECUERDA: La API de python para conectar nodos es `group.links.new(nodo_salida.outputs[0], nodo_entrada.inputs[0])`.
Debes manejar excepciones si algún nodo específico cambia de nombre. ¡ES UN RETO DE ALTO NIVEL! Solo devuelve CÓDIGO PYTHON.
'''

print('🚀 Pidiendo código GeoNodes a DeepSeek...')
codigo_ia = api.call_coder_model(prompt)

if '```python' in codigo_ia:
    codigo_ia = codigo_ia.split('```python')[1].split('```')[0].strip()
elif '```' in codigo_ia:
    codigo_ia = codigo_ia.split('```')[1].strip()

# Guardamos el código para que Blender lo ejecute
with open('/opt/zuly/generado_geonodes.py', 'w', encoding='utf-8') as f:
    f.write(codigo_ia)

print('✅ Código guardado. Ejecutando en Blender Remoto sin renderizar...')
os.system('/opt/blender/blender --background --python /opt/zuly/generado_geonodes.py')

print('🎬 Ejecución de GeoNodes completada. Archivo .blend guardado.')
"""

def run_geonodes_test():
    print(f"Conectando a {ip} para la Prueba 1.5: GeoNodes Extremo...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(ip, username=user, password=password, timeout=15)
        
        # Subimos el script python en lugar de ejecutarlo inline
        print("Subiendo script de test al servidor...")
        sftp = ssh.open_sftp()
        with open("remote_geonodes.py", "w", encoding="utf-8") as f:
            f.write(remote_test_script)
        sftp.put("remote_geonodes.py", "/opt/zuly/remote_geonodes.py")
        
        # Ejecutamos la prueba en el servidor
        print("Ejecutando script de GeoNodes en el servidor (esto tomará tiempo)...")
        stdin, stdout, stderr = ssh.exec_command("python3 /opt/zuly/remote_geonodes.py")
        out = stdout.read().decode('utf-8').strip()
        err = stderr.read().decode('utf-8').strip()
        
        if out: print(out)
        if err: print("\nERRORES:", err)
        
        # Descargamos el archivo .blend
        print("\nDescargando archivo .blend a la PC local...")
        try:
            sftp.get('/opt/zuly/geonodes_edificio.blend', 'geonodes_edificio.blend')
            print("✅ ARCHIVO GEONODES DESCARGADO LOCALMENTE: geonodes_edificio.blend")
        except Exception as e:
            print("No se pudo encontrar el archivo .blend...", e)
            
        sftp.close()
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    run_geonodes_test()
