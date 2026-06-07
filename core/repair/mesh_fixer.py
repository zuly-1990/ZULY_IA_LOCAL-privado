"""
mesh_fixer.py — Corrector de problemas en mallas 3D
Usa operadores nativos de Blender para máxima fiabilidad.
"""

from typing import Optional, Dict, Any

# Lazy import de Blender (solo en modo real)
bpy = None

def _import_blender():
    """Importa bpy solo cuando se necesita (modo real)."""
    global bpy
    if bpy is None:
        import bpy as _bpy
        bpy = _bpy


def fix_mesh(obj_name: str, adapter: Optional[Any] = None) -> Dict:
    """
    Repara una malla aplicando operaciones estándar.

    Args:
        obj_name: Nombre del objeto en Blender
        adapter: Adaptador (si es None o mock, simula reparación)

    Returns:
        Dict con resultados de la reparación
    """
    # Modo mock
    if adapter is None or getattr(adapter, 'is_mock', False):
        return _mock_repair(obj_name)

    # Modo real
    return _real_repair(obj_name)


def _mock_repair(obj_name: str) -> Dict:
    """Simula reparación para pruebas sin Blender."""
    is_dirty = any(k in obj_name.lower() for k in ['dirty', 'bad', 'issue', 'defect'])
    return {
        'merged_verts': 4 if is_dirty else 0,
        'fixed_normals': True,
        'filled_holes': 2 if is_dirty else 0,
        'success': True
    }


def _real_repair(obj_name: str) -> Dict:
    """Reparación real usando operadores de Blender."""
    _import_blender()  # Import lazy de bpy
    obj = bpy.data.objects.get(obj_name)

    if not obj or obj.type != 'MESH':
        return {
            'merged_verts': 0,
            'fixed_normals': False,
            'filled_holes': 0,
            'success': False
        }

    # Guardar estado original
    original_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
    original_selection = bpy.context.selected_objects.copy()

    try:
        # Preparar objeto
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Contar estado inicial
        bpy.ops.object.mode_set(mode='OBJECT')
        initial_verts = len(obj.data.vertices)
        initial_faces = len(obj.data.polygons)

        # Entrar en modo edición y reparar
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        # Operaciones de reparación
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.fill_holes(sides=0)
        bpy.ops.mesh.delete_loose()

        # Volver a objeto para contar resultados
        bpy.ops.object.mode_set(mode='OBJECT')
        final_verts = len(obj.data.vertices)
        final_faces = len(obj.data.polygons)

        merged_verts = max(0, initial_verts - final_verts)
        filled_holes = max(0, final_faces - initial_faces)

        return {
            'merged_verts': merged_verts,
            'fixed_normals': True,
            'filled_holes': filled_holes,
            'success': True
        }

    except Exception as e:
        return {
            'merged_verts': 0,
            'fixed_normals': False,
            'filled_holes': 0,
            'success': False,
            'error': str(e)
        }

    finally:
        # Restaurar estado original
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            for ob in original_selection:
                if ob.name in bpy.data.objects:
                    ob.select_set(True)
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=original_mode)
        except RuntimeError:
            pass
