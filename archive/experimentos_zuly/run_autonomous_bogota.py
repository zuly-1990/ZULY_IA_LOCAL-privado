import os
import time
import paramiko
from core.external.multi_api_orchestrator import MultiAPIOrchestrator
from core.cognition.evaluators.render_evaluator import RenderEvaluator

ip = "167.233.69.104"
user = "root"
password = "ZULY.server.77"

def run_autonomous_loop():
    print("="*60)
    print("🏙️ INICIANDO MAPEO AUTÓNOMO: PLAZA DE BOLÍVAR, BOGOTÁ")
    print("="*60)

    api = MultiAPIOrchestrator()
    evaluator = RenderEvaluator()
    
    max_iter = 5
    
    # Prompt inicial
    historial_prompt = """
Eres el Arquitecto de Código de ZULY.
Objetivo: Mapear la Plaza de Bolívar en Bogotá en 3D (aprox lat 4.5981, lon -74.0760).
Instrucciones obligatorias:
1. Escribe un script en Python para Blender.
2. Usa `urllib.request` para hacer una consulta a la API de Overpass y obtener los polígonos de los edificios ("way[\"building\"]") en un bounding box pequeño alrededor de la plaza (ej: 4.596, -74.078, 4.600, -74.074).
3. Parsea el JSON, crea mallas en Blender para cada edificio usando la lat/lon escalada a coordenadas XY locales, y extrúyelas (Z) para darles volumen.
4. Crea una cámara ortográfica o perspectiva mirando hacia abajo para encuadrar la plaza.
5. Usa el motor CYCLES en CPU, ajusta `bpy.context.scene.render.engine = 'CYCLES'`, y renderiza a `/opt/zuly/bogota_render.png`.
6. Guarda el archivo como `/opt/zuly/bogota_map.blend`.
SOLO DEVUELVE EL CÓDIGO PYTHON.
"""

    for i in range(1, max_iter + 1):
        print(f"\n--- 🔄 ITERACIÓN {i}/{max_iter} ---")
        
        print("🧠 1. DeepSeek está programando el generador geográfico...")
        codigo_ia = api.call_coder_model(historial_prompt)
        
        if '```python' in codigo_ia:
            codigo_ia = codigo_ia.split('```python')[1].split('```')[0].strip()
        elif '```' in codigo_ia:
            codigo_ia = codigo_ia.split('```')[1].strip()
            
        with open('generado_bogota.py', 'w', encoding='utf-8') as f:
            f.write(codigo_ia)
            
        print("🌐 2. Enviando código a servidor remoto...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip, username=user, password=password, timeout=15)
            sftp = ssh.open_sftp()
            sftp.put('generado_bogota.py', '/opt/zuly/generado_bogota.py')
            
            print("⏳ 3. Ejecutando Blender remotamente (Descargando datos, modelando y renderizando con Cycles)...")
            # Removido el -f 1 porque el script python debe hacer el render
            stdin, stdout, stderr = ssh.exec_command("/opt/blender/blender --background --python /opt/zuly/generado_bogota.py")
            
            out = stdout.read().decode('utf-8').strip()
            err = stderr.read().decode('utf-8').strip()
            
            # Intentar descargar el render
            render_local = f"bogota_render_iter_{i}.png"
            try:
                sftp.get('/opt/zuly/bogota_render.png', render_local)
                print(f"📥 Render descargado: {render_local}")
                render_ok = True
            except:
                print("⚠️ Blender falló o no generó el render.")
                render_ok = False
                
            sftp.close()
            ssh.close()
            
        except Exception as e:
            print(f"Error de conexión: {e}")
            render_ok = False
            err = str(e)
            
        print("👁️ 4. Evaluando resultados con Gemini Vision...")
        if render_ok:
            contexto = {"target_concept": "Mapa 3D exacto de Plaza de Bolívar, Bogotá, con la catedral y el capitolio."}
            evaluacion = evaluator.evaluate(render_local, context=contexto)
            feedback = evaluacion['findings'][-1]
            
            print("--- FEEDBACK DE GEMINI ---")
            print(feedback)
            print("--------------------------")
            
            if evaluacion['score'] > 0.8 and "APROBADO" in feedback.upper():
                print("✅ ¡GEMINI HA APROBADO EL MAPA! Ciclo completado con éxito.")
                break
            else:
                print("❌ Gemini requiere mejoras. Retroalimentando a DeepSeek...")
                historial_prompt = f"""
Has escrito el script anterior, pero Gemini Visión ha detectado los siguientes errores visuales o faltas en el render:
{feedback}

Por favor, re-escribe TODO el código de Blender para arreglar estos problemas. Ajusta la lógica de OpenStreetMap o el render de la cámara según corresponda.
SOLO DEVUELVE EL CÓDIGO PYTHON.
"""
        else:
            print("❌ El script falló o no generó imagen. Retroalimentando errores técnicos a DeepSeek...")
            # Limitar el error para no desbordar el prompt
            err_cortado = err[-1000:] if len(err) > 1000 else err
            historial_prompt = f"""
Tu código falló durante la ejecución en Blender o no guardó la imagen correctamente en `/opt/zuly/bogota_render.png`.
Error de consola:
{err_cortado}

Corrige el error en el script de python y envíalo completo nuevamente.
SOLO DEVUELVE CÓDIGO.
"""

if __name__ == "__main__":
    run_autonomous_loop()
