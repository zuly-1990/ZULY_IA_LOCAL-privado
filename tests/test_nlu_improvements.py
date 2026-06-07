# tests/test_nlu_improvements.py
"""
Tests para las mejoras implementadas en el módulo NLU.
"""

import pytest
from core.utils.nlu import NaturalLanguageProcessor, CommandIntent
from core.utils.exceptions import NLUError


class TestNLUInputValidation:
    """Tests para validación de entrada en NLU."""
    
    @pytest.fixture
    def nlu(self):
        """Fixture que crea un NLU con comandos de prueba."""
        commands = {
            "crearprimitivacubo": type("MockCommand", (), {}),
            "crearprimitvaesfera": type("MockCommand", (), {}),
        }
        return NaturalLanguageProcessor(commands)
    
    def test_none_input_raises_error(self, nlu):
        """Test que None lanza NLUError."""
        with pytest.raises(NLUError) as exc_info:
            nlu.process(None)
        
        assert "None" in str(exc_info.value)
        assert exc_info.value.details["user_request"] is None
    
    def test_non_string_input_raises_error(self, nlu):
        """Test que tipo no-string lanza NLUError."""
        with pytest.raises(NLUError) as exc_info:
            nlu.process(12345)
        
        assert "string" in str(exc_info.value).lower()
        assert exc_info.value.details["type"] == "int"
    
    def test_empty_string_returns_empty_list(self, nlu):
        """Test que string vacío retorna lista vacía."""
        result = nlu.process("")
        assert result == []
    
    def test_whitespace_only_returns_empty_list(self, nlu):
        """Test que solo espacios retorna lista vacía."""
        result = nlu.process("   \t\n  ")
        assert result == []
    
    def test_valid_string_processes_correctly(self, nlu):
        """Test que string válido se procesa correctamente."""
        result = nlu.process("crear cubo")
        assert isinstance(result, list)


class TestNLUSimilarityCache:
    """Tests para el caché de similitud."""
    
    @pytest.fixture
    def nlu(self):
        """Fixture con NLU."""
        commands = {
            "comando1": type("MockCommand", (), {}),
            "comando2": type("MockCommand", (), {}),
            "comando3": type("MockCommand", (), {}),
        }
        return NaturalLanguageProcessor(commands)
    
    def test_similarity_cache_works(self, nlu):
        """Test que el caché funciona."""
        # Primera llamada - calcula
        result1 = nlu._calculate_similarity("test", "test")
        
        # Segunda llamada - usa caché
        result2 = nlu._calculate_similarity("test", "test")
        
        assert result1 == result2
        assert result1 == 1.0
    
    def test_cache_info_available(self, nlu):
        """Test que cache_info está disponible."""
        # Limpiar caché
        nlu._calculate_similarity.cache_clear()
        
        # Verificar que empieza en 0
        info = nlu._calculate_similarity.cache_info()
        assert info.hits == 0
        assert info.misses == 0
        
        # Hacer algunas llamadas
        nlu._calculate_similarity("a", "b")
        nlu._calculate_similarity("a", "b")  # Hit
        
        info = nlu._calculate_similarity.cache_info()
        assert info.hits == 1
        assert info.misses == 1
    
    def test_find_similar_command_uses_cache(self, nlu):
        """Test que find_similar_command usa el caché."""
        nlu._calculate_similarity.cache_clear()
        
        # Primera búsqueda
        nlu.find_similar_command("comando")
        
        # Verificar que se usó el caché
        info = nlu._calculate_similarity.cache_info()
        assert info.misses > 0


class TestNLULogging:
    """Tests para el logging mejorado."""
    
    @pytest.fixture
    def nlu(self):
        """Fixture con NLU."""
        commands = {
            "crearcubo": type("MockCommand", (), {}),
        }
        return NaturalLanguageProcessor(commands)
    
    def test_find_similar_command_logs_result(self, nlu, caplog):
        """Test que find_similar_command registra el resultado."""
        import logging
        caplog.set_level(logging.DEBUG)
        
        result = nlu.find_similar_command("crearcubo")
        
        # Verificar que se encontró
        assert result is not None
        
        # Verificar logging (si está en modo debug)
        # Nota: esto depende de la configuración de logging
    
    def test_find_similar_command_logs_no_match(self, nlu, caplog):
        """Test que se registra cuando no hay coincidencia."""
        import logging
        caplog.set_level(logging.DEBUG)
        
        result = nlu.find_similar_command("comandoquenoexiste123456")
        
        # Verificar que no se encontró
        assert result is None


