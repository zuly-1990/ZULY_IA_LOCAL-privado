import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

cmd = """
echo '=== ESTRUCTURA /opt/zuly ===' && ls -la /opt/zuly/ 2>&1 | head -30
echo '=== PAQUETES PYTHON CLAVE ===' && pip3 list 2>&1 | grep -Ei 'gemini|groq|sentence|transformers|google'
echo '=== VERSION BLENDER ===' && blender --version 2>&1 | head -2
echo '=== ORQUESTADOR ACTUALIZADO ===' && head -70 /opt/zuly/core/external/multi_api_orchestrator.py 2>&1
echo '=== RESULTADOS V8 PREVIOS ===' && ls -la /opt/zuly/resultados_masivos_v8/ 2>&1
"""

stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode('utf-8', errors='replace')
print(out)
err = stderr.read().decode('utf-8', errors='replace')
if err:
    print("STDERR:", err)
ssh.close()
