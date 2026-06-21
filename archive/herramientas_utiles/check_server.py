import paramiko

def execute_remote_command(ip, user, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=user, password=password, timeout=10)
        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        return out, err
    except Exception as e:
        return "", str(e)
    finally:
        ssh.close()

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

# Check for blender processes
out, err = execute_remote_command(ip, user, password, "ps aux | grep -i blender | grep -v grep")
print("=== Blender Processes ===")
print(out if out else "No blender processes found.")

# Look for recent files or directories that might be the test functions
out, err = execute_remote_command(ip, user, password, "find /root /home /var/www -maxdepth 3 -type d -name '*prueb*' -o -name '*test*' -o -name '*blender*' 2>/dev/null")
print("\n=== Found directories/files related to prueba/test/blender ===")
print(out if out else "No related files found.")
