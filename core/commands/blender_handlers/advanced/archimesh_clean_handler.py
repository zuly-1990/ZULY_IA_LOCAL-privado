# core/commands/blender_handlers/advanced/archimesh_clean_handler.py
"""
Handler limpio de Archimesh para Zuly.
Separación clara entre archimesh y fallback, con validación y organización.
"""
import bpy
import math
from typing import Dict, Any, Optional, List
from core.capabilities.archimesh_capability import verificar as verificar_archimesh
from core.utils.logging import log_info, log_success, log_error, log_warning


# ============ 1. VALIDACIÓN ============

def validar_objeto(obj, nombre_esperado: str = None) -> Dict[str, Any]:
    """
    Valida que el objeto creado sea válido.
    
    Args:
        obj: El objeto Blender a validar
        nombre_esperado: Nombre que debería tener
        
    Returns:
        Dict con status y mensaje
    """
    if obj is None:
        return {"valid": False, "error": "No se creó ningún objeto"}
    
    if not hasattr(obj, 'type'):
        return {"valid": False, "error": "Objeto no tiene atributo 'type'"}
    
    if obj.type != 'MESH':
        return {"valid": False, "error": f"Objeto es tipo '{obj.type}', se esperaba 'MESH'"}
    
    if not hasattr(obj, 'name'):
        return {"valid": False, "error": "Objeto no tiene nombre"}
    
    # Validar que tenga geometría
    if not obj.data or not hasattr(obj.data, 'vertices'):
        return {"valid": False, "error": "Objeto no tiene geometría válida"}
    
    if len(obj.data.vertices) == 0:
        return {"valid": False, "error": "Objeto tiene 0 vértices"}
    
    return {"valid": True, "obj": obj, "name": obj.name}


# ============ 2. FALLBACKS ============

def _crear_puerta_fallback(width: float = 0.9, height: float = 2.1, 
                           location: tuple = (0, 0, 0)) -> Any:
    """Fallback: Puerta simple con primitivas."""
    # Marco
    bpy.ops.mesh.primitive_cube_add(location=location, size=1)
    marco = bpy.context.active_object
    marco.scale = (width/2 + 0.05, 0.05, height/2 + 0.05)
    marco.name = "Puerta_Marco_Fallback"
    
    # Hoja
    bpy.ops.mesh.primitive_cube_add(location=(location[0], location[1] + 0.05, location[2] + height/2))
    hoja = bpy.context.active_object
    hoja.scale = (width/2 - 0.02, 0.02, height/2 - 0.02)
    hoja.name = "Puerta_Hoja_Fallback"
    
    # Picaporte
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02, 
        depth=0.08, 
        location=(location[0] + width/3, location[1] + 0.08, location[2] + height/2)
    )
    pica = bpy.context.active_object
    pica.rotation_euler[0] = 1.5708
    pica.name = "Puerta_Picaporte_Fallback"
    
    return hoja  # Retornar la hoja como objeto principal


def _crear_ventana_fallback(width: float = 1.2, height: float = 1.0,
                            location: tuple = (0, 0, 1.0)) -> Any:
    """Fallback: Ventana simple."""
    # Marco
    bpy.ops.mesh.primitive_cube_add(location=location)
    marco = bpy.context.active_object
    marco.scale = (width/2 + 0.03, 0.03, height/2 + 0.03)
    marco.name = "Ventana_Marco_Fallback"
    
    # Vidrio
    bpy.ops.mesh.primitive_cube_add(location=location)
    vidrio = bpy.context.active_object
    vidrio.scale = (width/2 - 0.01, 0.01, height/2 - 0.01)
    vidrio.name = "Ventana_Vidrio_Fallback"
    
    return vidrio


