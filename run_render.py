import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=user, password=password)

# Subir render_compiled.py
sftp = ssh.open_sftp()
sftp.put("render_compiled.py", "/opt/zuly/render_compiled.py")
sftp.close()

# Ejecutar render
print("=== EJECUTANDO RENDER EN EL SERVIDOR ===")
stdin, stdout, stderr = ssh.exec_command("blender -b -P /opt/zuly/render_compiled.py")
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))

# Descargar el render generado localmente
print("\n=== DESCARGANDO IMAGEN RENDERIZADA ===")
sftp = ssh.open_sftp()
try:
    sftp.get("/opt/zuly/resultados_masivos_v8/Villa_Saboye_V8_Render.png", "Villa_Saboye_V8_Render.png")
    print("Descargado con éxito: Villa_Saboye_V8_Render.png")
except Exception as e:
    print(f"Error descargando render: {e}")
sftp.close()

ssh.close()
