import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

print("Instalando unrar...")
ssh.exec_command("apt-get update && apt-get install -y unrar")
import time
time.sleep(5)

script = """
mkdir -p "/opt/zuly/planos_temp"
cd "/opt/zuly/planos_temp"
unrar x -y "/opt/zuly/Planos y premodelado.rar"
ls -R
"""
print("Extrayendo y listando...")
stdin, stdout, stderr = ssh.exec_command(script)
print("OUT:")
print(stdout.read().decode())
print("ERR:")
print(stderr.read().decode())

ssh.close()
