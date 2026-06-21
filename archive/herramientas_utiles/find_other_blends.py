import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("=== BUSCANDO OTROS ARCHIVOS .blend EN EL SERVIDOR ===")
stdin, stdout, stderr = ssh.exec_command("find /opt/zuly -name '*.blend'")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
