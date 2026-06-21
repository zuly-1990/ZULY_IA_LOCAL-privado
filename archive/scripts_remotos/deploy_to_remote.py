import os
import paramiko

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"
remote_base = "/opt/zuly"

local_base = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"

files_to_sync = [
    "core/cognition/zuly_memory_rag.py",
    "core/decision/confidence_router.py",
    "core/external/multi_api_orchestrator.py",
    "core/external/telegram_listener.py",
    "core/assembly/geometry_enforcer.py",
    "core/cognition/rag_3d_manager.py",
    "core/cognition/evaluators/multi_layer_vision.py",
    "core/cognition/evaluators/render_evaluator.py",
    "core/learning/knowledge_ingestor.py",
    "core/repair/auto_repairer.py",
    "core/assembly/handler_factory.py",
    "core/assembly/mass_processor.py",
    "core/assembly/mass_processor_v2.py",
    "core/assembly/mass_processor_v3.py",
    "compile_blend_v9.py",
    "web_ui/zuly_tutorial_autonomia.html"
]

def deploy_files():
    print(f"Conectando a {ip}...")
    transport = paramiko.Transport((ip, 22))
    transport.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=password)

    for file_path in files_to_sync:
        local_path = os.path.join(local_base, file_path).replace("\\", "/")
        remote_path = f"{remote_base}/{file_path}"
        remote_dir = os.path.dirname(remote_path)
        
        # Crear directorio remoto si no existe
        print(f"Asegurando directorio remoto: {remote_dir}")
        ssh.exec_command(f"mkdir -p {remote_dir}")
        
        if os.path.exists(local_path):
            print(f"Subiendo {local_path} -> {remote_path}")
            sftp.put(local_path, remote_path)
        else:
            print(f"ADVERTENCIA: Archivo local no encontrado: {local_path}")
            
    # Instalar dependencias en el servidor remoto
    print("Ejecutando instalación de dependencias en el servidor remoto...")
    # Asumimos que pip3 o el entorno virtual en /opt/zuly existe. Si no, usamos el python global.
    stdin, stdout, stderr = ssh.exec_command("pip3 install sentence-transformers groq openai gdown")
    
    print("Archivos transferidos exitosamente. La instalación se ejecutó en segundo plano.")
    
    sftp.close()
    transport.close()
    ssh.close()

if __name__ == "__main__":
    deploy_files()
