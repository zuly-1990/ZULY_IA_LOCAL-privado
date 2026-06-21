import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("=== LISTANDO NOMBRES DE OBJETOS IMPORTADOS DEL DXF ===")

script = """
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.dxf(filepath='/opt/zuly/planos_temp/Planos y premodelado/01 Primer Nivel v08.dxf')
for obj in bpy.context.scene.objects:
    print(f'OBJ: {obj.name} | Type: {obj.type}')
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/inspect_dxf_names.py', 'w') as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('blender -b -P /tmp/inspect_dxf_names.py')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
