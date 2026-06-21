import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

remote_path = '/opt/zuly/resultados_masivos_v9/Villa_Savoye_V9_Modelado3D_intento_3.blend'
local_path = 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/Villa_Savoye_V9_Modelado3D_intento_3.blend'

print(f"Descargando {remote_path} -> {local_path}...")
sftp = ssh.open_sftp()
sftp.get(remote_path, local_path)
print("¡Archivo 3D V9 descargado con éxito!")
sftp.close()
ssh.close()