def _crear_escalera_fallback(steps: int = 10, width: float = 1.0, 
                             total_height: float = 3.0, location: tuple = (0, 0, 0)) -> Any:
    """Fallback: Escalera simple con cubos."""
    depth = 0.3
    step_height = total_height / steps
    
    for i in range(steps):
        bpy.ops.mesh.primitive_cube_add(location=(
            location[0], 
            location[1] + i * depth, 
            location[2] + i * step_height + step_height/2
        ))
        step = bpy.context.active_object
        step.scale = (width/2, depth/2, step_height/2)
        step.name = f"Escalon_Fallback_{i+1}"
    
    # Retornar el último escalón como referencia
    return step


def _crear_columna_fallback(radius: float = 0.15, height: float = 3.0,
                            location: tuple = (0, 0, 1.5)) -> Any:
    """Fallback: Columna simple."""
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=location)
    col = bpy.context.active_object
    col.name = "Columna_Fallback"
    return col


def _crear_habitacion_fallback(width: float = 4.0, length: float = 5.0, height: float = 3.0,
                               location: tuple = (0, 0, 0)) -> Any:
    """Fallback: Habitación simple (5 paredes)."""
    paredes = []
    
    # Piso
    bpy.ops.mesh.primitive_cube_add(location=(location[0], location[1], location[2]))
    piso = bpy.context.active_object
    piso.scale = (width/2, length/2, 0.05)
    piso.name = "Habitacion_Piso_Fallback"
    paredes.append(piso)
    
    # 4 paredes
    wall_configs = [
        ((0, -length/2, height/2), (width/2, 0.05, height/2), "Pared_Front"),
        ((0, length/2, height/2), (width/2, 0.05, height/2), "Pared_Back"),
        ((-width/2, 0, height/2), (0.05, length/2, height/2), "Pared_Left"),
        ((width/2, 0, height/2), (0.05, length/2, height/2), "Pared_Right"),
    ]
    
    for loc, scale, name in wall_configs:
        bpy.ops.mesh.primitive_cube_add(location=(location[0]+loc[0], location[1]+loc[1], location[2]+loc[2]))
        pared = bpy.context.active_object
        pared.scale = scale
        pared.name = f"{name}_Fallback"
        paredes.append(pared)
    
    # Techo
    bpy.ops.mesh.primitive_cube_add(location=(location[0], location[1], location[2]+height))
    techo = bpy.context.active_object
    techo.scale = (width/2, length/2, 0.05)
    techo.name = "Habitacion_Techo_Fallback"
    paredes.append(techo)
    
    return paredes[0]  # Retornar el piso como referencia


# ============ 3. ARCHIMESH METHODS ============

def _crear_puerta_archimesh(width: float = 0.9, height: float = 2.1,
                            location: tuple = (0, 0, 0), rotation: float = 0) -> Any:
    """Archimesh: Puerta paramétrica."""
    bpy.ops.archimesh.create_door(width=width, height=height, depth=0.05)
    obj = bpy.context.active_object
    obj.location = location
    obj.rotation_euler[2] = math.radians(rotation)
    return obj


def _crear_ventana_archimesh(width: float = 1.2, height: float = 1.0,
                             location: tuple = (0, 0, 1.0), rotation: float = 0) -> Any:
    """Archimesh: Ventana paramétrica."""
    bpy.ops.archimesh.create_window(width=width, height=height, depth=0.05)
    obj = bpy.context.active_object
    obj.location = location
    obj.rotation_euler[2] = math.radians(rotation)
    return obj


def _crear_escalera_archimesh(steps: int = 10, width: float = 1.0,
                              total_height: float = 3.0, location: tuple = (0, 0, 0)) -> Any:
    """Archimesh: Escalera recta."""
    bpy.ops.archimesh.create_straight_stairs(step_num=steps, width=width, height=total_height)
    obj = bpy.context.active_object
    obj.location = location
    return obj


def _crear_columna_archimesh(radius: float = 0.15, height: float = 3.0,
                             location: tuple = (0, 0, 1.5)) -> Any:
    """Archimesh: Columna clásica."""
    bpy.ops.archimesh.create_column(column_height=height, column_radius=radius)
    obj = bpy.context.active_object
    obj.location = location
    return obj


