import paramiko

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

test_script = """
cd /opt/zuly
python3 -c "
import sys
from core.external.multi_api_orchestrator import MultiAPIOrchestrator

try:
    print('✅ Inicializando Orquestador Multi-IA...')
    api = MultiAPIOrchestrator()
    
    prompt = '''
    Eres un experto en Blender y Python (bpy).
    Escribe SOLO EL CÓDIGO PYTHON (sin explicaciones) para crear una escalera de caracol paramétrica en Blender 3.6.
    El código debe:
    1. Importar bpy y math.
    2. Crear 20 escalones rotando sobre el eje Z.
    3. Agruparlos en una colección llamada 'Escalera_Generada'.
    '''
    
    print('🚀 Enviando solicitud de arquitectura compleja a OpenRouter...')
    codigo_generado = api.call_coder_model(prompt)
    
    print('==================== CÓDIGO GENERADO POR IA ====================')
    print(codigo_generado)
    print('================================================================')
    print('✅ ¡El Arquitecto de Código respondió exitosamente!')
    
except Exception as e:
    print(f'❌ ERROR: {e}')
"
"""

def test_architect():
    print(f"Conectando a {ip} para probar al Arquitecto de Código...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=user, password=password, timeout=15)
        stdin, stdout, stderr = ssh.exec_command(test_script)
        out = stdout.read().decode('utf-8').strip()
        err = stderr.read().decode('utf-8').strip()
        
        print("\n--- SALIDA DEL SERVIDOR REMOTO ---")
        if out:
            print(out)
        if err:
            print("\nERRORES:")
            print(err)
    except Exception as e:
        print(f"Error de conexión: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    test_architect()
