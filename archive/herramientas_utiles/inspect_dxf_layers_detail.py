import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("=== VERIFICANDO PARTICIPACIÓN DE CAPAS EN EL OBJETO FINAL ===")

script = """
import bpy

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Importar DXF
bpy.ops.import_scene.dxf(filepath='/opt/zuly/planos_temp/Planos y premodelado/02 Segundo Nivel v02.dxf')

print('---DETALLE DE CAPAS ANTES DE UNIR---')
for obj in list(bpy.context.scene.objects):
    if obj.type == 'CURVE':
        # Convertir temporalmente a mesh para contar vertices de esta capa
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.convert(target='MESH')
        mesh_obj = bpy.context.active_object
        print(f'CAPA/OBJETO: {mesh_obj.name} | Vertices: {len(mesh_obj.data.vertices)}')
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/inspect_dxf_layers_detail.py', 'w') as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('blender -b -P /tmp/inspect_dxf_layers_detail.py')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
