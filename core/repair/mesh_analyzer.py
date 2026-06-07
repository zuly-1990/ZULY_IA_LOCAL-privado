"""
mesh_analyzer.py — Detector de problemas en mallas 3D
Usa bmesh para análisis preciso sin modificar la malla original.
"""

from typing import Optional, Dict, Any

# Lazy imports de Blender (solo en modo real)
bpy = None
bmesh = None

def _import_blender():
    """Importa bpy y bmesh solo cuando se necesitan (modo real)."""
    global bpy, bmesh
    if bpy is None:
        import bpy as _bpy
        import bmesh as _bmesh
        bpy = _bpy
        bmesh = _bmesh


def analyze_mesh(obj_name: str, adapter: Optional[Any] = None) -> Dict:
    """
    Analiza una malla en busca de problemas geométricos.

    Args:
        obj_name: Nombre del objeto en Blender
        adapter: Adaptador (si es None o mock, retorna datos simulados)

    Returns:
        Dict con los problemas encontrados
    """
    # Modo mock
    if adapter is None or getattr(adapter, 'is_mock', False):
        return _mock_analysis(obj_name)

    # Modo real
    return _real_analysis(obj_name)


def _mock_analysis(obj_name: str) -> Dict:
    """Simula análisis para pruebas sin Blender."""
    is_dirty = any(k in obj_name.lower() for k in ['dirty', 'bad', 'issue', 'defect'])
    return {
        'duplicated_verts': 4 if is_dirty else 0,
        'inverted_normals': is_dirty,
        'non_manifold_edges': 3 if is_dirty else 0,
        'holes': 2 if is_dirty else 0,
        'degenerate_faces': 1 if is_dirty else 0,
        'total_issues': 10 if is_dirty else 0
    }


def _real_analysis(obj_name: str) -> Dict:
    """Análisis real usando Blender API y bmesh."""
    _import_blender()  # Import lazy de bpy/bmesh
    obj = bpy.data.objects.get(obj_name)

    if not obj or obj.type != 'MESH':
        return _empty_result()

    # Guardar estado original
    original_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
    original_selection = bpy.context.selected_objects.copy()

    try:
        # Preparar objeto para edición
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

        # 1. Vértices duplicados (por posición)
        pos_count = {}
        for v in bm.verts:
            pos = tuple(round(c, 6) for c in v.co)
            pos_count[pos] = pos_count.get(pos, 0) + 1
        duplicated_verts = sum(max(0, count - 1) for count in pos_count.values())

        # 2. Caras degeneradas (área casi cero)
        degenerate_faces = sum(1 for f in bm.faces if f.calc_area() < 0.00001)

        # 3. Bordes no-manifold
        non_manifold_edges = sum(1 for e in bm.edges if not e.is_manifold)

        # 4. Agujeros (bordes frontera)
        holes = sum(1 for e in bm.edges if e.is_boundary)

        # 5. Normales invertidas (heurística por dirección al centro)
        inverted_normals = False
        if bm.faces and bm.verts:
            center = sum((v.co for v in bm.verts), bm.verts[0].co * 0) / len(bm.verts)
            inward_count = sum(
                1 for f in bm.faces
                if f.normal.dot(f.calc_center_median() - center) < 0
            )
            inverted_normals = inward_count > len(bm.faces) / 2

        total_issues = (
            duplicated_verts +
            (1 if inverted_normals else 0) +
            non_manifold_edges +
            holes +
            degenerate_faces
        )

        return {
            'duplicated_verts': duplicated_verts,
            'inverted_normals': inverted_normals,
            'non_manifold_edges': non_manifold_edges,
            'holes': holes,
            'degenerate_faces': degenerate_faces,
            'total_issues': total_issues
        }

    finally:
        # Restaurar estado original
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        for ob in original_selection:
            if ob.name in bpy.data.objects:
                ob.select_set(True)
        if original_mode != 'OBJECT':
            try:
                bpy.ops.object.mode_set(mode=original_mode)
            except RuntimeError:
                pass


def _empty_result() -> Dict:
    """Retorna resultado vacío para objetos inválidos."""
    return {
        'duplicated_verts': 0,
        'inverted_normals': False,
        'non_manifold_edges': 0,
        'holes': 0,
        'degenerate_faces': 0,
        'total_issues': 0
    }
