import bpy
import addon_utils
import json

addon_name = 'archimesh'
default_addons = ['archipack_20', 'measureit']

results = {}

print("--- INICIANDO VERIFICACIÓN DE ADDONS ---")

# Verificar Archimesh
state = addon_utils.check(addon_name)
if not state[0]:
    print(f"Activando {addon_name}...")
    try:
        # En Blender 3.6 enable no usa default_val
        addon_utils.enable(addon_name)
        # Forzar guardado de preferencias
        bpy.ops.wm.save_userpref()
        results[addon_name] = 'ACTIVATED'
    except Exception as e:
        results[addon_name] = f'ERROR: {str(e)}'
else:
    results[addon_name] = 'ALREADY_ACTIVE'

# Verificar otros
for addon in default_addons:
    state = addon_utils.check(addon)
    results[addon] = 'ACTIVE' if state[0] else 'NOT_INSTALLED'

print('ADDON_CHECK_START')
print(json.dumps(results))
print('ADDON_CHECK_END')
