import os
import json
import uuid
import pytest
from core.learning.repositories import StagingPatternRepository, VerifiedPatternRepository, QuarantinePatternRepository
from core.learning.pattern_memory import PatternMemory

@pytest.fixture
def mock_storage_dir(tmp_path):
    return str(tmp_path)

@pytest.fixture
def sample_pattern():
    return {
        "pattern_id": str(uuid.uuid4()),
        "user_request": "crear cubo de prueba",
        "context": {
            "origin": "laboratory",
            "blender_version": "3.6.0",
            "active_mode": "OBJECT",
            "environment_hash": "dummy_hash_123",
            "scene_before": {"objects": []}
        },
        "metadata": {
            "status": "STAGING",
            "uses": 0
        }
    }

def test_repositories_creation(mock_storage_dir):
    staging = StagingPatternRepository(storage_dir=mock_storage_dir)
    verified = VerifiedPatternRepository(storage_dir=mock_storage_dir)
    quarantine = QuarantinePatternRepository(storage_dir=mock_storage_dir)
    
    # Comprobar creación de archivos
    assert os.path.exists(os.path.join(mock_storage_dir, "patterns_staging.json"))
    assert os.path.exists(os.path.join(mock_storage_dir, "patterns_verified.json"))
    assert os.path.exists(os.path.join(mock_storage_dir, "patterns_quarantine.json"))

def test_repository_crud(mock_storage_dir, sample_pattern):
    staging = StagingPatternRepository(storage_dir=mock_storage_dir)
    
    # Create
    assert staging.add_pattern(sample_pattern) == True
    patterns = staging.load_all()
    assert len(patterns) == 1
    assert patterns[0]['pattern_id'] == sample_pattern['pattern_id']
    
    # Read
    fetched = staging.get_pattern(sample_pattern['pattern_id'])
    assert fetched is not None
    assert fetched['user_request'] == "crear cubo de prueba"
    
    # Update
    sample_pattern['metadata']['uses'] = 5
    assert staging.update_pattern(sample_pattern['pattern_id'], sample_pattern) == True
    fetched_updated = staging.get_pattern(sample_pattern['pattern_id'])
    assert fetched_updated['metadata']['uses'] == 5
    
    # Delete
    assert staging.delete_pattern(sample_pattern['pattern_id']) == True
    assert len(staging.load_all()) == 0

def test_pattern_memory_auto_hash(mocker):
    # Mocking repos for clean test
    mocker.patch('core.learning.repositories.StagingPatternRepository.load_all', return_value=[])
    mocker.patch('core.learning.repositories.VerifiedPatternRepository.load_all', return_value=[])
    mocker.patch('core.learning.repositories.StagingPatternRepository.add_pattern', return_value=True)

    pm = PatternMemory()
    
    mock_execution = {
        'command_executed': 'blender.create_cube',
        'confidence': 0.95,
        'success': True,
        'validation': {'verified': True, 'details': 'ok'},
        'mode': 'REACTIVE',
        'scene_state_pre': {'objects': [{'name': 'Camera'}, {'name': 'Light'}]},
        'scene_state': {'blender_version': '4.2.0'}
    }
    
    pattern_id = pm.store_pattern("crear cubo de prueba", mock_execution)
    
    assert pattern_id is not None
    assert len(pm.patterns) == 1
    
    pattern_stored = pm.patterns[0]
    
    # Verificar inyección de metadatos obligatorios de Fase 1
    assert 'environment_hash' in pattern_stored['context']
    assert pattern_stored['context']['environment_hash'] != ""
    assert pattern_stored['metadata']['status'] == "STAGING"
    assert pattern_stored['context']['blender_version'] == "4.2.0"
