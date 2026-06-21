import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

# Ver si el proceso sigue activo
stdin, stdout, stderr = ssh.exec_command("pgrep -a -f mass_processor_v3")
pids = stdout.read().decode('utf-8', errors='replace').strip()
print("=== PROCESO ACTIVO V9 ===")
print(pids if pids else "NO hay proceso")

# Leer el log nohup
print("\n=== LOG NOHUP (v9_output.log) ===")
stdin2, stdout2, stderr2 = ssh.exec_command("wc -l /opt/zuly/v9_output.log && tail -n 50 /opt/zuly/v9_output.log")
print(stdout2.read().decode('utf-8', errors='replace'))

# Ver si hay scripts temporales generados
print("\n=== SCRIPTS TEMPORALES V9 GENERADOS ===")
stdin3, stdout3, _ = ssh.exec_command("ls -lth /opt/zuly/temp_v9_*.py 2>/dev/null | head -5")
print(stdout3.read().decode('utf-8', errors='replace'))

# Resultados exitosos
print("\n=== RESULTADOS EN /opt/zuly/resultados_masivos_v9/ ===")
stdin4, stdout4, _ = ssh.exec_command("ls -lh /opt/zuly/resultados_masivos_v9/")
print(stdout4.read().decode('utf-8', errors='replace'))

# Log de aprendizaje
print("\n=== LOG DE APRENDIZAJE V9 ===")
stdin5, stdout5, _ = ssh.exec_command("cat /opt/zuly/bitacora/aprendizaje_v9.log 2>/dev/null || echo 'Sin exitos aun'")
print(stdout5.read().decode('utf-8', errors='replace'))

ssh.close()
