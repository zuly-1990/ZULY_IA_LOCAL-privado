import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

print("Verificando si planos_extruidos.blend existe...")
stdin, stdout, stderr = ssh.exec_command('ls -la /opt/zuly/planos_extruidos.blend')
out = stdout.read()
if len(out) > 0:
    print("El archivo existe. Descargándolo al escritorio...")
    sftp = ssh.open_sftp()
    sftp.get('/opt/zuly/planos_extruidos.blend', 'c:/Users/Admin/Desktop/planos_extruidos_zuly.blend')
    sftp.close()
    print("¡Descarga completada!")
else:
    print("El archivo no existe.")

ssh.close()
