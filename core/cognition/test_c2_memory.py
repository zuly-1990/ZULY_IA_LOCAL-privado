"""
Tests para C2 - Memory of Experiences
Tests de: almacenamiento, extracción, búsqueda y heurísticas
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from core.cognition.c2_experience_memory import (
    Experience, Learning, ExperienceType, MemoryStrategy,
    ExperienceStorage, ExperienceExtractor, PatternMatcher,
    HeuristicBuilder, C2ExperienceMemory
)


class TestExperienceStorage:
    """Tests del almacenamiento de experiencias"""
    
    @pytest.fixture
    def temp_db(self):
        """Crea BD temporal para tests"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
            db_path = f.name
        yield db_path
        try:
            Path(db_path).unlink(missing_ok=True)
        except PermissionError:
            pass  # En Windows, SQLite puede mantener locks
    
    def test_storage_creates_db(self, temp_db):
        """Verifica que se crea la BD"""
        storage = ExperienceStorage(temp_db)
        assert Path(temp_db).exists()
    
    def test_save_and_retrieve_experience(self, temp_db):
        """Guarda y recupera experiencia"""
        storage = ExperienceStorage(temp_db)
        
        exp = Experience(
            objective='Crear cubo 3D',
            evaluation_status='success',
            evaluation_score=0.95,
            parameters={'size': 10, 'color': 'red'},
            metrics_passed=4,
            metrics_total=4
        )
        
        exp_id = storage.save_experience(exp)
        assert exp_id > 0
        
        all_exp = storage.get_all_experiences()
        assert len(all_exp) == 1
        assert all_exp[0].objective == 'Crear cubo 3D'
    
    def test_get_experiences_by_status(self, temp_db):
        """Obtiene experiencias filtradas por estado"""
        storage = ExperienceStorage(temp_db)
        
        exp_success = Experience(
            objective='Test 1',
            evaluation_status='success',
            evaluation_score=0.9,
            parameters={},
            metrics_passed=4,
            metrics_total=4
        )
        
        exp_failed = Experience(
            objective='Test 2',
            evaluation_status='failed',
            evaluation_score=0.2,
            parameters={},
            metrics_passed=1,
            metrics_total=4
        )
        
        storage.save_experience(exp_success)
        storage.save_experience(exp_failed)
        
        successes = storage.get_experiences_by_status('success')
        failures = storage.get_experiences_by_status('failed')
        
        assert len(successes) == 1
        assert len(failures) == 1
    
    def test_get_recent_experiences(self, temp_db):
        """Obtiene experiencias recientes"""
        storage = ExperienceStorage(temp_db)
        
        exp = Experience(
            objective='Test',
            evaluation_status='success',
            evaluation_score=0.9,
            parameters={},
            metrics_passed=4,
            metrics_total=4
        )
        
        storage.save_experience(exp)
        
        recent = storage.get_recent_experiences(days=1)
        assert len(recent) == 1


class TestExperienceExtractor:
    """Tests de extracción de aprendizajes"""
    
    @staticmethod
    def create_test_experiences() -> list:
        """Crea experiencias de prueba"""
        return [
            Experience(
                objective='Crear cubo',
                evaluation_status='success',
                evaluation_score=0.95,
                parameters={'size': 10},
                metrics_passed=4,
                metrics_total=4,
                issues=[],
                recommendations=['Aumentar tamaño']
            ),
            Experience(
                objective='Crear esfera',
                evaluation_status='success',
                evaluation_score=0.85,
                parameters={'radius': 5},
                metrics_passed=3,
                metrics_total=4,
                issues=['Baja resolución'],
                recommendations=['Aumentar resolución']
            ),
            Experience(
                objective='Crear pirámide',
                evaluation_status='failed',
                evaluation_score=0.3,
                parameters={'sides': 3},
                metrics_passed=1,
                metrics_total=4,
                issues=['Error de geometría'],
                recommendations=['Usar parámetros correctos']
            ),
        ]
    
    def test_extract_common_issues(self):
        """Extrae problemas comunes"""
        exp = self.create_test_experiences()
        issues = ExperienceExtractor.extract_common_issues(exp)
        
        assert 'Baja resolución' in issues
        assert 'Error de geometría' in issues
    
    def test_extract_successful_patterns(self):
        """Extrae patrones exitosos"""
        exp = self.create_test_experiences()
        patterns = ExperienceExtractor.extract_successful_patterns(exp)
        
        assert len(patterns) == 2
        assert patterns[0]['score'] >= patterns[1]['score']
    
    def test_extract_failure_reasons(self):
        """Analiza razones de fracaso"""
        exp = self.create_test_experiences()
        failures = ExperienceExtractor.extract_failure_reasons(exp)
        
        assert 'Error de geometría' in failures
    
    def test_calculate_success_rate(self):
        """Calcula tasa de éxito"""
        exp = self.create_test_experiences()
        rate = ExperienceExtractor.calculate_success_rate(exp)
        
        assert 0.6 < rate < 0.7  # 2 de 3 exitosos
    
    def test_calculate_average_score(self):
        """Calcula score promedio"""
        exp = self.create_test_experiences()
        avg = ExperienceExtractor.calculate_average_score(exp)
        
        assert 0.5 < avg < 0.75


