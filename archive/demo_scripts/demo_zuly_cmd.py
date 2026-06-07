"""
Script interactivo para dar órdenes naturales a Zuly desde la terminal.
"""
from core.dialog import parse_user_input
from core.diagnostics.diagnostics import validate_params
from core.commands.blender_commands import execute_blender_action

def main():
    print("Bienvenido a Zuly CMD. Escribe una orden natural (ej: crea un cubo rojo rotando en eje z). Escribe 'salir' para terminar.")
    from core.learning_feedback import FeedbackLogger
    logger = FeedbackLogger()
    while True:
        orden = input(">> ")
        if orden.strip().lower() == "salir":
            print("Saliendo...")
            break
        params = parse_user_input(orden)
        valido, advertencias = validate_params(params)
        params['advertencias'] = advertencias
        print(f"Parámetros interpretados: {params}")
        execute_blender_action(params)
        if advertencias:
            print("Advertencias:")
            for adv in advertencias:
                print(f"- {adv}")
        # Feedback inteligente: registrar orden, resultado y sugerencia
        resultado = "ok" if valido else "error"
        sugerencia = advertencias[0] if advertencias else None
        logger.log(orden, params.get('intent'), params, resultado, sugerencia)
        # Si la orden es válida y es crear cubo, ejecuta Blender
        if params['intent'] == 'create_object' and params['object'] == 'cube':
            import subprocess
            print("Ejecutando Blender para crear el cubo real...")
            blender_path = "blender\\v3\\blender-3.6.0-zuly\\blender.exe"
            # Usar parámetros avanzados
            pos = params.get('position', (0,0,0))
            rot = params.get('rotation', (0,0,0))
            sca = params.get('scale', (1,1,1))
            color = params.get('color', 'gris')
            # Script Python para Blender
            blender_py = (
                f"import bpy; "
                f"bpy.ops.object.select_all(action='SELECT'); "
                f"bpy.ops.object.delete(use_global=False); "
                f"cubo = bpy.ops.mesh.primitive_cube_add(location={pos}, rotation=({rot[0]}*3.1416/180,{rot[1]}*3.1416/180,{rot[2]}*3.1416/180), scale={sca}); "
                f"obj = bpy.context.active_object; "
                f"mat = bpy.data.materials.new(name='mat_zuly'); "
                f"mat.diffuse_color = (1,0,0,1) if '{color}'=='rojo' else (0,0,1,1) if '{color}'=='azul' else (0,1,0,1) if '{color}'=='verde' else (0.5,0.5,0.5,1); "
                f"obj.data.materials.append(mat); "
                f"bpy.ops.wm.save_as_mainfile(filepath='export/cubo_zuly.blend')"
            )
            cmd = [
                blender_path,
                "--background",
                "--python-expr",
                blender_py
            ]
            try:
                subprocess.run(cmd, check=True)
                print("✅ Cubo creado y guardado en export/cubo_zuly.blend")
            except Exception as e:
                print(f"❌ Error ejecutando Blender: {e}")

if __name__ == "__main__":
    main()
