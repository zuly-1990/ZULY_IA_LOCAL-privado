import paramiko
import time

def run_ssh_commands():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('167.233.69.104', username='root', password='ZULY.server.77', timeout=15)
        
        commands = [
            "cd /opt/zuly && git pull origin main",
            "pkill -f zuly_scraper_arquitectura.py || true",
            "nohup bash -c 'export PYTHONPATH=/opt/zuly && python3 /opt/zuly/core/learning/zuly_scraper_arquitectura.py' > /opt/zuly/scraper.log 2>&1 &"
        ]

        for cmd in commands:
            print(f"Ejecutando: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            out = stdout.read().decode('utf-8', errors='ignore').strip()
            err = stderr.read().decode('utf-8', errors='ignore').strip()
            if out: print("Stdout:", out)
            if err: print("Stderr:", err)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    run_ssh_commands()