class TestPatternMatcher:
    """Tests de búsqueda de patrones"""
    
    @staticmethod
    def create_test_experiences() -> list:
        """Crea experiencias para pruebas"""
        return [
            Experience(
                objective='Crear cubo 3D rojo',
                evaluation_status='success',
                evaluation_score=0.9,
                parameters={},
                metrics_passed=4,
                metrics_total=4
            ),
            Experience(
                objective='Crear cubo 3D azul',
                evaluation_status='success',
                evaluation_score=0.88,
                parameters={},
                metrics_passed=4,
                metrics_total=4
            ),
            Experience(
                objective='Crear esfera',
                evaluation_status='failed',
                evaluation_score=0.3,
                parameters={},
                metrics_passed=1,
                metrics_total=4
            ),
        ]
    
    def test_find_similar_experiences(self):
        """Encuentra experiencias similares"""
        exp = self.create_test_experiences()
        
        similar = PatternMatcher.find_similar_experiences('Crear cubo', exp, threshold=0.5)
        
        assert len(similar) >= 2
        assert all(s[1] >= 0.5 for s in similar)
    
    def test_find_failed_cases(self):
        """Encuentra casos que fallaron"""
        exp = self.create_test_experiences()
        
        failed = PatternMatcher.find_failed_cases_for_objective('esfera', exp)
        
        assert len(failed) == 1
        assert failed[0].evaluation_status == 'failed'


class TestHeuristicBuilder:
    """Tests de construcción de heurísticas"""
    
    @staticmethod
    def create_test_experiences() -> list:
        """Crea experiencias para pruebas"""
        return [
            Experience(
                objective='Crear cubo',
                evaluation_status='success',
                evaluation_score=0.95,
                parameters={'size': 10, 'color': 'red'},
                metrics_passed=4,
                metrics_total=4,
                recommendations=['Aumentar tamaño']
            ),
            Experience(
                objective='Crear cubo',
                evaluation_status='success',
                evaluation_score=0.92,
                parameters={'size': 10, 'color': 'blue'},
                metrics_passed=4,
                metrics_total=4,
                recommendations=['Mejorar color']
            ),
            Experience(
                objective='Crear cubo',
                evaluation_status='success',
                evaluation_score=0.89,
                parameters={'size': 8, 'color': 'green'},
                metrics_passed=3,
                metrics_total=4,
                recommendations=['Aumentar resolución']
            ),
        ]
    
    def test_build_parameter_heuristics(self):
        """Construye heurísticas de parámetros"""
        exp = self.create_test_experiences()
        heuristics = HeuristicBuilder.build_parameter_heuristics(exp)
        
        assert 'size' in heuristics
        assert heuristics['size'] == 10  # Más frecuente
    
    def test_build_improvement_suggestions(self):
        """Construye sugerencias de mejora"""
        exp = self.create_test_experiences()
        
        suggestions = HeuristicBuilder.build_improvement_suggestions('Crear cubo', exp)
        
        assert len(suggestions) > 0


