import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

# Subir compile_blend_v9.py
sftp = ssh.open_sftp()
sftp.put("compile_blend_v9.py", "/opt/zuly/compile_blend_v9.py")
sftp.close()

# Ejecutarlo usando Blender en segundo plano
print("=== EJECUTANDO COMPILACIÓN V9 EN EL SERVIDOR ===")
stdin, stdout, stderr = ssh.exec_command("blender -b -P /opt/zuly/compile_blend_v9.py")
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))

ssh.close()
