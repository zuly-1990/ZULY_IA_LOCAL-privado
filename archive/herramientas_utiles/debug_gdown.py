import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("167.233.69.104", username="root", password="ZULY.server.77")

script = """
import gdown
print('Empezando descarga...')
res = gdown.download('https://drive.google.com/file/d/1zsSqLzypiDiPgBfmCZXaYqI2DGgRI5Tf/view?usp=sharing', '/opt/zuly/descargas/debug_file.dwg', fuzzy=True)
print('Resultado:', res)
"""

stdin, stdout, stderr = ssh.exec_command(f"python3 -c \"{script}\"")
print("STDOUT:", stdout.read().decode())
print("STDERR:", stderr.read().decode())
ssh.close()
