import bpy

# Abrir el archivo .blend de la animación
bpy.ops.wm.open_mainfile(filepath=r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/animacion_cubo_amarillo_rotando_z.blend")

# Configurar render para video (FFmpeg, formato MP4)
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'
bpy.context.scene.render.filepath = r"c:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/pruebas_cubo/animacion_cubo_amarillo_rotando_z.mp4"

# Renderizar animación como video
bpy.ops.render.render(animation=True)

print("Video de animación generado en export/pruebas_cubo/animacion_cubo_amarillo_rotando_z.mp4")
