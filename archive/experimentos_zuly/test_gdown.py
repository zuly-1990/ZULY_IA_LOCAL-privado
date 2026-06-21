import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("167.233.69.104", username="root", password="ZULY.server.77")

script = """
import gdown
import os
print("Testing gdown...")
url = "https://drive.google.com/file/d/1zsSqLzypiDiPgBfmCZXaYqI2DGgRI5Tf/view?usp=sharing"
out = "/opt/zuly/descargas/test_download.dwg"
res = gdown.download(url, out, fuzzy=True)
print("Result:", res)
"""

stdin, stdout, stderr = ssh.exec_command(f"python3 -c '{script}'")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
