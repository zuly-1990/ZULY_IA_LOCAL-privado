import paramiko

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("Matando procesos viejos...")
ssh.exec_command("pkill -f telegram_listener.py")
import time
time.sleep(2)

command = "nohup bash -c 'export PYTHONPATH=/opt/zuly; python3 /opt/zuly/core/external/telegram_listener.py' > /opt/zuly/telegram.log 2>&1 &"
stdin, stdout, stderr = ssh.exec_command(command)
print("Ejecutado en remoto.")

ssh.close()
