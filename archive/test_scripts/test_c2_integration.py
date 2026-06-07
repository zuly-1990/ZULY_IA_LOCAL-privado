"""
Test de Integración C2 con LYZU Core
====================================

Verifica que C2 se integra correctamente con LYZU.
"""

import pytest
from pathlib import Path
from lyzu_core import LYZUCore


class TestC2LYZUIntegration:
    """Tests de integración C2 con LYZU Core"""
    
    def test_c2_initialization_enabled(self):
        """C2 se inicializa cuando enable_cognition=True"""
        lyzu = LYZUCore(enable_cognition=True)
        
        assert lyzu.cognition_enabled
        assert lyzu.memory_system is not None
    
    def test_c2_initialization_disabled(self):
        """C2 es None cuando enable_cognition=False"""
        lyzu = LYZUCore(enable_cognition=False)
        
        assert not lyzu.cognition_enabled
        assert lyzu.memory_system is None
    
    def test_c2_get_memory_insights_enabled(self):
        """Obtiene insights de C2 cuando está habilitado"""
        lyzu = LYZUCore(enable_cognition=True)
        
        insights = lyzu.get_memory_insights()
        assert insights is not None
        assert 'total_experiences' in insights
    
    def test_c2_get_memory_insights_disabled(self):
        """Retorna None cuando C2 está deshabilitado"""
        lyzu = LYZUCore(enable_cognition=False)
        
        insights = lyzu.get_memory_insights()
        assert insights is None
    
    def test_c2_get_suggestions_enabled(self):
        """Obtiene sugerencias de C2 cuando está habilitado"""
        lyzu = LYZUCore(enable_cognition=True)
        
        suggestions = lyzu.get_suggestions_for_objective('Crear cubo')
        assert suggestions is not None
        assert 'objective' in suggestions
    
    def test_c2_get_suggestions_disabled(self):
        """Retorna None cuando C2 está deshabilitado"""
        lyzu = LYZUCore(enable_cognition=False)
        
        suggestions = lyzu.get_suggestions_for_objective('Crear cubo')
        assert suggestions is None
    
    def test_c2_export_memory_enabled(self):
        """Exporta memoria cuando C2 está habilitado"""
        lyzu = LYZUCore(enable_cognition=True)
        
        export_path = Path('bitacora/test_memory_export.json')
        success = lyzu.export_memory(str(export_path))
        
        assert success
        assert export_path.exists()
        
        # Limpiar
        export_path.unlink(missing_ok=True)
    
    def test_c2_export_memory_disabled(self):
        """Retorna False cuando C2 está deshabilitado"""
        lyzu = LYZUCore(enable_cognition=False)
        
        success = lyzu.export_memory('bitacora/test.json')
        assert not success
    
    def test_backward_compatibility_with_c2(self):
        """LYZU funciona normalmente con C2 habilitado"""
        lyzu1 = LYZUCore(enable_cognition=True)
        lyzu2 = LYZUCore(enable_cognition=False)
        
        # Ambas deberían tener los componentes básicos
        assert lyzu1.entity_extractor is not None
        assert lyzu1.intent_manager is not None
        assert lyzu1.intent_router is not None
        assert lyzu1.dialog_manager is not None
        
        assert lyzu2.entity_extractor is not None
        assert lyzu2.intent_manager is not None
        assert lyzu2.intent_router is not None
        assert lyzu2.dialog_manager is not None
    
    def test_c2_default_enabled(self):
        """C2 está habilitado por defecto"""
        lyzu = LYZUCore()  # Sin parámetros
        
        assert lyzu.cognition_enabled
        assert lyzu.memory_system is not None
    
    def test_c1_c2_both_enabled(self):
        """Tanto C1 como C2 pueden estar habilitados"""
        lyzu = LYZUCore(enable_cognition=True)
        
        assert lyzu.evaluator is not None
        assert lyzu.memory_system is not None
    
    def test_c1_c2_both_disabled(self):
        """Tanto C1 como C2 pueden estar deshabilitados"""
        lyzu = LYZUCore(enable_cognition=False)
        
        assert lyzu.evaluator is None
        assert lyzu.memory_system is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
