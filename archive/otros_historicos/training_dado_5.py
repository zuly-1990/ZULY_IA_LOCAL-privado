
import sys
import os
from pathlib import Path

# Configurar paths de ZULY
zuly_path = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
sys.path.append(str(zuly_path))

import bpy
from lyzu_core import LYZUCore
from core.utils.logging import log_info, log_success

print("\n" + "="*60)
print("ENTRENAMIENTO ZULY: CASO 1 - EL DADO 5")
print("="*60)

# Limpiar escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Iniciar ZULY
lyzu = LYZUCore(mode='reactive')

try:
    # 1. CREAR DADO
    print("\n[1/4] Solicitando creación de dado...")
    res1 = lyzu.process_user_input("Crea un dado de parqués")
    
    # 2. RENOMBRAR
    print("\n[2/4] Renombrando a 'dado 5'...")
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.name = "dado 5"
            log_success(f"Objeto renombrado a: {obj.name}")
            break
            
    # 3. GUARDAR
    print("\n[3/4] Guardando en ZULY_PROJECTS...")
    projects_dir = zuly_path / "ZULY_PROJECTS"
    projects_dir.mkdir(parents=True, exist_ok=True)
    filepath = str(projects_dir / "dado_5.blend")
    
    res_save = lyzu.process_user_input(f"Guarda la escena en {filepath}")
    
    if os.path.exists(filepath):
        print(f"\n✅ ARCHIVO CREADO EXITOSAMENTE: {filepath}")
        print(f"   Objetos en escena: {[obj.name for obj in bpy.data.objects]}")
    else:
        print("\n❌ ERROR: El archivo no se generó.")

except Exception as e:
    print(f"\n❌ ERROR CRÍTICO EN SESIÓN: {e}")

print("\n" + "="*60)
print("FIN DE SESIÓN - ESPERANDO VISTO BUENO")
print("="*60)
