import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='PASSWORD_REMOVED')

test_script = """import google.generativeai as genai
import sys
try:
    genai.configure(api_key='GEMINI_KEY_REMOVED')
    model = genai.GenerativeModel('gemini-2.5-flash')
    resp = model.generate_content('hola')
    print('OK:', resp.text)
except Exception as e:
    print('ERROR:', e)
"""
sftp = ssh.open_sftp()
with sftp.file('/tmp/test_gemini_remote.py', 'w') as f:
    f.write(test_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('python3 /tmp/test_gemini_remote.py')
print("STDOUT:", stdout.read().decode())
print("STDERR:", stderr.read().decode())
ssh.close()
