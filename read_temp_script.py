import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

stdin, stdout, stderr = ssh.exec_command("cat /opt/zuly/temp_v9_01_Primer_Nivel_v08.py")
print("=== CONTENIDO DE /opt/zuly/temp_v9_01_Primer_Nivel_v08.py ===")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
