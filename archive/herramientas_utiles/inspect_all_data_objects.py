import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("=== INSPECCIONANDO TODOS LOS BLOQUES DE DATOS DE OBJETOS EN EL MAESTRO ===")

script = """
import bpy
print('---DATOS DE OBJETOS DE MEMORIA (bpy.data.objects)---')
for obj in bpy.data.objects:
    print(f'NAME: {obj.name} | Type: {obj.type} | Linked to scene: {obj.name in bpy.context.scene.objects}')
print('---FIN---')
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/inspect_all_data_objects.py', 'w') as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('blender -b "/opt/zuly/planos_temp/Planos y premodelado/Villa Saboye v05 Pre Modelado.blend" -P /tmp/inspect_all_data_objects.py')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