def _crear_habitacion_archimesh(width: float = 4.0, length: float = 5.0,
                               location: tuple = (0, 0, 0)) -> Any:
    """Archimesh: Habitación completa."""
    bpy.ops.archimesh.create_room(width=width, length=length, height=3.0)
    obj = bpy.context.active_object
    obj.location = location
    return obj


# ============ 4. ORGANIZACIÓN POST-CREACIÓN ============

def organizar_objeto_archimesh(obj, nombre_base: str, tipo: str) -> Dict[str, Any]:
    """
    Organiza y renombra objetos creados por Archimesh.
    Archimesh crea múltiples objetos desordenados - esto los limpia.
    
    Args:
        obj: Objeto principal
        nombre_base: Nombre base para renombrar
        tipo: Tipo de elemento (door, window, etc.)
        
    Returns:
        Dict con objetos organizados
    """
    if obj is None:
        return {"error": "No hay objeto para organizar"}
    
    objetos_relacionados = []
    
    # Buscar objetos creados recientemente por archimesh
    # (generalmente tienen nombres genéricos o empiezan con el tipo)
    for o in bpy.context.scene.objects:
        if o.select_get() or (o.name.startswith(("Door", "Window", "Stairs", "Column", "Room"))):
            objetos_relacionados.append(o)
    
    # Renombrar el principal
    obj.name = f"{nombre_base}_{tipo}_Main"
    
    # Renombrar relacionados
    for i, o in enumerate(objetos_relacionados):
        if o != obj:
            o.name = f"{nombre_base}_{tipo}_Part_{i+1}"
    
    # Mover a colección organizada
    collection_name = f"ZULY_{tipo.upper()}s"
    if collection_name not in bpy.data.collections:
        col = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(col)
    else:
        col = bpy.data.collections[collection_name]
    
    # Vincular objetos a la colección
    for o in objetos_relacionados:
        if o.name not in col.objects:
            col.objects.link(o)
            # Desvincular de la colección principal si está ahí
            if o.name in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.unlink(o)
    
    return {
        "main_object": obj.name,
        "related_objects": [o.name for o in objetos_relacionados if o != obj],
        "collection": collection_name,
        "count": len(objetos_relacionados)
    }


# ============ 5. HANDLERS PÚBLICOS (API ZULY) ============

