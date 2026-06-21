import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('167.233.69.104', username='root', password='ZULY.server.77')

script = """
import bpy

print("⚙️ ZULY: Activando addon DXF...")
bpy.ops.preferences.addon_enable(module="io_import_dxf")

print("🗑️ ZULY: Limpiando escena por defecto...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print("📂 ZULY: Importando DXF...")
ruta_dxf = "/opt/zuly/planos_temp/Planos y premodelado/01 Primer Nivel v08.dxf"
try:
    bpy.ops.import_scene.dxf(filepath=ruta_dxf)
    print("✅ DXF importado correctamente.")
except Exception as e:
    print(f"⚠️ Error en importación DXF: {e}")

print("🔁 ZULY: Convirtiendo curvas a mallas...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.convert(target='MESH')

print("🧩 ZULY: Uniendo todas las mallas en un solo objeto...")
bpy.ops.object.join()

print("📏 ZULY: Entrando a modo edición para extruir paredes a 3 metros de altura...")
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 3)})

print("↩️ ZULY: Regresando a modo objeto...")
bpy.ops.object.mode_set(mode='OBJECT')

print("💾 ZULY: Guardando archivo...")
bpy.ops.wm.save_as_mainfile(filepath="/opt/zuly/planos_extruidos.blend")
"""

sftp = ssh.open_sftp()
with sftp.file('/opt/zuly/zuly_dxf_script.py', 'w') as f:
    f.write(script)
sftp.close()

print("Ejecutando script de Zuly en Blender en el servidor...")
stdin, stdout, stderr = ssh.exec_command('blender -b -P /opt/zuly/zuly_dxf_script.py')
print("STDOUT:", stdout.read().decode())
print("STDERR:", stderr.read().decode())

ssh.close()
