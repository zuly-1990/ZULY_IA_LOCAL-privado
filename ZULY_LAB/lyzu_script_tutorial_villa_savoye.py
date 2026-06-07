# Script LYZU generado desde YouTube
# Autogenerado - 22 Febrero 2026

from lyzu_core import LYZUCore

# Inicializar LYZU
lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)

# Historial de comandos
commands_executed = []


# Paso 1: R (100% confianza)
# Original: Creación de Columnas Circulares: Shift+A -> Mesh -> Circle. En modo edición: A (seleccionar vértices
result = lyzu.process_user_input("Rotate object")
commands_executed.append(result)

# Paso 2: R (95% confianza)
# Original: Requisito CAD: Los elementos (muros, columnas, vidrios) deben ser polilíneas cerradas para facilitar
result = lyzu.process_user_input("Rotate object")
commands_executed.append(result)

# Paso 3: G (100% confianza)
# Original: Exportación: Guardar como AutoCAD 2018 DXF.
result = lyzu.process_user_input("Move object with parameters {'values': ['2018']}")
commands_executed.append(result)

# Paso 4: G (95% confianza)
# Original: Resolución de Zoom: Si el zoom falla o es errático, usar el punto (.) del teclado numérico para cent
result = lyzu.process_user_input("Move object with parameters {}")
commands_executed.append(result)

# Paso 5: G (100% confianza)
# Original: Organización de Niveles: Importar plantas por separado. Unir segmentos con Ctrl+J. Desplazar niveles
result = lyzu.process_user_input("Move object with parameters {'axes': ['Z']}")
commands_executed.append(result)

# Paso 6: G (100% confianza)
# Original: Fachadas y Cortes: Rotar 90 grados y usar el Snap (Vertex) para alinear las elevaciones con la plant
result = lyzu.process_user_input("Move object with parameters {'values': ['90', '2'], 'axes': ['y', 'y'], 'is_rotation': True}")
commands_executed.append(result)

# Paso 7: G (100% confianza)
# Original: Punto de Pivote: Reubicar el origen del objeto (Set Origin -> Origin to Cursor) usando Shift + Click
result = lyzu.process_user_input("Move object with parameters {'values': ['3']}")
commands_executed.append(result)

# Paso 8: R (100% confianza)
# Original: Modelado de Losas: Seleccionar contorno con Alt + Click (si es polilínea) -> F (Fill) -> E (Extrude)
result = lyzu.process_user_input("Rotate object")
commands_executed.append(result)

# Paso 9: R (95% confianza)
# Original: Separación de Objetos: Seleccionar parte del mesh -> L (Linked) -> P (Separate Selection) para crear
result = lyzu.process_user_input("Rotate object")
commands_executed.append(result)

# Paso 10: G (100% confianza)
# Original: Limpieza de Geometría: Si hay errores en la extrusión, usar 'Merge by Distance' (M o Clic derecho ->
result = lyzu.process_user_input("Move object with parameters {'values': ['0']}")
commands_executed.append(result)

# Paso 11: R (100% confianza)
# Original: Ventanas y Carpintería: Duplicar aristas (Shift+D), extrudir y repetir acciones con Shift+R (Array m
result = lyzu.process_user_input("Rotate object")
commands_executed.append(result)

# Paso 12: R (100% confianza)
# Original: Selección en X-Ray: Usar Alt+Z para ver y seleccionar caras inferiores o traseras ocultas.
result = lyzu.process_user_input("Rotate object")
commands_executed.append(result)

# Paso 13: G (95% confianza)
# Original: Unión Masiva: Ctrl+J para consolidar elementos similares en un solo objeto antes de organizar colecc
result = lyzu.process_user_input("Move object with parameters {}")
commands_executed.append(result)

# Paso 14: G (100% confianza)
# Original: Gestión de Colecciones: Crear carpetas por niveles (Nivel 1, 2, 3) en el Outliner para mantener el o
result = lyzu.process_user_input("Move object with parameters {'values': ['1', '2', '3']}")
commands_executed.append(result)

# Mostrar resultados
print(f"Comandos ejecutados: {len(commands_executed)}")
for i, result in enumerate(commands_executed, 1):
    print(f"  {i}. Status: {result.get('status', 'UNKNOWN')}")
