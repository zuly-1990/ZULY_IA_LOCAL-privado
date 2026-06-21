import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("167.233.69.104", username="root", password="ZULY.server.77")

print("Installing gdown...")
stdin, stdout, stderr = ssh.exec_command("pip3 install gdown")
# Wait for the command to finish
exit_status = stdout.channel.recv_exit_status()
print("Exit status:", exit_status)

print("Checking gdown version...")
stdin, stdout, stderr = ssh.exec_command("python3 -c 'import gdown; print(gdown.__version__)'")
try:
    print(stdout.read().decode('utf-8', errors='ignore'))
except Exception as e:
    print("Stdout read error:", e)

ssh.close()
