import os
import subprocess
import glob
import sys

# Asegurar que se puede importar desde la raíz del proyecto
sys.path.append('/opt/zuly')

from core.external.multi_api_orchestrator import MultiAPIOrchestrator

def extract_python_code(response: str) -> str:
    if "```python" in response:
        return response.split("```python")[1].split("```")[0].strip()
    return response.strip()

def process_dxf(dxf_path: str, output_dir: str, orchestrator: MultiAPIOrchestrator):
    basename = os.path.basename(dxf_path)
    blend_name = basename.replace('.dxf', '_extruido.blend')
    output_path = os.path.join(output_dir, blend_name)
    
    print(f"\n" + "="*50)
    print(f"⚙️ ZULY MASIVO: Iniciando {basename}")
    print("="*50)
    
    prompt = f"""Eres Zuly, la Arquitecta Maestra de Código.
Tu tarea es generar un script de Python 100% funcional para Blender 3.6 que haga lo siguiente de manera autónoma:
1. Importar `bpy` y cualquier librería necesaria.
2. Limpiar toda la escena por defecto (`bpy.ops.object.select_all(action='SELECT')` y `delete`).
3. Activar el addon DXF: `bpy.ops.preferences.addon_enable(module='io_import_dxf')`
4. Verificar si el archivo existe antes de importar. La ruta es EXACTA: `{dxf_path}`
5. Importar el archivo usando `bpy.ops.import_scene.dxf(filepath=...)`.
6. OBLIGATORIO: Encontrar todas las curvas importadas, seleccionarlas, convertirlas a MESH y unirlas en un solo objeto (Mesh Activo).
7. OBLIGATORIO: Entrar en modo edición y extruir toda la malla 3.0 metros hacia arriba (Z global).
8. PRUEBAS DE PERFECCIÓN (Añade esta lógica en Python al final de tu script):
   - Extrae el conteo de vértices y polígonos del objeto activo.
   - Si `len(objeto.data.vertices) == 0` o `len(objeto.data.polygons) == 0`: lanza `ValueError("Fallo: La malla está vacía sin vértices o caras.")`
   - Si `objeto.dimensions.z < 2.9`: lanza `ValueError("Fallo: La dimensión Z es menor a 3 metros. La extrusión falló.")`
9. Si aprueba, guarda el archivo en: `{output_path}` usando `bpy.ops.wm.save_as_mainfile()`.
10. Imprime mensajes en la consola con `print()` para que yo sepa el progreso.

Devuelve ÚNICAMENTE el código Python en un bloque ```python ... ```. No digas nada más.
"""
    
    max_retries = 3
    current_prompt = prompt
    
    for attempt in range(1, max_retries + 1):
        print(f"⏳ [Intento {attempt}/{max_retries}] Pidiendo a Gemini generar el código Blender...")
        
        # Llamar a Gemini (Usa advanced model con rotación)
        response = orchestrator.call_advanced_model(current_prompt)
        code = extract_python_code(response)
        
        # Escribir a script temporal
        safe_name = basename.replace(' ', '_')
        temp_script = f"/opt/zuly/temp_mass_{safe_name}.py"
        with open(temp_script, "w", encoding="utf-8") as f:
            f.write(code)
            
        print(f"🚀 [Intento {attempt}/{max_retries}] Ejecutando en Sandbox de Blender...")
        cmd = ["blender", "-b", "-P", temp_script]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_path):
            print(f"✅ ¡PERFECTO! El modelo pasó todas las pruebas matemáticas y se guardó en: {output_path}")
            return True
        else:
            print(f"❌ Error en intento {attempt}. Blender se quejó o las pruebas de perfección fallaron.")
            # Capturar logs para corrección
            error_output = result.stdout[-2000:] + "\nSTDERR:\n" + result.stderr[-1000:]
            
            # Preparar prompt de autocorrección
            current_prompt = f"""El script que generaste para '{basename}' falló con este error al ejecutarse en Blender.
El código de salida fue {result.returncode}.

LOGS DEL ERROR:
{error_output}

Por favor, como experta Arquitecta Zuly, analiza detenidamente el error, corrige tu código Python y vuelve a intentarlo.
RECUERDA:
- Siempre incluir `import bpy` y `bpy.ops.preferences.addon_enable(module='io_import_dxf')` antes de importar.
- Ruta DXF origen: `{dxf_path}`
- Ruta BLEND destino: `{output_path}`
- Asegurar que seleccionas los objetos correctos tras la importación.

Responde ÚNICAMENTE con el nuevo código Python corregido dentro de un bloque ```python ... ```.
"""
            
    print(f"⚠️ [ZULY] Me rindo con {basename}. Agoté mis {max_retries} intentos de auto-corrección.")
    return False

def main():
    print("==================================================")
    print("🚀 ZULY V7: INICIANDO PIPELINE DE PRUEBAS MASIVAS 🚀")
    print("==================================================")
    
    orchestrator = MultiAPIOrchestrator()
    if not orchestrator.gemini_keys:
        print("❌ Error: No se encontraron llaves de Gemini en el orquestador.")
        return
        
    dxf_folder = "/opt/zuly/planos_temp/Planos y premodelado/"
    output_folder = "/opt/zuly/resultados_masivos/"
    
    os.makedirs(output_folder, exist_ok=True)
    
    dxf_files = glob.glob(os.path.join(dxf_folder, "*.dxf"))
    if not dxf_files:
        print(f"❌ No se encontraron archivos DXF en: {dxf_folder}")
        return
        
    # Filtrar para procesar solo unos pocos si es necesario, pero el usuario quiere "pruebas masivas".
    # Procesaremos todos!
    print(f"📂 ¡Encontrados {len(dxf_files)} planos arquitectónicos DXF para modelar!")
    
    exitos = 0
    for dxf in dxf_files:
        success = process_dxf(dxf, output_folder, orchestrator)
        if success:
            exitos += 1
            
    print("==================================================")
    print(f"🏆 REPORTE FINAL: {exitos}/{len(dxf_files)} Modelos 3D generados con Perfección Absoluta.")
    print(f"Los resultados están en: {output_folder}")
    print("==================================================")

if __name__ == "__main__":
    main()
