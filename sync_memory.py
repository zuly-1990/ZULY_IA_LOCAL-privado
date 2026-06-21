import paramiko
import os

print("="*50)
print("🧠 ZULY MEMORY SYNC (Linux -> Local)")
print("="*50)

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

remote_db = "/opt/zuly/bitacora/memory.db"
local_dir = "bitacora"
local_db = os.path.join(local_dir, "memory.db")

if not os.path.exists(local_dir):
    os.makedirs(local_dir)

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=password)
    
    sftp = ssh.open_sftp()
    
    # Check if remote memory exists
    try:
        sftp.stat(remote_db)
        print("Descargando memoria desde la Nube...")
        sftp.get(remote_db, local_db)
        print("✅ Memoria sincronizada con éxito. Ahora puedes hacer 'git commit' para respaldarla en GitHub.")
    except FileNotFoundError:
        print("⚠️ Zuly aún no ha creado recuerdos en la Nube (memory.db no existe).")
    
    sftp.close()
    ssh.close()
except Exception as e:
    print(f"❌ Error sincronizando memoria: {e}")