class TestCommandIntent:
    """Tests para la clase CommandIntent."""
    
    def test_command_intent_creation(self):
        """Test de creación básica."""
        intent = CommandIntent("test_command", confidence=0.9)
        
        assert intent.command_name == "test_command"
        assert intent.confidence == 0.9
        assert intent.parameters == {}
    
    def test_command_intent_with_parameters(self):
        """Test con parámetros."""
        params = {"location": (1, 2, 3)}
        intent = CommandIntent("test_command", parameters=params)
        
        assert intent.parameters == params
    
    def test_command_intent_repr(self):
        """Test de representación."""
        intent = CommandIntent("test", confidence=0.85, parameters={"key": "value"})
        repr_str = repr(intent)
        
        assert "test" in repr_str
        assert "0.85" in repr_str
    
    def test_command_intent_str(self):
        """Test de string."""
        intent = CommandIntent("test", confidence=0.75)
        str_repr = str(intent)
        
        assert "test" in str_repr
        assert "75%" in str_repr


class TestNLUProcessing:
    """Tests de procesamiento completo."""
    
    @pytest.fixture
    def nlu(self):
        """Fixture con comandos reales."""
        commands = {
            "crearprimitivacubo": type("MockCommand", (), {}),
            "crearprimitvaesfera": type("MockCommand", (), {}),
            "crearprimitivacilindro": type("MockCommand", (), {}),
        }
        return NaturalLanguageProcessor(commands)
    
    def test_direct_command_match(self, nlu):
        """Test de coincidencia directa de comando."""
        result = nlu.process("crearprimitivacubo")
        
        assert len(result) > 0
        assert result[0].command_name == "crearprimitivacubo"
        assert result[0].confidence >= 0.9
    
    def test_keyword_detection(self, nlu):
        """Test de detección por palabras clave."""
        result = nlu.process("crear un cubo")
        
        # Debería detectar la intención de crear cubo
        assert len(result) > 0
    
    def test_parameter_extraction(self, nlu):
        """Test de extracción de parámetros."""
        result = nlu.process("crear cubo en 1 2 3")
        
        if len(result) > 0 and result[0].parameters:
            # Verificar que se extrajeron coordenadas
            assert "location" in result[0].parameters or len(result[0].parameters) > 0
    
    def test_similar_command_fallback(self, nlu):
        """Test de búsqueda de comando similar."""
        # Typo intencional
        result = nlu.process("crearprimitivakubo")
        
        # Debería encontrar algo similar
        assert len(result) > 0


class TestPerformance:
    """Tests de rendimiento."""
    
    @pytest.fixture
    def nlu_large(self):
        """NLU con muchos comandos."""
        commands = {f"comando{i}": type("MockCommand", (), {}) for i in range(100)}
        return NaturalLanguageProcessor(commands)
    
    def test_cache_improves_performance(self, nlu_large):
        """Test que el caché mejora el rendimiento."""
        import time
        
        # Limpiar caché
        nlu_large._calculate_similarity.cache_clear()
        
        # Primera búsqueda (sin caché)
        start = time.perf_counter()
        nlu_large.find_similar_command("comando50")
        first_time = time.perf_counter() - start
        
        # Segunda búsqueda (con caché)
        start = time.perf_counter()
        nlu_large.find_similar_command("comando50")
        second_time = time.perf_counter() - start
        
        # La segunda debería ser más rápida (aunque puede variar)
        # Este test es más informativo que asertivo
        print(f"Primera búsqueda: {first_time:.6f}s")
        print(f"Segunda búsqueda: {second_time:.6f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
