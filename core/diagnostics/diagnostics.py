# diagnostics.py
"""
Valida parámetros, registra orden, acción y errores/adverts.
"""

def validate_params(params):
    """Valida objeto y valores seguros."""
    objetos_validos = ["cube", "sphere", "plane", "monkey", "cylinder", "circle"]
    colores_validos = ["rojo", "azul", "verde", "amarillo", "gris", "blanco", "negro"]
    tamanos_validos = ["pequeño", "grande", "normal"]
    advertencias = []
    valido = True
    if params["object"] not in objetos_validos:
        advertencias.append(f"Objeto '{params['object']}' no reconocido. Usando 'cube' por defecto.")
        params["object"] = "cube"
        valido = False
    if params["color"] and params["color"] not in colores_validos:
        advertencias.append(f"Color '{params['color']}' no reconocido. Usando 'gris' por defecto.")
        params["color"] = "gris"
        valido = False
    if params["size"] and params["size"] not in tamanos_validos:
        advertencias.append(f"Tamaño '{params['size']}' no reconocido. Usando 'normal' por defecto.")
        params["size"] = "normal"
        valido = False
    if params["count"] < 1:
        advertencias.append("Cantidad menor a 1. Usando 1 por defecto.")
        params["count"] = 1
        valido = False
    return valido, advertencias

def log_action(orden, resultado, errores):
    """Registra en consola y log."""
    print(f"Orden: {orden}\nResultado: {resultado}\nErrores: {errores}")
