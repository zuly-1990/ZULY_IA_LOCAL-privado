import os
import paramiko

def run():
    ip = "167.233.69.104"
    user = "root"
    password = "ZULY.server.77"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=password)
    
    script = """
import bpy
print('---OBJETOS MESH---')
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print(f'OBJ: {obj.name} | V: {len(obj.data.vertices)} | F: {len(obj.data.polygons)} | Z: {obj.dimensions.z}')
print('---FIN---')
"""
    # Escribir el script en remoto
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/inspect.py', 'w') as f:
        f.write(script)
    sftp.close()
    
    stdin, stdout, stderr = ssh.exec_command('blender -b "/opt/zuly/planos_temp/Planos y premodelado/Villa Saboye v05 Pre Modelado.blend" -P /tmp/inspect.py')
    print(stdout.read().decode())
    print("ERR", stderr.read().decode())
    
run()
