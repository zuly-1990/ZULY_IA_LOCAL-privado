"""
Test mínimo – BlenderSemanticObserver (Fase 5.16)

Regla:
- Verifica interpretación semántica
- Verifica seguridad (no side effects)
"""

from core.environment.blender_semantic_observer import BlenderSemanticObserver


def test_1_analyze_returns_dict():
    observer = BlenderSemanticObserver()
    result = observer.analyze({})
    assert isinstance(result, dict)


def test_2_analyze_handles_empty_or_no_blender():
    observer = BlenderSemanticObserver()
    
    # Caso 1: Vacío
    res_empty = observer.analyze({})
    assert res_empty["scene_type"] == "EMPTY_SCENE"
    assert res_empty["confidence"] == 1.0

    # Caso 2: No Blender (simulado desde BlenderObserver robusto)
    snapshot_no_blender = {
        "object_count": 0,
        "objects": [],
        "source": "no_blender"
    }
    res_no_blender = observer.analyze(snapshot_no_blender)
    assert res_no_blender["scene_type"] == "EMPTY_SCENE"


def test_3_analyze_basic_modeling_classification():
    observer = BlenderSemanticObserver()
    
    # Simular snapshot con cubos (Basic Modeling)
    snapshot = {
        "object_count": 2,
        "objects": [
            {"name": "Cube", "type": "MESH", "collections": ["Collection"]},
            {"name": "Sphere", "type": "MESH", "collections": ["Collection"]}
        ],
        "source": "blender"
    }
    
    result = observer.analyze(snapshot)
    
    assert result["scene_type"] == "BASIC_MODELING"
    assert result["object_summary"]["MESH"] == 2
    assert result["confidence"] > 0.8


def test_4_analyze_scene_with_camera():
    observer = BlenderSemanticObserver()
    
    # Simular escena con cámara
    snapshot = {
        "object_count": 2,
        "objects": [
            {"name": "Cube", "type": "MESH", "collections": ["Collection"]},
            {"name": "Camera", "type": "CAMERA", "collections": ["Collection"]}
        ],
        "source": "blender"
    }
    
    result = observer.analyze(snapshot)
    
    assert result["scene_type"] == "SCENE_WITH_CAMERAS"
    assert result["object_summary"]["CAMERA"] == 1


def test_5_collections_detection():
    observer = BlenderSemanticObserver()
    
    snapshot = {
        "object_count": 1,
        "objects": [
            {"name": "Cube", "type": "MESH", "collections": ["MyCollection", "Scene"]}
        ],
        "source": "blender"
    }
    
    result = observer.analyze(snapshot)
    
    assert "MyCollection" in result["collections_detected"]
    assert "Scene" in result["collections_detected"]