class TestC2ExperienceMemory:
    """Tests de la memoria principal C2"""
    
    @pytest.fixture
    def temp_db(self):
        """Crea BD temporal"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
            db_path = f.name
        yield db_path
        try:
            Path(db_path).unlink(missing_ok=True)
        except PermissionError:
            pass  # En Windows, SQLite puede mantener locks
    
    @pytest.fixture
    def memory(self, temp_db):
        """Crea instancia de memoria"""
        return C2ExperienceMemory(temp_db)
    
    def test_record_experience(self, memory):
        """Registra experiencia desde C1"""
        exp_id = memory.record_experience(
            objective='Crear cubo',
            evaluation={
                'status': 'success',
                'score': 0.95,
                'metrics_passed': 4,
                'metrics_total': 4,
                'issues': [],
                'recommendations': ['Bien'],
                'parameters': {'size': 10}
            }
        )
        
        assert exp_id > 0
    
    def test_get_insights(self, memory):
        """Obtiene insights de experiencias"""
        # Registrar algunas experiencias
        memory.record_experience('Test 1', {
            'status': 'success', 'score': 0.9,
            'metrics_passed': 4, 'metrics_total': 4,
            'issues': [], 'recommendations': [], 'parameters': {}
        })
        
        memory.record_experience('Test 2', {
            'status': 'failed', 'score': 0.3,
            'metrics_passed': 1, 'metrics_total': 4,
            'issues': ['Error'], 'recommendations': [], 'parameters': {}
        })
        
        insights = memory.get_insights()
        
        assert insights['total_experiences'] == 2
        assert insights['success_rate'] == 0.5
        assert 'average_score' in insights
    
    def test_get_suggestions_for(self, memory):
        """Obtiene sugerencias para objetivo"""
        memory.record_experience('Crear cubo 3D', {
            'status': 'success', 'score': 0.95,
            'metrics_passed': 4, 'metrics_total': 4,
            'issues': [], 'recommendations': ['OK'],
            'parameters': {'size': 10}
        })
        
        suggestions = memory.get_suggestions_for('Crear cubo')
        
        assert 'similar_experiences' in suggestions
        assert suggestions['similar_experiences'] >= 0
    
    def test_get_all_learnings(self, memory):
        """Obtiene todas las lecciones aprendidas"""
        # Registrar experiencias exitosas
        for i in range(5):
            memory.record_experience(f'Test {i}', {
                'status': 'success', 'score': 0.9,
                'metrics_passed': 4, 'metrics_total': 4,
                'issues': [], 'recommendations': [], 'parameters': {}
            })
        
        learnings = memory.get_all_learnings()
        
        assert len(learnings) > 0
        assert any(l['type'] == 'positive' for l in learnings)
    
    def test_export_memory(self, memory, tmp_path):
        """Exporta memoria a JSON"""
        memory.record_experience('Test', {
            'status': 'success', 'score': 0.9,
            'metrics_passed': 4, 'metrics_total': 4,
            'issues': [], 'recommendations': [], 'parameters': {}
        })
        
        export_path = tmp_path / 'memory.json'
        success = memory.export_memory(export_path)
        
        assert success
        assert export_path.exists()
        
        with open(export_path) as f:
            data = json.load(f)
        
        assert 'exported_at' in data
        assert 'total_experiences' in data
        assert data['total_experiences'] == 1


    @pytest.fixture
    def temp_db(self):
        """Crea BD temporal para tests"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
            db_path = f.name
        yield db_path
        try:
            Path(db_path).unlink(missing_ok=True)
        except PermissionError:
            pass  # En Windows, SQLite puede mantener locks
    
    def test_full_workflow(self, temp_db):
        """Test del flujo completo: registrar → analizar → sugerir"""
        memory = C2ExperienceMemory(temp_db)
        
        # Fase 1: Registrar experiencias
        for i in range(10):
            status = 'success' if i % 2 == 0 else 'failed'
            score = 0.9 if status == 'success' else 0.3
            
            memory.record_experience(f'Crear objeto {i}', {
                'status': status,
                'score': score,
                'metrics_passed': 4 if status == 'success' else 1,
                'metrics_total': 4,
                'issues': [] if status == 'success' else ['Error genérico'],
                'recommendations': ['Bien'] if status == 'success' else ['Revisar'],
                'parameters': {'id': i}
            })
        
        # Fase 2: Analizar
        insights = memory.get_insights()
        assert insights['total_experiences'] == 10
        assert insights['success_rate'] == 0.5
        
        # Fase 3: Sugerir para nuevo objetivo
        suggestions = memory.get_suggestions_for('Crear objeto nuevo')
        assert 'similar_experiences' in suggestions


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
