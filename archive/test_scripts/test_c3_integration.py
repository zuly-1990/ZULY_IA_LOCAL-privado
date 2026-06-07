"""
Test de Integración C3 con LYZU Core
====================================

Verifica que C3 se integra correctamente con LYZU.
"""

import pytest
from lyzu_core import LYZUCore


class TestC3LYZUIntegration:
    """Tests de integración C3 con LYZU Core"""
    
    def test_c3_initialization_enabled(self):
        """C3 se inicializa cuando enable_cognition=True"""
        lyzu = LYZUCore(enable_cognition=True)
        
        assert lyzu.cognition_enabled
        assert lyzu.objectives_system is not None
    
    def test_c3_initialization_disabled(self):
        """C3 es None cuando enable_cognition=False"""
        lyzu = LYZUCore(enable_cognition=False)
        
        assert not lyzu.cognition_enabled
        assert lyzu.objectives_system is None
    
    def test_c3_decompose_objective(self):
        """Descompone objetivo cuando C3 está habilitado"""
        lyzu = LYZUCore(enable_cognition=True)
        
        plan = lyzu.decompose_objective('crear escena 3d')
        assert plan is not None
        assert len(plan.tasks) > 0
    
    def test_c3_decompose_objective_disabled(self):
        """Retorna None cuando C3 está deshabilitado"""
        lyzu = LYZUCore(enable_cognition=False)
        
        plan = lyzu.decompose_objective('crear escena 3d')
        assert plan is None
    
    def test_c3_get_next_tasks(self):
        """Obtiene siguientes tareas"""
        lyzu = LYZUCore(enable_cognition=True)
        
        plan = lyzu.decompose_objective('crear escena 3d')
        next_tasks = lyzu.get_next_tasks_for_plan(plan, [])
        
        assert next_tasks is not None
        assert len(next_tasks) > 0
    
    def test_c3_get_next_tasks_disabled(self):
        """Retorna None cuando C3 está deshabilitado"""
        lyzu = LYZUCore(enable_cognition=False)
        
        result = lyzu.get_next_tasks_for_plan(None, [])
        assert result is None
    
    def test_c3_export_plan(self):
        """Exporta plan cuando C3 está habilitado"""
        from pathlib import Path
        
        lyzu = LYZUCore(enable_cognition=True)
        plan = lyzu.decompose_objective('crear escena 3d')
        
        export_path = Path('bitacora/test_plan_export.json')
        success = lyzu.export_plan(plan, str(export_path))
        
        assert success
        assert export_path.exists()
        
        # Limpiar
        export_path.unlink(missing_ok=True)
    
    def test_c3_export_plan_disabled(self):
        """Retorna False cuando C3 está deshabilitado"""
        lyzu = LYZUCore(enable_cognition=False)
        
        success = lyzu.export_plan(None, 'bitacora/test.json')
        assert not success
    
    def test_c1_c2_c3_all_enabled(self):
        """C1, C2 y C3 pueden estar habilitados juntos"""
        lyzu = LYZUCore(enable_cognition=True)
        
        assert lyzu.evaluator is not None
        assert lyzu.memory_system is not None
        assert lyzu.objectives_system is not None
    
    def test_c1_c2_c3_all_disabled(self):
        """C1, C2 y C3 pueden estar deshabilitados"""
        lyzu = LYZUCore(enable_cognition=False)
        
        assert lyzu.evaluator is None
        assert lyzu.memory_system is None
        assert lyzu.objectives_system is None
    
    def test_backward_compatibility_c3(self):
        """LYZU funciona normalmente con C3 habilitado"""
        lyzu1 = LYZUCore(enable_cognition=True)
        lyzu2 = LYZUCore(enable_cognition=False)
        
        # Ambas deberían tener componentes básicos
        assert lyzu1.entity_extractor is not None
        assert lyzu1.intent_manager is not None
        assert lyzu1.dialog_manager is not None
        
        assert lyzu2.entity_extractor is not None
        assert lyzu2.intent_manager is not None
        assert lyzu2.dialog_manager is not None
    
    def test_c3_default_enabled(self):
        """C3 está habilitado por defecto"""
        lyzu = LYZUCore()  # Sin parámetros
        
        assert lyzu.cognition_enabled
        assert lyzu.objectives_system is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
