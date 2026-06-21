import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

stdin, stdout, stderr = ssh.exec_command('find / -name "*Planos y premodelado.rar" 2>/dev/null')
print("FIND RESULT:")
print(stdout.read().decode())

ssh.close()
