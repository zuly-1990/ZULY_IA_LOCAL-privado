import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

print("=== BUSCANDO TODAS LAS CAPAS DEFINIDAS EN EL ARCHIVO DXF ===")

script = """
import re

dxf_path = "/opt/zuly/planos_temp/Planos y premodelado/01 Primer Nivel v08.dxf"
layers = set()
with open(dxf_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
    for i in range(len(lines) - 1):
        if lines[i].strip() == "8": # Group code 8 is for layer names in DXF
            layers.add(lines[i+1].strip())

print("Capas encontradas en el DXF:")
for layer in sorted(layers):
    print(f" - {layer}")
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/extract_dxf_layers.py', 'w') as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('python3 /tmp/extract_dxf_layers.py')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
