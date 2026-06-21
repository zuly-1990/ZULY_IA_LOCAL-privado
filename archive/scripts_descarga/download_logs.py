import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

print("Descargando logs de Zuly...")
sftp = ssh.open_sftp()
try:
    sftp.get('/opt/zuly/telegram.log', 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/remote_telegram.log')
    sftp.get('/opt/zuly/zuly_autorun.log', 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/remote_autorun.log')
    print("Logs descargados")
except Exception as e:
    print(f"Error: {e}")
sftp.close()
ssh.close()
