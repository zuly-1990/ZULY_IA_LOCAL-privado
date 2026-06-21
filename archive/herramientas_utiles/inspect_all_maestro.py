import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("=== LISTANDO TODOS LOS OBJETOS EN VILLA SABOYE MAESTRO ===")

script = """
import bpy
print('---TODOS LOS OBJETOS EN EL MAESTRO---')
for obj in bpy.context.scene.objects:
    print(f'OBJ: {obj.name} | Type: {obj.type} | Parent: {obj.parent.name if obj.parent else "None"} | Location: {obj.location}')
print('---FIN---')
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/inspect_all_maestro.py', 'w') as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('blender -b "/opt/zuly/planos_temp/Planos y premodelado/Villa Saboye v05 Pre Modelado.blend" -P /tmp/inspect_all_maestro.py')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
