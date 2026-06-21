import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("=== INSPECCIONANDO ZULY_MAESTRO.blend ===")

script = """
import bpy
print('---OBJETOS MESH EN ZULY_MAESTRO---')
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print(f'OBJ: {obj.name} | V: {len(obj.data.vertices)} | F: {len(obj.data.polygons)} | Z: {round(obj.dimensions.z, 3)}')
print('---FIN---')
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/inspect_maestro.py', 'w') as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('blender -b "/opt/zuly/ZULY_MAESTRO.blend" -P /tmp/inspect_maestro.py')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
