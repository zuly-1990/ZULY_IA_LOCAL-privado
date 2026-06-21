import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

print("Ejecutando blender...")
stdin, stdout, stderr = ssh.exec_command('blender -b -P /opt/zuly/temp_telegram_script.py')
salida = stdout.read().decode('utf-8', 'ignore')

with open("c:/Users/Admin/Desktop/ZULY_IA_LOCAL/blender_output.txt", "w", encoding="utf-8") as f:
    f.write(salida)

print("Salida guardada en blender_output.txt")
ssh.close()
