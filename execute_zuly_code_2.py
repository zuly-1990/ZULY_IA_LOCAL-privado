import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

print("Ejecutando script de Zuly en Blender en el servidor...")
stdin, stdout, stderr = ssh.exec_command('blender -b -P /opt/zuly/zuly_dxf_script.py')
out = stdout.read().decode('utf-8', errors='ignore')
err = stderr.read().decode('utf-8', errors='ignore')
print("STDOUT:", out)
print("STDERR:", err)

ssh.close()
