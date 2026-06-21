import paramiko

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

def search_remote():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=user, password=password, timeout=10)
        print("--- Buscando GEMINI_API_KEY en /opt/zuly ---")
        stdin, stdout, stderr = ssh.exec_command("grep -rnw '/opt/zuly' -e 'GEMINI_API_KEY' -e 'google.generativeai' -e 'import google.generativeai' -e 'genai.configure' --include='*.py' --include='*.env' --include='*.ini' 2>/dev/null")
        out = stdout.read().decode('utf-8').strip()
        if out:
            print(out)
        else:
            print("No se encontraron referencias directas de código a Gemini API en archivos .py o .env")
            
        print("\n--- Listando archivos .env ---")
        stdin, stdout, stderr = ssh.exec_command("find /opt/zuly -name '*.env' -o -name '.env*' 2>/dev/null")
        out2 = stdout.read().decode('utf-8').strip()
        if out2:
            print(out2)
            # Imprimir contenido de los .env (ocultando un poco si hay keys)
            for file in out2.split('\n'):
                if file.strip():
                    stdin, stdout, stderr = ssh.exec_command(f"cat {file.strip()}")
                    print(f"Contenido de {file}:")
                    print(stdout.read().decode('utf-8').strip())
        else:
            print("No se encontraron archivos .env")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    search_remote()
