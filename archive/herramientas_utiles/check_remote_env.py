import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

# Print remote env variables
stdin, stdout, stderr = ssh.exec_command("env | grep GEMINI")
print("=== GEMINI ENV ===")
print(stdout.read().decode('utf-8', errors='replace'))

stdin2, stdout2, stderr2 = ssh.exec_command("python3 -c 'import os; print(\"GEMINI_API_KEY:\", repr(os.environ.get(\"GEMINI_API_KEY\")))'")
print("=== GEMINI PYTHON ENV ===")
print(stdout2.read().decode('utf-8', errors='replace'))

ssh.close()
