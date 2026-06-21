import paramiko

def execute_remote_command(ip, user, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=user, password=password, timeout=10)
        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except Exception as e:
        return str(e)
    finally:
        ssh.close()

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

files_to_read = [
    "/opt/zuly/ZULY_LAB/RESUMEN_5_PRUEBAS_REALES.txt",
    "/opt/zuly/bitacora/REPORTE_PRUEBAS_BLENDER_EJECUTADAS.md",
    "/opt/zuly/REPORTE_10_PRUEBAS_FINALES.md",
    "/opt/zuly/bitacora/REPORTE_PRUEBA_REAL_INTEGRACION.md"
]

for f in files_to_read:
    print(f"=== {f} ===")
    out = execute_remote_command(ip, user, password, f"head -n 25 {f}")
    if not out:
        out = "Empty or not found."
    print(out)
    print("\n")

