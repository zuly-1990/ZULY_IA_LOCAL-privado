import paramiko
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("Matando procesos anteriores de V9...")
stdin0, stdout0, _ = ssh.exec_command("pkill -f mass_processor_v3; sleep 2; echo OK")
print(stdout0.read().decode('utf-8', errors='replace').strip())

# Limpiar log anterior
ssh.exec_command("rm -f /opt/zuly/v9_output.log")
time.sleep(1)

print("Lanzando ZULY V9 (Volumetric 3D Modeling) en el servidor remoto...")
# Redirigir TANTO stdout COMO stderr al log con &> (bash)
cmd = "cd /opt/zuly && nohup python3 -u core/assembly/mass_processor_v3.py &> /opt/zuly/v9_output.log &"
stdin, stdout, stderr = ssh.exec_command(cmd)
time.sleep(3)

print("Proceso lanzado en background. PID del proceso:")
stdin2, stdout2, stderr2 = ssh.exec_command("pgrep -f mass_processor_v3")
print(stdout2.read().decode('utf-8', errors='replace'))
ssh.close()
print("Hecho. El log estara en /opt/zuly/v9_output.log")
