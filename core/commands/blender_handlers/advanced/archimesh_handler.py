# core/commands/blender_handlers/advanced/archimesh_handler.py
"""
Handlers para generar elementos arquitectónicos usando Archimesh (add-on nativo de Blender).
Archimesh permite crear puertas, ventanas, escaleras, columnas, estanterías y techos paramétricos.
"""
import bpy
import math
from typing import Dict, Any, Optional
from core.utils.logging import log_info, log_warning, log_error, log_success


def ensure_archimesh_enabled():
    """Asegura que el add-on archimesh esté activado."""
    import addon_utils
    enabled, loaded = addon_utils.check("archimesh")
    if not enabled:
        try:
            addon_utils.enable("archimesh")
            log_info("[ARCHIMESH] Add-on archimesh activado")
        except Exception as e:
            log_error(f"[ARCHIMESH] No se pudo activar archimesh: {e}")
            return False
    return True


def crear_puerta_archimesh(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea una puerta paramétrica usando Archimesh.
    
    Args:
        params: {
            'width': ancho de la puerta (default: 0.9),
            'height': altura (default: 2.1),
            'depth': grosor (default: 0.05),
            'style': estilo ('modern', 'classic', 'panel') (default: 'modern'),
            'location': [x, y, z] posición (default: [0, 0, 0]),
            'rotation': rotación en Z grados (default: 0),
            'door_open': ángerto de apertura en grados (default: 0)
        }
    """
    if not ensure_archimesh_enabled():
        return {"status": "error", "message": "Archimesh no disponible"}
    
    width = params.get('width', 0.9)
    height = params.get('height', 2.1)
    depth = params.get('depth', 0.05)
    style = params.get('style', 'modern')
    location = params.get('location', [0, 0, 0])
    rotation = params.get('rotation', 0)
    door_open = params.get('door_open', 0)
    
    try:
        # Crear puerta usando operador de archimesh
        bpy.ops.archimesh.create_door(
            width=width,
            height=height,
            depth=depth,
            door_open=door_open
        )
        
        door_obj = bpy.context.active_object
        door_obj.name = f"Puerta_{style}_{width}x{height}"
        door_obj.location = location
        door_obj.rotation_euler[2] = math.radians(rotation)
        
        log_success(f"[ARCHIMESH] Puerta creada: {door_obj.name}")
        
        return {
            "status": "success",
            "object_name": door_obj.name,
            "type": "door",
            "width": width,
            "height": height,
            "style": style,
            "location": location
        }
    except Exception as e:
        log_error(f"[ARCHIMESH] Error creando puerta: {e}")
        return {"status": "error", "message": str(e)}


def crear_ventana_archimesh(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea una ventana paramétrica usando Archimesh.
    
    Args:
        params: {
            'width': ancho (default: 1.0),
            'height': altura (default: 1.2),
            'depth': grosor (default: 0.05),
            'style': estilo ('rectangular', 'arch', 'circular') (default: 'rectangular'),
            'location': [x, y, z] (default: [0, 0, 1.0]),
            'rotation': rotación Z grados (default: 0),
            'window_panes': número de paneles (default: 2)
        }
    """
    if not ensure_archimesh_enabled():
        return {"status": "error", "message": "Archimesh no disponible"}
    
    width = params.get('width', 1.0)
    height = params.get('height', 1.2)
    depth = params.get('depth', 0.05)
    style = params.get('style', 'rectangular')
    location = params.get('location', [0, 0, 1.0])
    rotation = params.get('rotation', 0)
    window_panes = params.get('window_panes', 2)
    
    try:
        bpy.ops.archimesh.create_window(
            width=width,
            height=height,
            depth=depth,
            window_panes=window_panes
        )
        
        window_obj = bpy.context.active_object
        window_obj.name = f"Ventana_{style}_{width}x{height}"
        window_obj.location = location
        window_obj.rotation_euler[2] = math.radians(rotation)
        
        log_success(f"[ARCHIMESH] Ventana creada: {window_obj.name}")
        
        return {
            "status": "success",
            "object_name": window_obj.name,
            "type": "window",
            "width": width,
            "height": height,
            "style": style,
            "location": location
        }
    except Exception as e:
        log_error(f"[ARCHIMESH] Error creando ventana: {e}")
        return {"status": "error", "message": str(e)}


def crear_escalera_archimesh(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea una escalera paramétrica usando Archimesh.
    
    Args:
        params: {
            'steps': número de escalones (default: 10),
            'width': ancho (default: 1.0),
            'height': altura total (default: 3.0),
            'style': tipo ('straight', 'u_stairs', 'spiral') (default: 'straight'),
            'location': [x, y, z] (default: [0, 0, 0]),
            'rotation': rotación Z grados (default: 0),
            'step_depth': profundidad de escalón (default: 0.3)
        }
    """
    if not ensure_archimesh_enabled():
        return {"status": "error", "message": "Archimesh no disponible"}
    
    steps = params.get('steps', 10)
    width = params.get('width', 1.0)
    height = params.get('height', 3.0)
    style = params.get('style', 'straight')
    location = params.get('location', [0, 0, 0])
    rotation = params.get('rotation', 0)
    step_depth = params.get('step_depth', 0.3)
    
    try:
        # Archimesh usa diferentes operadores según el tipo de escalera
        if style == 'straight':
            bpy.ops.archimesh.create_straight_stairs(
                step_num=steps,
                width=width,
                height=height,
                step_depth=step_depth
            )
        elif style == 'u_stairs':
            bpy.ops.archimesh.create_u_stairs(
                step_num=steps,
                width=width,
                height=height
            )
        elif style == 'spiral':
            bpy.ops.archimesh.create_spiral_stairs(
                step_num=steps,
                width=width,
                height=height
            )
        else:
            bpy.ops.archimesh.create_straight_stairs(
                step_num=steps,
                width=width,
                height=height
            )
        
        stairs_obj = bpy.context.active_object
        stairs_obj.name = f"Escalera_{style}_{steps}pasos"
        stairs_obj.location = location
        stairs_obj.rotation_euler[2] = math.radians(rotation)
        
        log_success(f"[ARCHIMESH] Escalera creada: {stairs_obj.name}")
        
        return {
            "status": "success",
            "object_name": stairs_obj.name,
            "type": "stairs",
            "steps": steps,
            "style": style,
            "height": height,
            "location": location
        }
    except Exception as e:
        log_error(f"[ARCHIMESH] Error creando escalera: {e}")
        return {"status": "error", "message": str(e)}


def crear_columna_archimesh(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea una columna arquitectónica usando Archimesh.
    
    Args:
        params: {
            'height': altura (default: 3.0),
            'radius': radio (default: 0.15),
            'style': forma ('circular', 'square', 'octogonal') (default: 'circular'),
            'location': [x, y, z] (default: [0, 0, 0]),
            'base': tipo de base ('none', 'simple', 'elaborate') (default: 'simple')
        }
    """
    if not ensure_archimesh_enabled():
        return {"status": "error", "message": "Archimesh no disponible"}
    
    height = params.get('height', 3.0)
    radius = params.get('radius', 0.15)
    style = params.get('style', 'circular')
    location = params.get('location', [0, 0, 0])
    base = params.get('base', 'simple')
    
    try:
        # Archimesh crea columnas con el operador de arco (arch)
        bpy.ops.archimesh.create_column(
            column_height=height,
            column_radius=radius,
            base_type=base
        )
        
        col_obj = bpy.context.active_object
        col_obj.name = f"Columna_{style}_{height}m"
        col_obj.location = location
        
        log_success(f"[ARCHIMESH] Columna creada: {col_obj.name}")
        
        return {
            "status": "success",
            "object_name": col_obj.name,
            "type": "column",
            "height": height,
            "radius": radius,
            "style": style,
            "location": location
        }
    except Exception as e:
        log_error(f"[ARCHIMESH] Error creando columna: {e}")
        return {"status": "error", "message": str(e)}


def crear_estanteria_archimesh(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea una estantería paramétrica usando Archimesh.
    
    Args:
        params: {
            'shelves': número de estantes (default: 5),
            'width': ancho (default: 1.0),
            'height': altura (default: 2.0),
            'depth': profundidad (default: 0.4),
            'location': [x, y, z] (default: [0, 0, 0]),
            'rotation': rotación Z grados (default: 0),
            'thickness': grosor de estantes (default: 0.02)
        }
    """
    if not ensure_archimesh_enabled():
        return {"status": "error", "message": "Archimesh no disponible"}
    
    shelves = params.get('shelves', 5)
    width = params.get('width', 1.0)
    height = params.get('height', 2.0)
    depth = params.get('depth', 0.4)
    location = params.get('location', [0, 0, 0])
    rotation = params.get('rotation', 0)
    thickness = params.get('thickness', 0.02)
    
    try:
        bpy.ops.archimesh.create_shelves(
            shelf_num=shelves,
            width=width,
            height=height,
            depth=depth,
            thickness=thickness
        )
        
        shelf_obj = bpy.context.active_object
        shelf_obj.name = f"Estanteria_{shelves}estantes"
        shelf_obj.location = location
        shelf_obj.rotation_euler[2] = math.radians(rotation)
        
        log_success(f"[ARCHIMESH] Estantería creada: {shelf_obj.name}")
        
        return {
            "status": "success",
            "object_name": shelf_obj.name,
            "type": "shelves",
            "shelves": shelves,
            "width": width,
            "height": height,
            "location": location
        }
    except Exception as e:
        log_error(f"[ARCHIMESH] Error creando estantería: {e}")
        return {"status": "error", "message": str(e)}


def crear_techo_archimesh(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea un techo/paramétrico usando Archimesh.
    
    Args:
        params: {
            'width': ancho (default: 4.0),
            'length': largo (default: 6.0),
            'height': altura máxima (default: 2.5),
            'style': tipo ('gable', 'hip', 'shed') (default: 'gable'),
            'location': [x, y, z] (default: [0, 0, 3.0]),
            'overhang': alero (default: 0.3)
        }
    """
    if not ensure_archimesh_enabled():
        return {"status": "error", "message": "Archimesh no disponible"}
    
    width = params.get('width', 4.0)
    length = params.get('length', 6.0)
    height = params.get('height', 2.5)
    style = params.get('style', 'gable')
    location = params.get('location', [0, 0, 3.0])
    overhang = params.get('overhang', 0.3)
    
    try:
        bpy.ops.archimesh.create_roof(
            width=width,
            length=length,
            height=height,
            roof_type=style,
            overhang=overhang
        )
        
        roof_obj = bpy.context.active_object
        roof_obj.name = f"Techo_{style}_{width}x{length}"
        roof_obj.location = location
        
        log_success(f"[ARCHIMESH] Techo creado: {roof_obj.name}")
        
        return {
            "status": "success",
            "object_name": roof_obj.name,
            "type": "roof",
            "style": style,
            "width": width,
            "length": length,
            "height": height,
            "location": location
        }
    except Exception as e:
        log_error(f"[ARCHIMESH] Error creando techo: {e}")
        return {"status": "error", "message": str(e)}


# Diccionario de handlers exportado para Zuly
ARCHIMESH_HANDLERS = {
    "puerta": crear_puerta_archimesh,
    "ventana": crear_ventana_archimesh,
    "escalera": crear_escalera_archimesh,
    "columna": crear_columna_archimesh,
    "estanteria": crear_estanteria_archimesh,
    "techo": crear_techo_archimesh,
    "door": crear_puerta_archimesh,
    "window": crear_ventana_archimesh,
    "stairs": crear_escalera_archimesh,
    "column": crear_columna_archimesh,
    "shelves": crear_estanteria_archimesh,
    "roof": crear_techo_archimesh
}


def execute_archimesh_command(command_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejecuta un comando Archimesh según el tipo.
    
    Args:
        command_type: tipo de elemento ('puerta', 'ventana', 'escalera', etc.)
        params: parámetros para el elemento
        
    Returns:
        Resultado de la operación
    """
    handler = ARCHIMESH_HANDLERS.get(command_type.lower())
    if not handler:
        available = list(ARCHIMESH_HANDLERS.keys())
        return {
            "status": "error",
            "message": f"Tipo '{command_type}' no reconocido. Disponibles: {available}"
        }
    
    return handler(params)


if __name__ == "__main__":
    # Test rápido si se ejecuta directamente
    print("Archimesh Handler - Test de disponibilidad")
    if ensure_archimesh_enabled():
        print("✅ Archimesh está activo y listo")
    else:
        print("❌ No se pudo activar Archimesh")
