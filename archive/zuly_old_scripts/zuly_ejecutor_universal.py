#!/usr/bin/env python3
"""
ZULY - EJECUTOR UNIVERSAL
UN SOLO script que ejecuta TODAS las operaciones
Sin crear .blend nuevos
"""

import subprocess
import time
from pathlib import Path
import tempfile
import sys

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_3.blend")

def obtener_comando():
    """Obtener comando del usuario"""
    print("\n" + "="*70)
    print("🤖 ZULY - EJECUTOR UNIVERSAL")
    print("="*70)
    print("\nOpciones disponibles:")
    print("  1. escalar <valor>       - Escalar el cubo (ej: 1.5)")
    print("  2. rotar <grados>        - Rotar en Z (ej: 45)")
    print("  3. color_rojo_x          - Cambiar agujero X a rojo")
    print("  4. color_azul_z          - Cambiar agujero Z a azul")
    print("  5. color_verde           - Cambiar cubo a verde")
    print("  6. bevel <valor>         - Cambiar bevel (ej: 0.3)")
    print("  7. limpiar               - Restaurar cubo original")
    print("  8. info                  - Ver estado actual")
    
    cmd = input("\n📝 Comando: ").strip().lower()
    return cmd

def ejecutar_operacion(comando):
    """Ejecutar operación en cubo_3.blend"""
    
    # Parsear comando
    partes = comando.split()
    op = partes[0] if partes else ""
    param = partes[1] if len(partes) > 1 else None
    
    print(f"\n[ZULY] Ejecutando: {comando}")
    
    # Crear script dinámico basado en operación
    if op == "escalar":
        valor = float(param) if param else 1.5
        blender_code = f"""
import bpy
filepath = r'C:\\\\Users\\\\Admin\\\\Desktop\\\\ZULY_IA_LOCAL\\\\ZULY_PROJECTS\\\\cubo_3.blend'
bpy.ops.wm.open_mainfile(filepath=filepath)
obj = bpy.data.objects.get('CuboBase')
if obj:
    obj.scale = ({valor}, {valor}, {valor})
    print("[OK] Escalado a {valor}")
bpy.ops.wm.save_mainfile(filepath=filepath)
"""
    
    elif op == "rotar":
        grados = float(param) if param else 45
        import math
        rad = math.radians(grados)
        blender_code = f"""
import bpy
import math
filepath = r'C:\\\\Users\\\\Admin\\\\Desktop\\\\ZULY_IA_LOCAL\\\\ZULY_PROJECTS\\\\cubo_3.blend'
bpy.ops.wm.open_mainfile(filepath=filepath)
obj = bpy.data.objects.get('CuboBase')
if obj:
    obj.rotation_euler[2] = {rad}
    print("[OK] Rotado {grados} grados")
bpy.ops.wm.save_mainfile(filepath=filepath)
"""
    
    elif op == "color_rojo_x":
        blender_code = """
import bpy
filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_3.blend'
bpy.ops.wm.open_mainfile(filepath=filepath)
obj = bpy.data.objects.get('CuboBase')
if obj and len(obj.data.materials) > 1:
    mat = obj.data.materials[1]
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1.0, 0.0, 0.0, 1.0)
    print("[OK] Agujero X: ROJO")
bpy.ops.wm.save_mainfile(filepath=filepath)
"""
    
    elif op == "color_azul_z":
        blender_code = """
import bpy
filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_3.blend'
bpy.ops.wm.open_mainfile(filepath=filepath)
obj = bpy.data.objects.get('CuboBase')
if obj and len(obj.data.materials) > 2:
    mat = obj.data.materials[2]
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.0, 0.3, 1.0, 1.0)
    print("[OK] Agujero Z: AZUL")
bpy.ops.wm.save_mainfile(filepath=filepath)
"""
    
    elif op == "info":
        blender_code = """
import bpy
filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_3.blend'
bpy.ops.wm.open_mainfile(filepath=filepath)
print("[INFO] Escena actual:")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print(f"  - {obj.name}: scale={obj.scale}, rotation={obj.rotation_euler}")
        if obj.data.materials:
            print(f"    Materiales: {[m.name for m in obj.data.materials]}")
"""
    
    else:
        print(f"❌ Comando no reconocido: {op}")
        return False
    
    # Ejecutar script
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(blender_code)
            script_file = Path(f.name)
        
        cmd = [str(BLENDER_PATH), "--background", "--python", str(script_file)]
        result = subprocess.run(cmd, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Operación completada")
            return True
        else:
            print(f"❌ Error en ejecución")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    finally:
        if script_file.exists():
            script_file.unlink()

# LOOP PRINCIPAL
print("\n🎯 ZULY EN MODO INTERACTIVO")
print("Trabajando SOLO con: cubo_3.blend")

while True:
    try:
        comando = obtener_comando()
        
        if comando.lower() == "salir" or comando.lower() == "exit":
            print("\n👋 ZULY terminado")
            break
        
        ejecutar_operacion(comando)
        print("\n💡 Recarga en Blender (F5) para ver cambios")
        
    except KeyboardInterrupt:
        print("\n\n👋 ZULY terminado")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
