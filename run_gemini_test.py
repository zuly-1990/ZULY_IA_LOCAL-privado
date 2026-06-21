import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

# Subir test_gemini_keys.py
sftp = ssh.open_sftp()
sftp.put("test_gemini_keys.py", "/opt/zuly/test_gemini_keys.py")
sftp.close()

# Ejecutarlo
print("=== EJECUTANDO PRUEBA DE LLAVES Y MODELOS ===")
stdin, stdout, stderr = ssh.exec_command("python3 /opt/zuly/test_gemini_keys.py")
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))

ssh.close()
