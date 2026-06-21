import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

print("Descargando temp_telegram_script.py...")
sftp = ssh.open_sftp()
sftp.get('/opt/zuly/temp_telegram_script.py', 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/temp_telegram_script.py')
sftp.close()
ssh.close()
