import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

# Matar el proceso actual (puede estar colgado)
ssh.exec_command("pkill -f mass_processor_v2")
import time; time.sleep(2)

# Ejecutar directamente y capturar TANTO stdout como stderr
print("=== PRUEBA DIRECTA DEL SCRIPT V8 (timeout 20s) ===")
stdin, stdout, stderr = ssh.exec_command(
    "cd /opt/zuly && python3 core/assembly/mass_processor_v2.py 2>&1 | head -50",
    timeout=25
)
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
