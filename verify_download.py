import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("167.233.69.104", username="root", password="ZULY.server.77")

print("--- ÚLTIMOS LOGS DE TELEGRAM ---")
stdin, stdout, stderr = ssh.exec_command("tail -n 15 /opt/zuly/telegram.log")
print(stdout.read().decode())

print("\n--- ARCHIVOS EN LA CARPETA DE DESCARGAS ---")
stdin, stdout, stderr = ssh.exec_command("ls -lh /opt/zuly/descargas/")
print(stdout.read().decode())

ssh.close()
