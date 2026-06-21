import paramiko
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

print("Buscando archivos .blend...")
sftp = ssh.open_sftp()
archivos = ['/opt/zuly/planos_extruidos.blend', '/opt/zuly/Planos y premodelado_extraido/primer_nivel_v08_levantado.blend']

encontrado = False
for arch in archivos:
    try:
        sftp.stat(arch)
        nombre = os.path.basename(arch)
        sftp.get(arch, f'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/{nombre}')
        print(f"¡ENCONTRADO Y DESCARGADO! -> {nombre}")
        encontrado = True
    except FileNotFoundError:
        pass

if not encontrado:
    print("Ningún archivo .blend de la extrusión fue encontrado en esas rutas.")

sftp.close()
ssh.close()
