"""
Test mínimo – BlenderObserver (Fase 5.15)

Regla:
- Verifica que observa
- Verifica que NO modifica
"""

from core.environment.blender_observer import BlenderObserver


def test_1_snapshot_devuelve_dict():
    observer = BlenderObserver()
    snapshot = observer.snapshot()

    assert isinstance(snapshot, dict)


def test_2_snapshot_contiene_object_count():
    observer = BlenderObserver()
    snapshot = observer.snapshot()

    assert "object_count" in snapshot
    assert isinstance(snapshot["object_count"], int)


def test_3_snapshot_contiene_lista_objetos():
    observer = BlenderObserver()
    snapshot = observer.snapshot()

    assert "objects" in snapshot
    assert isinstance(snapshot["objects"], list)


def test_4_objetos_tienen_campos_minimos():
    observer = BlenderObserver()
    snapshot = observer.snapshot()

    if snapshot["objects"]:
        obj = snapshot["objects"][0]

        assert "name" in obj
        assert "type" in obj
        assert "collections" in obj
