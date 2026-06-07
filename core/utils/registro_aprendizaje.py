import datetime
import os

def registrar_aprendizaje(accion, script, parametros, resultado, archivos, observaciones, leccion):
    fecha = datetime.datetime.now().strftime('%Y-%m-%d')
    nombre_archivo = f"bitacora/REGISTRO_APRENDIZAJE_{fecha}.md"
    contenido = f"""# Registro de Aprendizaje Zuly\n\n**Fecha:** {fecha}\n**Acción ejecutada:** {accion}\n**Script generado:** {script}\n**Parámetros usados:**\n{parametros}\n**Resultado:**\n{resultado}\n**Archivos generados:**\n{archivos}\n**Observaciones:**\n{observaciones}\n**Lección aprendida:**\n{leccion}\n\n---\n*Registro generado automáticamente por GitHub Copilot en modo agente.*\n"""
    
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    
    with open(ruta, 'a', encoding='utf-8') as f:
        f.write(contenido)
    print(f"Registro de aprendizaje guardado en {ruta}")

# Ejemplo de uso (solo para pruebas exitosas)
# registrar_aprendizaje(
#     accion="Crear 15 cubos rojos y 15 azules, renderizar y guardar escena",
#     script="crear_15_rojos_15_azules.py",
#     parametros="- 15 cubos rojos (ubicación: eje x, y=0)\n- 15 cubos azules (ubicación: eje x, y=4)\n- Materiales: Rojo y Azul\n- Cámara: posición (15, -20, 15)",
#     resultado="Cubos creados y coloreados correctamente\nRender generado: 15_rojos_15_azules_render.png\nArchivo .blend guardado: 15_rojos_15_azules.blend",
#     archivos="- export/pruebas_cubo/15_rojos_15_azules_render.png\n- export/pruebas_cubo/15_rojos_15_azules.blend",
#     observaciones="El script fue corregido para limpiar la escena y asegurar la cámara\nEl render y el archivo .blend se generaron sin errores",
#     leccion="Es fundamental limpiar la escena y asignar la cámara antes de renderizar\nLos scripts automáticos permiten reproducir y documentar cada acción"
# )
