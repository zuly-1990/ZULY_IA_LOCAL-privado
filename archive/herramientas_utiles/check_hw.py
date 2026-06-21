import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("167.233.69.104", username="root", password="ZULY.server.77")

stdin, stdout, stderr = ssh.exec_command("free -m")
print("RAM:")
print(stdout.read().decode())

stdin, stdout, stderr = ssh.exec_command("lscpu | grep 'Model name'")
print("CPU:")
print(stdout.read().decode())

stdin, stdout, stderr = ssh.exec_command("nvidia-smi || echo 'No GPU'")
print("GPU:")
print(stdout.read().decode())

ssh.close()
