import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("=== DETECTANDO CAPAS EN EL DXF Y COMPILADO ===")

# Script para contar objetos por su nombre de capa original en Blender despues de importar
script = """
import bpy
import os

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Importar
bpy.ops.import_scene.dxf(filepath='/opt/zuly/planos_temp/Planos y premodelado/01 Primer Nivel v08.dxf')

print('---OBJETOS IMPORTADOS POR NOMBRE/CAPA---')
objects = list(bpy.context.scene.objects)
print(f'Total objetos importados: {len(objects)}')
# Agrupar por capa/nombre
capas = {}
for obj in objects:
    name = obj.name.split('|')[0] if '|' in obj.name else 'Sin_Capa'
    capas[name] = capas.get(name, 0) + 1
    
for capa, count in sorted(capas.items(), key=lambda x: x[1], reverse=True):
    print(f'Capa: {capa} | Cantidad de objetos: {count}')
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/inspect_dxf_layers.py', 'w') as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('blender -b -P /tmp/inspect_dxf_layers.py')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
