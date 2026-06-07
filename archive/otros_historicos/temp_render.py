import bpy
import os

blend_path = os.path.join(os.getcwd(), "ZULY_PROJECTS", "dado_2.blend")

if os.path.exists(blend_path):
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    bpy.context.scene.render.filepath = os.path.join(os.getcwd(), "revisar_dado.png")
    bpy.context.scene.render.image_settings.quality = 85
    bpy.ops.render.render(write_still=True)
    print("[OK] Renderizado guardado: revisar_dado.png")
else:
    print("[ERROR] Archivo no encontrado")