def crear_puerta(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler Zuly: Crea una puerta (Archimesh o Fallback).
    
    Args:
        params: {
            'width': ancho (default: 0.9),
            'height': altura (default: 2.1),
            'location': (x, y, z),
            'rotation': grados (default: 0)
        }
    """
    width = params.get('width', 0.9)
    height = params.get('height', 2.1)
    location = params.get('location', (0, 0, 0))
    rotation = params.get('rotation', 0)
    nombre = params.get('name', 'Puerta_Zuly')
    
    try:
        if verificar_archimesh():
            obj = _crear_puerta_archimesh(width, height, location, rotation)
            method = "archimesh"
        else:
            obj = _crear_puerta_fallback(width, height, location)
            method = "fallback"
        
        # Validar
        val = validar_objeto(obj, nombre)
        if not val["valid"]:
            return {"status": "error", "message": val["error"]}
        
        # Organizar
        org = organizar_objeto_archimesh(obj, nombre, "door")
        
        return {
            "status": "success",
            "method": method,
            "object_name": obj.name,
            "organized": org,
            "validation": val
        }
        
    except Exception as e:
        log_error(f"[ARCHIMESH_HANDLER] Error creando puerta: {e}")
        return {"status": "error", "message": str(e)}


def crear_ventana(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handler Zuly: Crea una ventana."""
    width = params.get('width', 1.2)
    height = params.get('height', 1.0)
    location = params.get('location', (0, 0, 1.0))
    rotation = params.get('rotation', 0)
    nombre = params.get('name', 'Ventana_Zuly')
    
    try:
        if verificar_archimesh():
            obj = _crear_ventana_archimesh(width, height, location, rotation)
            method = "archimesh"
        else:
            obj = _crear_ventana_fallback(width, height, location)
            method = "fallback"
        
        val = validar_objeto(obj, nombre)
        if not val["valid"]:
            return {"status": "error", "message": val["error"]}
        
        org = organizar_objeto_archimesh(obj, nombre, "window")
        
        return {
            "status": "success",
            "method": method,
            "object_name": obj.name,
            "organized": org
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}


def crear_escalera(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handler Zuly: Crea una escalera."""
    steps = params.get('steps', 10)
    width = params.get('width', 1.0)
    total_height = params.get('height', 3.0)
    location = params.get('location', (0, 0, 0))
    nombre = params.get('name', 'Escalera_Zuly')
    
    try:
        if verificar_archimesh():
            obj = _crear_escalera_archimesh(steps, width, total_height, location)
            method = "archimesh"
        else:
            obj = _crear_escalera_fallback(steps, width, total_height, location)
            method = "fallback"
        
        val = validar_objeto(obj, nombre)
        if not val["valid"]:
            return {"status": "error", "message": val["error"]}
        
        org = organizar_objeto_archimesh(obj, nombre, "stairs")
        
        return {
            "status": "success",
            "method": method,
            "object_name": obj.name,
            "organized": org
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}


def crear_columna(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handler Zuly: Crea una columna."""
    radius = params.get('radius', 0.15)
    height = params.get('height', 3.0)
    location = params.get('location', (0, 0, 1.5))
    nombre = params.get('name', 'Columna_Zuly')
    
    try:
        if verificar_archimesh():
            obj = _crear_columna_archimesh(radius, height, location)
            method = "archimesh"
        else:
            obj = _crear_columna_fallback(radius, height, location)
            method = "fallback"
        
        val = validar_objeto(obj, nombre)
        if not val["valid"]:
            return {"status": "error", "message": val["error"]}
        
        org = organizar_objeto_archimesh(obj, nombre, "column")
        
        return {
            "status": "success",
            "method": method,
            "object_name": obj.name,
            "organized": org
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}


def crear_habitacion(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handler Zuly: Crea una habitación completa."""
    width = params.get('width', 4.0)
    length = params.get('length', 5.0)
    location = params.get('location', (0, 0, 0))
    nombre = params.get('name', 'Habitacion_Zuly')
    
    try:
        if verificar_archimesh():
            obj = _crear_habitacion_archimesh(width, length, location)
            method = "archimesh"
        else:
            obj = _crear_habitacion_fallback(width, length, 3.0, location)
            method = "fallback"
        
        # Para habitaciones, validamos diferente (puede ser una colección de objetos)
        if isinstance(obj, list):
            val = validar_objeto(obj[0], nombre) if obj else {"valid": False, "error": "Lista vacía"}
        else:
            val = validar_objeto(obj, nombre)
        
        if not val["valid"]:
            return {"status": "error", "message": val["error"]}
        
        # Organizar
        org = organizar_objeto_archimesh(obj[0] if isinstance(obj, list) else obj, nombre, "room")
        
        return {
            "status": "success",
            "method": method,
            "object_name": obj[0].name if isinstance(obj, list) else obj.name,
            "organized": org
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============ 6. HANDLERS REGISTRADOS ============

HANDLERS = {
    "archimesh_door": crear_puerta,
    "archimesh_window": crear_ventana,
    "archimesh_stairs": crear_escalera,
    "archimesh_column": crear_columna,
    "archimesh_room": crear_habitacion,
    # Aliases en español
    "archimesh_puerta": crear_puerta,
    "archimesh_ventana": crear_ventana,
    "archimesh_escalera": crear_escalera,
    "archimesh_columna": crear_columna,
    "archimesh_habitacion": crear_habitacion,
}


def execute(handler_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Punto de entrada principal para Zuly.
    
    Args:
        handler_name: Nombre del handler (ej: "archimesh_door")
        params: Parámetros para el handler
        
    Returns:
        Resultado de la operación
    """
    if handler_name not in HANDLERS:
        return {
            "status": "error",
            "message": f"Handler '{handler_name}' no encontrado",
            "available": list(HANDLERS.keys())
        }
    
    return HANDLERS[handler_name](params)
