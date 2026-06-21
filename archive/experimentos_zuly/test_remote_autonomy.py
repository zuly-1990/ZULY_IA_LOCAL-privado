import paramiko

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

test_script = """
cd /opt/zuly
python3 -c "
import sys
import os

try:
    from core.decision.confidence_router import ConfidenceRouter
    from core.external.multi_api_orchestrator import MultiAPIOrchestrator
    from core.repair.auto_repairer import AutoRepairer
    from core.learning.knowledge_ingestor import KnowledgeIngestor
    
    print('✅ Módulos de Autonomía importados correctamente en el servidor.')
    
    router = ConfidenceRouter()
    print('✅ ConfidenceRouter instanciado.')
    
    route, ctx = router.route_command('crear un muro de 5 metros')
    print(f'✅ Prueba de enrutamiento exitosa. Ruta seleccionada: {route}')
    
    api = MultiAPIOrchestrator()
    print('✅ MultiAPIOrchestrator listo.')
    
    repairer = AutoRepairer()
    print('✅ AutoRepairer listo.')
    
    print('🚀 TODAS LAS PRUEBAS REMOTAS HAN FINALIZADO CON ÉXITO.')
except Exception as e:
    import traceback
    print(f'❌ ERROR en el servidor remoto: {e}')
    traceback.print_exc()
"
"""

def test_remote():
    print(f"Conectando a {ip} para ejecutar pruebas remotas...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=user, password=password, timeout=15)
        stdin, stdout, stderr = ssh.exec_command(test_script)
        out = stdout.read().decode('utf-8').strip()
        err = stderr.read().decode('utf-8').strip()
        
        print("\n--- SALIDA DEL SERVIDOR REMOTO ---")
        if out:
            print(out)
        if err:
            print("\nERRORES:")
            print(err)
    except Exception as e:
        print(f"Error de conexión: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    test_remote()
