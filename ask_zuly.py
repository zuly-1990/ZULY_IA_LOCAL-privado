import paramiko

MEGA_PROMPT = """Eres un ingeniero de software experto en algoritmos generativos. Escribe un script de Python puro (usando numpy y PIL/Pillow) que implemente un generador de "String Art" (Hilorama algorítmico).
Requisitos:
1. Leer una imagen, convertirla a escala de grises.
2. Calcular 250 coordenadas (x,y) de clavos (pines) en el perímetro de un círculo.
3. Implementar un Algoritmo Greedy: Desde el clavo actual, evaluar qué línea hacia otro clavo atraviesa los píxeles más oscuros.
4. Seleccionar ese clavo de destino, registrar el índice, y aclarar (dibujar línea blanca) sobre esos píxeles en la matriz de la imagen para "borrarlos".
5. Iterar 3000 veces.
6. Guardar la lista de índices recorridos en 'secuencia_clavos.json'.

Proporciona ÚNICAMENTE el código Python completo, sin explicaciones ni formato markdown extra. Usa comentarios en español."""

def run_ssh_commands():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('167.233.69.104', username='root', password='ZULY.server.77', timeout=15)
        
        script_remoto = f'''
import os
import sys

# Cargar variables de entorno manualmente desde .env
with open("/opt/zuly/.env") as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip('"').strip("'")

sys.path.append("/opt/zuly")
from core.external.multi_api_orchestrator import MultiAPIOrchestrator

prompt = """{MEGA_PROMPT}"""

zuly = MultiAPIOrchestrator()
resultado = zuly.call_coder_model(prompt)
print("$$$START$$$")
print(resultado)
print("$$$END$$$")
'''
        sftp = ssh.open_sftp()
        with sftp.file('/tmp/ask_deepseek.py', 'w') as f:
            f.write(script_remoto)
        sftp.close()
        
        stdin, stdout, stderr = ssh.exec_command('export PYTHONPATH=/opt/zuly; python3 /tmp/ask_deepseek.py')
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        
        if "$$$START$$$" in out:
            codigo = out.split("$$$START$$$")[1].split("$$$END$$$")[0].strip()
            # Guardar el codigo que generó DeepSeek en un archivo local
            with open("C:/Users/Admin/Desktop/ZULY_IA_LOCAL/calculadora_hilos.py", "w", encoding="utf-8") as f:
                # Quitar los backticks de markdown si DeepSeek los puso
                codigo = codigo.replace("```python", "").replace("```", "").strip()
                f.write(codigo)
            print("CODIGO GENERADO Y GUARDADO EN calculadora_hilos.py")
        else:
            print("Output crudo:", out)
        
        err = stderr.read().decode('utf-8', errors='ignore').strip()
        if err:
            print("Stderr:", err)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    run_ssh_commands()
