import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

print("Descargando Primer_Nivel_Extruido.blend...")
sftp = ssh.open_sftp()
sftp.get('/opt/zuly/Primer_Nivel_Extruido.blend', 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/Primer_Nivel_Extruido.blend')
print("¡Archivo descargado con éxito!")
sftp.close()
ssh.close()
