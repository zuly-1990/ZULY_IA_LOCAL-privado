import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("=== VERIFICANDO ESTADO DE ZULY EN EL SERVIDOR ===")

# 1. Ver archivos en la carpeta de resultados
print("\n--- ARCHIVOS EN resultados_masivos_v8 ---")
stdin, stdout, stderr = ssh.exec_command("ls -lh /opt/zuly/resultados_masivos_v8/")
print(stdout.read().decode('utf-8', errors='replace').strip())

# 2. Ver la bitacora de aprendizaje
print("\n--- BITÁCORA DE APRENDIZAJE (aprendizaje_v8.log) ---")
stdin, stdout, stderr = ssh.exec_command("cat /opt/zuly/bitacora/aprendizaje_v8.log 2>/dev/null || echo 'No hay bitacora'")
print(stdout.read().decode('utf-8', errors='replace').strip())

# 3. Ver procesos de Blender o Zuly activos
print("\n--- PROCESOS DE ZULY/BLENDER CORRIENDO ---")
stdin, stdout, stderr = ssh.exec_command("ps aux | grep -E 'python3|blender' | grep -v grep")
print(stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
