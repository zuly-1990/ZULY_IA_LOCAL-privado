import paramiko

def execute_remote_command(ip, user, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=user, password=password, timeout=10)
        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode().strip()
        return out
    except Exception as e:
        return str(e)
    finally:
        ssh.close()

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

print("=== Docker Containers ===")
print(execute_remote_command(ip, user, password, "docker ps -a"))

print("\n=== Blender installation ===")
print(execute_remote_command(ip, user, password, "which blender || echo 'Blender not in PATH'"))

print("\n=== Broader search for test/prueba/blender ===")
print(execute_remote_command(ip, user, password, "find / -maxdepth 4 -type d -iname '*blender*' -o -iname '*prueb*' -o -iname '*test*' 2>/dev/null"))
